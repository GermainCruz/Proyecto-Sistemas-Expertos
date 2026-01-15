# -*- coding: utf-8 -*-
"""
knowledge_base.py
Modulo desarrollado por Germain - Base de Conocimiento del Sistema Experto
"""

import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_diseases_from_dataset():
    """Carga enfermedades desde CSV"""
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "diseases_knowledge.csv")
    
    try:
        df = pd.read_csv(dataset_path)
        knowledge_base = {}
        
        for _, row in df.iterrows():
            disease_name = str(row['enfermedad']).strip()
            
            main_symptoms = [s.strip() for s in str(row['sintomas_principales']).split('|') if s.strip()]
            secondary_symptoms = [s.strip() for s in str(row['sintomas_secundarios']).split('|') if s.strip()]
            recommendations = [r.strip() for r in str(row['recomendaciones']).split('|') if r.strip()]
            
            knowledge_base[disease_name] = {
                'symptoms_main': main_symptoms,
                'symptoms_secondary': secondary_symptoms,
                'symptoms_all': main_symptoms + secondary_symptoms,
                'description': str(row['descripcion']).strip(),
                'severity': str(row['severidad']).strip(),
                'recommendations': recommendations,
                'category': str(row['categoria']).strip()
            }
        
        return knowledge_base
        
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return {}

def get_knowledge_base():
    """Retorna la base de conocimiento completa"""
    return load_diseases_from_dataset()

def get_disease_names():
    """Lista de nombres de enfermedades"""
    return sorted(list(get_knowledge_base().keys()))

def get_disease_info(disease_name):
    """Informacion de una enfermedad especifica"""
    return get_knowledge_base().get(disease_name, None)

def get_symptoms_for_disease(disease_name, include_secondary=True):
    """Sintomas asociados a una enfermedad"""
    disease_info = get_disease_info(disease_name)
    if not disease_info:
        return []
    return disease_info.get("symptoms_all" if include_secondary else "symptoms_main", [])

