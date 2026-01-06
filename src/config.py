"""
Configuración centralizada de la aplicación.
Carga variables de entorno y valida configuración.
"""
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global de la aplicación con validación."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === Seguridad ===
    encryption_key: str = Field(
        ...,
        description="Clave de cifrado AES-256 (64 caracteres hexadecimales)",
    )

    # === Aplicación ===
    app_env: Literal["development", "production"] = "development"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # === Dashboard ===
    dashboard_port: int = 8501
    dashboard_host: str = "localhost"

    # === Paths ===
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data")
    encrypted_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent / "data" / "encrypted"
    )
    processed_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent / "data" / "processed"
    )
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "logs")

    @field_validator("encryption_key")
    @classmethod
    def validate_encryption_key(cls, v: str) -> str:
        """Valida que la clave de cifrado tenga el formato correcto."""
        if len(v) != 64:
            raise ValueError(
                "La clave de cifrado debe tener 64 caracteres hexadecimales (32 bytes)"
            )
        try:
            bytes.fromhex(v)
        except ValueError as e:
            raise ValueError("La clave debe ser una cadena hexadecimal válida") from e
        return v

    def __init__(self, **kwargs):
        """Inicializa y crea directorios necesarios."""
        super().__init__(**kwargs)
        self._create_directories()

    def _create_directories(self) -> None:
        """Crea directorios necesarios si no existen."""
        for directory in [
            self.encrypted_dir,
            self.processed_dir,
            self.logs_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)


# Singleton de configuración
settings = Settings()
