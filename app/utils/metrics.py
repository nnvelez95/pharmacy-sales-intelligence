"""
Utilidades para cálculo de métricas del dashboard
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula KPIs principales del negocio.
    
    Args:
        df: DataFrame con datos procesados
        
    Returns:
        Diccionario con KPIs
    """
    kpis = {
        # Ventas
        "total_ventas_cajas": df["Cajas Vend."].sum(),
        "total_ingresos": df["ingreso_total"].sum(),
        "total_ganancia": df["ganancia"].sum(),
        "margen_promedio": df["margen_porcentaje"].mean(),
        
        # Productos
        "productos_unicos": df["Producto"].nunique(),
        "productos_vendidos": df[df["Cajas Vend."] > 0]["Producto"].nunique(),
        "productos_sin_ventas": df[df["Cajas Vend."] == 0]["Producto"].nunique(),
        
        # Inventario
        "stock_total": df["Cajas Stock"].sum(),
        "valor_stock": (df["Costo"] * df["Cajas Stock"]).sum(),
        
        # Comercial
        "laboratorios_activos": df[df["Cajas Vend."] > 0]["Laboratorio"].nunique(),
        "rubros_activos": df[df["Cajas Vend."] > 0]["Rubro"].nunique(),
        
        # Ticket promedio
        "ticket_promedio": df[df["Cajas Vend."] > 0]["PVP"].mean(),
    }
    
    return kpis


def calculate_growth(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula crecimiento mes a mes.
    
    Args:
        df: DataFrame con columna 'mes_num'
        
    Returns:
        DataFrame con métricas de crecimiento
    """
    monthly = df.groupby("mes_num").agg({
        "ingreso_total": "sum",
        "ganancia": "sum",
        "Cajas Vend.": "sum"
    }).reset_index()
    
    monthly["crecimiento_ingresos"] = monthly["ingreso_total"].pct_change() * 100
    monthly["crecimiento_ventas"] = monthly["Cajas Vend."].pct_change() * 100
    
    return monthly


def get_top_products(df: pd.DataFrame, n: int = 10, metric: str = "Cajas Vend.") -> pd.DataFrame:
    """
    Obtiene top N productos por métrica.
    
    Args:
        df: DataFrame
        n: Cantidad de productos
        metric: Métrica para ordenar
        
    Returns:
        DataFrame con top productos (sin duplicados de columnas)
    """
    # Columnas base
    base_columns = ["Producto", "Laboratorio", "Rubro"]
    
    # Columnas adicionales (evitando duplicados)
    additional_columns = ["ingreso_total", "ganancia", "Cajas Vend."]
    
    # Construir lista de columnas sin duplicados
    columns = base_columns.copy()
    
    # Agregar la métrica primero si no está en base_columns
    if metric not in columns:
        columns.append(metric)
    
    # Agregar columnas adicionales que no estén ya incluidas
    for col in additional_columns:
        if col not in columns and col in df.columns:
            columns.append(col)
    
    # Retornar top N productos
    return df.nlargest(n, metric)[columns]
