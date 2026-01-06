"""
Extractores de datos - Carga segura desde archivos cifrados
"""
from pathlib import Path
from typing import List, Optional

import pandas as pd

from src.config import settings
from src.security.data_manager import data_manager
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataExtractor:
    """
    Extractor de datos con soporte para cifrado.
    Maneja la carga de datos mensuales y consolidación.
    """

    def __init__(self):
        """Inicializa el extractor de datos."""
        self.data_manager = data_manager
        self.encrypted_dir = settings.encrypted_dir
        logger.info("DataExtractor inicializado")

    def load_monthly_data(self, month: str) -> pd.DataFrame:
        """
        Carga datos de un mes específico desde archivo cifrado.

        Args:
            month: Nombre del mes (ej: 'enero', 'febrero')

        Returns:
            DataFrame con los datos del mes

        Example:
            >>> extractor = DataExtractor()
            >>> df_enero = extractor.load_monthly_data('enero')
        """
        encrypted_file = self.encrypted_dir / f"{month.lower()}.enc"

        if not encrypted_file.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {encrypted_file}")

        logger.info(f"Cargando datos de {month}...")
        
        # Manejo especial para noviembre (usa tabs en lugar de ;)
        separator = "\t" if month.lower() == "noviembre" else ";"
        
        df = self.data_manager.load_encrypted_csv(
            encrypted_file,
            encoding="latin1",
            sep=separator,
            skiprows=10,
        )

        df["mes"] = month.capitalize()
        logger.info(f"✓ {month.capitalize()}: {len(df):,} registros cargados")

        return df

    def load_all_months(self) -> pd.DataFrame:
        """
        Carga y consolida todos los meses del año.

        Returns:
            DataFrame consolidado con columna 'mes' y 'mes_num'

        Example:
            >>> extractor = DataExtractor()
            >>> df_completo = extractor.load_all_months()
            >>> print(df_completo['mes'].unique())
        """
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]

        dataframes = []
        failed_months = []

        logger.info("Iniciando carga de datos mensuales...")

        for i, mes in enumerate(meses, 1):
            try:
                df = self.load_monthly_data(mes)
                df["mes_num"] = i
                dataframes.append(df)
            except Exception as e:
                logger.error(f"✗ Error cargando {mes}: {e}")
                failed_months.append(mes)

        if not dataframes:
            raise ValueError("No se pudo cargar ningún archivo mensual")

        df_consolidado = pd.concat(dataframes, ignore_index=True)
        
        logger.info(
            f"✅ Consolidación completada: {len(df_consolidado):,} registros "
            f"({len(dataframes)}/{len(meses)} meses exitosos)"
        )

        if failed_months:
            logger.warning(f"Meses con errores: {', '.join(failed_months)}")

        return df_consolidado

    def load_annual_data(self) -> pd.DataFrame:
        """
        Carga el archivo anual consolidado.

        Returns:
            DataFrame con datos anuales

        Example:
            >>> extractor = DataExtractor()
            >>> df_anual = extractor.load_annual_data()
        """
        encrypted_file = self.encrypted_dir / "anual.enc"

        if not encrypted_file.exists():
            logger.warning("Archivo anual no encontrado")
            return pd.DataFrame()

        logger.info("Cargando datos anuales...")
        df = self.data_manager.load_encrypted_csv(encrypted_file)
        logger.info(f"✓ Datos anuales: {len(df):,} registros")

        return df


# Instancia global
extractor = DataExtractor()
