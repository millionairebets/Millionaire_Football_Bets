import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 🏦 Função para calcular a aposta com base na escala de risco
def calcular_aposta(banca, risco):
    if risco == 0:
        return banca * 0.01  # Aposta de 1% da banca para risco 0
    elif risco == 10:
        return banca * 0.05  # Aposta de 5% da banca para risco 10
    else:
        # Para riscos entre 1 e 9, fazemos um ajuste proporcional
        return banca * (risco * 0.005)  # Aposta proporcional (de 1% a 5%)

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
def exibir_apostas(banca, jogos, risco):
    st.write("### Jogos de Futebol Hoje ⚽️")
    st.write(jogos)

    st.write("### Gestão de Banca 💸")
    st.write(f"Sua banca atual: **{banca}€**")
    st.write(f"Risco da aposta: **{risco}/10**")

    for i, jogo in jogos.iterrows():
        st.write(f"#### {jogo['Equipa Casa']} vs {jogo['Equipa Visitante']} ({jogo['Data']})")
        
        # Probabilidades e odds para os mercados
        probabilidade_1x2 = 45.9  # Exemplo de probabilidade para empate
        odds_1x2 = 3.5  # Exemplo de odds para empate

        probabilidade_ou2_5 = 55.3  # Exemplo de probabilidade para Over 2.5
        odds_ou2_5 = 1.8  # Exemplo de odds para Over 2.5
        
        probabilidade_ou1_5 = 70.2  # Exemplo de probabilidade para Over 1.5
        odds_ou1_5 = 1.3  # Exemplo de odds para Over 1.5
        
        # Calculando as apostas com base no risco
        aposta_1x2 = calcular_aposta(banca, risco)
        aposta_ou2_5 = calcular_aposta(banca, risco)
        aposta_ou1_5 = calcular_aposta(banca, risco)

        # Exibindo as informações
        st.write(f"👀 **Probabilidade de Empate: {probabilidade_1x2}%**")
        st.write(f"💰 Aposta sugerida para Empate: **{round(aposta_1x2, 2)}€**")
        st.write(f"**Odds para Empate: {odds_1x2}**")
        
        st.write(f"👀 **Probabilidade de Over 2.5: {probabilidade_ou2_5}%**")
        st.write(f"💰 Aposta sugerida para Over 2.5: **{round(aposta_ou2_5, 2)}€**")
        st.write(f"**Odds para Over 2.5: {odds_ou2_5}**")
        
        st.write(f"👀 **Probabilidade de Over 1.5: {probabilidade_ou1_5}%**")
        st.write(f"💰 Aposta sugerida para Over 1.5: **{round(aposta_ou1_5, 2)}€**")
        st.write(f"**Odds para Over 1.5: {odds_ou1_5}**")
        
        st.write("---")

# 🎯 Função principal do Streamlit
def app():
    st.title("📈 Previsões e Gestão de Banca para Apostas Futebolísticas")
    
    # 💼 Gestão de Banca
    banca_inicial = st.number_input("Insira sua banca inicial (em €):", value=1000, min_value=1)
    
    # 🎯 Escolher o nível de risco
    risco = st.slider("Selecione o nível de risco da aposta (0 a 10)", min_value=0, max_value=10, value=5)

    # Obter os jogos de hoje
    jogos_hoje = obter_jogos_hoje()
    
    if not jogos_hoje.empty:
        exibir_apostas(banca_inicial, jogos_hoje, risco)
    else:
        st.write("⚠️ Não há jogos de futebol para hoje!")

if __name__ == "__main__":
    app()
