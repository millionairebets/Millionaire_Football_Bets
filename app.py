import streamlit as st
import pandas as pd
import pickle
import requests
from datetime import datetime

# Carregar o modelo treinado
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="⚽ IA Football Predictor", layout="centered")

st.title("⚽ Previsões de Futebol com IA")
st.markdown("Previsões automáticas para os jogos de hoje da Premier League usando inteligência artificial.")

# Token da API
API_KEY = "4b144fcaead140608f8732d7668abb7a"

# Função para buscar jogos de hoje
@st.cache_data
def get_today_matches():
    url = "https://v3.football.api-sports.io/fixtures?league=39&season=2023&date=" + datetime.today().strftime('%Y-%m-%d')
    headers = {
        "x-apisports-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get("response", [])

# Função dummy para gerar features (exemplo simplificado)
def extract_features(match):
    # Simulação de features com dados genéricos (para demo)
    return pd.DataFrame([{
        "home_attack": 1.2,
        "away_attack": 0.9,
        "home_form": 0.7,
        "away_form": 0.6,
    }])

# Buscar jogos
matches = get_today_matches()
if not matches:
    st.warning("Sem jogos hoje na Premier League.")
else:
    for match in matches:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        date = match["fixture"]["date"]

        features = extract_features(match)
        prediction = model.predict(features)[0]
        proba = model.predict_proba(features)[0]

        st.subheader(f"{home} 🆚 {away}")
        st.markdown(f"📅 **Data:** {date[:10]}")

        # Resultado 1X2
        if prediction == "H":
            result = "🏠 Vitória da Casa"
        elif prediction == "A":
            result = "🚗 Vitória do Visitante"
        else:
            result = "🤝 Empate"

