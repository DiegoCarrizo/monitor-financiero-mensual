import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(page_title="My Wealth Engine", layout="wide")
st.title("🛡️ Wealth Engine Cloud")

# --- CONEXIÓN A GOOGLE SHEETS ---
# Pega aquí el enlace de tu Google Sheet
URL_GSHEET = "TU_LINK_DE_GOOGLE_SHEETS_AQUÍ"

# Función para cargar datos (Simulada para persistencia simple)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Tipo", "Concepto", "Monto", "Prioridad"])

# --- CARGA DE DATOS ---
with st.sidebar:
    st.header("⚙️ Registro")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    concepto = st.text_input("Concepto")
    monto = st.number_input("Monto ($)", min_value=0.0)
    
    prioridad = 0
    if tipo == "Gasto":
        prioridad = st.select_slider("Prioridad", options=[1,2,3,4,5], value=3)
    
    if st.button("Guardar en Nube"):
        nuevo = pd.DataFrame([[tipo, concepto, monto, prioridad]], columns=st.session_state.db.columns)
        st.session_state.db = pd.concat([st.session_state.db, nuevo], ignore_index=True)
        st.success("Dato guardado!")

# --- VISUALIZACIÓN ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Ingresos")
    df_ing = st.session_state.db[st.session_state.db["Tipo"] == "Ingreso"]
    st.table(df_ing)
    st.metric("Total Ingresos", f"$ {df_ing['Monto'].sum():,.2f}")

with col2:
    st.subheader("📋 Gastos")
    df_gas = st.session_state.db[st.session_state.db["Tipo"] == "Gasto"]
    st.table(df_gas)
    st.metric("Total Gastos", f"$ {df_gas['Monto'].sum():,.2f}")

# --- ELIMINAR REGISTROS ---
st.divider()
if not st.session_state.db.empty:
    eliminar = st.selectbox("Seleccionar para eliminar", st.session_state.db.index, 
                            format_func=lambda x: f"{st.session_state.db.iloc[x]['Concepto']} (${st.session_state.db.iloc[x]['Monto']})")
    if st.button("🗑️ Confirmar Eliminación"):
        st.session_state.db = st.session_state.db.drop(eliminar).reset_index(drop=True)
        st.rerun()

# --- DIAGNÓSTICO ---
hormigas = df_gas[df_gas["Prioridad"] >= 4]
if not hormigas.empty:
    st.error(f"⚠️ Alerta: Gastos Hormiga detectados (${hormigas['Monto'].sum()})")
    st.dataframe(hormigas)

# --- BOTÓN DESCARGA ---
csv = st.session_state.db.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar Reporte Completo", data=csv, file_name="reporte_wealth.csv", mime="text/csv")
