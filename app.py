# --- GRÁFICO HISTÓRICO Y ANÁLISIS DE LAS EXPECTATIVAS DE INFLACIÓN (T10YIE) ---
st.markdown("---")
st.markdown('<div id="inflacion"></div>', unsafe_allow_html=True)
st.subheader("📈 Evolución Histórica: Expectativas de Inflación (10Y)")
st.markdown("Permite visualizar si las expectativas de inflación están repuntando con fuerza o se mantienen ancladas.")

try:
    # Obtenemos los datos históricos de los últimos 3 años de la serie T10YIE
    data_inflacion = fred.get_series("T10YIE").dropna()
    data_inf_reciente = data_inflacion.loc['2023-01-01':]
    
    # Gráfico de líneas interactivo nativo
    st.line_chart(data_inf_reciente)
    
    # Análisis rápido basado en la variación reciente (últimos 3 meses aprox)
    ultimo_inf = data_inflacion.iloc[-1]
    hace_tres_meses = data_inflacion.iloc[-60] if len(data_inflacion) >= 60 else data_inflacion.iloc[0]
    variacion_trimestral = ultimo_inf - hace_tres_meses
    
    if variacion_trimestral > 0.25:
        st.warning(f"⚠️ **Alerta de Inflación:** Las expectativas han repuntado un **+{variacion_trimestral:.2f} pts** en los últimos meses. Ojo a la presión sobre los tipos.")
    else:
        st.info(f"ℹ️ Las expectativas de inflación se mantienen relativamente estables (último valor: **{ultimo_inf:.2f}%**).")
        
except Exception as e:
    st.error(f"No se pudo cargar el histórico de expectativas de inflación: {e}")
