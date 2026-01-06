"""
Componentes de visualización para el dashboard
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional


def create_sales_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Gráfico de tendencia de ventas mensuales."""
    monthly = df.groupby(["mes", "mes_num"]).agg({
        "ingreso_total": "sum",
        "ganancia": "sum",
        "Cajas Vend.": "sum"
    }).reset_index().sort_values("mes_num")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly["mes"],
        y=monthly["ingreso_total"],
        name="Ingresos",
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly["mes"],
        y=monthly["ganancia"],
        name="Ganancia",
        mode="lines+markers",
        line=dict(color="#2ca02c", width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Tendencia de Ventas Mensuales",
        xaxis_title="Mes",
        yaxis_title="Monto ($)",
        hovermode="x unified",
        template="plotly_white",
        height=400
    )
    
    return fig


def create_category_chart(df: pd.DataFrame) -> go.Figure:
    """Gráfico de ventas por categoría."""
    category_sales = df.groupby("Rubro").agg({
        "ingreso_total": "sum",
        "Cajas Vend.": "sum"
    }).reset_index().nlargest(15, "ingreso_total")
    
    fig = px.bar(
        category_sales,
        x="ingreso_total",
        y="Rubro",
        orientation="h",
        title="Top 15 Rubros por Ingresos",
        labels={"ingreso_total": "Ingresos ($)", "Rubro": "Categoría"},
        color="ingreso_total",
        color_continuous_scale="Blues",
        height=500
    )
    
    fig.update_layout(template="plotly_white")
    
    return fig


def create_margin_distribution(df: pd.DataFrame) -> go.Figure:
    """Distribución de márgenes de ganancia."""
    fig = px.histogram(
        df[df["margen_porcentaje"].between(0, 100)],
        x="margen_porcentaje",
        nbins=50,
        title="Distribución de Márgenes de Ganancia",
        labels={"margen_porcentaje": "Margen (%)"},
        color_discrete_sequence=["#ff7f0e"],
        height=400
    )
    
    fig.update_layout(
        xaxis_title="Margen de Ganancia (%)",
        yaxis_title="Cantidad de Productos",
        template="plotly_white"
    )
    
    return fig


def create_top_products_chart(df: pd.DataFrame, n: int = 10) -> go.Figure:
    """Top N productos por ventas."""
    top = df.nlargest(n, "Cajas Vend.")[["Producto", "Cajas Vend.", "ingreso_total"]]
    top["Producto_short"] = top["Producto"].str[:30] + "..."
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=top["Cajas Vend."],
        y=top["Producto_short"],
        orientation="h",
        marker=dict(color="#d62728"),
        name="Cajas Vendidas"
    ))
    
    fig.update_layout(
        title=f"Top {n} Productos Más Vendidos",
        xaxis_title="Cajas Vendidas",
        yaxis_title="Producto",
        template="plotly_white",
        height=400
    )
    
    return fig


def create_stock_alert_chart(df: pd.DataFrame) -> go.Figure:
    """Alertas de productos con bajo stock."""
    # Productos con ventas pero poco stock
    low_stock = df[
        (df["Cajas Vend."] > 0) & 
        (df["Cajas Stock"] < 5) &
        (df["Cajas Stock"] >= 0)
    ].nlargest(15, "Cajas Vend.")
    
    fig = px.scatter(
        low_stock,
        x="Cajas Stock",
        y="Cajas Vend.",
        size="ingreso_total",
        color="Rubro",
        hover_data=["Producto", "Laboratorio"],
        title="⚠️ Productos con Alto Movimiento y Bajo Stock",
        labels={
            "Cajas Stock": "Stock Actual",
            "Cajas Vend.": "Ventas (cajas)",
            "ingreso_total": "Ingresos"
        },
        height=500
    )
    
    fig.update_layout(template="plotly_white")
    
    return fig
