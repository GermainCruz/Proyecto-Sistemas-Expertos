# -*- coding: utf-8 -*-
"""
cases.py
Módulo de Gestión de Casos Simulados y Pruebas
Permite cargar, visualizar y ejecutar casos de prueba
"""

import streamlit as st
import pandas as pd
import os
from inference_engine import diagnose, InferenceEngine
from symptoms import display_selected_symptoms


def load_test_cases():
    """Carga casos de prueba desde CSV"""
    cases_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_cases.csv")
    
    try:
        df = pd.read_csv(cases_path)
        cases = []
        
        for _, row in df.iterrows():
            symptoms = [s.strip() for s in str(row['sintomas']).split('|') if s.strip()]
            
            case = {
                'id': str(row['caso_id']).strip(),
                'nombre': str(row['nombre_caso']).strip(),
                'symptoms': symptoms,
                'expected_diagnosis': str(row['diagnostico_esperado']).strip(),
                'severity': str(row['severidad']).strip(),
                'edad': int(row['edad']),
                'sexo': str(row['sexo']).strip(),
                'descripcion': str(row['descripcion_caso']).strip()
            }
            cases.append(case)
        
        return cases
        
    except FileNotFoundError:
        st.warning("⚠️ Archivo test_cases.csv no encontrado. Usando casos predeterminados.")
        return get_default_test_cases()
    except Exception as e:
        st.error(f"Error al cargar casos: {str(e)}")
        return get_default_test_cases()


def get_default_test_cases():
    """Casos de prueba predeterminados"""
    return [
        {
            'id': 'caso_001',
            'nombre': 'Gripe Estacional Clásica',
            'symptoms': [
                'Fiebre alta (más de 38.5°C)',
                'Tos seca',
                'Dolores musculares (mialgia)',
                'Fatiga extrema',
                'Dolor de cabeza (cefalea)',
                'Escalofríos'
            ],
            'expected_diagnosis': 'Gripe (Influenza)',
            'severity': 'moderada',
            'edad': 35,
            'sexo': 'F',
            'descripcion': 'Paciente con síntomas gripales típicos de inicio súbito'
        },
        {
            'id': 'caso_002',
            'nombre': 'Resfriado Común',
            'symptoms': [
                'Congestión nasal',
                'Secreción nasal (rinorrea)',
                'Estornudos frecuentes',
                'Dolor de garganta',
                'Tos leve'
            ],
            'expected_diagnosis': 'Resfriado Común',
            'severity': 'leve',
            'edad': 28,
            'sexo': 'M',
            'descripcion': 'Síntomas leves de vías respiratorias superiores'
        },
        {
            'id': 'caso_003',
            'nombre': 'Gastroenteritis Aguda',
            'symptoms': [
                'Diarrea acuosa',
                'Náuseas',
                'Vómitos',
                'Dolor abdominal',
                'Fiebre baja (37.5°C - 38.5°C)',
                'Debilidad general'
            ],
            'expected_diagnosis': 'Gastroenteritis',
            'severity': 'moderada',
            'edad': 42,
            'sexo': 'F',
            'descripcion': 'Cuadro gastrointestinal agudo con deshidratación leve'
        },
        {
            'id': 'caso_004',
            'nombre': 'Migraña Severa',
            'symptoms': [
                'Dolor de cabeza (cefalea)',
                'Náuseas',
                'Vómitos',
                'Visión borrosa',
                'Mareos'
            ],
            'expected_diagnosis': 'Migraña',
            'severity': 'moderada-grave',
            'edad': 31,
            'sexo': 'F',
            'descripcion': 'Cefalea pulsátil intensa con síntomas neurológicos'
        },
        {
            'id': 'caso_005',
            'nombre': 'Neumonía Bacteriana',
            'symptoms': [
                'Tos con flema (productiva)',
                'Fiebre alta (más de 38.5°C)',
                'Dificultad para respirar (disnea)',
                'Dolor en el pecho al respirar',
                'Escalofríos',
                'Fatiga extrema'
            ],
            'expected_diagnosis': 'Neumonía',
            'severity': 'grave',
            'edad': 68,
            'sexo': 'M',
            'descripcion': 'Infección respiratoria baja con compromiso pulmonar'
        },
        {
            'id': 'caso_006',
            'nombre': 'Crisis Asmática',
            'symptoms': [
                'Dificultad para respirar (disnea)',
                'Silbidos al respirar',
                'Opresión en el pecho',
                'Tos persistente',
                'Falta de aliento'
            ],
            'expected_diagnosis': 'Asma (Crisis)',
            'severity': 'moderada-grave',
            'edad': 25,
            'sexo': 'M',
            'descripcion': 'Exacerbación de asma bronquial con broncoespasmo'
        },
        {
            'id': 'caso_007',
            'nombre': 'Diabetes Tipo 2 Descompensada',
            'symptoms': [
                'Sed intensa',
                'Fatiga extrema',
                'Visión borrosa',
                'Pérdida de peso inexplicable',
                'Mareos'
            ],
            'expected_diagnosis': 'Diabetes Tipo 2 (síntomas iniciales)',
            'severity': 'moderada-grave',
            'edad': 55,
            'sexo': 'M',
            'descripcion': 'Hiperglucemia con síntomas metabólicos'
        },
        {
            'id': 'caso_008',
            'nombre': 'Infarto Agudo de Miocardio',
            'symptoms': [
                'Dolor en el pecho',
                'Dolor que irradia al brazo izquierdo',
                'Sudoración fría',
                'Náuseas',
                'Dificultad para respirar (disnea)',
                'Palpitaciones'
            ],
            'expected_diagnosis': 'Infarto Agudo de Miocardio (sospecha)',
            'severity': 'grave',
            'edad': 62,
            'sexo': 'M',
            'descripcion': 'EMERGENCIA - Dolor torácico con signos de isquemia cardíaca'
        },
        {
            'id': 'caso_009',
            'nombre': 'Apendicitis Aguda',
            'symptoms': [
                'Dolor periumbilical que migra a cuadrante inferior derecho',
                'Náuseas',
                'Vómitos',
                'Fiebre',
                'Pérdida de apetito'
            ],
            'expected_diagnosis': 'Apendicitis Aguda',
            'severity': 'moderada-grave',
            'edad': 22,
            'sexo': 'F',
            'descripcion': 'Abdomen agudo quirúrgico'
        },
        {
            'id': 'caso_010',
            'nombre': 'Meningitis Bacteriana',
            'symptoms': [
                'Fiebre alta (más de 38.5°C)',
                'Dolor de cabeza (cefalea)',
                'Rigidez de nuca',
                'Fotofobia',
                'Náuseas',
                'Vómitos'
            ],
            'expected_diagnosis': 'Meningitis (sospecha)',
            'severity': 'grave',
            'edad': 19,
            'sexo': 'M',
            'descripcion': 'EMERGENCIA - Síndrome meníngeo completo'
        }
    ]


