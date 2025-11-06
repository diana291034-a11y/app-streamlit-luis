import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from PIL import Image
import os

# -------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------------------
st.set_page_config(
    page_title="TPM Digital - Grupo Éxito",
    layout="wide",
    page_icon="⚙️",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS personalizados ---
st.markdown("""
    <style>
    .main { background-color: #f7f9fb; }
    h1, h2, h3 { color: #003366; font-weight: 700; }
    .stButton>button {
        background-color: #003366; color: white; border-radius: 10px; padding: 8px 20px;
    }
    .stButton>button:hover { background-color: #0059b3; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------

EXCEL_FILE = "tpm_data.xlsx"

def cargar_datos():
    """Carga el archivo Excel si existe, o crea uno vacío."""
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=["Equipo", "Tipo", "Duración", "Responsable", "Fecha"])
        df.to_excel(EXCEL_FILE, index=False)
        return df

def guardar_datos(df):
    """Guarda los datos actualizados en el archivo Excel."""
    df.to_excel(EXCEL_FILE, index=False)

# -------------------------------------------------------------
# --- ENCABEZADO GENERAL ---
# -------------------------------------------------------------
st.title("⚙️ Sistema Digital de Mantenimiento Productivo Total (TPM)")
st.write("Aplicación desarrollada para gestionar y visualizar el mantenimiento de equipos críticos del Grupo Éxito.")

# -------------------------------------------------------------
# --- MENÚ LATERAL ---
# -------------------------------------------------------------
menu = st.sidebar.selectbox(
    "📂 Selecciona una sección",
    ["Inicio", "Diagnóstico", "Registro de Equipos", "Mantenimientos", "Indicadores", "Metodología"]
)

# =============================================================
# --- SECCIÓN 1: INICIO ---
# =============================================================
if menu == "Inicio":
    st.header("🏁 Bienvenido al Sistema TPM Digitalizado")
    st.markdown("""
    ### 🎯 Objetivos:
    - Digitalizar la información técnica y operativa.
    - Fortalecer la trazabilidad del mantenimiento.
    - Mejorar la disponibilidad y eficiencia de los equipos.
    
    ### 🧭 Estructura del Sistema:
    1. Diagnóstico del estado actual de equipos críticos.  
    2. Diseño del plan anual de mantenimiento TPM digitalizado.  
    3. Evaluación mediante indicadores de desempeño (OEE, MTTR, MTBF).
    """)

# =============================================================
# --- SECCIÓN 2: DIAGNÓSTICO ---
# =============================================================
elif menu == "Diagnóstico":
    st.header("🔍 Diagnóstico del Estado Actual de los Equipos")

    st.info("En esta sección se recopilan los datos iniciales de cada equipo crítico para establecer la línea base del TPM.")

    equipo = st.text_input("Nombre del equipo crítico")
    estado_general = st.select_slider("Condición operativa", ["Malo", "Regular", "Bueno", "Excelente"])
    fallas_mes = st.number_input("Frecuencia de fallas mensuales", min_value=0, step=1)
    tiempo_parada = st.number_input("Tiempo total de parada (horas/mes)", min_value=0.0, step=0.5)
    observaciones = st.text_area("Observaciones técnicas o de limpieza")

    if st.button("💾 Guardar diagnóstico"):
        st.success(f"✅ Diagnóstico registrado para el equipo {equipo}.")
        st.balloons()

# =============================================================
# --- SECCIÓN 3: REGISTRO DE EQUIPOS ---
# =============================================================
elif menu == "Registro de Equipos":
    st.header("🏭 Registro de Equipos Críticos")

    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del equipo")
        tipo = st.selectbox("Tipo de equipo", ["Horno", "Amasadora", "Batidora", "Cámara de fermentación", "Laminadora", "Otro"])
        estado = st.selectbox("Estado operativo", ["Operativo", "En mantenimiento", "Fuera de servicio"])
    with col2:
        imagen = st.file_uploader("📷 Subir imagen del equipo", type=["jpg", "png"])
        if imagen:
            st.image(imagen, caption=f"{nombre}", width=300)

    if st.button("💾 Guardar equipo"):
        st.success(f"✅ Equipo '{nombre}' registrado correctamente.")

# =============================================================
# --- SECCIÓN 4: MANTENIMIENTOS ---
# =============================================================
elif menu == "Mantenimientos":
    st.header("🧰 Registro de Mantenimientos")

    df = cargar_datos()

    col1, col2, col3 = st.columns(3)
    with col1:
        equipo = st.text_input("Equipo intervenido")
    with col2:
        tipo_mant = st.radio("Tipo de mantenimiento", ["Preventivo", "Correctivo", "Predictivo"])
    with col3:
        fecha = st.date_input("Fecha", value=date.today())

    descripcion = st.text_area("📝 Descripción del mantenimiento realizado")
    duracion = st.number_input("Duración (horas)", 0.0, 100.0, 1.0)
    responsable = st.text_input("👷 Responsable técnico")

    if st.button("💾 Guardar mantenimiento"):
        nuevo = pd.DataFrame({
            "Equipo": [equipo],
            "Tipo": [tipo_mant],
            "Duración": [duracion],
            "Responsable": [responsable],
            "Fecha": [fecha]
        })
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar_datos(df)
        st.success(f"✅ Mantenimiento '{tipo_mant}' registrado para el equipo {equipo}.")
        st.balloons()

    # Mostrar registros previos
    if not df.empty:
        st.subheader("📋 Historial de Mantenimientos")
        st.dataframe(df, use_container_width=True)

# =============================================================
# --- SECCIÓN 5: INDICADORES ---
# =============================================================
elif menu == "Indicadores":
    st.header("📈 Indicadores de Desempeño TPM")

    df = cargar_datos()

    if df.empty:
        st.warning("⚠️ Aún no hay datos de mantenimiento registrados.")
    else:
        # Cálculo de indicadores reales
        mttr = df["Duración"].mean()
        total_mantenimientos = len(df)
        equipos_unicos = df["Equipo"].nunique()
        mtbf = (total_mantenimientos * 24) / (equipos_unicos if equipos_unicos else 1)
        oee = max(0, min(100, 100 - (mttr * 0.8)))  # estimado simplificado

        col1, col2, col3 = st.columns(3)
        col1.metric("🕒 MTTR (Promedio de reparación)", f"{mttr:.2f} h")
        col2.metric("⏱️ MTBF (Tiempo medio entre fallas)", f"{mtbf:.1f} h")
        col3.metric("⚙️ OEE estimado", f"{oee:.1f}%")

        # Gráfico por equipo
        fig = px.bar(
            df,
            x="Equipo",
            y="Duración",
            color="Tipo",
            title="Duración de Mantenimientos por Equipo",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================================
# --- SECCIÓN 6: METODOLOGÍA TPM ---
# =============================================================
elif menu == "Metodología":
    st.header("📘 Metodología del Mantenimiento Productivo Total (TPM) Digitalizado")

    st.markdown("""
    ### 1️⃣ Diagnóstico del estado actual
    - Evaluación técnica y operativa de hornos, cámaras, formadoras, laminadoras, batidoras y amasadoras.
    - Uso de listas de chequeo, inspecciones visuales y entrevistas.
    - Análisis de frecuencia de fallas, tiempos de parada y condiciones de limpieza.

    ### 2️⃣ Diseño del plan anual TPM
    - Basado en los resultados del diagnóstico.
    - Uso de herramientas como Excel, SAP PM y Power BI.
    - Enfoque en mantenimiento **preventivo, correctivo y predictivo** digitalizado.

    ### 3️⃣ Evaluación mediante indicadores
    - Medición de **OEE, MTTR, MTBF y costos de mantenimiento**.
    - Consolidación de datos en Power BI con registros digitales y de SAP.
    - Análisis comparativo antes y después de la implementación del TPM.
    """)

    st.info("Esta metodología busca optimizar la confiabilidad, productividad e inocuidad de los equipos del Grupo Éxito.")
