"""
Módulo: Gestión de Síntomas
Responsable: Luis (Integrante 1)

Descripción:
    - Define el listado oficial de síntomas del sistema desde un dataset
    - Implementa la interfaz de captura de síntomas del usuario
    - Valida la entrada (mínimo 1 síntoma seleccionado)

Funcionalidades:
    - Carga de síntomas desde data/symptoms_list.csv
    - Interfaz Streamlit con checkboxes por categoría
    - Visualización de síntomas seleccionados
"""

import streamlit as st
import pandas as pd
import os

# ====================================
# CARGA DE SÍNTOMAS DESDE DATASET
# ====================================

def load_symptoms_from_dataset():
    """Carga los síntomas desde el dataset CSV."""
    # Ruta al archivo de dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "symptoms_list.csv")
    
    try:
        # Leer el dataset
        df = pd.read_csv(dataset_path)
        
        # Verificar que las columnas necesarias existan
        if 'categoria' not in df.columns or 'sintoma' not in df.columns:
            raise ValueError("El dataset debe tener columnas 'categoria' y 'sintoma'")
        
        # Crear diccionario con emojis
        symptoms_dict = {}
        for _, row in df.iterrows():
            categoria = str(row['categoria']).strip()
            sintoma = str(row['sintoma']).strip()
            
            # Asignar emoji según categoría
            if "Generales" in categoria:
                key = f"🌡️ {categoria}"
            elif "Respiratorios" in categoria:
                key = f"🫁 {categoria}"
            elif "Digestivos" in categoria:
                key = f"🤢 {categoria}"
            elif "Neurológicos" in categoria:
                key = f"🧠 {categoria}"
            elif "Cardiovasculares" in categoria:
                key = f"❤️ {categoria}"
            elif "Dermatológicos" in categoria:
                key = f"🧴 {categoria}"
            else:
                key = f"📋 {categoria}"
            
            if key not in symptoms_dict:
                symptoms_dict[key] = []
            symptoms_dict[key].append(sintoma)
        
        return symptoms_dict
        
    except FileNotFoundError:
        st.error("❌ Dataset no encontrado: data/symptoms_list.csv")
        st.info("Por favor, asegúrese de que el archivo de dataset exista en la carpeta 'data'.")
        return {}
    except Exception as e:
        st.error(f"❌ Error al cargar el dataset: {str(e)}")
        return {}


def get_all_symptoms():
    """Retorna el listado completo de síntomas desde el dataset."""
    return load_symptoms_from_dataset()


def get_all_symptoms_flat():
    """Retorna todos los síntomas en una lista plana."""
    symptoms_dict = get_all_symptoms()
    all_symptoms = []
    for symptoms in symptoms_dict.values():
        all_symptoms.extend(symptoms)
    return sorted(all_symptoms)


# ====================================
# INTERFAZ DE CAPTURA
# ====================================

def render_symptom_selector():
    """Renderiza la interfaz de selección de síntomas."""
    st.markdown("### 🩺 Seleccione uno o más síntomas que esté experimentando:")
    
    symptoms_dict = get_all_symptoms()
    if not symptoms_dict:
        st.warning("No hay síntomas disponibles. Verifique el dataset.")
        return []
    
    selected_symptoms = []
    
    for category, symptoms in symptoms_dict.items():
        with st.expander(category, expanded=False):  
            cols = st.columns(2)
            for idx, symptom in enumerate(sorted(symptoms)):  
                col = cols[idx % 2]
                if col.checkbox(symptom, key=f"symptom_{category}_{symptom}"):
                    selected_symptoms.append(symptom)
    
    return selected_symptoms


def validate_symptoms(selected_symptoms):
    """Valida que se haya seleccionado al menos un síntoma."""
    return len(selected_symptoms) > 0


# ====================================
# VISUALIZACIÓN
# ====================================

def display_selected_symptoms(selected_symptoms):
    """Muestra los síntomas seleccionados con resumen."""
    if not selected_symptoms:
        st.warning("Seleccione al menos un síntoma.")
        return

    symptoms_dict = get_all_symptoms()
    if not symptoms_dict:
        return

    # Calcular categorías afectadas
    category_counts = {}
    for category, symptoms in symptoms_dict.items():
        count = len([s for s in selected_symptoms if s in symptoms])
        if count > 0:
            category_counts[category] = count

    total = len(selected_symptoms)
    severity, emoji = (
        ("Alta", "❗") if total >= 5 else
        ("Media", "⚠️") if total >= 3 else
        ("Baja", "✅")
    )

    # 🎨 COLORES ADAPTADOS AL TEMA OSCURO
    card_bg = "#4a6fa5"
    text_color = "white"
    border_color = "#3a5a7e"

    # === TÍTULO ===
    st.markdown("### ✅ Resumen de síntomas")

    # === CARDS POR CATEGORÍA ===
    for category, symptoms in symptoms_dict.items():
        category_symptoms = [s for s in selected_symptoms if s in symptoms]
        if not category_symptoms:
            continue

        emoji_cat = category.split()[0]
        cat_name = " ".join(category.split()[1:])

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
            border: 2px solid {card_bg};
        ">
            <h4 style="
                display: flex;
                align-items: center;
                gap: 10px;
                color: #2c3e50;
            ">
                <span style="font-size: 24px;">{emoji_cat}</span>
                <span>{cat_name}</span>
                <span style="
                    margin-left: auto;
                    background: {card_bg};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                ">
                    {len(category_symptoms)} síntoma{"s" if len(category_symptoms) > 1 else ""}
                </span>
            </h4>
        </div>
        """, unsafe_allow_html=True)

        for symptom in sorted(category_symptoms):
            st.markdown(f"""
            <div style="
                background: #f0f2f5;
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 8px;
                border-left: 4px solid {card_bg};
                box-shadow: 0 2px 4px rgba(0,0,0,0.08);
                font-size: 14px;
                font-weight: 500;
                color: #2c3e50;
            ">
                <span style="color: {card_bg}; margin-right: 8px;">✓</span>
                {symptom}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # === CARDS DE RESUMEN ===
    col1, col2, col3 = st.columns(3)
    for col, title, value in [
        (col1, "Total de síntomas", total),
        (col2, "Categorías afectadas", len(category_counts)),
        (col3, "Nivel de severidad", f"{emoji} {severity}")
    ]:
        with col:
            st.markdown(f"""
            <div style="
                background: {card_bg};
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                border: 1px solid {border_color};
                color: {text_color};
                font-weight: bold;
            ">
                <div style="font-size: 22px; margin-bottom: 8px;">{title}</div>
                <div style="font-size: 32px;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ====================================
# MAIN
# ====================================

def main():
    """Función principal para pruebas independientes."""
    st.set_page_config(
        page_title="Gestión de Síntomas",
        page_icon="🩺",
        layout="wide"
    )

    st.title("🩺 Gestión de Síntomas")
    st.info("Seleccione los síntomas para el diagnóstico. Los datos se cargan desde el dataset.")

    selected = render_symptom_selector()
    st.markdown("---")

    if validate_symptoms(selected):
        st.session_state["selected_symptoms"] = selected
        display_selected_symptoms(selected)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Continuar al diagnóstico", type="primary"):
            st.success("Síntomas guardados correctamente")
            st.balloons()

        if st.button("🔄 Limpiar selección"):
            for k in list(st.session_state.keys()):
                if k.startswith("symptom_") or k == "selected_symptoms":
                    del st.session_state[k]
            st.rerun()
    else:
        st.warning("Seleccione al menos un síntoma para continuar.")


if __name__ == "__main__":
    main()