import streamlit as st
import pandas as pd
from fredapi import Fred

# Configuración de la página web (Título limpio y en español)
st.set_page_config(
    page_title="Panel Macro y Bonos Global", 
    page_icon="📊", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS PARA CORREGIR EL ANCLAJE Y EL SCROLL TÁCTIL EN MÓVILES ---
st.markdown(
    """
    <style>
    /* Desactiva la captura de gestos táctiles en los gráficos para que el scroll del móvil sea perfecto */
    iframe, [data-testid="stArrowVegaLiteChart"], .vega-embed {
        pointer-events: none;
    }
    div[id] {
        scroll-margin-top: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Panel Global Macro y de Riesgo Financiero")
st.markdown("Datos macroeconómicos en tiempo real obtenidos directamente desde la Reserva Federal (FRED).")

# Obtenemos la API Key de los secretos de Streamlit
try:
    fred_api_key = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=fred_api_key)
except Exception:
    st.error("Falta configurar la clave FRED API en los Secrets de Streamlit.")
    st.stop()

# Diccionario de series e información en castellano
series_dict = {
    "High Yield General (OAS)": {
        "codigo": "BAMLH0A0HYM2",
        "info": "Mide el exceso de rendimiento que exigen los inversores por los bonos corporativos de alto riesgo frente a los bonos gubernamentales seguros."
    },
    "Segmento CCC (Riesgo Alto)": {
        "codigo": "BAMLH0A3HYC",
        "info": "Diferencial de tipos de las empresas más vulnerables y con mayor probabilidad de impago dentro del universo de bonos de alto rendimiento."
    },
    "Tipos Reales 10Y (EE.UU.)": {
        "codigo": "DFII10",
        "info": "Rendimiento de los bonos del Tesoro a 10 años descontando la inflación esperada. Mide el coste real del dinero a largo plazo."
    },
    "Índice de Estrés Financiero": {
        "codigo": "STLFSI4",
        "info": "Mide el nivel de tensión en los mercados financieros globales. Valores superiores a 0 indican estrés elevado en el sistema."
    },
    "Curva de Tipos (10Y - 2Y)": {
        "codigo": "T10Y2Y",
        "info": "Diferencia entre el bono a 10 años y el a 2 años. Si es negativa (invertida), históricamente ha sido un aviso de recesión."
    },
    "Expectativas de Inflación (10Y)": {
        "codigo": "T10YIE",
        "info": "Inflación media anual que los inversores anticipan para la próxima década basándose en el mercado de deuda."
    }
}

valores_obtenidos = {}

# --- BLOQUE CON AVISO DE CARGA (SPINNER) ---
with st.spinner("🔄 Conectando con la API de la Reserva Federal y cargando datos..."):

    for nombre, datos_serie in series_dict.items():
        try:
            codigo = datos_serie["codigo"]
            explicacion = datos_serie["info"]
            
            data = fred.get_series(codigo).dropna()
            ultimo = data.iloc[-1]
            anterior = data.iloc[-2]
            var = ultimo - anterior
            valores_obtenidos[nombre] = ultimo
            
            if nombre == "Índice de Estrés Financiero":
                st.markdown('<div id="estres"></div>', unsafe_allow_html=True)
                
            st.subheader(f"🔹 {nombre}")
            col1, col2, col3 = st.columns(3)
            
            col1.metric("Valor Actual", f"{ultimo:.2f}")
            col2.metric("Variación", f"{var:+.2f}")
            col3.text(f"Fecha: {data.index[-1].strftime('%Y-%m-%d')}")
            
            with st.expander(f"ℹ️ ¿Qué mide este indicador?"):
                st.write(explicacion)
                
            st.divider()
            
        except Exception as e:
            st.error(f"Error al cargar {nombre}: {e}")

    # --- GRÁFICO HISTÓRICO Y ANÁLISIS DE LA CURVA DE TIPOS ---
    st.markdown("---")
    st.markdown('<div id="curva"></div>', unsafe_allow_html=True)
    st.subheader("📈 Evolución Histórica: Curva de Tipos (10Y - 2Y)")
    st.markdown("Permite visualizar si venimos de una zona negativa profunda que cruza de nuevo hacia terreno positivo.")

    try:
        data_curva = fred.get_series("T10Y2Y").dropna()
        data_reciente = data_curva.loc['2023-01-01':]
        
        st.line_chart(data_reciente)
        
        ultimo_t10y2y = data_curva.iloc[-1]
        if ultimo_t10y2y < 0:
            st.warning("⚠️ **Atención:** La curva de tipos actual **sigue invertida**.")
        else:
            st.info("ℹ️ La curva de tipos actual está en **terreno positivo (normalizada)**.")
            
    except Exception as e:
        st.error(f"No se pudo cargar el histórico de la curva de tipos: {e}")

    # --- GRÁFICO HISTÓRICO Y ANÁLISIS DE LAS EXPECTATIVAS DE INFLACIÓN ---
    st.markdown("---")
    st.markdown('<div id="inflacion"></div>', unsafe_allow_html=True)
    st.subheader("📈 Evolución Histórica: Expectativas de Inflación (10Y)")
    st.markdown("Permite visualizar si las expectativas de inflación están repuntando con fuerza o se mantienen estables.")

    try:
        data_inflacion = fred.get_series("T10YIE").dropna()
        data_inf_reciente = data_inflacion.loc['2023-01-01':]
        
        st.line_chart(data_inf_reciente)
        
        ultimo_inf = data_inflacion.iloc[-1]
        hace_tres_meses = data_inflacion.iloc[-60] if len(data_inflacion) >= 60 else data_inflacion.iloc[0]
        variacion_trimestral = ultimo_inf - hace_tres_meses
        
        if variacion_trimestral > 0.25:
            st.warning(f"⚠️ **Alerta de Inflación:** Las expectativas han repuntado un **+{variacion_trimestral:.2f} pts** en los últimos meses.")
        else:
            st.info(f"ℹ️ Las expectativas de inflación se mantienen estables (último valor: **{ultimo_inf:.2f}%**).")
            
    except Exception as e:
        st.error(f"No se pudo cargar el histórico de expectativas de inflación: {e}")

# Bloque final: Resumen cruzado y guía
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

st.markdown("""
**• ¿Qué vigilar en este panel global?**
1. **[Estrés Financiero](#estres):** Tensión en el sistema interbancario y financiero global.
2. **[Curva de Tipos](#curva):** Inversión y normalización como antesala de ciclos económicos.
3. **[Expectativas de Inflación](#inflacion):** Presión sobre los tipos de interés oficiales.
""")

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
