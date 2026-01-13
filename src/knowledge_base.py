"""
Módulo: Base de Conocimiento
Responsable: Germain (Integrante 2)

Descripción:
    - Define las enfermedades comunes del sistema
    - Establece la relación entre enfermedades y síntomas
    - Implementa reglas básicas de asociación

Funcionalidades:
    - Estructura de datos de enfermedades
    - Mapeo enfermedad → síntomas
    - Interfaz de visualización en Streamlit
"""

import streamlit as st


# ====================================
# DEFINICIÓN DE ENFERMEDADES
# ====================================

def get_knowledge_base():
    """
    Retorna la base de conocimiento completa del sistema.
    
    Returns:
        dict: Diccionario con estructura {enfermedad: {síntomas, descripción, ...}}
    
    TODO (Germain):
        - Definir todas las enfermedades del sistema
        - Asociar síntomas a cada enfermedad
        - Agregar información adicional (descripción, severidad, etc.)
    
    Estructura sugerida:
        {
            "Gripe": {
                "symptoms": ["fiebre", "dolor de cabeza", "tos", ...],
                "description": "Infección viral respiratoria",
                "severity": "leve-moderada",
                "recommendations": ["Reposo", "Hidratación", ...]
            },
            ...
        }
    """
    knowledge_base = {}
    
    # TODO: Implementar base de conocimiento
    # Ejemplo:
    # knowledge_base = {
    #     "Gripe": {
    #         "symptoms": ["fiebre", "dolor de cabeza", "tos"],
    #         "description": "Infección viral del sistema respiratorio",
    #         "severity": "leve-moderada",
    #         "recommendations": ["Reposo", "Hidratación", "Analgésicos"]
    #     },
    #     "Gastritis": {
    #         "symptoms": ["dolor abdominal", "náuseas", "acidez"],
    #         ...
    #     },
    #     ...
    # }
    
    return knowledge_base


def get_disease_names():
    """
    Retorna la lista de nombres de enfermedades.
    
    Returns:
        list: Lista de nombres de enfermedades
    """
    return list(get_knowledge_base().keys())


def get_disease_info(disease_name):
    """
    Obtiene información completa de una enfermedad específica.
    
    Args:
        disease_name (str): Nombre de la enfermedad
    
    Returns:
        dict: Información de la enfermedad o None si no existe
    
    TODO (Germain):
        - Implementar búsqueda en la base de conocimiento
        - Manejar casos donde la enfermedad no existe
    """
    kb = get_knowledge_base()
    return kb.get(disease_name, None)


def get_symptoms_for_disease(disease_name):
    """
    Obtiene la lista de síntomas asociados a una enfermedad.
    
    Args:
        disease_name (str): Nombre de la enfermedad
    
    Returns:
        list: Lista de síntomas asociados
    """
    disease_info = get_disease_info(disease_name)
    if disease_info:
        return disease_info.get("symptoms", [])
    return []


# ====================================
# REGLAS BÁSICAS
# ====================================

def create_simple_rules():
    """
    Define reglas simples de asociación síntoma → enfermedad.
    
    Returns:
        dict: Diccionario de reglas
    
    TODO (Germain):
        - Implementar reglas básicas IF-THEN
        - Considerar síntomas obligatorios vs opcionales
        - Definir pesos o prioridades si es necesario
    
    Ejemplo de regla:
        IF fiebre AND dolor_de_cabeza AND tos THEN posible_gripe
    """
    rules = {}
    
    # TODO: Implementar reglas
    # Ejemplo:
    # rules = {
    #     "regla_gripe_1": {
    #         "conditions": ["fiebre", "tos", "dolor de cabeza"],
    #         "conclusion": "Gripe",
    #         "confidence": 0.8
    #     },
    #     ...
    # }
    
    return rules


# ====================================
# INTERFAZ DE VISUALIZACIÓN
# ====================================

def display_knowledge_base():
    """
    Muestra la base de conocimiento en formato legible.
    
    TODO (Germain):
        - Crear visualización clara de enfermedades y síntomas
        - Usar tablas, expandibles o cards
        - Agregar búsqueda/filtros si es necesario
    """
    st.header("📚 Base de Conocimiento")
    
    kb = get_knowledge_base()
    
    if not kb:
        st.warning("⚠️ La base de conocimiento aún no está implementada")
        return
    
    # TODO: Implementar visualización
    # Opciones:
    # 1. st.expander() para cada enfermedad
    # 2. st.dataframe() para vista tabular
    # 3. Cards personalizadas
    
    st.info("Total de enfermedades: " + str(len(kb)))


def display_disease_details(disease_name):
    """
    Muestra detalles de una enfermedad específica.
    
    Args:
        disease_name (str): Nombre de la enfermedad
    
    TODO (Germain):
        - Implementar vista detallada de enfermedad
        - Mostrar síntomas, descripción, recomendaciones
    """
    disease_info = get_disease_info(disease_name)
    
    if disease_info:
        st.subheader(f"🔍 {disease_name}")
        # TODO: Mostrar información detallada
        pass
    else:
        st.error(f"Enfermedad '{disease_name}' no encontrada")


# ====================================
# INTERFAZ PRINCIPAL (MODO DESARROLLO)
# ====================================

def main():
    """
    Función principal para ejecutar este módulo de forma independiente.
    Útil para desarrollo y pruebas de la base de conocimiento.
    """
    st.title("📚 Sistema Experto - Base de Conocimiento")
    st.markdown("**Módulo de desarrollo - Parte 2 (Germain)**")
    
    st.warning("⚠️ Este módulo está en desarrollo. Una vez completado, será integrado a la aplicación principal.")
    
    # Tabs para diferentes vistas
    tab1, tab2 = st.tabs(["Vista General", "Detalles por Enfermedad"])
    
    with tab1:
        display_knowledge_base()
    
    with tab2:
        diseases = get_disease_names()
        if diseases:
            selected_disease = st.selectbox(
                "Seleccione una enfermedad:",
                diseases
            )
            if selected_disease:
                display_disease_details(selected_disease)
        else:
            st.info("No hay enfermedades definidas aún")
    
    # Información de debug
    with st.expander("🔍 Debug - Estructura de Datos"):
        st.json(get_knowledge_base())


if __name__ == "__main__":
    main()
