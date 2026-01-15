# -*- coding: utf-8 -*-
"""
app.py
Aplicación Principal - Sistema Experto de Diagnóstico Médico
Integra todos los módulos del sistema
"""

import streamlit as st
import sys
import os
from datetime import datetime
import io
import hashlib
import time  # <-- AÑADE ESTA LÍNEA

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

    .pdf-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #667eea;
        margin-top: 2rem;
    }

    .history-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .history-item:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
    if 'last_diagnosis_id' not in st.session_state:
        st.session_state.last_diagnosis_id = 0
    # Variables para controlar el guardado
    if 'save_requested' not in st.session_state:
        st.session_state.save_requested = {}
    if 'just_saved' not in st.session_state:
        st.session_state.just_saved = False
    # Nuevas variables para PDF
    if 'pdf_bytes' not in st.session_state:
        st.session_state.pdf_bytes = None
    if 'pdf_generated' not in st.session_state:
        st.session_state.pdf_generated = False
    if 'pdf_filename' not in st.session_state:
        st.session_state.pdf_filename = None
    if 'show_pdf_section' not in st.session_state:
        st.session_state.show_pdf_section = False

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
        st.warning(
            "⚠️ **ATENCIÓN:** Esta condición requiere consulta médica pronta. No demore la atención profesional.")
    elif 'moderada' in severity_lower:
        st.info("ℹ️ **RECOMENDACIÓN:** Consulte con un profesional de la salud si los síntomas persisten o empeoran.")


def generate_diagnosis_hash(disease, confidence, timestamp):
    """Genera un hash único para un diagnóstico"""
    data = f"{disease}_{confidence}_{timestamp}"
    return hashlib.md5(data.encode()).hexdigest()[:8]


def display_diagnosis_result(result, rank):
    """Muestra un resultado de diagnóstico de forma atractiva - VERSIÓN MEJORADA"""
    confidence = result.get('final_confidence', result.get('confidence', 0))
    disease = result['disease']

    # Crear un ID único para este diagnóstico
    from hashlib import md5
    unique_id = md5(f"{disease}_{confidence}_{rank}".encode()).hexdigest()[:8]

    # Determinar color según confianza
    if confidence >= 0.8:
        emoji = "🟢"
    elif confidence >= 0.6:
        emoji = "🟡"
    elif confidence >= 0.4:
        emoji = "🟠"
    else:
        emoji = "🔴"

    with st.expander(f"{emoji} #{rank} - {disease} ({confidence * 100:.1f}%)", expanded=(rank == 1)):
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
            st.metric("Nivel de Confianza", f"{confidence * 100:.1f}%")
            st.metric("Severidad", result['severity'])
            st.progress(confidence)

        st.markdown("---")
        display_severity_alert(result['severity'])

        st.markdown("### 📋 Recomendaciones")
        for i, rec in enumerate(result['recommendations'], 1):
            st.markdown(f"{i}. {rec}")

        st.markdown("---")

        # ============================================
        # SISTEMA DE GUARDADO MEJORADO
        # ============================================

        # Verificar si ya está en el historial
        is_already_saved = any(
            h['disease'] == disease and
            abs(h['confidence'] - confidence) < 0.01
            for h in st.session_state.diagnosis_history
        )

        # Verificar si hay una solicitud pendiente para este
        is_pending = unique_id in st.session_state.save_requested

        if is_already_saved:
            st.success("✅ **Ya guardado en el historial**")
        elif is_pending:
            st.warning("⏳ **Pendiente de guardar...**")

            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirmar", key=f"confirm_{unique_id}"):
                    # Guardar definitivamente
                    st.session_state.last_diagnosis_id += 1
                    st.session_state.diagnosis_history.append({
                        'id': st.session_state.last_diagnosis_id,
                        'disease': disease,
                        'confidence': confidence,
                        'symptoms': result['matched_symptoms'],
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'category': result.get('category', 'N/A'),
                        'severity': result.get('severity', 'N/A'),
                        'description': result.get('description', ''),
                        'rank': rank
                    })
                    # Limpiar solicitud
                    del st.session_state.save_requested[unique_id]
                    st.session_state.just_saved = True
                    st.rerun()

            with col_cancel:
                if st.button("❌ Cancelar", key=f"cancel_{unique_id}"):
                    # Cancelar solicitud
                    del st.session_state.save_requested[unique_id]
                    st.rerun()
        else:
            # Botón para solicitar guardado
            if st.button("📌 **Guardar en Historial**", key=f"request_{unique_id}"):
                # Marcar como solicitado
                st.session_state.save_requested[unique_id] = {
                    'disease': disease,
                    'confidence': confidence,
                    'rank': rank,
                    'data': result
                }

