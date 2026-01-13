# Sistema Experto para Diagnóstico Inicial de Enfermedades Comunes

## 📋 Descripción
Sistema experto basado en reglas (IF-THEN) para brindar diagnósticos preliminares a partir de síntomas ingresados por el usuario. Desarrollado en Python con interfaz en Streamlit.

**⚠️ IMPORTANTE**: Este sistema NO reemplaza el diagnóstico médico profesional. Solo es un proyecto educativo.

## 🎯 Objetivo
Implementar un sistema de razonamiento basado en reglas para identificar enfermedades comunes (gripe, gastritis, infección respiratoria, etc.) a partir de síntomas.

## 👥 Equipo de Desarrollo
- **Luis** - Gestión de síntomas (Parte 1)
- **Germain** - Base de conocimiento (Parte 2)
- **Harry** - Motor de inferencia (Parte 3)
- **Tania** - Casos simulados y pruebas (Parte 4)
- **Favian** - Integración y flujo completo (Parte 5)

## 📁 Estructura del Proyecto
```
Proyecto Sist_Expertos/
├── src/                    # Código fuente principal
│   ├── symptoms.py         # Módulo de gestión de síntomas (Luis)
│   ├── knowledge_base.py   # Base de conocimiento (Germain)
│   ├── inference_engine.py # Motor de inferencia (Harry)
│   ├── cases.py           # Casos simulados (Tania)
│   └── app.py             # Aplicación integrada (Favian)
├── data/                   # Datos y casos de prueba
│   └── test_cases.csv     # Dataset de pruebas
├── tests/                  # Pruebas unitarias
├── docs/                   # Documentación adicional
├── requirements.txt        # Dependencias Python
└── README.md              # Este archivo
```

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd "Proyecto Sist_Expertos"
```

2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Ejecución

### Ejecutar la aplicación completa:
```bash
streamlit run src/app.py
```

### Ejecutar módulos individuales (desarrollo):
```bash
streamlit run src/symptoms.py
streamlit run src/knowledge_base.py
streamlit run src/inference_engine.py
streamlit run src/cases.py
```

## 🔧 Tecnologías
- **Python 3.8+**
- **Streamlit** - Interfaz de usuario
- **Pandas** - Manejo de datos (opcional)

## 📝 Workflow de Desarrollo

1. Cada integrante trabaja en su rama:
   ```bash
   git checkout -b feature/nombre-modulo
   ```

2. Desarrollar el módulo asignado

3. Probar el módulo individual

4. Hacer commit y push:
   ```bash
   git add .
   git commit -m "feat: descripción del cambio"
   git push origin feature/nombre-modulo
   ```

5. Crear Pull Request para revisión

6. Integrar en la rama principal

## 📚 Documentación de Módulos

Ver [Repartición.md](Repartición.md) para detalles de cada módulo y responsabilidades.

## 🤝 Contribución

Cada integrante debe:
- Desarrollar su módulo asignado
- Crear su interfaz parcial en Streamlit
- Documentar su código con comentarios
- Probar su módulo antes de integrar

## 📅 Curso
**Sistemas Inteligentes - VI Ciclo**  
Fecha: Enero 2026
