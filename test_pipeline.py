"""
Script de prueba del pipeline ETL
"""
from src.etl.pipeline import pipeline

def main():
    print("=" * 70)
    print("🧪 PRUEBA DEL PIPELINE ETL")
    print("=" * 70)
    
    # Ejecutar pipeline completo
    df = pipeline.run_full_pipeline()
    
    # Mostrar resultados
    print("\n📊 RESUMEN DE DATOS PROCESADOS:")
    print(f"   • Total de registros: {len(df):,}")
    print(f"   • Columnas: {len(df.columns)}")
    print(f"   • Meses: {df['mes'].nunique()}")
    print(f"   • Productos únicos: {df['Producto'].nunique():,}")
    print(f"   • Laboratorios: {df['Laboratorio'].nunique():,}")
    print(f"   • Rubros: {df['Rubro'].nunique():,}")
    
    print(f"\n💰 MÉTRICAS FINANCIERAS:")
    print(f"   • Ventas totales: {df['Cajas Vend.'].sum():,.0f} cajas")
    print(f"   • Ingresos totales: ${df['ingreso_total'].sum():,.2f}")
    print(f"   • Ganancia total: ${df['ganancia'].sum():,.2f}")
    print(f"   • Margen promedio: {df['margen_porcentaje'].mean():.2f}%")
    
    print(f"\n🔝 TOP 5 PRODUCTOS POR VENTAS:")
    top5 = df.nlargest(5, 'Cajas Vend.')[['Producto', 'Cajas Vend.', 'ingreso_total']]
    for idx, row in top5.iterrows():
        print(f"   • {row['Producto'][:50]}: {row['Cajas Vend.']:.0f} cajas (${row['ingreso_total']:,.2f})")
    
    print("\n" + "=" * 70)
    print("✅ PIPELINE FUNCIONANDO CORRECTAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    main()
