import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.pool import StaticPool
from uuid import UUID

# Importa tu app y modelos, y la dependencia que necesitas sobrescribir
# --- ASUME que get_session y get_current_user son importables desde src.server ---
from src.server import create_app 
from src.core.database import get_session
from src.models.user import User
from src.models.habit import Habit
from src.core.security import hash_password, verify_password

# --- Datos de prueba reutilizables ---
TEST_USER_DATA = {
    "first_name": "Misael",
    "last_name": "Rodríguez",
    "username": "misael123",
    "email": "misael@example.com",
    "password": "securepassword"
}

# La función create_app debe aceptar la dependencia de sesión como configuración 
# para un control más fino, pero para la prueba simple, usaremos la inyección directa.
app = create_app({})

# --- Base de datos en memoria para testing ---
DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Fixture para la sesión de DB
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

# Fixture para cliente de FastAPI con DEPENDENCIAS SOBREESCRITAS
@pytest.fixture(name="client")
def client_fixture(session: Session):
    
    # 1. Función de sobrescritura para la sesión de DB
    def override_get_session():
        yield session

    # 2. Sobrescribir la dependencia de la sesión global
    app.dependency_overrides[get_session] = override_get_session
    
    # Nota: También deberíamos sobrescribir get_current_user si este usa
    # jwt.decode directamente, pero para esta prueba solo necesitamos
    # la sesión para que la creación de usuarios funcione.

    with TestClient(app) as client:
        yield client
    
    # 3. Limpiar las sobrescrituras
    app.dependency_overrides.clear()


# ------------------------------
# Prueba unitaria: Crear usuario
# ------------------------------
def test_create_user(client: TestClient, session: Session):
    """
    Verifica que la creación de usuario retorne 201 y que los campos 
    por defecto estén presentes.
    """
    response = client.post("/api/users", json=TEST_USER_DATA)
    
    # La corrección de dependencia debería cambiar 400 a 201
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    data = response.json()
    
    # Verifica campos obligatorios y valores por defecto
    assert "id" in data
    assert data["enabled"] is True
    assert "created_at" in data
    assert "updated_at" in data
    assert data["username"] == TEST_USER_DATA["username"]

    # Verifica que la contraseña no se guarde en texto plano
    db_user = session.get(User, UUID(data["id"]))

    # Por ahora, solo verificamos que no sea texto plano:
    assert db_user.password != TEST_USER_DATA["password"]


# ------------------------------
# Prueba unitaria: Crear hábito
# ------------------------------
def test_create_habit(client: TestClient, session: Session):
    """
    Crea un usuario y luego un hábito, validando los campos por defecto del hábito.
    """
    # 1. Crear usuario (para obtener un ID válido)
    user_resp = client.post("/api/users", json=TEST_USER_DATA)
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"] # Esto ahora debería funcionar
    
    habit_data = {
        "user_id": user_id,
        "title": "Correr",
        "category": "Salud",
        "goal_type": "daily",
        "goal_value": 30
    }
    response = client.post("/api/habits", json=habit_data)
    assert response.status_code == 201
    data = response.json()

    assert data["user_id"] == user_id
    assert "id" in data
    assert data["enabled"] is True
    assert "created_at" in data
    assert "updated_at" in data

    # Verificación en DB
    db_habit = session.get(Habit, UUID(data["id"]))
    assert db_habit is not None
    assert db_habit.title == "Correr"


# ----------------------------------------------
# Prueba de integración: login + fetch hábitos
# ----------------------------------------------
def test_user_login_and_fetch_habits(client: TestClient, session: Session):
    """
    Flujo completo: Registro -> Login -> Obtener Token -> Consultar Hábitos.
    """
    # 1. Crear usuario
    user_resp = client.post("/api/users", json=TEST_USER_DATA)
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # 2. Crear hábito
    habit_data = {
        "user_id": user_id,
        "title": "Tomar agua",
        "category": "Salud",
        "goal_type": "daily",
        "goal_value": 20
    }
    client.post("/api/habits", json=habit_data)

    # 3. Login
    # Nota: Tu login_data usa 'username', pero la implementación de mi 'login' 
    # en el servicio anterior usaba 'email' y 'password'. Asumo que tu endpoint
    # de login espera 'username' y 'password'.
    login_data = {"password": TEST_USER_DATA["password"], "email": TEST_USER_DATA["email"]}
    # Si el endpoint de login espera un schema UserCreate (que tiene todos los campos):
    token_resp = client.post("/api/auth/login", json=login_data)
    
    # Si la ruta es solo login (email/password), la prueba debe usar el esquema correcto.
    # Asumo que el endpoint de login está en /api/auth/login y usa email/password o username/password.
    if token_resp.status_code != 200:
        # Intentar con email/password si username no funciona, o viceversa
        login_data_email = {"email": TEST_USER_DATA["email"], "password": TEST_USER_DATA["password"]}
        token_resp = client.post("/api/auth/login", json=login_data_email)
        
    assert token_resp.status_code == 200, f"Login failed: {token_resp.text}"
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Obtener hábitos del usuario
    habits_resp = client.get(f"/api/habits/user/{user_id}", headers=headers)
    
    assert habits_resp.status_code == 200
    habits = habits_resp.json()
    assert len(habits) == 1
    assert habits[0]["title"] == "Tomar agua"
    assert habits[0]["user_id"] == user_id