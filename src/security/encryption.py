"""
Sistema de cifrado/descifrado AES-256-GCM para protección de datos sensibles.

Características de seguridad:
- AES-256: Clave de 256 bits
- GCM: Modo autenticado que detecta manipulación
- Nonce único por operación (96 bits)
"""
import secrets
from pathlib import Path
from typing import Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataEncryptor:
    """
    Gestor de cifrado/descifrado de datos con AES-256-GCM.
    Implementa patrón Singleton.
    """

    _instance = None

    def __new__(cls):
        """Implementa patrón Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa el encriptador con la clave desde configuración."""
        if not hasattr(self, "_initialized"):
            self._key = bytes.fromhex(settings.encryption_key)
            self.backend = default_backend()
            self._initialized = True
            logger.info("Sistema de cifrado AES-256-GCM inicializado")

    def encrypt_file(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        chunk_size: int = 65536,
    ) -> None:
        """
        Cifra un archivo completo con AES-256-GCM.

        Args:
            input_path: Ruta del archivo a cifrar
            output_path: Ruta del archivo cifrado de salida
            chunk_size: Tamaño del buffer de lectura (64KB por defecto)
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

        # Generar nonce único (96 bits = 12 bytes)
        nonce = secrets.token_bytes(12)

        # Crear cifrador en modo GCM
        cipher = Cipher(
            algorithms.AES(self._key),
            modes.GCM(nonce),
            backend=self.backend,
        )
        encryptor = cipher.encryptor()

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Cifrar por chunks para manejar archivos grandes
        with input_path.open("rb") as f_in, output_path.open("wb") as f_out:
            # Escribir nonce al inicio
            f_out.write(nonce)

            # Cifrar datos en chunks
            while chunk := f_in.read(chunk_size):
                encrypted_chunk = encryptor.update(chunk)
                f_out.write(encrypted_chunk)

            # Finalizar y obtener tag de autenticación
            f_out.write(encryptor.finalize())
            f_out.write(encryptor.tag)  # Tag de 16 bytes

        logger.info(f"✓ Archivo cifrado: {input_path.name} -> {output_path.name}")

    def decrypt_file(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        chunk_size: int = 65536,
    ) -> None:
        """
        Descifra un archivo cifrado con AES-256-GCM.

        Args:
            input_path: Ruta del archivo cifrado
            output_path: Ruta del archivo descifrado de salida
            chunk_size: Tamaño del buffer de lectura
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Archivo cifrado no encontrado: {input_path}")

        with input_path.open("rb") as f_in:
            # Leer nonce (primeros 12 bytes)
            nonce = f_in.read(12)

            # Leer todo el contenido cifrado
            encrypted_data = f_in.read()

            # Separar tag de autenticación (últimos 16 bytes)
            tag = encrypted_data[-16:]
            ciphertext = encrypted_data[:-16]

        # Crear descifrador
        cipher = Cipher(
            algorithms.AES(self._key),
            modes.GCM(nonce, tag),
            backend=self.backend,
        )
        decryptor = cipher.decryptor()

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Descifrar y escribir
        with output_path.open("wb") as f_out:
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            f_out.write(plaintext)

        logger.info(f"✓ Archivo descifrado: {input_path.name}")


# Instancia global (Singleton)
encryptor = DataEncryptor()
