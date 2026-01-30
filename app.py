import streamlit as st
import pandas as pd

# Título de tu propia App
st.title("🛡️ Wealth Engine: Mi Monitor")
st.subheader("Proyecto independiente de control de capital")

# Formulario para anotar gastos
with st.form("registro"):
    concepto = st.text_input("¿En qué gastaste?")
    monto = st.number_input("¿Cuánto? ($)", min_value=0.0)
    prioridad = st.select_slider("Prioridad (1=Vital, 5=Eliminable)", options=[1,2,3,4,5])
    
    if st.form_submit_button("Registrar Gasto"):
        st.success(f"Guardado: {concepto} por ${monto}")

st.info("💡 Este es tu espacio privado para analizar tus cuentas.")
