# 🌍 Panel Global Macro y de Riesgo Financiero

Una aplicación web interactiva y en tiempo real desarrollada en **Python** con **Streamlit** y conectada directamente a la **API de la Reserva Federal de San Luis (FRED)**. 

El panel está diseñado para monitorizar de un vistazo el pulso de los mercados de deuda corporativa, las condiciones de liquidez interbancaria, la estructura de tipos de interés y las expectativas de inflación a largo plazo.

---

## 🚀 Características Principales

* **Datos en Tiempo Real:** Extracción automatizada de series macroeconómicas oficiales mediante `fredapi`.
* **Indicadores Clave de Riesgo:**
  * **High Yield General (OAS) & Segmento CCC:** Monitorización de primas de riesgo y tensiones en el crédito corporativo (con cálculo dinámico de la brecha de divergencia).
  * **Tipos Reales a 10 Años:** Coste real del dinero en EE. UU. descontando la inflación esperada.
  * **Índice de Estrés Financiero (STLFSI4):** Detección de tensiones en los mercados de financiación global.
  * **Curva de Tipos (10Y - 2Y):** Seguimiento de inversiones y procesos de normalización rápida.
  * **Expectativas de Inflación (10Y):** Seguimiento de la evolución de las previsiones de precios a diez años.
* **Gráficos Históricos Interactivos:** Visualización de tendencias de los últimos años para la Curva de Tipos y las Expectativas de Inflación.
* **Optimización Total para Móviles:** 
  * Comportamiento táctil optimizado para permitir un *scroll* vertical fluido sin interferencias en las gráficas.
  * Tarjetas con desplegables explicativos (`st.expander`) perfectamente adaptados a pantallas estrechas.
* **Navegación Interna Inteligente:** Guía interactiva con anclajes automáticos hacia cada sección del panel con compensación de margen superior.
* **Aviso de Carga:** Retroalimentación visual interactiva mientras se consultan los servidores de la FRED.
* **Localización y Accesibilidad:** Configurado de manera nativa para navegadores en español, evitando avisos automáticos de traducción de terceros.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Framework Web:** Streamlit (desplegado en Streamlit Community Cloud)
* **Librerías Principales:** `pandas`, `fredapi`
* **Estilos y Experiencia de Usuario:** HTML5, CSS3 integrado para control responsive y anclajes, JavaScript para metadatos del navegador.

---

## ⚙️ Configuración y Despliegue Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Instalar dependencias
Asegúrate de tener Python instalado y ejecuta:
```bash
pip install streamlit pandas fredapi
```

### 3. Configurar la API Key de FRED
Crea una carpeta llamada `.streamlit` en la raíz del proyecto y dentro añade un archivo llamado `secrets.toml` con tu clave personal:
```toml
FRED_API_KEY = "tu_clave_de_api_aqui"
```

### 4. Ejecutar la aplicación
```bash
streamlit run app.py
```

---

## 💡 Guía de Interpretación Global
El panel incluye una sección de resumen cruzado que evalúa automáticamente:
1. **Estrés Financiero:** Niveles de tensión sistémica interbancaria.
2. **Curva de Tipos:** Análisis de recesión e inversión/normalización.
3. **Expectativas de Inflación:** Presión sobre los tipos de los bancos centrales.

---

## ⚠️ Aviso Legal / Disclaimer
*Esta aplicación web tiene un propósito exclusivamente informativo, educativo y de análisis técnico personal. Los datos se obtienen de fuentes públicas (FRED), pero no se garantiza su precisión absoluta ni su actualización en tiempo real. **Este contenido no constituye en ningún caso asesoramiento financiero, recomendación de inversión ni oferta de compra o venta de activos.** El autor no asume ninguna responsabilidad por las decisiones financieras o de inversión tomadas en base a esta información. Consulte siempre con un profesional financiero cualificado antes de tomar decisiones de inversión.*
