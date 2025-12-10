import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import json
import feedparser
from app import *
from groq import Groq

# ---------------------------
# STREAMLIT UI
# ---------------------------

st.title("📊 Dashboard Financeiro com Groq + Yfinance + Google News")
st.write("Digite o nome da empresa ou ticker (ex: Petrobras, PETR4.SA, Vale, VALE3.SA)")

company_input = st.text_input("Empresa:")

if company_input:

    st.subheader("🔎 Identificando empresa…")

    # 1) Tenta usar como foi digitado
    data = yf.Ticker(company_input)
    try:
        current_price = data.info.get("regularMarketPrice", None)
    except:
        current_price = None

    # 2) Se falhar, usa Groq para descobrir o ticker
    if current_price is None:
        st.write("Não encontrado. Tentando identificar o ticker com Groq…")
        ticker = get_ticker_from_name(company_input)
        st.write(f"Groq sugeriu: **{ticker}**")

        data = yf.Ticker(ticker)
        try:
            current_price = data.info.get("regularMarketPrice", None)
        except:
            current_price = None
    else:
        ticker = company_input  # já era válido

    # 3) Se ainda assim não encontrou
    if current_price is None:
        st.error("Não foi possível obter os dados da empresa.")
        st.stop()

    # ---------------------------
    # VALOR ATUAL
    # ---------------------------
    st.subheader(f"💰 Valor atual da ação ({ticker})")
    st.metric("Preço Atual", f"R$ {current_price:.2f}")

    # ---------------------------
    # HISTÓRICO 2 ANOS
    # ---------------------------
    st.subheader("📈 Evolução nos últimos 2 anos")

    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=730)

    hist = data.history(start=start, end=end)

    if hist.empty:
        st.warning("Sem dados históricos disponíveis.")
    else:
        st.line_chart(hist["Close"])

# ---------------------------
# NOTÍCIAS reais via google
# ---------------------------

st.subheader("📰 Últimas 3 notícias relacionadas")

news = get_news_google(company_input)

if news:
    for item in news:
        st.markdown(f"### {item['title']}")
        st.write(f"[Abrir notícia]({item['link']})")
        st.write(f"🧠 **Resumo:** {item['summary']}")
        st.markdown("---")
else:
    st.info("Nenhuma notícia encontrada no Google News.")