def run_test_case(case, method='hybrid'):
    """Ejecuta un caso de prueba y retorna resultados"""
    results = diagnose(case['symptoms'], method)
    
    # Verificar si el diagnóstico esperado está en los resultados
    expected = case['expected_diagnosis']
    found = False
    position = None
    confidence = 0
    
    for i, result in enumerate(results, 1):
        if result['disease'] == expected:
            found = True
            position = i
            confidence = result.get('final_confidence', result.get('confidence', 0))
            break
    
    return {
        'case': case,
        'results': results,
        'expected_found': found,
        'expected_position': position,
        'expected_confidence': confidence,
        'total_diagnoses': len(results)
    }


def evaluate_test_cases(cases, method='hybrid'):
    """Evalúa múltiples casos de prueba"""
    total_cases = len(cases)
    successful = 0
    top3_hits = 0
    
    detailed_results = []
    
    for case in cases:
        result = run_test_case(case, method)
        detailed_results.append(result)
        
        if result['expected_found']:
            successful += 1
            if result['expected_position'] <= 3:
                top3_hits += 1
    
    accuracy = (successful / total_cases * 100) if total_cases > 0 else 0
    top3_accuracy = (top3_hits / total_cases * 100) if total_cases > 0 else 0
    
    return {
        'total_cases': total_cases,
        'successful': successful,
        'top3_hits': top3_hits,
        'accuracy': accuracy,
        'top3_accuracy': top3_accuracy,
        'detailed_results': detailed_results
    }


def display_case_card(case):
    """Muestra información de un caso"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    ">
        <h3>📋 {case['nombre']}</h3>
        <p><strong>ID:</strong> {case['id']}</p>
        <p><strong>Paciente:</strong> {case['sexo']}, {case['edad']} años</p>
        <p><strong>Severidad:</strong> {case['severity']}</p>
        <p><strong>Diagnóstico Esperado:</strong> {case['expected_diagnosis']}</p>
        <p><em>{case['descripcion']}</em></p>
    </div>
    """, unsafe_allow_html=True)


def display_test_result(test_result):
    """Muestra resultado de un test"""
    case = test_result['case']
    found = test_result['expected_found']
    position = test_result['expected_position']
    confidence = test_result['expected_confidence']
    
    if found:
        if position == 1:
            st.success(f"✅ CORRECTO - Diagnóstico en posición #{position} con {confidence*100:.1f}% confianza")
        elif position <= 3:
            st.warning(f"⚠️ PARCIAL - Diagnóstico en posición #{position} con {confidence*100:.1f}% confianza")
        else:
            st.info(f"ℹ️ ENCONTRADO - Diagnóstico en posición #{position} con {confidence*100:.1f}% confianza")
    else:
        st.error(f"❌ NO ENCONTRADO - El diagnóstico esperado no está en los resultados")
    
    # Mostrar top 3 resultados
    st.markdown("**Top 3 Diagnósticos:**")
    for i, result in enumerate(test_result['results'][:3], 1):
        conf = result.get('final_confidence', result.get('confidence', 0))
        disease = result['disease']
        
        # Marcar si es el esperado
        marker = "🎯 " if disease == case['expected_diagnosis'] else ""
        
        st.markdown(f"{i}. {marker}**{disease}** - {conf*100:.1f}% confianza")


