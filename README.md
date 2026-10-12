# 🌍 Panel Global Macro y de Riesgo Financiero

Una aplicación web interactiva y ligera construida con **Python**, **Streamlit** y la API de la Reserva Federal de San Luis (**FRED**). Este panel está diseñado para monitorizar en tiempo real el estrés del mercado de crédito, las primas de riesgo de bonos corporativos (*High Yield* y segmento *CCC*), los tipos de interés reales, el estrés financiero sistémico, el ciclo de la curva de tipos y las expectativas de inflación.

---

## 🚀 Características

- **Datos en tiempo real:** Conexión directa mediante API con FRED para extraer las series macroeconómicas más actualizadas.
- **Indicadores clave de crédito y macro:**
  - *High Yield General (OAS)* y *Segmento CCC (Riesgo Alto)*: Termómetro del riesgo de impago corporativo.
  - *Tipos Reales a 10 Años (DFII10)*: Contexto para activos refugio.
  - *Índice de Estrés Financiero (STLFSI4)*: Detección de tensiones a nivel sistémico e interbancario.
  - *Curva de Tipos (10Y - 2Y)*: Seguimiento histórico de alertas de ciclo económico.
  - *Expectativas de Inflación (10Y)*: Pulso de las presiones de precios a largo plazo.
- **Resumen cruzado automatizado:** Calcula la brecha de riesgo entre el segmento CCC y el mercado general de alto rendimiento para detectar divergencias o estrés focalizado.
- **Diseño web adaptado:** Desplegado mediante Streamlit Community Cloud para consultarlo cómodamente desde el navegador de cualquier dispositivo (móvil, tablet o PC).

---

## 🛠️ Requisitos e Instalación Local

Si deseas ejecutar este proyecto en tu propio entorno local (por ejemplo, en Linux / Manjaro) mediante la terminal:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/nombre-de-tu-repositorio.git
   cd nombre-de-tu-repositorio
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación web localmente con Streamlit:
   ```bash
   streamlit run app.py
   ```

---

## 📦 Estructura del Repositorio

- `app.py`: Código principal de la aplicación web en Streamlit.
- `requirements.txt`: Archivo con las dependencias de Python necesarias (`pandas`, `fredapi`, `streamlit`).
- `README.md`: Documentación del proyecto.

---

## 🔑 Configuración de la API (Secrets)

Para que la aplicación pueda consultar los datos de FRED, necesita una clave de API gratuita de la Reserva Federal. 

- **En despliegues en la nube (Streamlit Community Cloud):** Configura la clave en el panel de control de tu aplicación en la sección *Advanced settings > Secrets* usando el siguiente formato TOML:
  ```toml
  FRED_API_KEY = "tu_clave_api_de_fred_aqui"
  ```

---

## 💡 Guía Rápida de Interpretación

- **Brecha de Crédito (CCC vs General):** Si supera los `6.0` puntos, indica una **Divergencia**, señalando un castigo severo y focalizado en las empresas más frágiles y endeudadas.
- **Estrés Financiero (STLFSI4):** Valores por encima de `0` o `1` alertan de tensiones que van más allá del mercado corporativo, afectando a la estabilidad financiera global.
- **Curva de Tipos (T10Y2Y):** Los valores negativos (curva invertida) avisan históricamente de posibles enfriamientos o recesiones económicas de cara a los siguientes meses.

---

*Nota: Este proyecto tiene un carácter puramente informativo, analítico y educativo sobre el funcionamiento de los mercados financieros y macroeconomía.*
