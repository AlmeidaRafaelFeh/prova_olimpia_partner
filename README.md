# Aplicativo Filtro de Busca de Mercado Aberto (Olimpia Partner)

Este documento descreve a aplicação desenvolvida como parte da prova proposta pela Olimpia Partner. O objetivo principal é criar um aplicativo que implemente um filtro de busca para empresas com capital aberto, agregando e correlacionando dados financeiros e informativos relevantes para o usuário.

🎯 Objetivo da Aplicação
O aplicativo visa oferecer aos usuários uma ferramenta de busca intuitiva para analisar empresas de capital aberto. O filtro de busca foi concebido para correlacionar os seguintes grupos de informações, fornecendo uma visão 360° do ativo, resultando em um resumo construido pelo cloud.

Como rodar a aplicação;

Apos fazer o clone do repositório, siga os passos abaixo.

1 - Dentro do arquivo app.py, na linha 20 cole o endereço da sua api key 
nessa linha : client = Groq(api_key="digite sua API_Key")  
endereço para pegar uma chave gratis :(https://console.groq.com/keys)
    
2 - python3 -m venv venv

3 - source venv/bin/activate

4 - pip install -r requirements.txt

5 - streamlit run streamlit.py

Obs.: caso apareça algum conflito ou erro com o venv, remova o venv e o pycache 
utilizando o comando rm -rf <nome do arquivo>
