"""
Script para cifrar los archivos CSV iniciales.
Ejecutar UNA VEZ después de tener los CSVs en data/raw/
"""
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("🔄 Importando módulos...")

from src.config import settings
from src.security.data_manager import data_manager
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

print("✅ Módulos importados correctamente")


def main():
    """Cifra todos los archivos CSV de data/raw/"""
    print("\n🚀 Iniciando función main()...")
    
    raw_data_dir = Path(__file__).parent.parent / "data" / "raw"

    print("=" * 70)
    print("🔒 CIFRADO DE DATOS INICIALES")
    print("=" * 70)
    print(f"\nDirectorio fuente: {raw_data_dir}")
    print(f"Directorio destino: {settings.encrypted_dir}\n")

    # Crear directorio si no existe
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    if not raw_data_dir.exists():
        print(f"❌ Error: El directorio {raw_data_dir} no existe")
        print("   Por favor, coloca tus archivos CSV en data/raw/")
        return

    csv_files = list(raw_data_dir.glob("*.csv"))

    if not csv_files:
        print("❌ No se encontraron archivos CSV en data/raw/")
        print(f"\n💡 Asegúrate de que tus archivos estén en: {raw_data_dir}")
        print("   Los archivos deben tener extensión .csv")
        return

    print(f"📁 Archivos encontrados: {len(csv_files)}")
    for f in csv_files:
        print(f"   - {f.name}")

    print()
    confirm = input("¿Deseas continuar con el cifrado? (s/n): ")

    if confirm.lower() != "s":
        print("❌ Operación cancelada")
        return

    print()
    encrypted_files = data_manager.encrypt_all_csvs(raw_data_dir)

    print("\n" + "=" * 70)
    print(f"✅ COMPLETADO: {len(encrypted_files)} archivos cifrados")
    print("=" * 70)
    print("\n⚠️  IMPORTANTE:")
    print("   1. Los archivos cifrados están en data/encrypted/")
    print("   2. Puedes eliminar los CSV originales de data/raw/ por seguridad")
    print("   3. NUNCA subas a Git los archivos .csv originales")
    print("   4. Los archivos .enc SÍ pueden ir a Git (están protegidos)\n")


if __name__ == "__main__":
    print("=" * 70)
    print("🎬 Script iniciado")
    print("=" * 70)
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "=" * 70)
        print("🏁 Script finalizado")
        print("=" * 70)
