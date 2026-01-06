"""
🏥 Pharmacy Sales Intelligence Dashboard
Dashboard interactivo para análisis de ventas farmacéuticas
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ✅ CONFIGURACIÓN DE PANDAS
pd.set_option("styler.render.max_elements", 1_000_000)

from src.etl.pipeline import pipeline
from app.utils.metrics import calculate_kpis, get_top_products
from app.components.charts import (
    create_sales_trend_chart,
    create_category_chart,
    create_margin_distribution,
    create_top_products_chart,
    create_stock_alert_chart
)

# Configuración de la página
st.set_page_config(
    page_title="Pharmacy Sales Intelligence",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stAlert {
        background-color: #f0f2f6;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_data():
    """Carga datos con caché (1 hora)."""
    with st.spinner("🔐 Cargando datos cifrados de forma segura..."):
        df = pipeline.run_full_pipeline()
    return df


def main():
    """Función principal del dashboard."""
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Pharmacy Sales Intelligence</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Cargar datos
    try:
        df = load_data()
    except Exception as e:
        st.error(f"❌ Error cargando datos: {e}")
        st.info("💡 Asegúrate de que los archivos cifrados estén en data/encrypted/")
        st.stop()
    
    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de mes
    meses_disponibles = ["Todos"] + sorted(df["mes"].unique().tolist())
    mes_seleccionado = st.sidebar.selectbox("📅 Mes", meses_disponibles)
    
    # Filtro de rubro
    rubros_disponibles = ["Todos"] + sorted(df["Rubro"].unique().tolist())
    rubro_seleccionado = st.sidebar.selectbox("📁 Rubro", rubros_disponibles)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if mes_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["mes"] == mes_seleccionado]
    if rubro_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Rubro"] == rubro_seleccionado]
    
    # Calcular KPIs
    kpis = calculate_kpis(df_filtrado)
    
    # Información del dataset
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Info del Dataset")
    st.sidebar.metric("Registros totales", f"{len(df):,}")
    st.sidebar.metric("Registros filtrados", f"{len(df_filtrado):,}")
    st.sidebar.metric("Meses disponibles", df["mes"].nunique())
    
    # === SECCIÓN 1: KPIs PRINCIPALES ===
    st.header("📊 Indicadores Clave de Rendimiento (KPIs)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Ingresos Totales",
            f"${kpis['total_ingresos']:,.0f}",
            delta=f"{kpis['margen_promedio']:.1f}% margen"
        )
    
    with col2:
        st.metric(
            "📈 Ganancia Bruta",
            f"${kpis['total_ganancia']:,.0f}",
            delta=f"{(kpis['total_ganancia']/kpis['total_ingresos']*100):.1f}%"
        )
    
    with col3:
        st.metric(
            "📦 Ventas (Cajas)",
            f"{kpis['total_ventas_cajas']:,.0f}",
            delta=f"{kpis['productos_vendidos']} productos"
        )
    
    with col4:
        st.metric(
            "🏪 Stock Total",
            f"{kpis['stock_total']:,.0f}",
            delta=f"${kpis['valor_stock']:,.0f} valor"
        )
    
    st.markdown("---")
    
    # === SECCIÓN 2: ANÁLISIS TEMPORAL ===
    st.header("📈 Análisis Temporal")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(create_sales_trend_chart(df_filtrado), use_container_width=True)
    
    with col2:
        st.subheader("🎯 Métricas del Período")
        st.metric("Ticket Promedio", f"${kpis['ticket_promedio']:,.2f}")
        st.metric("Productos Únicos", f"{kpis['productos_unicos']:,}")
        st.metric("Laboratorios Activos", f"{kpis['laboratorios_activos']:,}")
        st.metric("Rubros Activos", f"{kpis['rubros_activos']:,}")
    
    st.markdown("---")
    
    # === SECCIÓN 3: ANÁLISIS DE PRODUCTOS ===
    st.header("🏆 Top Productos")
    
    tab1, tab2, tab3 = st.tabs(["🔝 Más Vendidos", "💰 Más Rentables", "⚠️ Alertas de Stock"])
    
    with tab1:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.plotly_chart(create_top_products_chart(df_filtrado, n=10), use_container_width=True)
        with col2:
            st.subheader("Top 10 por Ventas")
            top_ventas = get_top_products(df_filtrado, n=10, metric="Cajas Vend.")
            st.dataframe(
                top_ventas[["Producto", "Cajas Vend.", "ingreso_total"]],
                hide_index=True,
                use_container_width=True
            )
    
    with tab2:
        top_rentables = get_top_products(df_filtrado, n=15, metric="ganancia")
        st.dataframe(
            top_rentables[["Producto", "Laboratorio", "Rubro", "ganancia", "ingreso_total"]],
            hide_index=True,
            use_container_width=True,
            height=400
        )
    
    with tab3:
        st.plotly_chart(create_stock_alert_chart(df_filtrado), use_container_width=True)
        
        # Tabla de productos críticos
        productos_criticos = df_filtrado[
            (df_filtrado["Cajas Vend."] > 0) & 
            (df_filtrado["Cajas Stock"] == 0)
        ].nlargest(10, "Cajas Vend.")
        
        if len(productos_criticos) > 0:
            st.warning(f"⚠️ {len(productos_criticos)} productos con ventas pero SIN STOCK")
            st.dataframe(
                productos_criticos[["Producto", "Laboratorio", "Cajas Vend.", "ingreso_total"]],
                hide_index=True,
                use_container_width=True
            )
    
    st.markdown("---")
    
    # === SECCIÓN 4: ANÁLISIS POR CATEGORÍA ===
    st.header("📁 Análisis por Rubro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_category_chart(df_filtrado), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_margin_distribution(df_filtrado), use_container_width=True)
    
    st.markdown("---")
    
    # === SECCIÓN 5: DATOS DETALLADOS (MEJORADO) ===
    with st.expander("📋 Ver Datos Detallados"):
        st.subheader("Tabla de Datos Completa")
        
        # Info
        st.info(f"📊 Mostrando {len(df_filtrado):,} registros")
        
        # Opción de descarga
        col1, col2 = st.columns([3, 1])
        with col2:
            csv = df_filtrado[[
                "Producto", "Laboratorio", "Rubro", "mes",
                "PVP", "Costo", "Cajas Vend.", "Cajas Stock",
                "ingreso_total", "ganancia", "margen_porcentaje"
            ]].to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="datos_filtrados.csv",
                mime="text/csv",
            )
        
        # Mostrar tabla (limitada a primeros 1000 para performance)
        registros_a_mostrar = min(1000, len(df_filtrado))
        
        if len(df_filtrado) > 1000:
            st.warning(f"⚠️ Mostrando primeros {registros_a_mostrar:,} de {len(df_filtrado):,} registros. Descarga el CSV para ver todos.")
        
        st.dataframe(
            df_filtrado[[
                "Producto", "Laboratorio", "Rubro", "mes",
                "PVP", "Costo", "Cajas Vend.", "Cajas Stock",
                "ingreso_total", "ganancia", "margen_porcentaje"
            ]].head(registros_a_mostrar),
            hide_index=True,
            use_container_width=True,
            height=400
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888;'>
            <p>🔒 Datos protegidos con cifrado AES-256 | 
            Desarrollado con Streamlit & Python | 
            © 2026 Pharmacy Sales Intelligence</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