# ====================================
# FUNCIONES PARA PDF - VERSIÓN SIMPLIFICADA Y ROBUSTA
# ====================================

def create_simple_fallback_pdf(symptoms, results, method):
    """Crea un PDF muy simple como fallback - SIEMPRE FUNCIONA"""
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.cell(200, 10, txt="REPORTE MEDICO", ln=1, align='C')
        pdf.ln(5)

        # Información básica
        pdf.set_font("Arial", size=10)
        pdf.cell(100, 8, txt=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=1)
        pdf.cell(100, 8, txt=f"Metodo: {method}", ln=1)
        pdf.cell(100, 8, txt=f"Sintomas: {len(symptoms)}", ln=1)
        pdf.cell(100, 8, txt=f"Resultados: {len(results)}", ln=1)
        pdf.ln(10)

        # Síntomas
        if symptoms:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(200, 8, txt="SINTOMAS:", ln=1)
            pdf.set_font("Arial", size=9)
            for i, symptom in enumerate(symptoms[:10], 1):  # Máximo 10 síntomas
                safe_text = str(symptom)[:60]  # Limitar longitud
                pdf.cell(200, 6, txt=f"{i}. {safe_text}", ln=1)
            if len(symptoms) > 10:
                pdf.cell(200, 6, txt=f"... y {len(symptoms) - 10} mas", ln=1)

        pdf.ln(10)

        # Resultados
        if results:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(200, 8, txt="DIAGNOSTICOS:", ln=1)
            pdf.set_font("Arial", size=9)
            for i, result in enumerate(results[:5], 1):  # Máximo 5 resultados
                disease = str(result.get('disease', ''))[:40]
                confidence = result.get('final_confidence', result.get('confidence', 0)) * 100
                pdf.cell(200, 6, txt=f"{i}. {disease} ({confidence:.1f}%)", ln=1)

        pdf.ln(10)

        # Aviso
        pdf.set_font("Arial", 'I', 8)
        pdf.multi_cell(0, 4,
                       txt="IMPORTANTE: Este reporte es solo para fines educativos. No reemplaza el diagnostico medico profesional.")

        # Obtener bytes
        try:
            output = pdf.output(dest='S')
            if isinstance(output, str):
                return output.encode('latin-1')
            elif isinstance(output, bytearray):
                return bytes(output)
            else:
                return bytes(output) if hasattr(output, '__bytes__') else str(output).encode('latin-1')
        except:
            from io import BytesIO
            buffer = BytesIO()
            pdf.output(buffer)
            return buffer.getvalue()

    except:
        # Si todo falla, devolver PDF vacío pero válido
        return b'%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF'


def convert_to_bytes(data):
    """Convierte cualquier dato a bytes para st.download_button"""
    if data is None:
        return b''

    if isinstance(data, bytes):
        return data
    elif isinstance(data, bytearray):
        return bytes(data)
    elif isinstance(data, str):
        return data.encode('utf-8')
    elif hasattr(data, 'getvalue'):  # Para BytesIO
        return data.getvalue()
    else:
        try:
            return bytes(data)
        except:
            return str(data).encode('utf-8')


def clean_text_for_pdf(text, max_length=80):
    """Limpia el texto para que sea compatible con PDF"""
    if text is None:
        return ""

    text = str(text)

    # Reemplazar caracteres especiales
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Eliminar caracteres no ASCII
    text = ''.join(char for char in text if ord(char) < 256)

    # Limitar longitud
    return text[:max_length]


