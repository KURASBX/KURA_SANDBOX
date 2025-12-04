import secrets
from typing import Literal, Optional
from urllib.parse import quote_plus

from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 🌐 ENVIRONMENT
    ENVIRONMENT: Literal["development", "staging", "production"] = Field(
        default="development", description="Entorno de ejecución"
    )

    # 🚀 APP
    PROJECT_NAME: str = Field(
        default="Hexagonal FastAPI", description="Nombre del proyecto"
    )
    VERSION: str = Field(default="1.0.0", description="Versión de la API")
    API_V1_PREFIX: str = Field(default="/api/v1", description="Prefijo para la API v1")
    DEBUG: bool = Field(default=False, description="Modo debug")

    # 🗄️ DATABASE
    DATABASE_URL: Optional[str] = Field(
        default=None, description="URL completa de PostgreSQL"
    )

    DB_HOST: str = Field(default="localhost", description="Host de la base de datos")
    DB_PORT: int = Field(default=5432, description="Puerto de la base de datos")
    DB_USER: str = Field(default="postgres", description="Usuario de la base de datos")
    DB_PASSWORD: str = Field(
        default="password", description="Contraseña de la base de datos"
    )
    DB_NAME: str = Field(default="app_db", description="Nombre de la base de datos")
    DB_POOL_SIZE: int = Field(default=20, description="Tamaño del pool de conexiones")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Máximo overflow del pool")

    # 🔐 SECURITY
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Clave secreta para JWT",
    )
    ALGORITHM: str = Field(default="HS256", description="Algoritmo para JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Tiempo de expiración del token en minutos"
    )

    # 📊 LOGGING
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Nivel de logging"
    )
    LOG_FORMAT: str = Field(default="json", description="Formato de logs")
    ENABLE_SQL_LOGGING: bool = Field(default=False, env="ENABLE_SQL_LOGGING")

    # 🌍 CORS
    CORS_ORIGINS: list[str] = Field(
        default=["*"], description="Orígenes permitidos para CORS"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True, description="Permitir credenciales en CORS"
    )

    # ⚡ PERFORMANCE
    REQUEST_TIMEOUT: int = Field(
        default=30, description="Timeout de requests en segundos"
    )

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    JWT_SECRET: str = Field(
        default="not-use-default", description="Secreto para firma de JWT"
    )
    JWT_ALG: str = Field(default="HS256", description="Algoritmo para firma de JWT")
    JWT_AUDIENCE: str = Field(
        default="kura-api", description="Audiencia esperada en el JWT"
    )
    JWT_ISSUER: str = Field(
        default="https://idp.local", description="Emisor esperado del JWT"
    )
    CUB_PEPPER: str = Field(
        default="not-use-default", description="Pepper para hashing de contraseñas"
    )
    ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(
        default=3600, description="Tiempo de expiración del token en segundos"
    )
    WORM_PRIVATE_KEY: Optional[str] = Field(
        default=None, description="Clave privada PEM para firma WORM"
    )
    WORM_VERSION: str = Field(default="1.0", description="Versión del esquema WORM")
    WORM_ISSUER: str = Field(
        default="Alias Chile", description="Emisor de las evidencias WORM"
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        """Construir DATABASE_URL a partir de variables separadas si no existe"""
        if self.DATABASE_URL:
            return self.DATABASE_URL

        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("DEBUG", mode="before")
    @classmethod
    def set_debug_based_on_environment(cls, v, info):
        """Auto-configurar DEBUG basado en ENVIRONMENT"""
        if hasattr(info, "data") and "ENVIRONMENT" in info.data:
            return info.data["ENVIRONMENT"] == "development"
        return v

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def set_log_level_based_on_environment(cls, v, info):
        """Auto-configurar LOG_LEVEL basado en ENVIRONMENT"""
        if hasattr(info, "data") and "ENVIRONMENT" in info.data:
            if info.data["ENVIRONMENT"] == "development":
                return "DEBUG"
            if info.data["ENVIRONMENT"] == "production":
                return "WARNING"
        return v


# Instancia global
settings = Settings()


class DevelopmentSettings(Settings):
    """Configuración para desarrollo"""

    class Config:
        env_prefix = "DEV_"


class ProductionSettings(Settings):
    """Configuración para producción"""

    class Config:
        env_prefix = "PROD_"


class TestingSettings(Settings):
    """Configuración para testing"""

    class Config:
        env_prefix = "TEST_"
