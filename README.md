# Urban Routes - Pruebas de Automatización
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-orange)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-Testing%20Framework-green)](https://docs.pytest.org/)
[![Chrome](https://img.shields.io/badge/Chrome-Latest%20Stable-brightgreen)](https://www.google.com/chrome/)

**Autor:** Ahmed José Medina Ortiz
**Grupo:** QA Cohort 29

## 🚀 Demostración de Ejecución de Pruebas

Aquí puedes ver las pruebas en acción, interactuando con la aplicación web y validando sus funcionalidades.

[![Demostración de Pruebas Automatizadas con Selenium y Pytest](https://img.youtube.com/vi/qCp7TrAIaz0/0.jpg)](https://www.youtube.com/watch?v=qCp7TrAIaz0)


## Tecnologías Utilizadas
| Componente       | Versión  | Uso                              |
|------------------|----------|----------------------------------|
| Python           | 3.10+    | Lenguaje base                    |
| Selenium WebDriver | 4.0+   | Automatización navegador         |
| Pytest           | 7.0+     | Framework de testing             |
| ChromeDriver     | Compatible | Controlador navegador          |

## Descripción del Proyecto
Framework de Automatización de Pruebas para Aplicación Web Urban Routes para el flujo de reserva de taxis en Urban Routes, verificando:

```plaintext
1. Configuración de rutas
2. Selección de tarifas Comfort  
3. Validación OTP por SMS
4. Gestión de métodos de pago
5. Personalización de viaje
6. Confirmación de reserva

🚀 Cómo Ejecutar las Pruebas
Prerrequisitos
Python 3.10 o superior instalado

Google Chrome instalado (versión estable más reciente)

ChromeDriver (compatible con tu versión de Chrome)

## 🛠 Instalación
1. Clona el repositorio:
```bash
git clone https://github.com/AhmedMdna/qa-project-Urban-Routes-es
cd tu-repo
pip install pytest requests

2. Crea y activa un entorno virtual (recomendado):

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

🗂 Estructura
.
├── data.py # datos de pruebas y URL
├── main.py # Casos de prueba (9 casos) y Page Objects
└── README.md

▶ Ejecución
bash
# Ejecutar todas las pruebas:
pytest main.py -v

# Ejecutar prueba específica:
pytest main.py::TestUrbanRoutes::test4_add_credit_card -v

Licencia
Material educativo - TripleTen QA Automation © 2025
