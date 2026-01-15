# -*- coding: utf-8 -*-
"""
inference_engine.py
Motor de Inferencia del Sistema Experto
Implementa encadenamiento hacia adelante y hacia atrás
"""

import streamlit as st
from knowledge_base import get_knowledge_base, create_simple_rules
from collections import defaultdict
import math


class InferenceEngine:
    """Motor de inferencia con múltiples estrategias de razonamiento"""
    
    def __init__(self):
        self.knowledge_base = get_knowledge_base()
        self.rules = create_simple_rules()
        self.diagnosis_results = []
        
    def calculate_match_score(self, user_symptoms, disease_symptoms):
        """Calcula score de coincidencia entre síntomas del usuario y enfermedad"""
        if not disease_symptoms:
            return 0.0
        
        matches = len(set(user_symptoms) & set(disease_symptoms))
        total_disease = len(disease_symptoms)
        total_user = len(user_symptoms)
        
        # Precisión y recall
        precision = matches / total_user if total_user > 0 else 0
        recall = matches / total_disease if total_disease > 0 else 0
        
        # F1-Score
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0
        
        return f1_score
    
    def forward_chaining(self, user_symptoms):
        """Encadenamiento hacia adelante - De síntomas a diagnóstico"""
        results = []
        
        for disease_name, disease_info in self.knowledge_base.items():
            # Síntomas principales
            main_symptoms = disease_info['symptoms_main']
            # Todos los síntomas
            all_symptoms = disease_info['symptoms_all']
            
            # Calcular coincidencias
            main_matches = set(user_symptoms) & set(main_symptoms)
            all_matches = set(user_symptoms) & set(all_symptoms)
            
            # Score basado en síntomas principales
            main_score = len(main_matches) / len(main_symptoms) if main_symptoms else 0
            
            # Score general
            overall_score = self.calculate_match_score(user_symptoms, all_symptoms)
            
            # Peso combinado (70% principales, 30% general)
            combined_score = (main_score * 0.7) + (overall_score * 0.3)
            
            if combined_score > 0.2:  # Umbral mínimo
                results.append({
                    'disease': disease_name,
                    'confidence': combined_score,
                    'matched_symptoms': list(all_matches),
                    'main_matches': list(main_matches),
                    'category': disease_info['category'],
                    'severity': disease_info['severity'],
                    'description': disease_info['description'],
                    'recommendations': disease_info['recommendations']
                })
        
        # Ordenar por confianza
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results
    
    def backward_chaining(self, user_symptoms, hypothesis_disease):
        """Encadenamiento hacia atrás - Verifica una hipótesis"""
        if hypothesis_disease not in self.knowledge_base:
            return None
        
        disease_info = self.knowledge_base[hypothesis_disease]
        required_symptoms = disease_info['symptoms_main']
        all_symptoms = disease_info['symptoms_all']
        
        # Verificar síntomas presentes
        present = set(user_symptoms) & set(all_symptoms)
        missing = set(required_symptoms) - set(user_symptoms)
        
        # Calcular nivel de confirmación
        confirmation_level = len(present) / len(all_symptoms) if all_symptoms else 0
        
        return {
            'hypothesis': hypothesis_disease,
            'confirmed': confirmation_level > 0.5,
            'confidence': confirmation_level,
            'present_symptoms': list(present),
            'missing_symptoms': list(missing),
            'description': disease_info['description'],
            'recommendations': disease_info['recommendations']
        }
    
    def rule_based_inference(self, user_symptoms):
        """Inferencia basada en reglas IF-THEN"""
        matched_rules = []
        
        for rule in self.rules:
            required = set(rule['conditions']['required'])
            optional = set(rule['conditions'].get('optional', []))
            
            # Verificar condiciones requeridas
            required_met = required.issubset(set(user_symptoms))
            
            if required_met:
                # Contar opcionales cumplidos
                optional_met = len(optional & set(user_symptoms))
                total_optional = len(optional)
                
                # Ajustar confianza según opcionales
                base_confidence = rule['confidence']
                if total_optional > 0:
                    optional_bonus = (optional_met / total_optional) * 0.15
                    final_confidence = min(base_confidence + optional_bonus, 0.99)
                else:
                    final_confidence = base_confidence
                
                matched_rules.append({
                    'rule_id': rule['id'],
                    'conclusion': rule['conclusion'],
                    'confidence': final_confidence,
                    'required_met': list(required),
                    'optional_met': list(optional & set(user_symptoms))
                })
        
        matched_rules.sort(key=lambda x: x['confidence'], reverse=True)
        return matched_rules
    
    def hybrid_inference(self, user_symptoms):
        """Inferencia híbrida combinando múltiples métodos"""
        # Ejecutar todos los métodos
        forward_results = self.forward_chaining(user_symptoms)
        rule_results = self.rule_based_inference(user_symptoms)
        
        # Combinar resultados
        combined_results = {}
        
        # Agregar resultados de forward chaining
        for result in forward_results:
            disease = result['disease']
            combined_results[disease] = {
                'disease': disease,
                'forward_confidence': result['confidence'],
                'rule_confidence': 0,
                'final_confidence': result['confidence'],
                'matched_symptoms': result['matched_symptoms'],
                'category': result['category'],
                'severity': result['severity'],
                'description': result['description'],
                'recommendations': result['recommendations'],
                'method': 'forward_chaining'
            }
        
        # Agregar/actualizar con resultados de reglas
        for result in rule_results:
            disease = result['conclusion']
            if disease in combined_results:
                # Combinar confianzas (promedio ponderado)
                fwd_conf = combined_results[disease]['forward_confidence']
                rule_conf = result['confidence']
                combined_results[disease]['rule_confidence'] = rule_conf
                combined_results[disease]['final_confidence'] = (fwd_conf * 0.6) + (rule_conf * 0.4)
                combined_results[disease]['method'] = 'hybrid'
            else:
                # Solo de reglas
                disease_info = self.knowledge_base.get(disease, {})
                combined_results[disease] = {
                    'disease': disease,
                    'forward_confidence': 0,
                    'rule_confidence': result['confidence'],
                    'final_confidence': result['confidence'],
                    'matched_symptoms': result['required_met'] + result['optional_met'],
                    'category': disease_info.get('category', 'Desconocida'),
                    'severity': disease_info.get('severity', 'moderada'),
                    'description': disease_info.get('description', ''),
                    'recommendations': disease_info.get('recommendations', []),
                    'method': 'rule_based'
                }
        
        # Convertir a lista y ordenar
        final_results = list(combined_results.values())
        final_results.sort(key=lambda x: x['final_confidence'], reverse=True)
        
        return final_results
    
    def explain_diagnosis(self, diagnosis_result):
        """Genera explicación del diagnóstico"""
        disease = diagnosis_result['disease']
        confidence = diagnosis_result['final_confidence']
        matched = diagnosis_result['matched_symptoms']
        method = diagnosis_result['method']
        
        explanation = f"""
### Explicación del Diagnóstico: {disease}

**Nivel de Confianza:** {confidence*100:.1f}%

**Método de Inferencia:** {method.replace('_', ' ').title()}

**Síntomas Coincidentes ({len(matched)}):**
"""
        for symptom in matched:
            explanation += f"\n- ✓ {symptom}"
        
        explanation += f"""

**Categoría:** {diagnosis_result['category']}
**Severidad:** {diagnosis_result['severity']}

**Descripción:**
{diagnosis_result['description']}
"""
        
        return explanation
    
    def get_confidence_level_label(self, confidence):
        """Etiqueta según nivel de confianza"""
        if confidence >= 0.8:
            return "Muy Alta", "🟢"
        elif confidence >= 0.6:
            return "Alta", "🟡"
        elif confidence >= 0.4:
            return "Media", "🟠"
        else:
            return "Baja", "🔴"


