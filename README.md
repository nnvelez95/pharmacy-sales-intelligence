# 🏥 Pharmacy Sales Intelligence Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29+-red.svg)](https://streamlit.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: AES-256](https://img.shields.io/badge/encryption-AES--256-green.svg)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Last Commit](https://img.shields.io/github/last-commit/nnvelez95/pharmacy-sales-intelligence)

> **Plataforma de inteligencia de negocios para análisis de ventas farmacéuticas con cifrado de datos end-to-end, pipeline ETL automatizado y dashboard interactivo desarrollado con Python y Streamlit.**

---

## 🎯 Sobre el Proyecto

Sistema completo de Business Intelligence diseñado para analizar datos de ventas farmacéuticas manteniendo la **seguridad y confidencialidad** de la información mediante **cifrado AES-256-GCM**. 

### Problema que Resuelve
Las farmacias generan grandes volúmenes de datos de ventas, inventario y productos, pero carecen de herramientas accesibles para:
- Analizar tendencias de ventas
- Identificar productos rentables
- Gestionar inventario eficientemente
- Proteger datos sensibles del negocio

### Solución Implementada
Plataforma modular que integra:
1. **Seguridad**: Cifrado de archivos con AES-256
2. **ETL**: Pipeline automatizado para limpieza y transformación
3. **Analytics**: Cálculo de KPIs y métricas de negocio
4. **Visualización**: Dashboard interactivo con filtros dinámicos

---

## ✨ Características Principales

### 🔐 Seguridad
- **Cifrado AES-256-GCM** con autenticación de integridad
- Datos raw **nunca persisten sin cifrar**
- Descifrado en memoria durante procesamiento
- Gestión de claves mediante variables de entorno
- Compatible con estándares de seguridad empresarial

### 📊 Analytics
- **KPIs en tiempo real**: ingresos, ganancias, márgenes
- **Análisis temporal**: tendencias mensuales y estacionalidad
- **Top productos**: por ventas y rentabilidad
- **Gestión de inventario**: alertas de stock bajo
- **Análisis por categoría**: rubros y laboratorios
- **Distribución de márgenes**: histogramas interactivos

### 🎨 Dashboard Interactivo
- Filtros dinámicos por mes y categoría
- Visualizaciones con Plotly (zoom, pan, export)
- Tablas con formato profesional
- Descarga de datos filtrados en CSV
- Caché inteligente para performance
- Responsive design

### ⚙️ Pipeline ETL
- Extracción segura desde archivos cifrados
- Limpieza y normalización de datos
- Validaciones de calidad automáticas
- Cálculo de métricas derivadas
- Categorización automática de productos
- Complejidad O(n) optimizada

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│           Datos Raw (CSV)                   │
│  ├── enero.csv, febrero.csv, ...           │
│  └── Información sensible del negocio      │
└─────────────────────────────────────────────┘
                    ↓ Cifrado AES-256
┌─────────────────────────────────────────────┐
│        Datos Cifrados (*.enc)               │
│  ├── Solo legibles con clave correcta      │
│  └── Almacenados de forma segura           │
└─────────────────────────────────────────────┘
                    ↓ ETL Pipeline
┌─────────────────────────────────────────────┐
│       Procesamiento en Memoria              │
│  ├── Extracción y descifrado temporal      │
│  ├── Transformación y validación           │
│  └── Cálculo de métricas                   │
└─────────────────────────────────────────────┘
                    ↓ Agregación
┌─────────────────────────────────────────────┐
│          Dashboard Streamlit                │
│  ├── Solo visualiza datos agregados        │
│  └── Sin exposición de datos individuales  │
└─────────────────────────────────────────────┘
```

---

## 🚀 Instalación y Uso

### Prerequisitos
- Python 3.11 o superior
- pip o poetry para gestión de dependencias
- Git

### 1. Clonar el Repositorio
```bash
git clone https://github.com/nnvelez95/pharmacy-sales-intelligence.git
cd pharmacy-sales-intelligence
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar plantilla
cp .env.example .env

# Generar clave de cifrado (copiar el output)
python -c "import secrets; print(secrets.token_hex(32))"