def build_pdf_report(symptoms, results, method, top_n=5):
    """Genera un reporte PDF simplificado pero robusto"""
    try:
        from fpdf import FPDF

        # Crear PDF simple
        pdf = FPDF()
        pdf.add_page()

        # ============================================
        # ENCABEZADO
        # ============================================

        # Título
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "REPORTE DE DIAGNOSTICO MEDICO", 0, 1, 'C')

        # Línea
        pdf.line(20, 20, 190, 20)
        pdf.ln(5)

        # ============================================
        # INFORMACIÓN GENERAL
        # ============================================

        pdf.set_font("Arial", '', 10)

        # Fecha
        pdf.cell(30, 6, "Fecha:", 0, 0)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, datetime.now().strftime("%d/%m/%Y %H:%M"), 0, 1)

        # Método
        pdf.set_font("Arial", '', 10)
        pdf.cell(30, 6, "Metodo:", 0, 0)
        pdf.set_font("Arial", 'B', 10)
        method_names = {
            'hybrid': 'Hibrido',
            'forward': 'Forward',
            'rules': 'Reglas'
        }
        pdf.cell(0, 6, method_names.get(method, method), 0, 1)

        pdf.ln(5)

        # ============================================
        # SÍNTOMAS REPORTADOS
        # ============================================

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "SINTOMAS REPORTADOS", 0, 1)

        pdf.set_font("Arial", '', 10)

        if symptoms:
            symptom_count = len(symptoms)
            pdf.cell(0, 6, f"Total: {symptom_count} sintomas", 0, 1)
            pdf.ln(2)

            # Mostrar síntomas en columnas
            col_width = 90
            for i in range(0, min(symptom_count, 10), 2):  # Máximo 10 síntomas
                y = pdf.get_y()

                # Síntoma izquierdo
                if i < symptom_count:
                    symptom_left = clean_text_for_pdf(symptoms[i], 40)
                    pdf.set_xy(10, y)
                    pdf.cell(col_width, 6, f"{i + 1}. {symptom_left}", 0, 0)

                # Síntoma derecho
                if i + 1 < symptom_count:
                    symptom_right = clean_text_for_pdf(symptoms[i + 1], 40)
                    pdf.set_xy(10 + col_width, y)
                    pdf.cell(col_width, 6, f"{i + 2}. {symptom_right}", 0, 1)
                else:
                    pdf.ln(6)

            if symptom_count > 10:
                pdf.cell(0, 6, f"... y {symptom_count - 10} sintomas mas", 0, 1)
        else:
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 6, "No se reportaron sintomas", 0, 1)

        pdf.ln(10)

        # ============================================
        # RESULTADOS DEL DIAGNÓSTICO
        # ============================================

        pdf.set_font("Arial", 'B', 12)
        n = min(top_n, len(results))
        pdf.cell(0, 8, f"RESULTADOS (Top {n})", 0, 1)

        if results:
            for i, result in enumerate(results[:n], 1):
                confidence = result.get('final_confidence', result.get('confidence', 0)) * 100

                # Marco simple
                pdf.set_line_width(0.3)
                pdf.set_draw_color(200, 200, 200)
                pdf.rect(10, pdf.get_y(), 190, 25)

                # Número y nombre
                pdf.set_font("Arial", 'B', 11)
                disease_name = clean_text_for_pdf(result.get('disease', ''), 50)
                pdf.cell(180, 8, f"{i}. {disease_name}", 0, 1)

                # Confianza
                pdf.set_font("Arial", '', 10)
                pdf.cell(0, 6, f"Confianza: {confidence:.1f}%", 0, 1)

                # Detalles
                pdf.set_font("Arial", '', 9)

                if result.get('category'):
                    category = clean_text_for_pdf(result.get('category'), 30)
                    pdf.cell(90, 5, f"Categoria: {category}", 0, 0)

                if result.get('severity'):
                    severity = clean_text_for_pdf(result.get('severity'), 20)
                    pdf.cell(0, 5, f"Severidad: {severity}", 0, 1)
                else:
                    pdf.ln(5)

                pdf.ln(3)
        else:
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 6, "No se encontraron diagnosticos", 0, 1)

        pdf.ln(10)

        # ============================================
        # RESUMEN ESTADÍSTICO
        # ============================================

        if results:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 8, "RESUMEN", 0, 1)

            pdf.set_font("Arial", '', 10)

            # Estadísticas simples
            stats = [
                ("Total diagnosticos", str(len(results))),
                ("Mostrados", str(n)),
            ]

            # Calcular categorías únicas
            if results:
                categories = set()
                for r in results[:n]:
                    cat = r.get('category')
                    if cat:
                        categories.add(clean_text_for_pdf(cat, 20))
                stats.append(("Categorias", str(len(categories))))

            # Calcular condiciones graves
            severe_count = 0
            for r in results[:n]:
                severity = str(r.get('severity', '')).lower()
                if 'grave' in severity:
                    severe_count += 1
            stats.append(("Graves", str(severe_count)))

            # Mostrar estadísticas
            col_width = 50
            for label, value in stats:
                pdf.cell(col_width, 6, f"{label}:", 0, 0)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(0, 6, value, 0, 1)
                pdf.set_font("Arial", '', 10)

        pdf.ln(15)

        # ============================================
        # AVISO LEGAL
        # ============================================

        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(100, 100, 100)

        disclaimer = "IMPORTANTE: Este reporte es generado automaticamente. Es solo para fines educativos e informativos. No constituye un diagnostico medico profesional. Consulte siempre con un medico."

        pdf.multi_cell(0, 4, disclaimer, 0, 'C')

        # Pie de página
        pdf.set_y(-15)
        pdf.cell(0, 10, f"Pagina 1/1 - {datetime.now().strftime('%d/%m/%Y')}", 0, 0, 'C')

        # Obtener bytes del PDF
        try:
            output = pdf.output(dest='S')
            if isinstance(output, str):
                return output.encode('latin-1')
            elif isinstance(output, bytearray):
                return bytes(output)
            return output
        except:
            from io import BytesIO
            buffer = BytesIO()
            pdf.output(buffer)
            return buffer.getvalue()

    except Exception as e:
        # Si hay error, usar PDF simple
        return create_simple_fallback_pdf(symptoms, results, method)


