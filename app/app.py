import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import json
import feedparser
from groq import Groq

# ---------------------------
# MAP DOS TICKERS
# ---------------------------

with open("company_map.json", "r") as f:
    COMPANY_MAP = json.load(f)

# ---------------------------
# CONFIGURAR GROQ
# ---------------------------

client = Groq(api_key="digite sua API_Key")   # coloque sua gsk_...

# ---------------------------
# FUNÇÃO: converter nome → ticker via GROQ
# ---------------------------

def get_ticker_from_name(company_name: str):
    name = company_name.lower().strip()

    # 1. verificar no JSON
    if name in COMPANY_MAP:
        return COMPANY_MAP[name]

    # 2. se ele já digitou um ticker válido
    if name.endswith(".sa") and len(name) <= 8:
        return name.upper()

    # 3. fallback: Groq
    prompt = f"""
    Converta o nome abaixo para o ticker brasileiro (B3).
    Caso não tenha certeza, responda apenas o ticker mais provável.

    Nome da empresa: "{company_name}"

    Responda somente o ticker, exemplo: PETR4.SA
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10,
    )

    return response.choices[0].message.content.strip().upper()

# ---------------------------
# FUNÇAO QUE PESQUISA NOTICIAS NO GOOGLE
# ---------------------------

def get_news_google(company_name: str):
    query = company_name.replace(" ", "+")
    # url = f"https://news.google.com/rss/search?q={query}" PARA NOTICIAS INTERNACIONAIS
    RSS_URL = f"https://news.google.com/rss/search?q={query}+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt"

    # para vizualizar noticias internacionais, substitua o parametro do feedparser por (url)
    feed = feedparser.parse(RSS_URL) 

    noticias = []
    for entry in feed.entries[:3]:
        title = entry.title
        link = entry.link
        description = entry.get("summary", "")

    # resumo via Groq
        resumo = summarize_news_with_groq(title, description, link)

        noticias.append({
            "title": title,
            "link": link,
            "published": entry.published,
            "summary": resumo
        })

    return noticias

# ---------------------------
# FUNÇAO PARA O GROQ RESUMIR O ASSUNTO DA NOTICIA
# ---------------------------

def summarize_news_with_groq(title: str, description: str, link: str):
    prompt = f"""
    Resuma em português a seguinte notícia de forma objetiva e clara.
    Inclua contexto suficiente para alguém entender rapidamente do que se trata.

    Título: {title}
    Descrição: {description}
    Link: {link}

    Responda apenas com o resumo.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.1
    )

    return response.choices[0].message.content.strip()