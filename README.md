# 📊 Financial Risk Dashboard (Dashboard de Riesgo Financiero)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![FRED API](https://img.shields.io/badge/Data-FRED%20API-green.svg)](https://fred.stlouisfed.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional-grade, mobile-optimized macro and financial risk dashboard built with **Python**, **Streamlit**, and real-time data from the **Federal Reserve Economic Data (FRED)** API. Designed to provide instant market insights through an automated **"Risk Traffic Light"** system.

---

## 🌟 Key Features

*   **🚦 Automated Risk Traffic Light:** Instantly evaluates systemic financial stress, corporate high-yield spreads, and yield curve inversions to categorize current market risk into Green (Stable), Yellow (Caution), or Red (High Stress).
*   **🌐 Full Bilingual Support (ES / EN):** Seamlessly switch between Spanish and English via the sidebar to access translated metrics, descriptions, and economic insights.
*   **📱 Mobile-First UX:** Custom CSS overrides, touch-optimized Vega-Lite charts, responsive containers, and large status indicators designed for fluid mobile viewing.
*   **📈 Real-Time FRED Integration:** Pulls live economic indicators directly from the St. Louis Fed database, including:
    *   *High Yield Corporate Bond Spreads (OAS)*
    *   *CCC-rated High Yield Segment (Distressed Debt)*
    *   *10-Year Real Interest Rates (TIPS)*
    *   *St. Louis Fed Financial Stress Index (STLFSI4)*
    *   *Yield Curve (10Y - 2Y Treasury Spread)*
    *   *10-Year Breakeven Inflation Expectations*
*   **💡 Cross-Metric Intelligence:** Computes the credit spread gap (CCC vs. Broad High Yield) to detect credit market divergence or convergence.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **Web Framework:** Streamlit
*   **Data & Analytics:** Pandas, `fredapi`
*   **Visualization:** Streamlit Native Line Charts (Vega-Lite backend)
*   **Styling:** Custom CSS injected for mobile responsiveness and typography overrides

---

## 🚀 Quick Start / Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tu-usuario/financial-risk-dashboard.git
   cd financial-risk-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your FRED API Key:**
   Get a free API key from [FRED](https://fred.stlouisfed.org/docs/api/api_key.html). Create a folder named `.streamlit` in your project root and add a `secrets.toml` file:
   ```toml
   FRED_API_KEY = "tu_api_key_aqui"
   ```

4. **Run the application locally:**
   ```bash
   streamlit run app.py
   ```

---

## 📚 Educational Resources & References
The dashboard includes an integrated curation of official and educational sources in both English and Spanish (FRED, Banco de España, European Central Bank, Economipedia, and Investopedia) to help users interpret macro indicators.

---

## ⚖️ Disclaimer
*This web application is created strictly for informational, educational, and technical analysis purposes. Data is sourced from public Federal Reserve APIs (FRED), but accuracy or real-time delivery is not guaranteed. This content does not constitute financial advice, investment recommendations, or an offer to buy or sell securities.*

---
✨ *Tool built with Python, Streamlit, and assisted by **Gemini**.*
