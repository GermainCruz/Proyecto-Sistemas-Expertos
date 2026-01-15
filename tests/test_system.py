# -*- coding: utf-8 -*-
"""
test_system.py
Pruebas Unitarias del Sistema Experto
"""

import unittest
import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from symptoms import get_all_symptoms, get_all_symptoms_flat, validate_symptoms
from knowledge_base import (
    get_knowledge_base, 
    get_disease_names, 
    get_disease_info,
    create_simple_rules
)
from inference_engine import InferenceEngine, diagnose
from cases import load_test_cases, run_test_case


class TestSymptoms(unittest.TestCase):
    """Pruebas del módulo de síntomas"""
    
    def test_load_symptoms(self):
        """Verificar que se cargan los síntomas"""
        symptoms = get_all_symptoms()
        self.assertIsInstance(symptoms, dict)
        self.assertGreater(len(symptoms), 0)
    
    def test_symptoms_flat(self):
        """Verificar lista plana de síntomas"""
        symptoms = get_all_symptoms_flat()
        self.assertIsInstance(symptoms, list)
        self.assertGreater(len(symptoms), 0)
    
    def test_validate_symptoms_empty(self):
        """Validar lista vacía de síntomas"""
        self.assertFalse(validate_symptoms([]))
    
    def test_validate_symptoms_valid(self):
        """Validar lista con síntomas"""
        self.assertTrue(validate_symptoms(['Fiebre', 'Tos']))


class TestKnowledgeBase(unittest.TestCase):
    """Pruebas de la base de conocimiento"""
    
    def test_load_knowledge_base(self):
        """Verificar carga de KB"""
        kb = get_knowledge_base()
        self.assertIsInstance(kb, dict)
        self.assertGreater(len(kb), 0)
    
    def test_disease_names(self):
        """Verificar lista de enfermedades"""
        diseases = get_disease_names()
        self.assertIsInstance(diseases, list)
        self.assertGreater(len(diseases), 0)
    
    def test_disease_info_structure(self):
        """Verificar estructura de información de enfermedad"""
        diseases = get_disease_names()
        if diseases:
            disease = diseases[0]
            info = get_disease_info(disease)
            
            self.assertIsNotNone(info)
            self.assertIn('symptoms_main', info)
            self.assertIn('symptoms_secondary', info)
            self.assertIn('description', info)
            self.assertIn('severity', info)
            self.assertIn('recommendations', info)
            self.assertIn('category', info)
    
    def test_create_rules(self):
        """Verificar creación de reglas"""
        rules = create_simple_rules()
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        
        # Verificar estructura de regla
        rule = rules[0]
        self.assertIn('id', rule)
        self.assertIn('conditions', rule)
        self.assertIn('conclusion', rule)
        self.assertIn('confidence', rule)