def create_simple_rules():
    """Reglas IF-THEN para diagnostico"""
    return [
        {
            'id': 'gripe_clasica',
            'conditions': {
                'required': ['Fiebre alta (más de 38.5°C)', 'Tos seca', 'Dolores musculares (mialgia)'],
                'optional': ['Fatiga extrema', 'Dolor de cabeza (cefalea)']
            },
            'conclusion': 'Gripe (Influenza)',
            'confidence': 0.85
        },
        {
            'id': 'resfriado_tipico',
            'conditions': {
                'required': ['Congestión nasal', 'Estornudos frecuentes'],
                'optional': ['Dolor de garganta']
            },
            'conclusion': 'Resfriado Común',
            'confidence': 0.80
        },
        {
            'id': 'gastritis_caracteristica',
            'conditions': {
                'required': ['Dolor en la parte superior del abdomen', 'Acidez estomacal'],
                'optional': ['Náuseas', 'Ardor estomacal']
            },
            'conclusion': 'Gastritis Aguda',
            'confidence': 0.75
        },
        {
            'id': 'gastroenteritis_tipica',
            'conditions': {
                'required': ['Diarrea acuosa', 'Vómitos'],
                'optional': ['Dolor abdominal', 'Fiebre baja (37.5°C - 38.5°C)']
            },
            'conclusion': 'Gastroenteritis',
            'confidence': 0.80
        },
        {
            'id': 'neumonia_grave',
            'conditions': {
                'required': ['Tos con flema (productiva)', 'Fiebre alta (más de 38.5°C)', 'Dificultad para respirar (disnea)'],
                'optional': ['Dolor en el pecho al respirar', 'Escalofríos']
            },
            'conclusion': 'Neumonía',
            'confidence': 0.88
        },
        {
            'id': 'asma_crisis',
            'conditions': {
                'required': ['Dificultad para respirar (disnea)', 'Silbidos al respirar'],
                'optional': ['Opresión en el pecho', 'Tos persistente']
            },
            'conclusion': 'Asma (Crisis)',
            'confidence': 0.82
        },
        {
            'id': 'amigdalitis_aguda',
            'conditions': {
                'required': ['Dolor de garganta intenso', 'Dolor al tragar', 'Fiebre alta (más de 38.5°C)'],
                'optional': ['Inflamación de ganglios', 'Fatiga extrema']
            },
            'conclusion': 'Amigdalitis',
            'confidence': 0.83
        },
        {
            'id': 'migraña_severa',
            'conditions': {
                'required': ['Dolor de cabeza (cefalea)', 'Náuseas'],
                'optional': ['Visión borrosa', 'Mareos']
            },
            'conclusion': 'Migraña',
            'confidence': 0.70
        },
        {
            'id': 'diabetes_inicial',
            'conditions': {
                'required': ['Sed intensa', 'Fatiga extrema', 'Visión borrosa'],
                'optional': ['Pérdida de peso inexplicable', 'Mareos']
            },
            'conclusion': 'Diabetes Tipo 2 (síntomas iniciales)',
            'confidence': 0.78
        },
        {
            'id': 'hipertension_sintomatica',
            'conditions': {
                'required': ['Dolor de cabeza (cefalea)', 'Mareos'],
                'optional': ['Visión borrosa', 'Palpitaciones']
            },
            'conclusion': 'Hipertensión (sospecha)',
            'confidence': 0.72
        },
        {
            'id': 'anemia_tipica',
            'conditions': {
                'required': ['Fatiga extrema', 'Debilidad general', 'Mareos'],
                'optional': ['Dolor de cabeza (cefalea)', 'Falta de aliento']
            },
            'conclusion': 'Anemia (sospecha)',
            'confidence': 0.75
        },
        {
            'id': 'ansiedad_fisica',
            'conditions': {
                'required': ['Palpitaciones', 'Sudoración excesiva'],
                'optional': ['Mareos', 'Dificultad para respirar']
            },
            'conclusion': 'Ansiedad (manifestación física)',
            'confidence': 0.70
        },
        {
            'id': 'angina_pecho',
            'conditions': {
                'required': ['Dolor en el pecho', 'Dolor que irradia al brazo izquierdo'],
                'optional': ['Sudoración fría', 'Disnea de esfuerzo']
            },
            'conclusion': 'Angina de Pecho (sospecha)',
            'confidence': 0.85
        },
        {
            'id': 'infarto_miocardio',
            'conditions': {
                'required': ['Dolor en el pecho', 'Dolor que irradia al brazo izquierdo', 'Sudoración fría'],
                'optional': ['Náuseas', 'Ansiedad intensa']
            },
            'conclusion': 'Infarto Agudo de Miocardio (sospecha)',
            'confidence': 0.92
        },
        {
            'id': 'acv_sospecha',
            'conditions': {
                'required': ['Debilidad muscular', 'Confusión mental', 'Dificultad para hablar'],
                'optional': ['Pérdida de equilibrio', 'Visión borrosa']
            },
            'conclusion': 'Accidente Cerebrovascular (ACV - sospecha)',
            'confidence': 0.90
        },
        {
            'id': 'epilepsia_crisis',
            'conditions': {
                'required': ['Convulsiones', 'Pérdida de conciencia'],
                'optional': ['Rigidez muscular', 'Confusión mental']
            },
            'conclusion': 'Epilepsia (Crisis Convulsiva)',
            'confidence': 0.88
        },
        {
            'id': 'pielonefritis',
            'conditions': {
                'required': ['Fiebre alta (más de 38.5°C)', 'Dolor en la zona lumbar', 'Dolor al orinar (disuria)'],
                'optional': ['Náuseas', 'Orina turbia']
            },
            'conclusion': 'Pielonefritis (Infección Renal)',
            'confidence': 0.84
        },
        {
            'id': 'calculos_renales',
            'conditions': {
                'required': ['Dolor en la zona lumbar', 'Sangre en la orina (hematuria)'],
                'optional': ['Náuseas', 'Vómitos']
            },
            'conclusion': 'Cálculos Renales (Cólico Renal)',
            'confidence': 0.86
        },
        {
            'id': 'insuficiencia_cardiaca',
            'conditions': {
                'required': ['Dificultad para respirar (disnea)', 'Hinchazón en piernas', 'Fatiga extrema'],
                'optional': ['Edema periférico', 'Ortopnea']
            },
            'conclusion': 'Insuficiencia Cardíaca (descompensada)',
            'confidence': 0.87
        },
        {
            'id': 'crisis_hipertensiva',
            'conditions': {
                'required': ['Presión arterial sistólica >180 mmHg', 'Dolor de cabeza (cefalea)', 'Visión borrosa'],
                'optional': ['Náuseas', 'Dolor en el pecho']
            },
            'conclusion': 'Crisis Hipertensiva',
            'confidence': 0.89
        },
        {
            'id': 'leucemia_aguda',
            'conditions': {
                'required': ['Fatiga extrema', 'Fiebre sin foco infeccioso', 'Sangrado fácil', 'Hematomas espontáneos'],
                'optional': ['Petequias generalizadas', 'Adenopatías generalizadas']
            },
            'conclusion': 'Leucemia Aguda (sospecha)',
            'confidence': 0.81
        },
        {
            'id': 'meningitis_sospecha',
            'conditions': {
                'required': ['Fiebre alta (más de 38.5°C)', 'Dolor de cabeza (cefalea)', 'Rigidez de nuca'],
                'optional': ['Fotofobia', 'Vómitos']
            },
            'conclusion': 'Meningitis (sospecha)',
            'confidence': 0.91
        },
        {
            'id': 'apendicitis',
            'conditions': {
                'required': ['Dolor periumbilical que migra a cuadrante inferior derecho', 'Náuseas', 'Fiebre'],
                'optional': ['Vómitos', 'Rigidez abdominal']
            },
            'conclusion': 'Apendicitis Aguda',
            'confidence': 0.85
        },
        {
            'id': 'glaucoma_agudo',
            'conditions': {
                'required': ['Dolor ocular', 'Visión borrosa', 'Náuseas'],
                'optional': ['Vómitos', 'Ojo rojo']
            },
            'conclusion': 'Glaucoma Agudo',
            'confidence': 0.83
        },
        {
            'id': 'embolia_pulmonar',
            'conditions': {
                'required': ['Dificultad para respirar (disnea)', 'Dolor en el pecho al respirar', 'Taquicardia'],
                'optional': ['Tos con sangre (hemoptisis)', 'Ansiedad intensa']
            },
            'conclusion': 'Embolia Pulmonar (sospecha)',
            'confidence': 0.88
        },
        {
            'id': 'cetoacidosis_diabetica',
            'conditions': {
                'required': ['Sed intensa', 'Orina frecuente', 'Náuseas', 'Vómitos'],
                'optional': ['Confusión mental', 'Respiración rápida (taquipnea)']
            },
            'conclusion': 'Cetoacidosis Diabética',
            'confidence': 0.86
        }
    ]

