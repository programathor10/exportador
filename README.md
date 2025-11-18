# 📊 API Data Exporter – Python Script (API → Excel / JSON)

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

Este proyecto es un script modular en **Python** que se conecta a una **API REST**, valida la información obtenida y genera reportes automáticos en **Excel** y **JSON**.  
Incluye manejo de errores, logs, estructura profesional y parámetros por línea de comandos (CLI).

---

## 🧩 ¿Qué problema resuelve?

Muchos equipos necesitan:

- Descargar datos desde una API externa.
- Validar que la respuesta tenga el formato correcto.
- Unificar la información y generar reportes para análisis o negocio.

Este script automatiza ese flujo completo: **API → procesamiento → reporte listo**.

---

## 🚀 Características principales

- ✔ Conexión a API REST pública (JSONPlaceholder).
- ✔ Validación de datos (claves requeridas, tipos).
- ✔ Manejo de errores (HTTP, JSON inválido, claves faltantes, etc.).
- ✔ Estructura modular tipo proyecto real:
  - `api_client.py` → cliente HTTP.
  - `processors.py` → validación + armado del DataFrame.
  - `exporters.py` → exportadores a Excel/JSON.
  - `main.py` → punto de entrada con CLI.
- ✔ Exportación a:
  - **Excel (.xlsx)**
  - **JSON (.json)**
- ✔ CLI para configurar:
  - cantidad de registros (`--limit`)
  - formato de salida (`--format`)
  - directorio de salida (`--output-dir`)
  - nivel de logs (`--log-level`)

---

## 🧱 Estructura del Proyecto

```text
exportador/
├─ api_client.py        # Cliente HTTP: llamadas a la API y manejo de errores
├─ processors.py        # Validación de datos y combinación de info
├─ exporters.py         # Exportación a Excel y JSON
├─ main.py              # Script principal con interface de línea de comandos
├─ requirements.txt     # Dependencias del proyecto
└─ .gitignore           # Archivos a ignorar (entorno, output, cachés, etc.)
