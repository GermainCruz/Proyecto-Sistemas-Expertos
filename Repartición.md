Parte 1: Gestión de síntomas (Entrada del usuario)

Integrante 1 (LUIS)

Responsabilidad principal:
* Definir el listado oficial de síntomas.
* Diseñar cómo el usuario ingresa los síntomas.

Programación:
* Estructura de síntomas en Python.
* Interfaz en Streamlit con:
        - Checkboxes / multiselect de síntomas.
        - Validaciones (mínimo 1 síntoma).

Entregables:
* symptoms.py

* Vista Streamlit:
    - Selección de síntomas
    - Visualización de síntomas elegidos

👉 Esta parte alimenta a todo el sistema.



Parte 2: Base de conocimiento (enfermedades y reglas base)

Integrante 2 (GERMAIN)

Responsabilidad principal
* Definir las enfermedades comunes.
* Relacionarlas con síntomas mediante reglas.

Programación
* Diccionarios o estructuras tipo:
        enfermedad → síntomas asociados
* Reglas simples (sin inferencia compleja aún).


Interfaz en Streamlit
Mostrar:
* Lista de enfermedades
* Síntomas asociados a cada una

Entregables
* knowledge_base.py
* Vista informativa en Streamlit (debug / visualización)

👉 Es la “memoria” del sistema experto



Parte 3: Motor de inferencia

Integrante 3 (Harry)

Responsabilidad principal
* Implementar la lógica que decide el diagnóstico.

Programación
* Comparar síntomas del usuario vs reglas.
Calcular:
    - Nivel de coincidencia
    - Enfermedad más probable

Interfaz en Streamlit
* Botón: “Ejecutar diagnóstico”

Mostrar:
    - Enfermedad sugerida
    - Porcentaje o nivel de coincidencia

Entregables
    - inference_engine.py
    - Vista de resultados en Streamlit

👉 Aquí está la IA basada en reglas.



Parte 4: Casos simulados y pruebas

Integrante 4 (Tania)

Responsabilidad principal
* Crear casos clínicos simulados.
* Validar si el motor infiere correctamente.

Programación
* Dataset simulado (lista o CSV).
* Funciones de prueba automática.


Interfaz en Streamlit
* Selector de caso simulado.
* Comparar:
    - Diagnóstico esperado
    - Diagnóstico obtenido

Entregables
* cases.py o data.csv
* Vista de pruebas en Streamlit

👉 Sirve para demostrar que el sistema funciona.



Parte 5: Flujo completo y experiencia de usuario

Integrante 5 (Favian)

Responsabilidad principal
* Integrar todos los módulos.
* Mejorar experiencia del usuario.

Programación
* Orquestar el flujo:
    1. Selección de síntomas
    2. Inferencia
    3. Resultado

* Manejo de estados (st.session_state).

Interfaz en Streamlit
* Flujo limpio y ordenado.
* Mensajes claros:
    - Advertencia: “No reemplaza diagnóstico médico”

Entregables
* app.py (versión integrada)
* Navegación final de la app


👉 Convierte todo en una aplicación usable.