def search_diseases_by_symptom(symptom):
    """Busca enfermedades por sintoma"""
    kb = get_knowledge_base()
    results = []
    for name, info in kb.items():
        if symptom in info['symptoms_main']:
            results.append((name, True))
        elif symptom in info['symptoms_secondary']:
            results.append((name, False))
    return results

def get_all_categories():
    """Categorias disponibles"""
    kb = get_knowledge_base()
    return sorted(list(set(info['category'] for info in kb.values())))

def display_disease_card(disease_name, disease_info):
    """Muestra tarjeta de enfermedad"""
    with st.expander(f"{disease_name} | {disease_info['category']}", expanded=False):
        st.markdown(f"**Descripcion:** {disease_info['description']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Sintomas Principales:**")
            for symptom in disease_info['symptoms_main']:
                st.markdown(f"- {symptom}")
        with col2:
            st.markdown("**Sintomas Secundarios:**")
            for symptom in disease_info['symptoms_secondary']:
                st.markdown(f"- {symptom}")

def main():
    st.set_page_config(page_title="Base de Conocimiento", layout="wide")
    st.title("Base de Conocimiento")
    
    kb = get_knowledge_base()
    if not kb:
        st.error("No se pudo cargar la base de conocimiento")
        return
    
    st.success(f"Cargadas {len(kb)} enfermedades")
    
    tab1, tab2 = st.tabs(["Vista General", "Busqueda"])
    
    with tab1:
        for disease_name, disease_info in sorted(kb.items()):
            display_disease_card(disease_name, disease_info)
    
    with tab2:
        diseases = get_disease_names()
        selected = st.selectbox("Seleccione enfermedad:", diseases)
        if selected:
            display_disease_card(selected, get_disease_info(selected))

if __name__ == "__main__":
    main()
