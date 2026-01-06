"""
Gestor de datos que coordina cifrado/descifrado y carga segura.
"""
import tempfile
import os
from pathlib import Path
from typing import List, Union

import pandas as pd

from src.config import settings
from src.security.encryption import encryptor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SecureDataManager:
    """
    Gestor de datos con cifrado transparente.
    Los datos raw nunca se persisten sin cifrar.
    """

    def __init__(self):
        """Inicializa el gestor de datos seguros."""
        self.encryptor = encryptor
        logger.info("Gestor de datos seguros inicializado")

    def encrypt_all_csvs(
        self,
        source_dir: Path,
        pattern: str = "*.csv",
    ) -> List[Path]:
        """
        Cifra todos los archivos CSV de un directorio.

        Args:
            source_dir: Directorio con archivos CSV
            pattern: Patrón de archivos a cifrar

        Returns:
            Lista de archivos cifrados creados
        """
        source_dir = Path(source_dir)
        encrypted_files = []

        csv_files = list(source_dir.glob(pattern))

        if not csv_files:
            logger.warning(f"No se encontraron archivos CSV en {source_dir}")
            return encrypted_files

        logger.info(f"Cifrando {len(csv_files)} archivos CSV...")

        for csv_file in csv_files:
            encrypted_path = settings.encrypted_dir / f"{csv_file.stem}.enc"

            try:
                self.encryptor.encrypt_file(csv_file, encrypted_path)
                encrypted_files.append(encrypted_path)
            except Exception as e:
                logger.error(f"✗ Error cifrando {csv_file.name}: {e}")

        logger.info(f"✅ Completado: {len(encrypted_files)} archivos cifrados")
        return encrypted_files

    def load_encrypted_csv(
        self,
        encrypted_file: Union[str, Path],
        encoding: str = "latin1",
        sep: str = ";",
        skiprows: int = 10,
    ) -> pd.DataFrame:
        """
        Carga un CSV cifrado directamente a DataFrame.
        El archivo descifrado NUNCA se guarda en disco permanentemente.

        Args:
            encrypted_file: Archivo .enc cifrado
            encoding: Encoding del CSV original
            sep: Separador del CSV
            skiprows: Filas a omitir

        Returns:
            DataFrame con los datos
        """
        encrypted_file = Path(encrypted_file)

        if not encrypted_file.exists():
            raise FileNotFoundError(f"Archivo cifrado no encontrado: {encrypted_file}")

        # Crear archivo temporal con delete=False para Windows
        tmp_file = tempfile.NamedTemporaryFile(
            mode="wb", 
            delete=False,  # ✅ CAMBIO: No eliminar automáticamente
            suffix=".csv"
        )
        tmp_path = tmp_file.name
        tmp_file.close()  # ✅ CAMBIO: Cerrar antes de usar

        try:
            # Descifrar al archivo temporal
            self.encryptor.decrypt_file(encrypted_file, tmp_path)

            # Leer desde el archivo temporal
            df = pd.read_csv(
                tmp_path,
                encoding=encoding,
                sep=sep,
                skiprows=skiprows,
            )
            df.columns = df.columns.str.strip()

            logger.debug(f"CSV cargado: {encrypted_file.name} ({len(df)} filas)")

        finally:
            # ✅ CAMBIO: Eliminar manualmente el archivo temporal
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except Exception as e:
                logger.warning(f"No se pudo eliminar archivo temporal: {e}")

        return df


# Instancia global
data_manager = SecureDataManager()
