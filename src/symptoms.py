"""
Módulo: Gestión de Síntomas
Responsable: Luis (Integrante 1)

Descripción:
    - Define el listado oficial de síntomas del sistema
    - Implementa la interfaz de captura de síntomas del usuario
    - Valida la entrada (mínimo 1 síntoma seleccionado)

Funcionalidades:
    - Estructura de datos para síntomas
    - Interfaz Streamlit con checkboxes/multiselect
    - Visualización de síntomas seleccionados
"""

import streamlit as st


# ====================================
# DEFINICIÓN DE SÍNTOMAS
# ====================================

def get_all_symptoms():
    """
    Retorna el listado completo de síntomas disponibles.
    
    Returns:
        list: Lista de síntomas como strings
    
    TODO (Luis):
        - Definir todos los síntomas considerados en el sistema
        - Organizar por categorías si es necesario
        - Agregar descripciones si se requiere
    """
    symptoms = []
    
    # TODO: Agregar síntomas aquí
    # Ejemplo:
    # symptoms = [
    #     "Fiebre",
    #     "Dolor de cabeza",
    #     "Tos",
    #     "Dolor de garganta",
    #     ...
    # ]
    
    return symptoms


# ====================================
# INTERFAZ DE CAPTURA
# ====================================

def render_symptom_selector():
    """
    Renderiza la interfaz de selección de síntomas en Streamlit.
    
    Returns:
        list: Lista de síntomas seleccionados por el usuario
    
    TODO (Luis):
        - Implementar checkboxes o multiselect
        - Agregar validación (mínimo 1 síntoma)
        - Estilizar la interfaz
    """
    st.header("Seleccione sus síntomas")
    
    symptoms = get_all_symptoms()
    selected_symptoms = []
    
    # TODO: Implementar la interfaz de selección
    # Opciones:
    # 1. st.multiselect()
    # 2. st.checkbox() para cada síntoma
    # 3. Organizar en columnas para mejor visualización
    
    return selected_symptoms


def validate_symptoms(selected_symptoms):
    """
    Valida que se haya seleccionado al menos un síntoma.
    
    Args:
        selected_symptoms (list): Lista de síntomas seleccionados
    
    Returns:
        bool: True si la selección es válida, False en caso contrario
    
    TODO (Luis):
        - Implementar validación
        - Mostrar mensajes de error apropiados
    """
    # TODO: Implementar validación
    return True


def display_selected_symptoms(selected_symptoms):
    """
    Muestra los síntomas seleccionados de forma visual.
    
    Args:
        selected_symptoms (list): Lista de síntomas seleccionados
    
    TODO (Luis):
        - Crear visualización clara de síntomas seleccionados
        - Considerar usar st.pills, st.tags o similar
    """
    if selected_symptoms:
        st.subheader("Síntomas seleccionados:")
        # TODO: Implementar visualización
        pass
    else:
        st.info("No hay síntomas seleccionados")


# ====================================
# INTERFAZ PRINCIPAL (MODO DESARROLLO)
# ====================================

def main():
    """
    Función principal para ejecutar este módulo de forma independiente.
    Útil para desarrollo y pruebas del módulo de síntomas.
    """
    st.title("🩺 Sistema Experto - Gestión de Síntomas")
    st.markdown("**Módulo de desarrollo - Parte 1 (Luis)**")
    
    st.warning("⚠️ Este módulo está en desarrollo. Una vez completado, será integrado a la aplicación principal.")
    
    # Renderizar selector de síntomas
    selected = render_symptom_selector()
    
    # Validar y mostrar
    if selected:
        if validate_symptoms(selected):
            display_selected_symptoms(selected)
            
            # Guardar en session_state para uso posterior
            st.session_state['selected_symptoms'] = selected
            st.success(f"✅ {len(selected)} síntoma(s) seleccionado(s)")
        else:
            st.error("❌ Selección de síntomas inválida")
    
    # Información de debug
    with st.expander("🔍 Debug - Session State"):
        st.write(st.session_state)


if __name__ == "__main__":
    main()
