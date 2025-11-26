from decouple import config

class Config:
    __instance = None

    PORT: int = config("PORT", cast=int, default=5000)
    ENVIRONMENT: str = config("ENVIRONMENT", default='production')
    SECRET_KEY: str = config("SECRET_KEY", default="dev-secret-key-change-in-production")
    DB_URL: str = config("DB_URL", default="sqlite:///./habit_tracker.db")
    CLIENT_URL: str = config("CLIENT_URL", default="*")
    CIPHER_KEY: str = config("CIPHER_KEY", default="dev-cipher-key-change-in-production")

    RECAPTCHA_SECRET_KEY: str = config("RECAPTCHA_SECRET_KEY", default="")

    SMTP_SERVER: str = config("SMTP_SERVER", default="")
    SMTP_PORT: int = config("SMTP_PORT", default=587, cast=int)
    EMAIL_USER: str = config("EMAIL_USER", default="")
    EMAIL_PASSWORD: str = config("EMAIL_PASSWORD", default="")


    def __new__(cls):
        if Config.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError(f"El atributo '{key}' no puede ser modificado")
        super().__setattr__(key, value)
    
CONFIG = Config()
