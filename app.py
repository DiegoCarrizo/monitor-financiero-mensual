import streamlit as st
import pandas as pd

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="My Wealth Engine", layout="wide")

st.title("🛡️ Wealth Engine: Monitor de Capital")
st.markdown("---")

# USAMOS SESSION_STATE PARA QUE LOS DATOS NO SE BORREN AL TOCAR BOTONES
if 'gastos' not in st.session_state:
    st.session_state.gastos = pd.DataFrame(columns=["Fecha", "Concepto", "Monto", "Prioridad"])
if 'ingresos' not in st.session_state:
    st.session_state.ingresos = pd.DataFrame(columns=["Fecha", "Concepto", "Monto"])

# COLUMNAS PARA CARGA DE DATOS
col_ing, col_gas = st.columns(2)

with col_ing:
    with st.expander("💰 Cargar Ingreso", expanded=True):
        concepto_i = st.text_input("Origen del ingreso", key="ing_con")
        monto_i = st.number_input("Monto ($)", min_value=0.0, key="ing_mon")
        if st.button("Registrar Ingreso"):
            nuevo_i = pd.DataFrame([[pd.Timestamp.now(), concepto_i, monto_i]], 
                                   columns=st.session_state.ingresos.columns)
            st.session_state.ingresos = pd.concat([st.session_state.ingresos, nuevo_i], ignore_index=True)
            st.success("Ingreso registrado")

with col_gas:
    with st.expander("📉 Cargar Gasto", expanded=True):
        concepto_g = st.text_input("¿En qué gastaste?", key="gas_con")
        monto_g = st.number_input("Monto ($)", min_value=0.0, key="gas_mon")
        prioridad = st.select_slider("Prioridad (1=Vital | 5=Gasto Hormiga)", options=[1,2,3,4,5], value=3)
        if st.button("Registrar Gasto"):
            nuevo_g = pd.DataFrame([[pd.Timestamp.now(), concepto_g, monto_g, prioridad]], 
                                   columns=st.session_state.gastos.columns)
            st.session_state.gastos = pd.concat([st.session_state.gastos, nuevo_g], ignore_index=True)
            st.success("Gasto registrado")

st.markdown("---")

# SECCIÓN DE TABLAS Y ANÁLISIS
c1, c2 = st.columns(2)

with c1:
    st.subheader("📋 Detalle de Ingresos")
    st.dataframe(st.session_state.ingresos, use_container_width=True)
    total_i = st.session_state.ingresos["Monto"].sum()
    st.metric("Total Ingresos", f"$ {total_i:,.2f}")

with c2:
    st.subheader("📋 Detalle de Gastos")
    st.dataframe(st.session_state.gastos, use_container_width=True)
    total_g = st.session_state.gastos["Monto"].sum()
    st.metric("Total Gastos", f"$ {total_g:,.2f}", delta=f"-{total_g:,.2f}", delta_color="inverse")

st.markdown("---")

# MOTOR DE DETECCIÓN DE GASTOS HORMIGA
st.subheader("🔍 Diagnóstico de Salud Financiera")

# Filtramos los gastos con prioridad 4 y 5
hormigas = st.session_state.gastos[st.session_state.gastos["Prioridad"] >= 4]
ahorro_potencial = hormigas["Monto"].sum()

if ahorro_potencial > 0:
    st.error(f"⚠️ Se detectaron **Gastos Hormiga** por un total de: **$ {ahorro_potencial:,.2f}**")
    st.write("Sugerencia: Estos gastos son prescindibles. Eliminarlos mejoraría tu capacidad de ahorro mensual de inmediato.")
    st.table(hormigas[["Concepto", "Monto"]])
else:
    st.success("✅ No se detectaron gastos innecesarios de alta prioridad. ¡Tus cuentas están optimizadas!")

# SALDO FINAL
saldo = total_i - total_g
st.divider()
st.header(f"Saldo Neto Mensual: $ {saldo:,.2f}")
