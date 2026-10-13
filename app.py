import streamlit as st
import pandas as pd
from fredapi import Fred

# Configuración de la página web
st.set_page_config(
    page_title="Dashboard de Riesgo Financiero", 
    page_icon="📊", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- SELECTOR DE IDIOMA EN LA BARRA LATERAL ---
st.sidebar.header("🌐 Idioma / Language")
idioma = st.sidebar.radio("Selecciona idioma / Select language:", ["Español", "English"])

# --- CSS DE ESTILOS Y EXPERIENCIA DE USUARIO (MÓVILES Y SPINNER GRANDE) ---
st.markdown(
    """
    <style>
    /* Desactiva la captura de gestos táctiles en los gráficos para que el scroll del móvil sea perfecto */
    iframe, [data-testid="stArrowVegaLiteChart"], .vega-embed {
        pointer-events: none;
    }
    
    /* Corrige el margen superior de los anclajes para que el título no quede oculto */
    div[id] {
        scroll-margin-top: 80px;
    }

    /* Forzar tamaño grande y negrita en el texto del spinner de carga de Streamlit */
    [data-testid="stStatusWidget"] div, 
    .stSpinner > div > div > div,
    .stSpinner div p {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- DICCIONARIO DE TRADUCCIONES BILINGÜE ---
textos = {
    "Español": {
        "page_title": "📊 Dashboard de Riesgo Financiero",
        "subtitulo": "Datos macroeconómicos y de mercado en tiempo real obtenidos directamente desde la Reserva Federal (FRED).",
        "error_key": "Falta configurar la clave FRED API en los Secrets de Streamlit.",
        "spinner": "🔄 Conectando con la API de la Reserva Federal y cargando datos en tiempo real...",
        "exito": "✅ ¡Datos obtenidos correctamente desde la Reserva Federal (FRED)!",
        "semaforo_titulo": "🚦 Semáforo de Riesgo de Mercado",
        "semaforo_rojo": "🔴 **ALERTA DE TENSIÓN ELEVADA:** Se detectan niveles de estrés financiero o primas de riesgo corporativo elevados en el sistema.",
        "semaforo_amarillo": "🟡 **PRECAUCIÓN / VIGILANCIA:** Los mercados muestran señales mixtas o anomalías (como curva de tipos invertida), sugiriendo cautela en activos de riesgo.",
        "semaforo_verde": "🟢 **ENTORNO ESTABLE / CALMA:** Los indicadores globales de estrés y diferenciales de crédito se mantienen en rangos de normalidad.",
        "valor_actual": "Valor Actual",
        "variacion": "Variación",
        "fecha": "Fecha",
        "que_mide": "ℹ️ ¿Qué mide este indicador?",
        "curva_titulo": "📈 Evolución Histórica: Curva de Tipos (10Y - 2Y)",
        "curva_desc": "Permite visualizar si venimos de una zona negativa profunda (< 0) que cruza de nuevo hacia arriba (normalización rápida).",
        "curva_invertida": "⚠️ **Atención:** La curva de tipos actual **sigue invertida**.",
        "curva_normal": "ℹ️ La curva de tipos actual está en **terreno positivo (normalizada)**. Observa en el gráfico si este repunte viene de una caída profunda previa.",
        "inflacion_titulo": "📈 Evolución Histórica: Expectativas de Inflación (10Y)",
        "inflacion_desc": "Permite visualizar si las expectativas de inflación están repuntando con fuerza o se mantienen estables.",
        "inflacion_alerta": "⚠️ **Alerta de Inflación:** Las expectativas han repuntado en los últimos meses. Ojo a la presión sobre los tipos.",
        "inflacion_estable": "ℹ️ Las expectativas de inflación se mantienen relativamente estables.",
        "resumen_titulo": "💡 Resumen Cruzado y Guía de Interpretación Global",
        "brecha_texto": "• Brecha de crédito (CCC vs General):",
        "divergencia": "  -> **Estado de crédito: DIVERGENCIA.** Castigo severo focalizado en empresas frágiles.",
        "convergencia": "  -> **Estado de crédito: CONVERGENCIA.** Riesgo distribuido de forma homogénea.",
        "que_vigilar": """
**• ¿Qué vigilar en este panel global?**
1. **[Estrés Financiero](#estres):** Si supera los 0 o 1 puntos, el problema no es solo de bonos corporativos, sino que empieza a estrangular al sistema interbancario y financiero global.
2. **[Curva de Tipos](#curva):** Una curva profundamente invertida (`< 0`) seguida de una normalización rápida suele ser la antesala histórica de enfriamientos o recesiones económicas.
3. **[Expectativas de Inflación](#inflacion):** Si repuntan con fuerza, obligan a los bancos centrales a mantener los tipos de interés altos por más tiempo, penalizando a los activos de mayor riesgo.
""",
        "recursos_titulo": "📚 Recursos y Fuentes de Interés",
        "recursos_contenido": """
Si deseas profundizar en la teoría macroeconómica, el análisis de renta fija y el funcionamiento de los mercados de deuda, te recomiendo consultar las siguientes fuentes de referencia:

**🇪🇸 En Español:**
*   📖 **[Economipedia](https://economipedia.com/):** La enciclopedia económica de referencia para consultar conceptos clave de forma sencilla.
*   🏦 **[Banco de España - Estadísticas y Publicaciones](https://www.bde.es/):** Portal oficial para consultar informes económicos y estadísticas de tipos de interés.
*   🇪🇺 **[Banco Central Europeo (BCE) - Educación](https://www.ecb.europa.eu/):** Guías oficiales sobre política monetaria y estabilidad financiera.
*   💬 **[Rankia (Renta Fija y Macro)](https://www.rankia.com/):** Comunidad de referencia con análisis y debates sobre inversión en bonos.

**🇬🇧 En Inglés (Fuentes Oficiales):**
*   🌐 **[FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/):** Base de datos oficial de la Reserva Federal de San Luis.
*   📊 **[St. Louis Fed Education](https://www.stlouisfed.org/education):** Herramientas interactivas para entender la macroeconomía global.
""",
        "creditos": "✨ *Herramienta desarrollada con Python, Streamlit y asistida por **Gemini**.*",
        "disclaimer": "⚠️ **Aviso legal / Disclaimer:** Esta aplicación web tiene un propósito exclusivamente informativo, educativo y de análisis técnico personal. Los datos se obtienen de fuentes públicas (FRED), pero no se garantiza su precisión absoluta. **Este contenido no constituye asesoramiento financiero ni recomendación de inversión.**"
    },
    "English": {
        "page_title": "📊 Financial Risk Dashboard",
        "subtitulo": "Real-time macroeconomic and market risk metrics sourced directly from the Federal Reserve (FRED).",
        "error_key": "FRED API key is missing in Streamlit Secrets.",
        "spinner": "🔄 Connecting to Federal Reserve API and fetching real-time data...",
        "exito": "✅ Data successfully fetched from the Federal Reserve (FRED)!",
        "semaforo_titulo": "🚦 Market Risk Traffic Light",
        "semaforo_rojo": "🔴 **HIGH STRESS ALERT:** Elevated financial stress or corporate credit risk spreads detected in the system.",
        "semaforo_amarillo": "🟡 **CAUTION / WARNING:** Mixed signals or market anomalies (such as an inverted yield curve) suggest caution in risk assets.",
        "semaforo_verde": "🟢 **STABLE ENVIRONMENT:** Global financial stress indicators and credit spreads remain within normal ranges.",
        "valor_actual": "Current Value",
        "variacion": "Change",
        "fecha": "Date",
        "que_mide": "ℹ️ What does this indicator measure?",
        "curva_titulo": "📈 Historical Evolution: Yield Curve (10Y - 2Y)",
        "curva_desc": "Visualizes whether the curve is emerging from deep negative territory (< 0) back into positive ground.",
        "curva_invertida": "⚠️ **Warning:** The yield curve **remains inverted**.",
        "curva_normal": "ℹ️ The yield curve is currently in **positive territory (normalized)**.",
        "inflacion_titulo": "📈 Historical Evolution: Inflation Expectations (10Y)",
        "inflacion_desc": "Tracks whether long-term inflation expectations are surging or staying anchored.",
        "inflacion_alerta": "⚠️ **Inflation Warning:** Inflation expectations have ticked up in recent months.",
        "inflacion_estable": "ℹ️ Inflation expectations remain anchored within stable ranges.",
        "resumen_titulo": "💡 Cross-Metric Summary & Global Interpretation Guide",
        "brecha_texto": "• Credit Spread Gap (CCC vs Broad HY):",
        "divergencia": "  -> **Credit Status: DIVERGENCE.** Severe market distress concentrated in low-grade borrowers.",
        "convergencia": "  -> **Credit Status: CONVERGENCE.** Credit risk spread evenly across issuers.",
        "que_vigilar": """
**• Key indicators to monitor in this dashboard:**
1. **[Financial Stress Index](#estres):** Values exceeding 0 or 1 indicate systemic tension.
2. **[Yield Curve](#curva):** Deep inversion (`< 0`) historically precedes economic slowdowns.
3. **[Inflation Expectations](#inflacion):** Sharp increases force central banks to maintain higher policy rates.
""",
        "recursos_titulo": "📚 Educational Resources & Official Sources",
        "recursos_contenido": """
To deepen your understanding of macroeconomic theory and fixed income analysis:

**🇬🇧 English Sources (Official & Global):**
*   🌐 **[FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/):** St. Louis Fed's database.
*   📊 **[St. Louis Fed Education](https://www.stlouisfed.org/education):** Interactive macroeconomic guides.
*   📈 **[Investopedia - Bond Yields & Spreads](https://www.investopedia.com/):** Technical fixed-income definitions.
""",
        "creditos": "✨ *Tool built with Python, Streamlit, and assisted by **Gemini**.*",
        "disclaimer": "⚠️ **Disclaimer:** This web application is created strictly for informational and educational purposes. **This content does not constitute financial advice or investment recommendations.**"
    }
}

t = textos[idioma]

st.title(t["page_title"])
st.markdown(t["subtitulo"])

# Obtenemos la API Key de los secretos de Streamlit
try:
    fred_api_key = st.secrets["FRED_API_KEY"]
    fred = Fred(api_key=fred_api_key)
except Exception:
    st.error(t["error_key"])
    st.stop()

# Diccionario de series con descripciones bilingües
series_dict = {
    "High Yield General (OAS)": {
        "codigo": "BAMLH0A0HYM2",
        "info": "Mide el exceso de rendimiento que exigen los inversores por los bonos corporativos de alto riesgo frente a bonos seguros." if idioma == "Español" else "Measures the excess yield investors demand for holding high-risk corporate bonds over benchmark government bonds."
    },
    "Segmento CCC (Riesgo Alto)": {
        "codigo": "BAMLH0A3HYC",
        "info": "Diferencial de tipos de las empresas más vulnerables y con mayor probabilidad de impago dentro de alto rendimiento." if idioma == "Español" else "Option-adjusted spread for the lowest credit tier (CCC) representing borrowers with elevated default probabilities."
    },
    "Tipos Reales 10Y (EE.UU.)": {
        "codigo": "DFII10",
        "info": "Rendimiento del bono del Tesoro a 10 años descontando la inflación esperada. Coste real del dinero a largo plazo." if idioma == "Español" else "10-Year Treasury Inflation-Protected Securities (TIPS) yield, representing the real cost of capital."
    },
    "Índice de Estrés Financiero": {
        "codigo": "STLFSI4",
        "info": "Mide el nivel de tensión en los mercados financieros globales. Valores superiores a 0 indican estrés elevado." if idioma == "Español" else "St. Louis Fed Financial Stress Index. Values above zero indicate above-average market tension."
    },
    "Curva de Tipos (10Y - 2Y)": {
        "codigo": "T10Y2Y",
        "info": "Diferencia entre bono a 10 años y 2 años. Si es negativa (invertida), históricamente avisa de recesión." if idioma == "Español" else "10-Year minus 2-Year Treasury spread. Inversions (< 0) have historically preceded economic recessions."
    },
    "Expectativas de Inflación (10Y)": {
        "codigo": "T10YIE",
        "info": "Inflación media anual que los inversores anticipan para la próxima década basándose en la deuda pública." if idioma == "Español" else "10-Year Breakeven Inflation Rate reflecting market-implied average annual inflation over the next decade."
    }
}

valores_obtenidos = {}

# --- BLOQUE CON SPINNER Y PRE-CARGA DE DATOS ---
with st.spinner(t["spinner"]):
    for nombre, datos_serie in series_dict.items():
        try:
            codigo = datos_serie["codigo"]
            data = fred.get_series(codigo).dropna()
            ultimo = data.iloc[-1]
            valores_obtenidos[nombre] = ultimo
        except Exception:
            pass 

st.success(t["exito"])

# --- SEMÁFORO DE RIESGO MACRO GLOBAL ---
st.markdown(f"### {t['semaforo_titulo']}")

estres_financiero = valores_obtenidos.get("Índice de Estrés Financiero", 0)
curva_tipos = valores_obtenidos.get("Curva de Tipos (10Y - 2Y)", 0)
hy_general = valores_obtenidos.get("High Yield General (OAS)", 0)

if estres_financiero > 0.5 or hy_general > 5.5:
    st.error(t["semaforo_rojo"])
elif curva_tipos < 0:
    st.warning(t["semaforo_amarillo"])
else:
    st.success(t["semaforo_verde"])

st.markdown("---")

# --- PINTADO DE TARJETAS Y DESPLEGABLES ---
for nombre, datos_serie in series_dict.items():
    try:
        codigo = datos_serie["codigo"]
        explicacion = datos_serie["info"]
        
        data = fred.get_series(codigo).dropna()
        ultimo = data.iloc[-1]
        anterior = data.iloc[-2]
        var = ultimo - anterior
        
        if nombre == "Índice de Estrés Financiero":
            st.markdown('<div id="estres"></div>', unsafe_allow_html=True)
            
        st.subheader(f"🔹 {nombre}")
        col1, col2, col3 = st.columns(3)
        
        col1.metric(t["valor_actual"], f"{ultimo:.2f}")
        col2.metric(t["variacion"], f"{var:+.2f}")
        col3.text(f"{t['fecha']}: {data.index[-1].strftime('%Y-%m-%d')}")
        
        with st.expander(t["que_mide"]):
            st.write(explicacion)
            
        st.divider()
        
    except Exception as e:
        st.error(f"Error ({nombre}): {e}")

# --- GRÁFICO HISTÓRICO: CURVA DE TIPOS ---
try:
    st.markdown('<div id="curva"></div>', unsafe_allow_html=True)
    st.subheader(t["curva_titulo"])
    st.markdown(t["curva_desc"])

    data_curva = fred.get_series("T10Y2Y").dropna()
    data_reciente = data_curva.loc['2023-01-01':]
    
    st.line_chart(data_reciente)
    
    ultimo_t10y2y = data_curva.iloc[-1]
    if ultimo_t10y2y < 0:
        st.warning(t["curva_invertida"])
    else:
        st.info(t["curva_normal"])
        
except Exception as e:
    st.error(f"Error Curve: {e}")

# --- GRÁFICO HISTÓRICO: EXPECTATIVAS DE INFLACIÓN ---
try:
    st.markdown("---")
    st.markdown('<div id="inflacion"></div>', unsafe_allow_html=True)
    st.subheader(t["inflacion_titulo"])
    st.markdown(t["inflacion_desc"])

    data_inflacion = fred.get_series("T10YIE").dropna()
    data_inf_reciente = data_inflacion.loc['2023-01-01':]
    
    st.line_chart(data_inf_reciente)
    
    ultimo_inf = data_inflacion.iloc[-1]
    hace_tres_meses = data_inflacion.iloc[-60] if len(data_inflacion) >= 60 else data_inflacion.iloc[0]
    variacion_trimestral = ultimo_inf - hace_tres_meses
    
    if variacion_trimestral > 0.25:
        st.warning(t["inflacion_alerta"])
    else:
        st.info(t["inflacion_estable"])
        
except Exception as e:
    st.error(f"Error Inflation: {e}")

# --- RESUMEN CRUZADO Y GUÍA ---
st.markdown("---")
st.header(t["resumen_titulo"])

if "High Yield General (OAS)" in valores_obtenidos and "Segmento CCC (Riesgo Alto)" in valores_obtenidos:
    general = valores_obtenidos["High Yield General (OAS)"]
    ccc = valores_obtenidos["Segmento CCC (Riesgo Alto)"]
    brecha = ccc - general
    
    st.write(f"**{t['brecha_texto']}** {brecha:.2f} pts")
    if brecha > 6.0:
        st.warning(t["divergencia"])
    else:
        st.success(t["convergencia"])

st.markdown(t["que_vigilar"])

# --- RECURSOS EDUCATIVOS ---
st.markdown("---")
st.header(t["recursos_titulo"])
st.markdown(t["recursos_contenido"])

# --- PIE DE PÁGINA Y DISCLAIMER ---
st.markdown("---")
st.markdown(t["creditos"])
st.caption(t["disclaimer"])
