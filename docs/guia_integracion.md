# Guía de Integración del Sistema Experto

## 📋 Visión General

Esta guía explica cómo cada módulo se integra con los demás para formar el sistema completo.

## 🔗 Dependencias entre Módulos

```
app.py (Favian)
    ├── symptoms.py (Luis)
    ├── knowledge_base.py (Germain)
    │   └── usado por inference_engine.py
    ├── inference_engine.py (Harry)
    │   └── usa knowledge_base.py
    └── cases.py (Tania)
        └── usa inference_engine.py + knowledge_base.py
```

## 📝 Orden de Desarrollo Recomendado

### Fase 1: Fundamentos (Semana 1)
1. **Germain (Base de conocimiento)**
   - Definir enfermedades y síntomas
   - Crear estructura de datos
   - Implementar reglas básicas

2. **Luis (Gestión de síntomas)**
   - Usar síntomas definidos por Germain
   - Implementar interfaz de selección
   - Validaciones de entrada

### Fase 2: Lógica Central (Semana 2)
3. **Harry (Motor de inferencia)**
   - Implementar algoritmo de matching
   - Integrar con knowledge_base.py
   - Crear interfaz de resultados

### Fase 3: Validación (Semana 2-3)
4. **Tania (Casos de prueba)**
   - Crear casos simulados
   - Integrar con inference_engine.py
   - Implementar métricas

### Fase 4: Integración Final (Semana 3)
5. **Favian (Aplicación completa)**
   - Integrar todos los módulos
   - Implementar flujo completo
   - Pulir UX/UI

## 🔌 Interfaces entre Módulos

### symptoms.py → app.py
```python
# Luis debe exportar:
def get_all_symptoms() -> list
def render_symptom_selector() -> list  # Retorna síntomas seleccionados
def validate_symptoms(symptoms: list) -> bool
```

### knowledge_base.py → inference_engine.py
```python
# Germain debe exportar:
def get_knowledge_base() -> dict
def get_disease_info(disease_name: str) -> dict
def get_symptoms_for_disease(disease_name: str) -> list
```

### inference_engine.py → app.py
```python
# Harry debe exportar:
def infer_diagnosis(user_symptoms: list, knowledge_base: dict) -> list
def calculate_match(user_symptoms: list, disease_symptoms: list) -> float
def display_diagnosis_results(results: list) -> None
```

### cases.py → app.py
```python
# Tania debe exportar:
def get_test_cases() -> list
def run_all_tests(test_cases: list, inference_engine, knowledge_base: dict) -> dict
def display_test_results(results: dict) -> None
```

## 📦 Estructura de Datos Estándar

### Síntoma
```python
symptom: str
# Ejemplo: "fiebre", "dolor de cabeza"
```

### Enfermedad
```python
disease = {
    "symptoms": ["síntoma1", "síntoma2", ...],
    "description": "Descripción de la enfermedad",
    "severity": "leve|moderada|grave",
    "recommendations": ["recomendación1", "recomendación2", ...]
}
```

### Resultado de Diagnóstico
```python
result = (disease_name: str, confidence: float)
# Ejemplo: ("Gripe", 0.85)
```

### Caso de Prueba
```python
test_case = {
    "id": int,
    "name": str,
    "symptoms": list,
    "expected_diagnosis": str,
    "description": str,
    "severity": str
}
```

## 🔄 Flujo de Datos Completo

1. **Usuario selecciona síntomas** (symptoms.py)
   - Input: Interacción del usuario
   - Output: `selected_symptoms: list`

2. **Sistema obtiene base de conocimiento** (knowledge_base.py)
   - Output: `knowledge_base: dict`

3. **Motor de inferencia procesa** (inference_engine.py)
   - Input: `selected_symptoms`, `knowledge_base`
   - Output: `diagnosis_results: list[tuple]`

4. **Sistema muestra resultados** (app.py)
   - Input: `diagnosis_results`
   - Output: Interfaz visual

## 🧪 Testing de Integración

### Checklist antes de integrar
- [ ] Cada módulo funciona de forma independiente
- [ ] Las funciones exportadas tienen los nombres correctos
- [ ] Los tipos de datos coinciden con las interfaces
- [ ] Se probó con datos de ejemplo
- [ ] La documentación está actualizada

### Probar integración módulo por módulo
```python
# En app.py
# 1. Integrar symptoms + knowledge_base
# 2. Integrar inference_engine
# 3. Integrar cases
# 4. Probar flujo completo
```

## 🐛 Debugging

### Usar session_state para debug
```python
with st.expander("🔍 Debug"):
    st.write("Selected symptoms:", st.session_state.selected_symptoms)
    st.write("Diagnosis results:", st.session_state.diagnosis_results)
```

### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Síntomas recibidos: {selected_symptoms}")
```

## 📞 Comunicación entre Integrantes

### Al completar tu módulo:
1. Hacer commit y push a tu rama
2. Notificar en el grupo
3. Actualizar el README con tu progreso
4. Crear pull request con descripción clara

### Al necesitar ayuda:
1. Revisar esta guía
2. Revisar el código de ejemplo en cada módulo
3. Preguntar en el grupo

## ✅ Checklist Final

### Luis (symptoms.py)
- [ ] Lista completa de síntomas definida
- [ ] Interfaz de selección funcional
- [ ] Validación implementada
- [ ] Exporta funciones correctamente

### Germain (knowledge_base.py)
- [ ] Todas las enfermedades definidas
- [ ] Síntomas asociados a cada enfermedad
- [ ] Reglas básicas implementadas
- [ ] Interfaz de visualización funcional

### Harry (inference_engine.py)
- [ ] Algoritmo de matching implementado
- [ ] Cálculo de confianza funcional
- [ ] Ranking de diagnósticos correcto
- [ ] Interfaz de resultados clara

### Tania (cases.py)
- [ ] Casos de prueba definidos
- [ ] Ejecución de pruebas funcional
- [ ] Métricas implementadas
- [ ] CSV de casos creado

### Favian (app.py)
- [ ] Todos los módulos integrados
- [ ] Flujo completo funcional
- [ ] Estados gestionados correctamente
- [ ] UX pulida y clara

## 🚀 Deploy Final

Una vez todo integrado:
```bash
# Probar localmente
streamlit run src/app.py

# Verificar todos los flujos
# Ejecutar casos de prueba
# Revisar que no hay errores
```

## 📚 Recursos Adicionales

- [Documentación Streamlit](https://docs.streamlit.io)
- [Python Style Guide](https://peps.python.org/pep-0008/)
- [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
