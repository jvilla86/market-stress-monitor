import streamlit as st
import pandas as pd
from fredapi import Fred

# Configuración de la página web
st.set_page_config(page_title="Panel Macro y Bonos", page_icon="📊", layout="centered")

# --- CSS PARA CORREGIR EL MARGEN DE LOS ANCLAJES (EVITA QUE EL TÍTULO QUEDE OCULTO) ---
st.markdown(
    """
    <style>
    div[id] {
        scroll-margin-top: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        
        # Asignamos anclajes HTML según el indicador exacto dentro del bucle
        if nombre == "Índice de Estrés Financiero":
            st.markdown('<div id="estres"></div>', unsafe_allow_html=True)
        elif "Inflación" in nombre:
            st.markdown('<div id="inflacion"></div>', unsafe_allow_html=True)
            
        # Mostramos cada indicador en una tarjeta visual de Streamlit
        st.subheader(f"🔹 {nombre}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Valor Actual", f"{ultimo:.2f}")
        col2.metric("Variación", f"{var:+.2f}")
        col3.text(f"Fecha: {data.index[-1].strftime('%Y-%m-%d')}")
        st.divider()
        
    except Exception as e:
        st.error(f"Error al cargar {nombre}: {e}")

# --- GRÁFICO HISTÓRICO Y ANÁLISIS DE LA CURVA DE TIPOS (T10Y2Y) ---
st.markdown("---")
# Anclaje HTML para la curva de tipos
st.markdown('<div id="curva"></div>', unsafe_allow_html=True)
st.subheader("📈 Evolución Histórica: Curva de Tipos (10Y - 2Y)")
st.markdown("Permite visualizar si venimos de una zona negativa profunda (< 0) que cruza de nuevo hacia arriba (normalización rápida).")

try:
    # Obtenemos los datos históricos de los últimos 3 años de la serie T10Y2Y
    data_curva = fred.get_series("T10Y2Y").dropna()
    data_reciente = data_curva.loc['2023-01-01':]
    
    # Gráfico de líneas interactivo nativo
    st.line_chart(data_reciente)
    
    # Alerta automática basada en el valor actual
    ultimo_t10y2y = data_curva.iloc[-1]
    if ultimo_t10y2y < 0:
        st.warning("⚠️ **Atención:** La curva de tipos actual **sigue invertida**.")
    else:
        st.info("ℹ️ La curva de tipos actual está en **terreno positivo (normalizada)**. Observa en el gráfico si este repunte viene de una caída profunda previa.")
        
except Exception as e:
    st.error(f"No se pudo cargar el histórico de la curva de tipos: {e}")

# Bloque final: Resumen cruzado y guía de interpretación global
st.markdown("---")
st.header("💡 Resumen Cruzado y Guía de Interpretación Global")

if "High Yield General (OAS)" in valores_obtenidos and "Segmento CCC (Riesgo Alto)" in valores_obtenidos:
    general = valores_obtenidos["High Yield General (OAS)"]
    ccc = valores_obtenidos["Segmento CCC (Riesgo Alto)"]
    brecha = ccc - general
    
    st.write(f"**• Brecha de crédito (CCC vs General):** {brecha:.2f} pts")
    if brecha > 6.0:
        st.warning("  -> **Estado de crédito: DIVERGENCIA.** Castigo severo focalizado en empresas frágiles.")
    else:
        st.success("  -> **Estado de crédito: CONVERGENCIA.** Riesgo distribuido de forma homogénea.")

# Guía con enlaces hipertextuales internos
st.markdown("""
**• ¿Qué vigilar en este panel global?**
1. **[Estrés Financiero](#estres):** Si supera los 0 o 1 puntos, el problema no es solo de bonos corporativos, sino que empieza a estrangular al sistema interbancario y financiero global.
2. **[Curva de Tipos](#curva):** Una curva profundamente invertida (`< 0`) seguida de una normalización rápida suele ser la antesala histórica de enfriamientos o recesiones económicas.
3. **[Expectativas de Inflación](#inflacion):** Si repuntan con fuerza, obligan a los bancos centrales a mantener los tipos de interés altos por más tiempo, penalizando a los activos de mayor riesgo.
""")

# Descargo de responsabilidad legal al final de la web
st.markdown("---")
st.caption(
    "⚠️ **Aviso legal / Disclaimer:** Esta aplicación web tiene un propósito exclusivamente informativo, "
    "educativo y de análisis técnico personal. Los datos se obtienen de fuentes públicas (FRED), pero "
    "no se garantiza su precisión absoluta ni su actualización en tiempo real. **Este contenido no constituye "
    "en ningún caso asesoramiento financiero, recomendación de inversión ni oferta de compra o venta de "
    "activos.** El autor no asume ninguna responsabilidad por las decisiones financieras o de inversión "
    "tomadas en base a esta información. Consulte siempre con un profesional financiero cualificado antes "
    "de tomar decisiones de inversión."
)