class TestInferenceEngine(unittest.TestCase):
    """Pruebas del motor de inferencia"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.engine = InferenceEngine()
        self.test_symptoms = [
            'Fiebre alta (más de 38.5°C)',
            'Tos seca',
            'Dolores musculares (mialgia)'
        ]
    
    def test_engine_initialization(self):
        """Verificar inicialización del motor"""
        self.assertIsNotNone(self.engine.knowledge_base)
        self.assertIsNotNone(self.engine.rules)
    
    def test_calculate_match_score(self):
        """Verificar cálculo de score"""
        user_symptoms = ['A', 'B', 'C']
        disease_symptoms = ['A', 'B', 'C', 'D']
        
        score = self.engine.calculate_match_score(user_symptoms, disease_symptoms)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_forward_chaining(self):
        """Verificar encadenamiento hacia adelante"""
        results = self.engine.forward_chaining(self.test_symptoms)
        
        self.assertIsInstance(results, list)
        if results:
            result = results[0]
            self.assertIn('disease', result)
            self.assertIn('confidence', result)
            self.assertIn('matched_symptoms', result)
    
    def test_rule_based_inference(self):
        """Verificar inferencia basada en reglas"""
        results = self.engine.rule_based_inference(self.test_symptoms)
        
        self.assertIsInstance(results, list)
    
    def test_hybrid_inference(self):
        """Verificar método híbrido"""
        results = self.engine.hybrid_inference(self.test_symptoms)
        
        self.assertIsInstance(results, list)
        if results:
            result = results[0]
            self.assertIn('final_confidence', result)
            self.assertIn('method', result)
    
    def test_diagnose_function(self):
        """Verificar función principal de diagnóstico"""
        results = diagnose(self.test_symptoms, method='hybrid')
        
        self.assertIsInstance(results, list)
    
    def test_confidence_label(self):
        """Verificar etiquetas de confianza"""
        label, emoji = self.engine.get_confidence_level_label(0.9)
        self.assertEqual(label, "Muy Alta")
        self.assertEqual(emoji, "🟢")
        
        label, emoji = self.engine.get_confidence_level_label(0.7)
        self.assertEqual(label, "Alta")
        self.assertEqual(emoji, "🟡")
        
        label, emoji = self.engine.get_confidence_level_label(0.5)
        self.assertEqual(label, "Media")
        self.assertEqual(emoji, "🟠")
        
        label, emoji = self.engine.get_confidence_level_label(0.3)
        self.assertEqual(label, "Baja")
        self.assertEqual(emoji, "🔴")


class TestCases(unittest.TestCase):
    """Pruebas de casos de prueba"""
    
    def test_load_test_cases(self):
        """Verificar carga de casos de prueba"""
        cases = load_test_cases()
        
        self.assertIsInstance(cases, list)
        self.assertGreater(len(cases), 0)
    
    def test_case_structure(self):
        """Verificar estructura de caso"""
        cases = load_test_cases()
        if cases:
            case = cases[0]
            
            self.assertIn('id', case)
            self.assertIn('nombre', case)
            self.assertIn('symptoms', case)
            self.assertIn('expected_diagnosis', case)
            self.assertIn('severity', case)
    
    def test_run_single_case(self):
        """Verificar ejecución de caso individual"""
        cases = load_test_cases()
        if cases:
            case = cases[0]
            result = run_test_case(case, method='hybrid')
            
            self.assertIn('case', result)
            self.assertIn('results', result)
            self.assertIn('expected_found', result)
            self.assertIn('total_diagnoses', result)


class TestIntegration(unittest.TestCase):
    """Pruebas de integración del sistema completo"""
    
    def test_full_diagnosis_flow(self):
        """Verificar flujo completo de diagnóstico"""
        # 1. Obtener síntomas
        all_symptoms = get_all_symptoms_flat()
        self.assertGreater(len(all_symptoms), 0)
        
        # 2. Seleccionar algunos síntomas
        selected = all_symptoms[:5]
        self.assertTrue(validate_symptoms(selected))
        
        # 3. Realizar diagnóstico
        results = diagnose(selected, method='hybrid')
        self.assertIsInstance(results, list)
        
        # 4. Verificar estructura de resultados
        if results:
            result = results[0]
            self.assertIn('disease', result)
            self.assertIn('final_confidence', result)
    
    def test_knowledge_base_consistency(self):
        """Verificar consistencia de la base de conocimiento"""
        kb = get_knowledge_base()
        
        for disease, info in kb.items():
            # Verificar que todos los campos necesarios existen
            self.assertIsInstance(info['symptoms_main'], list)
            self.assertIsInstance(info['symptoms_secondary'], list)
            self.assertIsInstance(info['description'], str)
            self.assertIsInstance(info['severity'], str)
            self.assertIsInstance(info['recommendations'], list)
            
            # Verificar que hay al menos un síntoma
            self.assertGreater(len(info['symptoms_all']), 0)
    
    def test_all_inference_methods(self):
        """Verificar que todos los métodos de inferencia funcionan"""
        symptoms = [
            'Fiebre alta (más de 38.5°C)',
            'Tos seca',
            'Fatiga extrema'
        ]
        
        # Forward
        results_forward = diagnose(symptoms, method='forward')
        self.assertIsInstance(results_forward, list)
        
        # Rules
        results_rules = diagnose(symptoms, method='rules')
        self.assertIsInstance(results_rules, list)
        
        # Hybrid
        results_hybrid = diagnose(symptoms, method='hybrid')
        self.assertIsInstance(results_hybrid, list)


def run_tests():
    """Ejecutar todas las pruebas"""
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestSymptoms))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBase))
    suite.addTests(loader.loadTestsFromTestCase(TestInferenceEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS")
    print("="*70)
    print(f"Total de pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)