def diagnose(user_symptoms, method='hybrid'):
    """Función principal de diagnóstico"""
    if not user_symptoms:
        return []
    
    engine = InferenceEngine()
    
    if method == 'forward':
        results = engine.forward_chaining(user_symptoms)
    elif method == 'rules':
        rule_results = engine.rule_based_inference(user_symptoms)
        # Convertir formato
        results = []
        for r in rule_results:
            disease_info = engine.knowledge_base.get(r['conclusion'], {})
            results.append({
                'disease': r['conclusion'],
                'confidence': r['confidence'],
                'matched_symptoms': r['required_met'] + r['optional_met'],
                'category': disease_info.get('category', 'Desconocida'),
                'severity': disease_info.get('severity', 'moderada'),
                'description': disease_info.get('description', ''),
                'recommendations': disease_info.get('recommendations', [])
            })
    else:  # hybrid
        results = engine.hybrid_inference(user_symptoms)
    
    return results


def main():
    """Pruebas del motor de inferencia"""
    st.set_page_config(page_title="Motor de Inferencia", layout="wide")
    st.title("🔍 Motor de Inferencia - Sistema Experto Médico")
    
    # Síntomas de prueba
    test_symptoms = st.multiselect(
        "Seleccione síntomas de prueba:",
        [
            "Fiebre alta (más de 38.5°C)",
            "Tos seca",
            "Dolores musculares (mialgia)",
            "Fatiga extrema",
            "Dolor de cabeza (cefalea)",
            "Dificultad para respirar (disnea)",
            "Náuseas",
            "Vómitos"
        ]
    )
    
    method = st.radio(
        "Método de inferencia:",
        ['hybrid', 'forward', 'rules'],
        format_func=lambda x: {
            'hybrid': 'Híbrido (Recomendado)',
            'forward': 'Encadenamiento Hacia Adelante',
            'rules': 'Basado en Reglas'
        }[x]
    )
    
    if st.button("🔍 Realizar Diagnóstico") and test_symptoms:
        with st.spinner("Procesando..."):
            results = diagnose(test_symptoms, method)
            
            st.success(f"✅ Se encontraron {len(results)} posibles diagnósticos")
            
            for i, result in enumerate(results[:5], 1):
                confidence = result.get('final_confidence', result.get('confidence', 0))
                level, emoji = InferenceEngine().get_confidence_level_label(confidence)
                
                with st.expander(f"{emoji} #{i} - {result['disease']} ({confidence*100:.1f}%)", expanded=(i==1)):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Descripción:** {result['description']}")
                        st.markdown(f"**Síntomas coincidentes:** {len(result['matched_symptoms'])}")
                        for symptom in result['matched_symptoms']:
                            st.markdown(f"- ✓ {symptom}")
                    
                    with col2:
                        st.metric("Confianza", f"{confidence*100:.1f}%")
                        st.metric("Categoría", result['category'])
                        st.metric("Severidad", result['severity'])
                    
                    st.markdown("**Recomendaciones:**")
                    for rec in result['recommendations']:
                        st.markdown(f"- {rec}")


if __name__ == "__main__":
    main()