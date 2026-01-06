"""
Pipeline ETL completo - Orquestación de extracción, transformación y validación
"""
import pandas as pd
from typing import Optional

from src.etl.extractors import extractor
from src.etl.transformers import transformer
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ETLPipeline:
    """
    Pipeline ETL completo para procesamiento de datos de ventas.
    
    Workflow:
    1. Extract: Carga datos cifrados
    2. Transform: Limpia y valida
    3. Load: Prepara para análisis
    """

    def __init__(self):
        """Inicializa el pipeline ETL."""
        self.extractor = extractor
        self.transformer = transformer
        logger.info("ETLPipeline inicializado")

    def run_full_pipeline(self) -> pd.DataFrame:
        """
        Ejecuta el pipeline ETL completo para todos los meses.

        Returns:
            DataFrame consolidado, limpio y validado

        Example:
            >>> pipeline = ETLPipeline()
            >>> df = pipeline.run_full_pipeline()
            >>> print(df.shape)
        """
        logger.info("=" * 70)
        logger.info("🚀 INICIANDO PIPELINE ETL")
        logger.info("=" * 70)

        # 1. EXTRACT
        logger.info("\n📥 FASE 1: EXTRACCIÓN")
        df_raw = self.extractor.load_all_months()
        logger.info(f"   Datos cargados: {len(df_raw):,} registros")

        # 2. TRANSFORM
        logger.info("\n🔄 FASE 2: TRANSFORMACIÓN")
        df_clean = self.transformer.clean_dataframe(df_raw)
        logger.info(f"   Datos limpios: {len(df_clean):,} registros")

        # 3. VALIDATE
        logger.info("\n✅ FASE 3: VALIDACIÓN")
        validation_report = self.transformer.validate_data(df_clean)
        
        logger.info("   Métricas de calidad:")
        logger.info(f"      • Registros válidos: {validation_report['registros_validos']:,}")
        logger.info(f"      • Duplicados: {validation_report['duplicados']:,}")
        
        if "productos_margen_negativo" in validation_report:
            logger.info(f"      • Margen negativo: {validation_report['productos_margen_negativo']:,}")

        # 4. CATEGORIZE
        logger.info("\n🏷️  FASE 4: CATEGORIZACIÓN")
        df_final = self.transformer.categorize_products(df_clean)

        logger.info("\n" + "=" * 70)
        logger.info(f"✅ PIPELINE COMPLETADO: {len(df_final):,} registros listos")
        logger.info("=" * 70)

        return df_final

    def run_monthly_pipeline(self, month: str) -> pd.DataFrame:
        """
        Ejecuta el pipeline para un mes específico.

        Args:
            month: Nombre del mes (ej: 'enero')

        Returns:
            DataFrame del mes procesado

        Example:
            >>> pipeline = ETLPipeline()
            >>> df_enero = pipeline.run_monthly_pipeline('enero')
        """
        logger.info(f"Procesando mes: {month}")
        
        df_raw = self.extractor.load_monthly_data(month)
        df_clean = self.transformer.clean_dataframe(df_raw)
        df_final = self.transformer.categorize_products(df_clean)
        
        logger.info(f"✓ {month.capitalize()} procesado: {len(df_final):,} registros")
        
        return df_final


# Instancia global
pipeline = ETLPipeline()
