"""
Módulo: Aplicación Integrada
Responsable: Favian (Integrante 5)

Descripción:
    - Integra todos los módulos del sistema experto
    - Orquesta el flujo completo de la aplicación
    - Gestiona estados y transiciones
    - Proporciona una experiencia de usuario coherente

Flujo:
    1. Bienvenida y advertencias
    2. Selección de síntomas (Luis)
    3. Ejecución del motor de inferencia (Harry)
    4. Presentación de resultados
    5. Opciones adicionales (ver base de conocimiento, casos de prueba)
"""

import streamlit as st

# TODO (Favian): Descomentar cuando los módulos estén implementados
# from symptoms import render_symptom_selector, validate_symptoms, get_all_symptoms
# from knowledge_base import get_knowledge_base, get_disease_info
# from inference_engine import infer_diagnosis, display_diagnosis_results
# from cases import get_test_cases


# ====================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ====================================

def setup_page():
    """
    Configura la página de Streamlit.
    
    TODO (Favian):
        - Configurar título, icono, layout
        - Configurar tema si es necesario
        - Inicializar session_state
    """
    st.set_page_config(
        page_title="Sistema Experto - Diagnóstico",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def initialize_session_state():
    """
    Inicializa las variables de estado de la sesión.
    
    TODO (Favian):
        - Definir todas las variables de estado necesarias
        - Inicializar valores por defecto
        - Gestionar el flujo entre pasos
    
    Variables sugeridas:
        - current_step: paso actual del flujo
        - selected_symptoms: síntomas seleccionados
        - diagnosis_results: resultados del diagnóstico
        - show_details: mostrar detalles adicionales
    """
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'welcome'
    
    if 'selected_symptoms' not in st.session_state:
        st.session_state.selected_symptoms = []
    
    if 'diagnosis_results' not in st.session_state:
        st.session_state.diagnosis_results = None
    
    # TODO: Agregar más variables según sea necesario


# ====================================
# COMPONENTES DE LA INTERFAZ
# ====================================

def render_header():
    """
    Renderiza el encabezado de la aplicación.
    
    TODO (Favian):
        - Crear encabezado atractivo
        - Incluir logo o imagen si hay
        - Agregar descripción breve
    """
    st.title("🩺 Sistema Experto para Diagnóstico Inicial")
    st.markdown("### Sistema basado en reglas para enfermedades comunes")
    st.markdown("---")


def render_sidebar():
    """
    Renderiza la barra lateral con información y navegación.
    
    TODO (Favian):
        - Agregar información del sistema
        - Opciones de navegación
        - Información de ayuda
        - Créditos del equipo
    """
    with st.sidebar:
        st.header("ℹ️ Información")
        
        st.markdown("""
        **Sistema Experto** desarrollado para el curso de Sistemas Inteligentes.
        
        Este sistema utiliza razonamiento basado en reglas (IF-THEN) para
        sugerir posibles diagnósticos a partir de síntomas.
        """)
        
        st.warning("""
        ⚠️ **IMPORTANTE**
        
        Este sistema es solo con fines educativos.
        NO reemplaza el diagnóstico médico profesional.
        Ante cualquier síntoma, consulte a un médico.
        """)
        
        st.markdown("---")
        st.markdown("**Equipo de Desarrollo:**")
        st.markdown("""
        - Luis - Gestión de síntomas
        - Germain - Base de conocimiento
        - Harry - Motor de inferencia
        - Tania - Casos de prueba
        - Favian - Integración
        """)


def render_welcome():
    """
    Renderiza la pantalla de bienvenida.
    
    TODO (Favian):
        - Crear bienvenida atractiva
        - Explicar cómo funciona el sistema
        - Botón para comenzar
    """
    st.header("👋 Bienvenido al Sistema de Diagnóstico")
    
    st.markdown("""
    Este sistema le ayudará a identificar posibles enfermedades comunes
    basándose en los síntomas que usted presente.
    
    ### ¿Cómo funciona?
    
    1. **Seleccione sus síntomas**: Marque todos los síntomas que está experimentando
    2. **Análisis**: El sistema comparará sus síntomas con nuestra base de conocimiento
    3. **Resultados**: Recibirá un diagnóstico preliminar con recomendaciones
    
    ### Enfermedades consideradas
    
    El sistema puede identificar enfermedades comunes como:
    - Gripe
    - Gastritis
    - Infección respiratoria
    - Y más...
    """)
    
    st.warning("⚠️ **Recuerde**: Este diagnóstico es preliminar y no reemplaza la consulta médica.")
    
    if st.button("🚀 Comenzar diagnóstico", type="primary"):
        st.session_state.current_step = 'symptoms'
        st.rerun()


def render_symptom_selection():
    """
    Renderiza la fase de selección de síntomas.
    
    TODO (Favian):
        - Integrar el módulo de symptoms.py (Luis)
        - Validar la selección
        - Botón para continuar al diagnóstico
    """
    st.header("📝 Paso 1: Seleccione sus síntomas")
    
    # TODO: Integrar módulo de síntomas
    # selected = render_symptom_selector()
    
    # Versión temporal para desarrollo
    st.info("🔧 Módulo de síntomas en desarrollo (Luis)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Volver al inicio"):
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    with col2:
        if st.button("Continuar al diagnóstico ➡️", type="primary"):
            # TODO: Validar síntomas antes de continuar
            st.session_state.current_step = 'diagnosis'
            st.rerun()


def render_diagnosis():
    """
    Renderiza la fase de diagnóstico.
    
    TODO (Favian):
        - Integrar motor de inferencia (Harry)
        - Mostrar proceso de análisis
        - Presentar resultados
    """
    st.header("🔬 Paso 2: Análisis y Diagnóstico")
    
    # TODO: Integrar motor de inferencia
    # knowledge_base = get_knowledge_base()
    # results = infer_diagnosis(st.session_state.selected_symptoms, knowledge_base)
    # st.session_state.diagnosis_results = results
    
    # Versión temporal
    st.info("🔧 Motor de inferencia en desarrollo (Harry)")
    
    with st.spinner("Analizando síntomas..."):
        # Simulación
        import time
        time.sleep(1)
    
    st.success("✅ Análisis completado")
    
    # TODO: Mostrar resultados
    # display_diagnosis_results(results)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Volver a síntomas"):
            st.session_state.current_step = 'symptoms'
            st.rerun()
    
    with col2:
        if st.button("🔄 Nuevo diagnóstico"):
            # Limpiar estado
            st.session_state.selected_symptoms = []
            st.session_state.diagnosis_results = None
            st.session_state.current_step = 'welcome'
            st.rerun()


# ====================================
# FLUJO PRINCIPAL
# ====================================

def main():
    """
    Función principal que orquesta toda la aplicación.
    
    TODO (Favian):
        - Implementar navegación completa entre pasos
        - Gestionar estados correctamente
        - Asegurar experiencia fluida
        - Agregar funcionalidades extras (exportar, historial, etc.)
    """
    setup_page()
    initialize_session_state()
    
    render_header()
    render_sidebar()
    
    # Navegación según el paso actual
    current_step = st.session_state.current_step
    
    if current_step == 'welcome':
        render_welcome()
    
    elif current_step == 'symptoms':
        render_symptom_selection()
    
    elif current_step == 'diagnosis':
        render_diagnosis()
    
    else:
        st.error(f"Paso desconocido: {current_step}")
        if st.button("Volver al inicio"):
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Sistema Experto - Sistemas Inteligentes VI Ciclo | Enero 2026"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
