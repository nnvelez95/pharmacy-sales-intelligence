# 🏥 Pharmacy Sales Intelligence Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: AES-256](https://img.shields.io/badge/encryption-AES--256-green.svg)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Objetivo

Plataforma de inteligencia de negocios para análisis de ventas farmacéuticas con:

- 📊 **Analytics avanzados** (ventas, inventario, rentabilidad)
- 🤖 **Machine Learning** (forecasting, segmentación)
- 🔒 **Seguridad de datos** (cifrado AES-256)
- 📱 **Dashboard interactivo** (Streamlit)

## 🔐 Seguridad

**⚠️ DATOS CONFIDENCIALES**: Los datos están cifrados con AES-256. Solo el propietario con la clave de cifrado puede procesarlos.

## 🚀 Quick Start

```bash
# Clonar repositorio
git clone <tu-repo>
cd pharmacy-sales-intelligence

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (crear .env)
cp .env.example .env
# EDITAR .env con tu clave de cifrado

# Cifrar tus datos (primera vez)
python src/security/encrypt_data.py

# Ejecutar dashboard
streamlit run app/streamlit_app.py
```

## 📁 Estructura del Proyecto

```
pharmacy-sales-intelligence/
├── data/
│   ├── encrypted/          # Datos cifrados (en Git)
│   └── processed/          # Procesados (NO en Git)
├── src/
│   ├── security/           # Cifrado/descifrado
│   ├── etl/                # Extracción y transformación
│   ├── analytics/          # Análisis de negocio
│   └── ml/                 # Machine Learning
├── app/                    # Dashboard Streamlit
├── tests/                  # Tests unitarios
└── notebooks/              # Jupyter notebooks
```

## 🛠️ Stack Tecnológico

- **Python 3.11+** con Type Hints
- **Cryptography** (AES-256-GCM)
- **Polars** (procesamiento rápido)
- **Streamlit** (dashboard)
- **Plotly** (visualizaciones)
- **Scikit-learn, Prophet** (ML)

## 📊 Análisis Disponibles

1. **Ventas Temporales**: Tendencias mensuales, estacionalidad
2. **Productos**: Top sellers, ABC analysis, rentabilidad
3. **Inventario**: Rotación, sobre/sub-stock
4. **Forecasting**: Predicción de demanda (3-6 meses)
5. **Segmentación**: Clustering de productos

## 🤝 Contribuir

Este proyecto usa datos confidenciales. Contribuciones son bienvenidas en la lógica de análisis y visualización, NO en datos.

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

Desarrollado por [Tu Nombre] | [LinkedIn](#) | [Portfolio](#)
