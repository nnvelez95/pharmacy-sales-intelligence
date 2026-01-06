"""
Transformadores de datos - Limpieza, validación y preparación
"""
from typing import List, Optional

import pandas as pd
import numpy as np

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataTransformer:
    """
    Transformador de datos con validaciones y limpieza.
    Aplica reglas de negocio y prepara datos para análisis.
    """

    def __init__(self):
        """Inicializa el transformador."""
        self.numeric_columns = ["Costo", "PVP", "Cajas Vend.", "Cajas Stock"]
        logger.info("DataTransformer inicializado")

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia y prepara un DataFrame para análisis.

        Args:
            df: DataFrame raw

        Returns:
            DataFrame limpio y validado

        Transformaciones:
        - Normaliza nombres de columnas
        - Convierte tipos de datos
        - Elimina registros inválidos
        - Calcula métricas derivadas
        """
        df = df.copy()
        
        logger.info(f"Limpiando DataFrame: {len(df):,} registros")

        # 1. Normalizar nombres de columnas
        df.columns = df.columns.str.strip()

        # 2. Convertir columnas numéricas
        for col in self.numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # 3. Eliminar fila "zzzz" (placeholder del sistema)
        if "Producto" in df.columns:
            df = df[df["Producto"].str.lower() != "zzzz"]

        # 4. Eliminar registros sin producto
        df = df.dropna(subset=["Producto"])

        # 5. Normalizar strings
        string_columns = ["Producto", "Laboratorio", "Rubro"]
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].str.strip()

        # 6. Calcular métricas derivadas
        df = self._add_calculated_fields(df)

        logger.info(f"✓ Limpieza completada: {len(df):,} registros válidos")

        return df

    def _add_calculated_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrega campos calculados para análisis financiero.

        Args:
            df: DataFrame con datos limpios

        Returns:
            DataFrame con columnas adicionales

        Campos agregados:
        - ingreso_total: PVP × Cajas Vendidas
        - costo_total: Costo × Cajas Vendidas
        - ganancia: Ingreso - Costo
        - margen_porcentaje: (Ganancia / Ingreso) × 100
        - precio_unitario_ganancia: PVP - Costo
        """
        # Calcular ingresos y costos totales
        df["ingreso_total"] = df["PVP"] * df["Cajas Vend."]
        df["costo_total"] = df["Costo"] * df["Cajas Vend."]
        
        # Calcular ganancia
        df["ganancia"] = df["ingreso_total"] - df["costo_total"]
        
        # Calcular margen porcentual
        df["margen_porcentaje"] = np.where(
            df["ingreso_total"] > 0,
            (df["ganancia"] / df["ingreso_total"]) * 100,
            0
        )
        
        # Ganancia por unidad
        df["precio_unitario_ganancia"] = df["PVP"] - df["Costo"]
        
        # Margen unitario
        df["margen_unitario_porcentaje"] = np.where(
            df["PVP"] > 0,
            (df["precio_unitario_ganancia"] / df["PVP"]) * 100,
            0
        )

        return df

    def validate_data(self, df: pd.DataFrame) -> dict:
        """
        Valida la calidad de los datos y genera reporte.

        Args:
            df: DataFrame a validar

        Returns:
            Diccionario con métricas de calidad

        Example:
            >>> transformer = DataTransformer()
            >>> report = transformer.validate_data(df)
            >>> print(report['registros_totales'])
        """
        report = {
            "registros_totales": len(df),
            "registros_validos": len(df[df["Producto"].notna()]),
            "columnas": len(df.columns),
            "nulos_por_columna": df.isnull().sum().to_dict(),
            "duplicados": df.duplicated(subset=["IDProducto"]).sum(),
        }

        # Validaciones de negocio
        if "PVP" in df.columns and "Costo" in df.columns:
            report["productos_margen_negativo"] = len(df[df["PVP"] < df["Costo"]])
            report["productos_precio_cero"] = len(df[df["PVP"] == 0])

        if "Cajas Stock" in df.columns:
            report["productos_stock_negativo"] = len(df[df["Cajas Stock"] < 0])

        logger.info(f"Reporte de validación: {report['registros_validos']}/{report['registros_totales']} válidos")

        return report

    def categorize_products(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categoriza productos según criterios de negocio.

        Args:
            df: DataFrame con datos

        Returns:
            DataFrame con columnas de categorización adicionales

        Categorías:
        - categoria_precio: Bajo, Medio, Alto, Premium, Lujo
        - categoria_venta: Sin Ventas, Baja, Media, Alta
        - categoria_stock: Sin Stock, Bajo, Medio, Alto
        """
        df = df.copy()

        # Categoría por precio
        df["categoria_precio"] = pd.cut(
            df["PVP"],
            bins=[0, 5000, 10000, 20000, 50000, float("inf")],
            labels=["Bajo", "Medio", "Alto", "Premium", "Lujo"],
        )

        # Categoría por ventas
        df["categoria_venta"] = pd.cut(
            df["Cajas Vend."],
            bins=[-float("inf"), 0, 1, 5, float("inf")],
            labels=["Sin Ventas", "Baja", "Media", "Alta"],
        )

        # Categoría por stock
        df["categoria_stock"] = pd.cut(
            df["Cajas Stock"],
            bins=[-float("inf"), 0, 5, 20, float("inf")],
            labels=["Sin Stock", "Bajo", "Medio", "Alto"],
        )

        logger.info("✓ Productos categorizados")

        return df


# Instancia global
transformer = DataTransformer()
