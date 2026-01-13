"""
Módulo: Motor de Inferencia
Responsable: Harry (Integrante 3)

Descripción:
    - Implementa la lógica de razonamiento basado en reglas
    - Compara síntomas del usuario con la base de conocimiento
    - Calcula coincidencias y determina el diagnóstico más probable

Funcionalidades:
    - Algoritmo de matching de síntomas
    - Cálculo de porcentaje de coincidencia
    - Ranking de enfermedades probables
    - Interfaz de ejecución y resultados en Streamlit
"""

import streamlit as st


# ====================================
# MOTOR DE INFERENCIA
# ====================================

def calculate_match(user_symptoms, disease_symptoms):
    """
    Calcula el porcentaje de coincidencia entre síntomas del usuario
    y síntomas de una enfermedad.
    
    Args:
        user_symptoms (list): Síntomas seleccionados por el usuario
        disease_symptoms (list): Síntomas asociados a la enfermedad
    
    Returns:
        float: Porcentaje de coincidencia (0.0 - 1.0)
    
    TODO (Harry):
        - Implementar algoritmo de matching
        - Considerar diferentes estrategias:
            * Intersección simple
            * Coeficiente de Jaccard
            * Ponderación de síntomas críticos
    
    Ejemplo:
        user: ["fiebre", "tos", "dolor de cabeza"]
        disease: ["fiebre", "tos", "dolor de cabeza", "congestión"]
        match: 3/4 = 0.75 (75%)
    """
    match_percentage = 0.0
    
    # TODO: Implementar cálculo de coincidencia
    
    return match_percentage


def infer_diagnosis(user_symptoms, knowledge_base):
    """
    Realiza la inferencia completa: evalúa todas las enfermedades
    y retorna las más probables.
    
    Args:
        user_symptoms (list): Síntomas del usuario
        knowledge_base (dict): Base de conocimiento completa
    
    Returns:
        list: Lista de tuplas (enfermedad, porcentaje) ordenadas por probabilidad
    
    TODO (Harry):
        - Implementar lógica de inferencia
        - Iterar sobre todas las enfermedades
        - Calcular match para cada una
        - Ordenar por porcentaje descendente
        - Filtrar resultados con match muy bajo (threshold)
    """
    results = []
    
    # TODO: Implementar motor de inferencia
    # Pseudocódigo:
    # for disease_name, disease_info in knowledge_base.items():
    #     disease_symptoms = disease_info['symptoms']
    #     match = calculate_match(user_symptoms, disease_symptoms)
    #     results.append((disease_name, match))
    # 
    # results.sort(key=lambda x: x[1], reverse=True)
    # return results
    
    return results


def apply_rules(user_symptoms, rules):
    """
    Aplica reglas IF-THEN definidas en la base de conocimiento.
    
    Args:
        user_symptoms (list): Síntomas del usuario
        rules (dict): Reglas definidas
    
    Returns:
        list: Conclusiones derivadas de las reglas aplicadas
    
    TODO (Harry):
        - Implementar evaluación de reglas
        - Verificar condiciones (IF)
        - Aplicar conclusiones (THEN)
        - Considerar confianza/certeza de reglas
    """
    conclusions = []
    
    # TODO: Implementar aplicación de reglas
    
    return conclusions


def get_top_diagnosis(diagnosis_results, top_n=3):
    """
    Obtiene las N enfermedades más probables.
    
    Args:
        diagnosis_results (list): Resultados completos de inferencia
        top_n (int): Número de resultados a retornar
    
    Returns:
        list: Top N diagnósticos más probables
    """
    return diagnosis_results[:top_n]


# ====================================
# INTERPRETACIÓN DE RESULTADOS
# ====================================

def interpret_confidence(match_percentage):
    """
    Interpreta el porcentaje de coincidencia en categorías legibles.
    
    Args:
        match_percentage (float): Porcentaje de coincidencia (0.0-1.0)
    
    Returns:
        str: Interpretación ("Muy probable", "Probable", "Poco probable", etc.)
    
    TODO (Harry):
        - Definir rangos de confianza
        - Retornar interpretación apropiada
    """
    # TODO: Implementar interpretación
    # Ejemplo:
    # if match_percentage >= 0.8: return "Muy probable"
    # elif match_percentage >= 0.6: return "Probable"
    # elif match_percentage >= 0.4: return "Posible"
    # else: return "Poco probable"
    
    return "Sin determinar"


# ====================================
# INTERFAZ DE RESULTADOS
# ====================================

def display_diagnosis_results(results):
    """
    Muestra los resultados del diagnóstico de forma visual.
    
    Args:
        results (list): Lista de tuplas (enfermedad, porcentaje)
    
    TODO (Harry):
        - Crear visualización clara de resultados
        - Usar progress bars, métricas, o gráficos
        - Mostrar interpretación de confianza
        - Agregar recomendaciones
    """
    st.header("🔬 Resultados del Diagnóstico")
    
    if not results:
        st.warning("No se pudo determinar un diagnóstico con los síntomas proporcionados")
        return
    
    # TODO: Implementar visualización
    # Ideas:
    # 1. st.metric() para el diagnóstico principal
    # 2. st.progress() para mostrar porcentajes
    # 3. st.expander() para detalles de cada enfermedad
    # 4. Gráfico de barras con top diagnósticos
    
    st.success(f"✅ Se encontraron {len(results)} posibles diagnóstico(s)")


def display_recommendations(disease_name, disease_info):
    """
    Muestra recomendaciones basadas en el diagnóstico.
    
    Args:
        disease_name (str): Nombre de la enfermedad diagnosticada
        disease_info (dict): Información de la enfermedad
    
    TODO (Harry):
        - Mostrar recomendaciones de la base de conocimiento
        - Agregar advertencias médicas apropiadas
    """
    st.subheader("💡 Recomendaciones")
    
    # TODO: Implementar visualización de recomendaciones


# ====================================
# INTERFAZ PRINCIPAL (MODO DESARROLLO)
# ====================================

def main():
    """
    Función principal para ejecutar este módulo de forma independiente.
    Útil para desarrollo y pruebas del motor de inferencia.
    """
    st.title("🔬 Sistema Experto - Motor de Inferencia")
    st.markdown("**Módulo de desarrollo - Parte 3 (Harry)**")
    
    st.warning("⚠️ Este módulo está en desarrollo. Una vez completado, será integrado a la aplicación principal.")
    
    # Simulación de entrada (para pruebas)
    st.subheader("Datos de Prueba")
    
    # TODO: Importar desde otros módulos cuando estén listos
    # from symptoms import get_all_symptoms
    # from knowledge_base import get_knowledge_base
    
    test_symptoms = st.multiselect(
        "Síntomas de prueba (simular entrada del usuario):",
        ["fiebre", "tos", "dolor de cabeza", "náuseas"],
        default=["fiebre", "tos"]
    )
    
    if st.button("🚀 Ejecutar Diagnóstico"):
        if test_symptoms:
            with st.spinner("Analizando síntomas..."):
                # TODO: Llamar al motor de inferencia real
                st.info("Motor de inferencia en desarrollo...")
                
                # Simulación de resultados
                # results = infer_diagnosis(test_symptoms, knowledge_base)
                # display_diagnosis_results(results)
        else:
            st.error("Seleccione al menos un síntoma")
    
    # Información de debug
    with st.expander("🔍 Debug - Información"):
        st.write("Síntomas seleccionados:", test_symptoms)


if __name__ == "__main__":
    main()