def generate_html_report(symptoms, results, method, top_n=5):
    """Genera reporte en formato HTML"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Diagnóstico</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 20px;
                padding: 0;
                color: #333;
                background: #f5f5f5;
            }}

            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}

            .header {{
                text-align: center;
                padding-bottom: 20px;
                border-bottom: 2px solid #3498db;
                margin-bottom: 20px;
            }}

            .header h1 {{
                color: #2c3e50;
                margin: 0 0 10px 0;
            }}

            .info {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                border-left: 4px solid #3498db;
            }}

            .section {{
                margin-bottom: 25px;
            }}

            .section-title {{
                color: #3498db;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
                margin-bottom: 15px;
            }}

            .symptoms-list {{
                list-style: none;
                padding: 0;
            }}

            .symptoms-list li {{
                padding: 5px 0;
                border-bottom: 1px dashed #eee;
            }}

            .diagnosis-card {{
                background: #f8f9fa;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 5px;
                border-left: 4px solid #3498db;
            }}

            .diagnosis-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }}

            .confidence {{
                background: #3498db;
                color: white;
                padding: 3px 10px;
                border-radius: 10px;
                font-size: 12px;
            }}

            .stats {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-top: 20px;
            }}

            .stat-item {{
                background: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }}

            .stat-value {{
                font-size: 24px;
                font-weight: bold;
                margin: 5px 0;
            }}

            .disclaimer {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin-top: 20px;
                border-radius: 5px;
                font-size: 14px;
            }}

            .footer {{
                text-align: center;
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Reporte de Diagnóstico Médico</h1>
                <p>Sistema Experto de Apoyo al Diagnóstico</p>
            </div>

            <div class="info">
                <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                <p><strong>Método:</strong> {method}</p>
                <p><strong>Síntomas reportados:</strong> {len(symptoms)}</p>
            </div>

            <div class="section">
                <h2 class="section-title">Síntomas Reportados</h2>
                <ul class="symptoms-list">
    """

    for symptom in symptoms:
        safe_symptom = str(symptom).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html_content += f'<li>{safe_symptom}</li>'

    html_content += f"""
                </ul>
            </div>

            <div class="section">
                <h2 class="section-title">Resultados del Diagnóstico</h2>
    """

    n = min(top_n, len(results))
    for i, result in enumerate(results[:top_n], 1):
        confidence = result.get('final_confidence', result.get('confidence', 0)) * 100

        disease_name = str(result.get('disease', '')).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        category = str(result.get('category', 'No especificada')).replace('&', '&amp;').replace('<', '&lt;').replace(
            '>', '&gt;')
        severity = str(result.get('severity', 'No especificada')).replace('&', '&amp;').replace('<', '&lt;').replace(
            '>', '&gt;')

        html_content += f"""
                <div class="diagnosis-card">
                    <div class="diagnosis-header">
                        <h3 style="margin: 0;">{i}. {disease_name}</h3>
                        <span class="confidence">{confidence:.1f}%</span>
                    </div>
                    <p><strong>Categoría:</strong> {category}</p>
                    <p><strong>Severidad:</strong> {severity}</p>
        """

        if result.get('matched_symptoms'):
            html_content += f"""
                    <p><strong>Síntomas coincidentes ({len(result['matched_symptoms'])}):</strong></p>
                    <ul style="font-size: 14px; margin-top: 5px;">
            """
            for symptom in result['matched_symptoms'][:3]:
                safe_symptom = str(symptom).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_content += f'<li>{safe_symptom}</li>'

            if len(result['matched_symptoms']) > 3:
                html_content += f'<li>... y {len(result["matched_symptoms"]) - 3} más</li>'

            html_content += '</ul>'

        html_content += '</div>'

    html_content += f"""
            </div>

            <div class="section">
                <h2 class="section-title">Estadísticas</h2>
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">{len(results)}</div>
                        <div>Total diagnósticos</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{n}</div>
                        <div>Mostrados</div>
                    </div>
    """

    # Calcular categorías únicas
    categories = set()
    for r in results[:n]:
        cat = r.get('category')
        if cat:
            categories.add(str(cat))

    # Calcular condiciones graves
    severe_count = 0
    for r in results[:n]:
        severity = str(r.get('severity', '')).lower()
        if 'grave' in severity:
            severe_count += 1

    html_content += f"""
                    <div class="stat-item">
                        <div class="stat-value">{len(categories)}</div>
                        <div>Categorías</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{severe_count}</div>
                        <div>Condiciones graves</div>
                    </div>
                </div>
            </div>

            <div class="disclaimer">
                <p><strong>IMPORTANTE:</strong> Este reporte ha sido generado automáticamente por un sistema experto. Su propósito es únicamente educativo e informativo, y no constituye un diagnóstico médico profesional. Consulte siempre con un médico especialista.</p>
            </div>

            <div class="footer">
                <p>Sistema Experto de Diagnóstico Médico | Versión 1.0</p>
                <p>© {datetime.now().strftime('%Y')} - Fines educativos</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html_content.encode('utf-8')


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
        6. **Guarde** los diagnósticos importantes en el historial

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
                help="Cantidad de diagnósticos más probables a mostrar",
                key="top_n"
            )

        # Botón de diagnóstico
        st.markdown("---")
        if st.button("🔍 Realizar Diagnóstico", type="primary", use_container_width=True, key="run_diagnosis"):
            with st.spinner("🔄 Procesando diagnóstico..."):
                # Realizar diagnóstico
                results = diagnose(selected_symptoms, method)
                st.session_state.diagnosis_results = results
                st.session_state.diagnosis_method = method
                st.session_state.diagnosis_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Resetear estado PDF
                st.session_state.pdf_generated = False
                st.session_state.pdf_bytes = None
                st.session_state.show_pdf_section = True

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
                        avg_conf = sum(r.get('final_confidence', r.get('confidence', 0)) for r in results[:5]) / min(5,
                                                                                                                     len(results))
                        st.metric("Confianza Promedio (Top 5)", f"{avg_conf * 100:.1f}%")
                    with col3:
                        categories = set(r['category'] for r in results[:top_n])
                        st.metric("Categorías Afectadas", len(categories))
                    with col4:
                        severe_count = sum(1 for r in results[:top_n] if 'grave' in str(r.get('severity', '')).lower())
                        st.metric("Condiciones Graves", severe_count)

                else:
                    st.warning("⚠️ No se encontraron diagnósticos que coincidan con los síntomas seleccionados.")
                    st.info("💡 Intente agregar más síntomas o consulte directamente con un profesional de la salud.")
    else:
        st.warning("⚠️ Por favor, seleccione al menos un síntoma para continuar.")

        # Render persistente de resultados tras diagnóstico
    if st.session_state.get('diagnosis_results'):
        curr_top_n = st.session_state.get('top_n', 5)

        st.markdown("---")
        st.markdown("## 📊 Resultados del Diagnóstico")

        for i, result in enumerate(st.session_state.diagnosis_results[:curr_top_n], 1):
            display_diagnosis_result(result, i)

        st.markdown("---")
        st.markdown("### 📈 Estadísticas del Diagnóstico")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Diagnósticos", len(st.session_state.diagnosis_results))
        with col2:
            avg_conf = sum(
                r.get('final_confidence', r.get('confidence', 0))
                for r in st.session_state.diagnosis_results[:5]
            ) / min(5, len(st.session_state.diagnosis_results))
            st.metric("Confianza Promedio (Top 5)", f"{avg_conf * 100:.1f}%")
        with col3:
            categories = set(r['category'] for r in st.session_state.diagnosis_results[:curr_top_n])
            st.metric("Categorías Afectadas", len(categories))
        with col4:
            severe_count = sum(
                1 for r in st.session_state.diagnosis_results[:curr_top_n]
                if 'grave' in str(r.get('severity', '')).lower()
            )
            st.metric("Condiciones Graves", severe_count)

    # Sección PDF (solo se muestra si hay resultados)
    if st.session_state.get('show_pdf_section', False) and st.session_state.diagnosis_results:
        st.markdown("---")
        st.markdown("### 📄 Reporte de Diagnóstico")

        # Generar PDF si aún no se ha generado
        if not st.session_state.pdf_generated:
            with st.spinner("Generando reporte PDF..."):
                try:
                    pdf_bytes = build_pdf_report(
                        st.session_state.selected_symptoms,
                        st.session_state.diagnosis_results,
                        st.session_state.diagnosis_method,
                        top_n=top_n
                    )
                    if pdf_bytes and len(pdf_bytes) > 100:  # Verificar que no esté vacío
                        safe_bytes = convert_to_bytes(pdf_bytes)
                        st.session_state.pdf_bytes = safe_bytes
                        st.session_state.pdf_generated = True
                        st.session_state.pdf_filename = f"diagnostico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        st.success("✅ PDF generado correctamente!")
                    else:
                        # Si el PDF está vacío o corrupto, generar uno simple
                        pdf_bytes = create_simple_fallback_pdf(
                            st.session_state.selected_symptoms,
                            st.session_state.diagnosis_results,
                            st.session_state.diagnosis_method
                        )
                        safe_bytes = convert_to_bytes(pdf_bytes)
                        st.session_state.pdf_bytes = safe_bytes
                        st.session_state.pdf_generated = True
                        st.session_state.pdf_filename = f"diagnostico_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        st.info("📄 Se generó un PDF simple")
                except Exception as e:
                    st.error(f"❌ Error crítico: {str(e)}")
                    # Último intento con PDF mínimo
                    pdf_bytes = create_simple_fallback_pdf(
                        st.session_state.selected_symptoms,
                        st.session_state.diagnosis_results,
                        st.session_state.diagnosis_method
                    )
                    safe_bytes = convert_to_bytes(pdf_bytes)
                    st.session_state.pdf_bytes = safe_bytes
                    st.session_state.pdf_generated = True
                    st.session_state.pdf_filename = f"diagnostico_minimo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    st.warning("⚠️ Se generó un PDF mínimo debido a errores")

        # Mostrar opciones de PDF
        if st.session_state.pdf_generated and st.session_state.pdf_bytes:
            col1, col2 = st.columns([1, 1])

            with col1:
                # Botón para regenerar
                if st.button("🔄 Regenerar PDF", use_container_width=True, key="regenerate_pdf"):
                    with st.spinner("Regenerando PDF..."):
                        try:
                            pdf_bytes = build_pdf_report(
                                st.session_state.selected_symptoms,
                                st.session_state.diagnosis_results,
                                st.session_state.diagnosis_method,
                                top_n=top_n
                            )
                            if pdf_bytes:
                                safe_bytes = convert_to_bytes(pdf_bytes)
                                st.session_state.pdf_bytes = safe_bytes
                                st.session_state.pdf_filename = f"diagnostico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                                st.success("✅ PDF regenerado correctamente!")
                        except:
                            st.error("❌ No se pudo regenerar el PDF")

            with col2:
                # Botón de descarga
                safe_bytes = convert_to_bytes(st.session_state.pdf_bytes)
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=safe_bytes,
                    file_name=st.session_state.pdf_filename,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                    key="download_pdf_main"
                )

            # Opciones alternativas
            st.markdown("---")
            with st.expander("🌐 Otras opciones de exportación", expanded=False):
                col_alt1, col_alt2 = st.columns(2)

                with col_alt1:
                    # Reporte HTML
                    try:
                        html_report = generate_html_report(
                            st.session_state.selected_symptoms,
                            st.session_state.diagnosis_results,
                            st.session_state.diagnosis_method,
                            top_n=top_n
                        )
                        st.download_button(
                            "📊 Descargar HTML",
                            data=html_report,
                            file_name=f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True,
                            key="download_html"
                        )
                    except Exception as e:
                        st.error(f"Error HTML: {str(e)}")

                with col_alt2:
                    # Limpiar sección PDF
                    if st.button("🗑️ Ocultar sección PDF", use_container_width=True, key="hide_pdf"):
                        st.session_state.show_pdf_section = False
        else:
            if not st.session_state.pdf_generated:
                st.warning("⚠️ El PDF no se ha generado. Intente nuevamente.")

    # ============================================
    # SECCIÓN DE CONFIRMACIÓN DE GUARDADO EN HISTORIAL
    # ============================================

    # Solo mostrar si hay diagnósticos pendientes de guardar
    if st.session_state.get('save_confirmed', False) and st.session_state.pending_saves:
        st.markdown("---")
        st.markdown("### 💾 Confirmar Guardado en Historial")
        st.markdown("Los siguientes diagnósticos están listos para guardar:")

        # Mostrar lista de diagnósticos pendientes
        for i, pending in enumerate(st.session_state.pending_saves, 1):
            st.info(f"**{i}.** {pending['disease']} - {pending['confidence'] * 100:.1f}% de confianza")

        # Botones de confirmación
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirmar y Guardar Todo", type="primary", key="confirm_save_all"):
                saved_count = 0
                for pending in st.session_state.pending_saves:
                    # Verificar si ya existe en el historial
                    already_exists = False
                    for existing in st.session_state.diagnosis_history:
                        if (existing['disease'] == pending['disease'] and
                                abs(existing['confidence'] - pending['confidence']) < 0.01):
                            already_exists = True
                            break

                    if not already_exists:
                        st.session_state.last_diagnosis_id += 1
                        st.session_state.diagnosis_history.append({
                            'id': st.session_state.last_diagnosis_id,
                            **pending,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        saved_count += 1

                st.success(f"✅ {saved_count} diagnóstico(s) guardado(s) en el historial!")

                # Limpiar pendientes
                st.session_state.pending_saves = []
                st.session_state.save_confirmed = False

                # Pequeña pausa y actualizar
                time.sleep(1)
                st.rerun()

        with col2:
            if st.button("❌ Cancelar", key="cancel_save_all"):
                st.session_state.pending_saves = []
                st.session_state.save_confirmed = False
                st.info("❌ Guardado cancelado")
                st.rerun()

        st.markdown("---")
        # Mostrar mensaje si se acaba de guardar algo
        if st.session_state.get('just_saved', False):
            st.success("🎉 **¡Diagnóstico guardado exitosamente!** Ve a la página de 📜 Historial para verlo.")
            st.session_state.just_saved = False

        # Mostrar botón para guardar todos si hay muchos pendientes
        pending_count = len(st.session_state.save_requested)
        if pending_count > 0:
            st.markdown("---")
            st.markdown(f"### 💾 Tienes {pending_count} diagnóstico(s) pendiente(s)")

            # Mostrar lista de pendientes
            for uid, request in st.session_state.save_requested.items():
                disease = request['disease']
                confidence = request['confidence'] * 100
                st.info(f"• **{disease}** - {confidence:.1f}% de confianza")

            col_save_all, col_cancel_all = st.columns(2)

            with col_save_all:
                if st.button("💾 **Guardar Todos**", type="primary", use_container_width=True, key="save_all_button"):
                    saved_count = 0
                    for uid, request in list(st.session_state.save_requested.items()):
                        # Verificar que no exista ya
                        exists = any(
                            h['disease'] == request['disease'] and
                            abs(h['confidence'] - request['confidence']) < 0.01
                            for h in st.session_state.diagnosis_history
                        )

                        if not exists:
                            st.session_state.last_diagnosis_id += 1
                            st.session_state.diagnosis_history.append({
                                'id': st.session_state.last_diagnosis_id,
                                'disease': request['disease'],
                                'confidence': request['confidence'],
                                'symptoms': request['data']['matched_symptoms'],
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'category': request['data'].get('category', 'N/A'),
                                'severity': request['data'].get('severity', 'N/A'),
                                'description': request['data'].get('description', ''),
                                'rank': request['rank']
                            })
                            saved_count += 1

                        # Eliminar de pendientes
                        del st.session_state.save_requested[uid]

                    st.session_state.just_saved = True
                    st.success(f"✅ **{saved_count} diagnóstico(s) guardado(s)**")
                    time.sleep(1)
                    st.rerun()

            with col_cancel_all:
                if st.button("🗑️ **Cancelar Todos**", type="secondary", use_container_width=True,
                             key="cancel_all_button"):
                    st.session_state.save_requested = {}
                    st.info("❌ **Todos los pendientes cancelados**")
                    time.sleep(1)
                    st.rerun()

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
    """Página de historial - VERSIÓN SIMPLIFICADA Y CONFIABLE"""

    import time  #

    st.markdown("## 📜 Historial de Diagnósticos")


    # Botón para actualizar
    if st.button("🔄 Actualizar", key="refresh_history"):
        st.rerun()

    # Mostrar estadísticas
    history_count = len(st.session_state.diagnosis_history)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total guardados", history_count)
    with col2:
        if history_count > 0:
            avg_conf = sum(h['confidence'] for h in st.session_state.diagnosis_history) / history_count
            st.metric("Confianza promedio", f"{avg_conf * 100:.1f}%")
        else:
            st.metric("Confianza promedio", "0%")
    with col3:
        if history_count > 0:
            unique_diseases = len(set(h['disease'] for h in st.session_state.diagnosis_history))
            st.metric("Enfermedades únicas", unique_diseases)
        else:
            st.metric("Enfermedades únicas", 0)

    st.markdown("---")

    if history_count == 0:
        st.info("📭 **No hay diagnósticos guardados en el historial**")
        st.markdown("""
        ### Cómo guardar diagnósticos:

        1. **Realice un diagnóstico** en la página 🏠 Inicio
        2. **Haga clic en "📌 Guardar en Historial"** en cualquier resultado
        3. **Confirme el guardado** cuando se le pregunte
        4. Los diagnósticos guardados **aparecerán aquí automáticamente**
        """)
        return

    st.success(f"✅ **{history_count} diagnóstico(s) guardado(s)**")

    # Filtros simples
    search_term = st.text_input("🔍 Buscar por nombre de enfermedad:",
                                placeholder="Ej: Gripe, Neumonía...",
                                key="history_search")

    # Filtrar historial
    filtered_history = st.session_state.diagnosis_history

    if search_term:
        filtered_history = [
            h for h in filtered_history
            if search_term.lower() in h['disease'].lower()
        ]

    if not filtered_history:
        st.warning("⚠️ **No hay diagnósticos que coincidan con la búsqueda**")
        return

    # Mostrar historial (ordenado por fecha más reciente primero)
    st.markdown(f"**Mostrando {len(filtered_history)} de {history_count} diagnósticos:**")

    # Ordenar por ID (más reciente primero)
    for item in sorted(filtered_history, key=lambda x: x.get('id', 0), reverse=True):
        with st.expander(f"#{item.get('id', '?')} - {item['disease']} ({item['confidence'] * 100:.1f}%)",
                         expanded=False):
            col_left, col_right = st.columns([3, 1])

            with col_left:
                st.markdown(f"**Enfermedad:** {item['disease']}")
                st.markdown(f"**Confianza:** {item['confidence'] * 100:.1f}%")
                st.markdown(f"**Fecha:** {item.get('timestamp', 'No registrada')}")
                st.markdown(f"**Categoría:** {item.get('category', 'N/A')}")
                st.markdown(f"**Severidad:** {item.get('severity', 'N/A')}")

                if item.get('description'):
                    st.markdown("---")
                    st.markdown(f"**Descripción:** {item.get('description')}")

                if item.get('symptoms'):
                    st.markdown("---")
                    st.markdown(f"**Síntomas coincidentes ({len(item['symptoms'])}):**")
                    for symptom in item['symptoms'][:3]:
                        st.markdown(f"✓ {symptom}")
                    if len(item['symptoms']) > 3:
                        st.markdown(f"*... y {len(item['symptoms']) - 3} más*")

            with col_right:
                # Barra de progreso visual
                st.progress(item['confidence'])

                # Botón para eliminar
                delete_key = f"delete_{item.get('id', 0)}_{int(datetime.now().timestamp())}"
                if st.button("🗑️ Eliminar", key=delete_key, use_container_width=True):
                    # Eliminar del historial
                    st.session_state.diagnosis_history = [
                        h for h in st.session_state.diagnosis_history
                        if h.get('id') != item.get('id')
                    ]
                    st.success("✅ Diagnóstico eliminado")
                    time.sleep(1)
                    st.rerun()

    # Botón para limpiar todo
    st.markdown("---")
    if st.button("🗑️ **Limpiar Todo el Historial**", type="secondary", use_container_width=True):
        st.session_state.diagnosis_history = []
        st.success("✅ Historial limpiado completamente")
        time.sleep(1)
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

        # Mostrar estadísticas del historial en sidebar
        st.markdown("---")
        st.markdown("### 📜 Historial")
        st.metric("Diagnósticos guardados", len(st.session_state.diagnosis_history))

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