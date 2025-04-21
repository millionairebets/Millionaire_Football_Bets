import streamlit as st
import pandas as pd
import numpy as np

# Função para prever o 1X2 (Resultado)
def predict_result(home_team, away_team):
    # Aqui pode-se substituir por um modelo de IA real
    result = np.random.choice(["Home Win", "Draw", "Away Win"])
    return result

# Função para prever o Over/Under (2.5)
def predict_over_under(home_team, away_team):
    # Substituir por um modelo real
    over_under = np.random.choice(["Over 2.5", "Under 2.5"])
    return over_under

# Função para calcular a gestão de banca
def calculate_bet_probability(probability):
    return round(probability * 100, 2)

# Interface Streamlit
st.title("Millionaire Football Bets - Previsões de Apostas")
st.sidebar.header("Escolha as Equipas")

# Inserir equipas
home_team = st.sidebar.text_input("Equipa da Casa", "Arsenal")
away_team = st.sidebar.text_input("Equipa Fora", "Liverpool")

# Previsões
if st.sidebar.button("Prever"):
    result = predict_result(home_team, away_team)
    over_under = predict_over_under(home_team, away_team)
    prob_1x2 = np.random.rand()
    prob_over_under = np.random.rand()

    st.subheader(f"Previsão para o jogo: {home_team} vs {away_team}")
    st.write(f"**Resultado (1X2)**: {result}")
    st.write(f"**Golos (Over/Under 2.5)**: {over_under}")
    
    st.write(f"**Probabilidade de 1X2**: {calculate_bet_probability(prob_1x2)}%")
    st.write(f"**Probabilidade de Over/Under 2.5**: {calculate_bet_probability(prob_over_under)}%")

    # Gestão de Banca
    st.write("### Gestão de Banca")
    st.write(f"Aposta recomendada para 1X2: {calculate_bet_probability(prob_1x2)}% da banca")
    st.write(f"Aposta recomendada para Over/Under 2.5: {calculate_bet_probability(prob_over_under)}% da banca")
