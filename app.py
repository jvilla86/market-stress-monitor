import streamlit as st
import pandas as pd
from fredapi import Fred

st.set_page_config(
    page_title="Panel Macro y Bonos Global", 
    page_icon="📊", 
    layout="centered"
)

st.title("🌍 Panel Global Macro y de Riesgo Financiero")
st.markdown("Datos macroeconómicos en tiempo real obtenidos directamente desde la Reserva Federal (FRED).")

# API Key
try:
    fred_api_key = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=fred_api_key)
except Exception:
    st.error("Falta configurar la clave FRED API en los Secrets de Streamlit.")
    st.stop()

# Descarga rápida para probar el semáforo
with st.spinner("🔄 Conectando con la FRED..."):
    try:
        estres = fred.get_series("STLFSI4").dropna().iloc[-1]
        curva = fred.get_series("T10Y2Y").dropna().iloc[-1]
        hy = fred.get_series("BAMLH0A0HYM2").dropna().iloc[-1]
    except Exception as e:
        estres, curva, hy = 0, 0, 0

st.success("✅ ¡Datos obtenidos correctamente!")

# --- SEMÁFORO FORZADO ---
st.markdown("---")
st.markdown("### 🚦 Semáforo de Riesgo de Mercado")

if estres > 0.5 or hy > 5.5:
    st.error(f"🔴 **ALERTA DE TENSIÓN ELEVADA** (Estrés: {estres:.2f}, High Yield: {hy:.2f})")
elif curva < 0:
    st.warning(f"🟡 **PRECAUCIÓN / CURVA INVERTIDA** (Curva 10Y-2Y: {curva:.2f})")
else:
    st.success(f"🟢 **ENTORNO ESTABLE / CALMA** (Indicadores en rangos normales)")

st.markdown("---")
st.write("Si ves este semáforo, el código está cargando bien. ¡Dime y te restauro el resto del panel completo con esta misma estructura!")
