import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 📊 Função para calcular a aposta com base na Regra de Kelly
def calcular_aposta(banca, probabilidade, odds):
    p = probabilidade / 100  # Convertendo para valor decimal
    q = 1 - p
    f = (p * odds - q) / odds  # Fórmula da Regra de Kelly
    aposta = banca * f
    return aposta

# 🌍 Função para obter jogos de futebol que acontecem hoje
def obter_jogos_hoje():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": "4b144fcaead140608f8732d7668abb7a"}  # Sua chave de API

    response = requests.get(url, headers=headers)
    data = response.json()

    jogos = []
    for match in data['matches']:
        data_jogo = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        if data_jogo.date() == datetime.today().date():
            jogo = {
                'Equipa Casa': match['homeTeam']['name'],
                'Equipa Visitante': match['awayTeam']['name'],
                'Data': data_jogo.strftime('%H:%M'),
                'Competição': match['competition']['name']
            }
            jogos.append(jogo)
    
    return pd.DataFrame(jogos)

# 🏦 Função para exibir as recomendações de aposta
def exibir_apostas(banca, jogos):
    st.write("### Jogos de Futebol Hoje ⚽️")
    st.write(jogos)

    st.write("### Gestão de Banca 💸")
    st.write(f"Sua banca atual: **{banca}€**")

    for i, jogo in jogos.iterrows():
        st.write(f"#### {jogo['Equipa Casa']} vs {jogo['Equipa Visitante']} ({jogo['Data']})")
        probabilidade_1x2 = 45.9  # Exemplo de probabilidade para empate
        odds = 3.5  # Exemplo de odds para empate

        # Calculando a aposta para 1X2 usando a Regra de Kelly
        aposta = calcular_aposta(banca, probabilidade_1x2, odds)
        st.write(f"👀 **Probabilidade de Empate: {probabilidade_1x2}%**")
        st.write(f"💰 Aposta sugerida para empate: **{round(aposta, 2)}€**")
        st.write("---")

# 🎯 Função principal do Streamlit
def app():
    st.title("📈 Previsões e Gestão de Banca para Apostas Futebolísticas")
    
    # 💼 Gestão de Banca
    banca_inicial = st.number_input("Insira sua banca inicial (em €):", value=1000, min_value=1)
    
    # Obter os jogos de hoje
    jogos_hoje = obter_jogos_hoje()
    
    if not jogos_hoje.empty:
        exibir_apostas(banca_inicial, jogos_hoje)
    else:
        st.write("⚠️ Não há jogos de futebol para hoje!")

if __name__ == "__main__":
    app()
