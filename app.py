import streamlit as st
import pandas as pd
from fredapi import Fred

# Configuración de la página web
st.set_page_config(page_title="Panel Macro y Bonos", page_icon="📊", layout="centered")

st.title("🌍 Panel Global Macro y de Riesgo Financiero")
st.markdown("Datos en tiempo real obtenidos desde la Reserva Federal (FRED).")

# Obtenemos la API Key de los secretos de Streamlit (para que sea seguro)
try:
    fred_api_key = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=fred_api_key)
except Exception:
    st.error("Falta configurar la clave FRED API en los Secrets de Streamlit.")
    st.stop()

series_dict = {
    "High Yield General (OAS)": "BAMLH0A0HYM2",
    "Segmento CCC (Riesgo Alto)": "BAMLH0A3HYC",
    "Tipos Reales 10Y (EE.UU.)": "DFII10",
    "Índice de Estrés Financiero": "STLFSI4",
    "Curva de Tipos (10Y - 2Y)": "T10Y2Y",
    "Expectativas de Inflación (10Y)": "T10YIE"
}

valores_obtenidos = {}

for nombre, codigo in series_dict.items():
    try:
        data = fred.get_series(codigo).dropna()
        ultimo = data.iloc[-1]
        anterior = data.iloc[-2]
        var = ultimo - anterior
        valores_obtenidos[nombre] = ultimo

        # Mostramos cada indicador en una tarjeta visual de Streamlit
        st.subheader(f"🔹 {nombre}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Valor Actual", f"{ultimo:.2f}")
        col2.metric("Variación", f"{var:+.2f}")
        col3.text(f"Fecha: {data.index[-1].strftime('%Y-%m-%d')}")
        st.divider()

    except Exception as e:
        st.error(f"Error al cargar {nombre}: {e}")

# Resumen cruzado
if "High Yield General (OAS)" in valores_obtenidos and "Segmento CCC (Riesgo Alto)" in valores_obtenidos:
    general = valores_obtenidos["High Yield General (OAS)"]
    ccc = valores_obtenidos["Segmento CCC (Riesgo Alto)"]
    brecha = ccc - general

    st.subheader("💡 Resumen Cruzado de Crédito")
    st.write(f"**Brecha de crédito (CCC vs General):** {brecha:.2f} pts")
    if brecha > 6.0:
        st.warning("Estado: **DIVERGENCIA**. Castigo severo focalizado en empresas frágiles.")
    else:
        st.success("Estado: **CONVERGENCIA**. Riesgo distribuido de forma homogénea.")