# Editar .env y pegar la clave
# ENCRYPTION_KEY=tu-clave-generada-aqui
```

### 5. Cifrar tus Datos (Primera vez)
```bash
# Colocar archivos CSV en data/raw/
# Luego ejecutar:
python scripts/encrypt_initial_data.py
```

### 6. Ejecutar Dashboard
```bash
streamlit run app/streamlit_app.py
```

El dashboard se abrirá automáticamente en `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
pharmacy-sales-intelligence/
├── app/                        # Dashboard Streamlit
│   ├── components/            # Componentes de visualización
│   │   └── charts.py         # Gráficos con Plotly
│   ├── utils/                # Utilidades del dashboard
│   │   └── metrics.py        # Cálculo de KPIs
│   └── streamlit_app.py      # Aplicación principal
│
├── src/                       # Código fuente
│   ├── security/             # Sistema de cifrado
│   │   ├── encryption.py     # AES-256-GCM
│   │   └── data_manager.py   # Gestor de datos cifrados
│   ├── etl/                  # Pipeline ETL
│   │   ├── extractors.py     # Carga de datos
│   │   ├── transformers.py   # Limpieza y validación
│   │   └── pipeline.py       # Orquestación
│   ├── analytics/            # (Futuro) Análisis avanzados
│   ├── ml/                   # (Futuro) Machine Learning
│   ├── utils/                # Utilidades generales
│   │   └── logger.py         # Sistema de logging
│   └── config.py             # Configuración centralizada
│
├── data/                      # Directorio de datos
│   ├── encrypted/            # Archivos cifrados (*.enc)
│   ├── processed/            # Cache temporal (no en Git)
│   └── raw/                  # CSVs originales (no en Git)
│
├── scripts/                   # Scripts de utilidad
│   └── encrypt_initial_data.py
│
├── tests/                     # Tests unitarios
│   ├── unit/
│   └── integration/
│
├── notebooks/                 # Jupyter notebooks
├── logs/                      # Archivos de log
├── .env.example              # Template de configuración
├── .gitignore                # Archivos ignorados por Git
├── requirements.txt          # Dependencias Python
├── CHANGELOG.md              # Historial de cambios
├── CONTRIBUTING.md           # Guía de contribución
├── LICENSE                   # Licencia MIT
└── README.md                 # Este archivo
```

---

## 🛠️ Stack Tecnológico

| Categoría | Tecnología | Propósito |
|-----------|-----------|-----------|
| Lenguaje | Python 3.11+ | Core del proyecto |
| Seguridad | cryptography | Cifrado AES-256-GCM |
| Data Processing | Pandas, Polars | Transformación de datos |
| Validación | Pydantic | Validación de configuración |
| Dashboard | Streamlit | Interfaz web interactiva |
| Visualización | Plotly, Altair | Gráficos interactivos |
| ML | Scikit-learn, Prophet | Análisis predictivo |
| Testing | Pytest | Tests automatizados |
| Code Quality | Black, Pylint, MyPy | Linting y type checking |

---

## 📊 Métricas del Proyecto

- **~71,000 registros** de datos procesados
- **12 meses** de información histórica
- **6,000+ productos** únicos analizados
- **800+ laboratorios** en el catálogo
- **40+ rubros** categorizados
- **<2 segundos** de carga del dashboard (con caché)

---

## 🔒 Nota de Seguridad

Los archivos `*.enc` en este repositorio están protegidos con **AES-256-GCM**.

⚠️ **Información importante:**

- Los datos raw **NUNCA** están en el repositorio
- Solo el propietario con la clave correcta puede descifrarlos
- El descifrado ocurre en memoria durante el procesamiento
- No se persisten datos sin cifrar en ningún momento
- Compatible con normativas de protección de datos

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre nuestro código de conducta y el proceso para enviar pull requests.

### Áreas de Contribución
- 🐛 Reportar bugs o errores
- ✨ Sugerir nuevas funcionalidades
- 📝 Mejorar documentación
- 🧪 Agregar tests
- 🎨 Mejorar visualizaciones
- 🤖 Implementar modelos de ML

---

## 📈 Roadmap

### Versión 1.1 (En desarrollo)
- [ ] Tests unitarios con Pytest (cobertura >80%)
- [ ] GitHub Actions para CI/CD
- [ ] Pre-commit hooks automáticos
- [ ] Documentación API con Sphinx

### Versión 2.0 (Futuro)
- [ ] Módulo de Machine Learning (forecasting, clustering)
- [ ] Análisis de sentiment en productos
- [ ] Sistema de recomendaciones
- [ ] API REST con FastAPI
- [ ] Base de datos SQL para históricos
- [ ] Multi-farmacia support

---

## 📫 Contacto

**Norberto Velez**

- 💼 LinkedIn: www.linkedin.com/in/norberto-velez-672916172
- 📧 Email: nnvelez95@gmail.com
- 🐙 GitHub: [@nnvelez95](https://github.com/nnvelez95)

**Project Link:** [https://github.com/nnvelez95/pharmacy-sales-intelligence](https://github.com/nnvelez95/pharmacy-sales-intelligence)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- [Streamlit](https://streamlit.io) - Framework para el dashboard
- [Plotly](https://plotly.com) - Visualizaciones interactivas
- [Cryptography](https://cryptography.io) - Biblioteca de cifrado
- [Pandas](https://pandas.pydata.org) - Análisis de datos
- [Pydantic](https://pydantic-docs.helpmanual.io) - Validación de datos

---

## ⭐ Star History

Si este proyecto te resultó útil, considera darle una estrella ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=nnvelez95/pharmacy-sales-intelligence&type=Date)](https://star-history.com/#nnvelez95/pharmacy-sales-intelligence&Date)

---

<div align="center">
  <sub>Desarrollado con ❤️ y ☕ por Norberto Velez</sub>
</div>
