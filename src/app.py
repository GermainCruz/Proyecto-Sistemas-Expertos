# -*- coding: utf-8 -*-
"""
app.py
Aplicación Principal - Sistema Experto de Diagnóstico Médico
Integra todos los módulos del sistema
"""

import streamlit as st
import sys
import os

# Agregar directorio src al path
sys.path.insert(0, os.path.dirname(__file__))

from symptoms import (
    render_symptom_selector, 
    validate_symptoms, 
    display_selected_symptoms,
    get_all_symptoms_flat
)
from knowledge_base import (
    get_knowledge_base, 
    get_disease_names,
    get_all_categories,
    display_disease_card
)
from inference_engine import (
    diagnose, 
    InferenceEngine
)
from cases import (
    load_test_cases,
    run_test_case,
    evaluate_test_cases,
    display_case_card,
    display_test_result
)


# ====================================
# CONFIGURACIÓN DE LA PÁGINA
# ====================================

st.set_page_config(
    page_title="Sistema Experto Médico",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ====================================
# ESTILOS CSS
# ====================================

def load_custom_css():
    """Aplica estilos personalizados"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .diagnosis-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 2px solid #e9ecef;
    }
    
    .diagnosis-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .emergency-alert {
        background: #fee;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-alert {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        border-left: 4px solid #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


# ====================================
# FUNCIONES AUXILIARES
# ====================================

def initialize_session_state():
    """Inicializa variables de sesión"""
    if 'selected_symptoms' not in st.session_state:
        st.session_state.selected_symptoms = []
    if 'diagnosis_results' not in st.session_state:
        st.session_state.diagnosis_results = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'diagnosis_history' not in st.session_state:
        st.session_state.diagnosis_history = []


def display_header():
    """Muestra el encabezado principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Sistema Experto de Diagnóstico Médico</h1>
        <p>Sistema de inferencia basado en conocimiento para apoyo al diagnóstico</p>
    </div>
    """, unsafe_allow_html=True)


def display_severity_alert(severity):
    """Muestra alerta según severidad"""
    severity_lower = severity.lower()
    
    if 'grave' in severity_lower:
        st.markdown("""
        <div class="emergency-alert">
            <h3>🚨 ALERTA DE EMERGENCIA</h3>
            <p><strong>Esta condición requiere atención médica URGENTE</strong></p>
            <p>Por favor, acuda inmediatamente a un servicio de emergencias o llame al 911</p>
        </div>
        """, unsafe_allow_html=True)
    elif 'moderada-grave' in severity_lower:
        st.warning("⚠️ **ATENCIÓN:** Esta condición requiere consulta médica pronta. No demore la atención profesional.")
    elif 'moderada' in severity_lower:
        st.info("ℹ️ **RECOMENDACIÓN:** Consulte con un profesional de la salud si los síntomas persisten o empeoran.")


def display_diagnosis_result(result, rank):
    """Muestra un resultado de diagnóstico de forma atractiva"""
    confidence = result.get('final_confidence', result.get('confidence', 0))
    disease = result['disease']
    
    # Determinar color según confianza
    if confidence >= 0.8:
        color = "#28a745"
        emoji = "🟢"
    elif confidence >= 0.6:
        color = "#ffc107"
        emoji = "🟡"
    elif confidence >= 0.4:
        color = "#fd7e14"
        emoji = "🟠"
    else:
        color = "#dc3545"
        emoji = "🔴"
    
    with st.expander(f"{emoji} #{rank} - {disease} ({confidence*100:.1f}%)", expanded=(rank==1)):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {disease}")
            st.markdown(f"**Categoría:** {result['category']}")
            st.markdown(f"**Descripción:** {result['description']}")
            
            st.markdown("---")
            st.markdown(f"**Síntomas Coincidentes ({len(result['matched_symptoms'])}):**")
            for symptom in result['matched_symptoms']:
                st.markdown(f"✓ {symptom}")
        
        with col2:
            st.metric("Nivel de Confianza", f"{confidence*100:.1f}%")
            st.metric("Severidad", result['severity'])
            
            # Barra de confianza visual
            st.progress(confidence)
        
        st.markdown("---")
        display_severity_alert(result['severity'])
        
        st.markdown("### 📋 Recomendaciones")
        for i, rec in enumerate(result['recommendations'], 1):
            st.markdown(f"{i}. {rec}")
        
        # Botón para agregar al historial
        if st.button(f"📌 Guardar en Historial", key=f"save_{rank}_{disease}"):
            st.session_state.diagnosis_history.append({
                'disease': disease,
                'confidence': confidence,
                'symptoms': result['matched_symptoms'],
                'timestamp': st.session_state.get('diagnosis_timestamp', 'N/A')
            })
            st.success("✅ Agregado al historial")


# ====================================
# PÁGINAS DE LA APLICACIÓN
# ====================================

def page_home():
    """Página principal de diagnóstico"""
    st.markdown("## 🩺 Nueva Consulta de Diagnóstico")
    
    # Instrucciones
    with st.expander("ℹ️ Instrucciones de Uso", expanded=False):
        st.markdown("""
        ### Cómo usar el sistema:
        
        1. **Seleccione los síntomas** que está experimentando de la lista categorizada
        2. Revise el resumen de síntomas seleccionados
        3. Seleccione el **método de inferencia** (se recomienda Híbrido)
        4. Haga clic en **"Realizar Diagnóstico"**
        5. Revise los resultados ordenados por nivel de confianza
        
        ⚠️ **IMPORTANTE:** Este sistema es solo de apoyo educativo. 
        Siempre consulte con un profesional de la salud calificado.
        """)
    
    # Selector de síntomas
    st.markdown("---")
    selected_symptoms = render_symptom_selector()
    
    # Validar y mostrar resumen
    if validate_symptoms(selected_symptoms):
        st.session_state.selected_symptoms = selected_symptoms
        
        st.markdown("---")
        display_selected_symptoms(selected_symptoms)
        
        st.markdown("---")
        st.markdown("### ⚙️ Configuración de Diagnóstico")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            method = st.radio(
                "Método de Inferencia:",
                ['hybrid', 'forward', 'rules'],
                index=0,
                format_func=lambda x: {
                    'hybrid': '🔄 Híbrido (Recomendado) - Combina múltiples métodos',
                    'forward': '➡️ Encadenamiento Hacia Adelante - De síntomas a diagnóstico',
                    'rules': '📋 Basado en Reglas - Utiliza reglas IF-THEN predefinidas'
                }[x],
                help="El método híbrido proporciona los mejores resultados al combinar diferentes estrategias de inferencia"
            )
        
        with col2:
            top_n = st.slider(
                "Número de resultados a mostrar:",
                min_value=3,
                max_value=10,
                value=5,
                help="Cantidad de diagnósticos más probables a mostrar"
            )
        
        # Botón de diagnóstico
        st.markdown("---")
        if st.button("🔍 Realizar Diagnóstico", type="primary", use_container_width=True):
            with st.spinner("🔄 Procesando diagnóstico..."):
                # Realizar diagnóstico
                results = diagnose(selected_symptoms, method)
                st.session_state.diagnosis_results = results
                st.session_state.diagnosis_timestamp = st.session_state.get('diagnosis_timestamp', 'Ahora')
                
                # Mostrar resultados
                if results:
                    st.success(f"✅ Diagnóstico completado. Se encontraron {len(results)} posibles condiciones.")
                    
                    st.markdown("---")
                    st.markdown("## 📊 Resultados del Diagnóstico")
                    
                    # Mostrar top N resultados
                    for i, result in enumerate(results[:top_n], 1):
                        display_diagnosis_result(result, i)
                    
                    # Estadísticas
                    st.markdown("---")
                    st.markdown("### 📈 Estadísticas del Diagnóstico")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Diagnósticos", len(results))
                    with col2:
                        avg_conf = sum(r.get('final_confidence', r.get('confidence', 0)) for r in results[:5]) / min(5, len(results))
                        st.metric("Confianza Promedio (Top 5)", f"{avg_conf*100:.1f}%")
                    with col3:
                        categories = set(r['category'] for r in results[:top_n])
                        st.metric("Categorías Afectadas", len(categories))
                    with col4:
                        severe_count = sum(1 for r in results[:top_n] if 'grave' in r['severity'].lower())
                        st.metric("Condiciones Graves", severe_count)
                    
                    # Botón para descargar reporte
                    if st.button("📄 Generar Reporte PDF"):
                        st.info("🚧 Función de generación de reporte en desarrollo")
                
                else:
                    st.warning("⚠️ No se encontraron diagnósticos que coincidan con los síntomas seleccionados.")
                    st.info("💡 Intente agregar más síntomas o consulte directamente con un profesional de la salud.")
    
    else:
        st.warning("⚠️ Por favor, seleccione al menos un síntoma para continuar.")


def page_knowledge_base():
    """Página de exploración de la base de conocimiento"""
    st.markdown("## 📚 Base de Conocimiento")
    
    kb = get_knowledge_base()
    diseases = get_disease_names()
    categories = get_all_categories()
    
    # Estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Enfermedades", len(diseases))
    with col2:
        st.metric("Categorías", len(categories))
    with col3:
        total_symptoms = sum(len(info['symptoms_all']) for info in kb.values())
        st.metric("Total Síntomas", len(set(get_all_symptoms_flat())))
    
    st.markdown("---")
    
    # Pestañas
    tab1, tab2, tab3 = st.tabs(["🔍 Buscar Enfermedad", "📂 Por Categoría", "📊 Estadísticas"])
    
    with tab1:
        search = st.text_input("🔍 Buscar enfermedad:", placeholder="Ej: Gripe, Neumonía...")
        
        filtered_diseases = [d for d in diseases if search.lower() in d.lower()] if search else diseases
        
        st.markdown(f"**Mostrando {len(filtered_diseases)} enfermedades:**")
        
        for disease in filtered_diseases:
            display_disease_card(disease, kb[disease])
    
    with tab2:
        selected_category = st.selectbox("Seleccione categoría:", ["Todas"] + categories)
        
        if selected_category == "Todas":
            filtered = diseases
        else:
            filtered = [d for d in diseases if kb[d]['category'] == selected_category]
        
        st.markdown(f"**{len(filtered)} enfermedades en esta categoría:**")
        
        for disease in filtered:
            display_disease_card(disease, kb[disease])
    
    with tab3:
        st.markdown("### 📊 Distribución por Categoría")
        
        category_counts = {}
        for disease, info in kb.items():
            cat = info['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        import pandas as pd
        df_cat = pd.DataFrame({
            'Categoría': list(category_counts.keys()),
            'Cantidad': list(category_counts.values())
        }).sort_values('Cantidad', ascending=False)
        
        st.dataframe(df_cat, use_container_width=True)
        
        st.markdown("### 📊 Distribución por Severidad")
        
        severity_counts = {}
        for info in kb.values():
            sev = info['severity']
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        df_sev = pd.DataFrame({
            'Severidad': list(severity_counts.keys()),
            'Cantidad': list(severity_counts.values())
        }).sort_values('Cantidad', ascending=False)
        
        st.dataframe(df_sev, use_container_width=True)


def page_test_cases():
    """Página de casos de prueba"""
    st.markdown("## 🧪 Casos de Prueba")
    
    cases = load_test_cases()
    
    if not cases:
        st.error("❌ No se pudieron cargar los casos de prueba")
        return
    
    st.success(f"✅ {len(cases)} casos de prueba disponibles")
    
    tab1, tab2, tab3 = st.tabs(["📋 Ver Casos", "🔬 Prueba Individual", "📊 Evaluación Completa"])
    
    with tab1:
        st.markdown("### 📚 Biblioteca de Casos")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            severity_filter = st.multiselect(
                "Filtrar por severidad:",
                options=list(set(c['severity'] for c in cases)),
                default=None
            )
        with col2:
            age_range = st.slider("Rango de edad:", 0, 100, (0, 100))
        
        filtered_cases = cases
        if severity_filter:
            filtered_cases = [c for c in filtered_cases if c['severity'] in severity_filter]
        filtered_cases = [c for c in filtered_cases if age_range[0] <= c['edad'] <= age_range[1]]
        
        st.markdown(f"**Mostrando {len(filtered_cases)} casos:**")
        
        for case in filtered_cases:
            with st.expander(f"{case['id']} - {case['nombre']}", expanded=False):
                display_case_card(case)
                st.markdown("**Síntomas:**")
                for symptom in case['symptoms']:
                    st.markdown(f"- {symptom}")
    
    with tab2:
        case_options = [f"{c['id']} - {c['nombre']}" for c in cases]
        selected = st.selectbox("Seleccione un caso:", case_options)
        
        if selected:
            case_id = selected.split(' - ')[0]
            case = next(c for c in cases if c['id'] == case_id)
            
            display_case_card(case)
            
            method = st.radio(
                "Método:",
                ['hybrid', 'forward', 'rules'],
                format_func=lambda x: {'hybrid': 'Híbrido', 'forward': 'Forward', 'rules': 'Reglas'}[x]
            )
            
            if st.button("🔍 Ejecutar Diagnóstico"):
                with st.spinner("Procesando..."):
                    result = run_test_case(case, method)
                    st.markdown("---")
                    display_test_result(result)
    
    with tab3:
        st.markdown("### 📊 Evaluación del Sistema")
        
        method = st.radio(
            "Método para evaluación:",
            ['hybrid', 'forward', 'rules'],
            key='eval_method'
        )
        
        if st.button("🚀 Ejecutar Evaluación Completa"):
            with st.spinner(f"Evaluando {len(cases)} casos..."):
                evaluation = evaluate_test_cases(cases, method)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Casos", evaluation['total_cases'])
                with col2:
                    st.metric("Exitosos", evaluation['successful'])
                with col3:
                    st.metric("Precisión", f"{evaluation['accuracy']:.1f}%")
                with col4:
                    st.metric("Top-3", f"{evaluation['top3_accuracy']:.1f}%")
                
                st.markdown("---")
                for result in evaluation['detailed_results']:
                    with st.expander(f"{result['case']['id']} - {result['case']['nombre']}"):
                        display_test_result(result)


def page_history():
    """Página de historial"""
    st.markdown("## 📜 Historial de Diagnósticos")
    
    if not st.session_state.diagnosis_history:
        st.info("📭 No hay diagnósticos guardados en el historial")
        return
    
    st.success(f"✅ {len(st.session_state.diagnosis_history)} diagnósticos guardados")
    
    for i, item in enumerate(reversed(st.session_state.diagnosis_history), 1):
        with st.expander(f"#{i} - {item['disease']} ({item['confidence']*100:.1f}%)"):
            st.markdown(f"**Confianza:** {item['confidence']*100:.1f}%")
            st.markdown(f"**Timestamp:** {item['timestamp']}")
            st.markdown("**Síntomas:**")
            for symptom in item['symptoms']:
                st.markdown(f"- {symptom}")
    
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.diagnosis_history = []
        st.rerun()


# ====================================
# APLICACIÓN PRINCIPAL
# ====================================

def main():
    """Función principal de la aplicación"""
    load_custom_css()
    initialize_session_state()
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📍 Navegación")
        
        page = st.radio(
            "Ir a:",
            ['🏠 Inicio', '📚 Base de Conocimiento', '🧪 Casos de Prueba', '📜 Historial'],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Información")
        st.info("""
        **Sistema Experto Médico**
        
        Versión: 1.0
        
        Desarrollado con:
        - Python
        - Streamlit
        - Lógica de Inferencia
        
        ⚠️ Solo para fines educativos
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Estadísticas del Sistema")
        kb = get_knowledge_base()
        st.metric("Enfermedades", len(kb))
        st.metric("Síntomas", len(get_all_symptoms_flat()))
        st.metric("Casos de Prueba", len(load_test_cases()))
    
    # Páginas
    if '🏠 Inicio' in page:
        page_home()
    elif '📚 Base de Conocimiento' in page:
        page_knowledge_base()
    elif '🧪 Casos de Prueba' in page:
        page_test_cases()
    elif '📜 Historial' in page:
        page_history()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 20px;">
        <p>Sistema Experto de Diagnóstico Médico | Desarrollado con ❤️ usando Streamlit</p>
        <p><small>⚠️ Este sistema es solo para fines educativos y de investigación. 
        No reemplaza el juicio clínico profesional.</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()