def main():
    """Interfaz principal del módulo de casos"""
    st.set_page_config(page_title="Casos de Prueba", layout="wide")
    st.title("🧪 Casos de Prueba - Sistema Experto Médico")
    
    # Cargar casos
    cases = load_test_cases()
    
    if not cases:
        st.error("No se pudieron cargar los casos de prueba")
        return
    
    st.success(f"✅ Cargados {len(cases)} casos de prueba")
    
    tab1, tab2, tab3 = st.tabs(["📋 Ver Casos", "🧪 Prueba Individual", "📊 Evaluación Completa"])
    
    with tab1:
        st.markdown("### 📚 Biblioteca de Casos de Prueba")
        for case in cases:
            with st.expander(f"{case['id']} - {case['nombre']}", expanded=False):
                display_case_card(case)
                
                st.markdown("**Síntomas:**")
                for symptom in case['symptoms']:
                    st.markdown(f"- {symptom}")
    
    with tab2:
        st.markdown("### 🔬 Prueba Individual de Caso")
        
        case_options = [f"{c['id']} - {c['nombre']}" for c in cases]
        selected_case_str = st.selectbox("Seleccione un caso:", case_options)
        
        if selected_case_str:
            case_id = selected_case_str.split(' - ')[0]
            selected_case = next(c for c in cases if c['id'] == case_id)
            
            display_case_card(selected_case)
            
            method = st.radio(
                "Método de inferencia:",
                ['hybrid', 'forward', 'rules'],
                format_func=lambda x: {
                    'hybrid': 'Híbrido',
                    'forward': 'Encadenamiento Adelante',
                    'rules': 'Basado en Reglas'
                }[x]
            )
            
            if st.button("🔍 Ejecutar Diagnóstico"):
                with st.spinner("Procesando..."):
                    test_result = run_test_case(selected_case, method)
                    
                    st.markdown("---")
                    display_test_result(test_result)
                    
                    st.markdown("---")
                    st.markdown("### 📊 Todos los Resultados")
                    
                    for i, result in enumerate(test_result['results'][:10], 1):
                        conf = result.get('final_confidence', result.get('confidence', 0))
                        with st.expander(f"#{i} - {result['disease']} ({conf*100:.1f}%)", expanded=(i<=3)):
                            st.markdown(f"**Descripción:** {result['description']}")
                            st.markdown(f"**Categoría:** {result['category']}")
                            st.markdown(f"**Severidad:** {result['severity']}")
                            
                            st.markdown("**Síntomas Coincidentes:**")
                            for symptom in result['matched_symptoms']:
                                st.markdown(f"- ✓ {symptom}")
    
    with tab3:
        st.markdown("### 📊 Evaluación Completa del Sistema")
        
        method = st.radio(
            "Método para evaluación:",
            ['hybrid', 'forward', 'rules'],
            key='eval_method',
            format_func=lambda x: {
                'hybrid': 'Híbrido',
                'forward': 'Encadenamiento Adelante',
                'rules': 'Basado en Reglas'
            }[x]
        )
        
        if st.button("🚀 Ejecutar Evaluación Completa"):
            with st.spinner(f"Evaluando {len(cases)} casos..."):
                evaluation = evaluate_test_cases(cases, method)
                
                # Métricas principales
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total de Casos", evaluation['total_cases'])
                with col2:
                    st.metric("Casos Exitosos", evaluation['successful'])
                with col3:
                    st.metric("Precisión", f"{evaluation['accuracy']:.1f}%")
                with col4:
                    st.metric("Top-3 Precisión", f"{evaluation['top3_accuracy']:.1f}%")
                
                st.markdown("---")
                
                # Resultados detallados
                st.markdown("### 📋 Resultados Detallados")
                
                for test_result in evaluation['detailed_results']:
                    case = test_result['case']
                    
                    with st.expander(f"{case['id']} - {case['nombre']}", expanded=False):
                        display_test_result(test_result)
                
                # Gráfico de rendimiento
                st.markdown("---")
                st.markdown("### 📈 Análisis de Rendimiento")
                
                positions = []
                confidences = []
                case_names = []
                
                for result in evaluation['detailed_results']:
                    case_names.append(result['case']['id'])
                    positions.append(result['expected_position'] if result['expected_found'] else None)
                    confidences.append(result['expected_confidence'] if result['expected_found'] else 0)
                
                # Crear DataFrame para visualización
                df_results = pd.DataFrame({
                    'Caso': case_names,
                    'Posición': positions,
                    'Confianza': [c*100 for c in confidences],
                    'Encontrado': ['✅' if p is not None else '❌' for p in positions]
                })
                
                st.dataframe(df_results, use_container_width=True)


if __name__ == "__main__":
    main()