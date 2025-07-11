
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Financeiro B3", layout="wide")
st.title("📈 Dashboard Fundamentalista - B3")

empresas = {
    "PETR4": "PETR4.SA",
    "ELET3": "ELET3.SA",
    "PRIO3": "PRIO3.SA",
    "RAIZ4": "RAIZ4.SA",
    "RRRP3": "RRRP3.SA",
    "VALE3": "VALE3.SA",
    "CSNA3": "CSNA3.SA",
    "GGBR4": "GGBR4.SA",
    "USIM5": "USIM5.SA",
    "CMIN3": "CMIN3.SA",
    "ITUB4": "ITUB4.SA",
    "BBDC4": "BBDC4.SA",
    "BBAS3": "BBAS3.SA",
    "SANB11": "SANB11.SA",
    "BPAC11": "BPAC11.SA",
    "MGLU3": "MGLU3.SA",
    "LREN3": "LREN3.SA",
    "AMER3": "AMER3.SA",
    "ARZZ3": "ARZZ3.SA",
    "VIIA3": "VIIA3.SA",
    "JBSS3": "JBSS3.SA",
    "BRFS3": "BRFS3.SA",
    "MRFG3": "MRFG3.SA",
    "RAIL3": "RAIL3.SA",
    "ABEV3": "ABEV3.SA"
}

selecionadas = st.multiselect("Selecione os ativos:", list(empresas.keys()), default=["PETR4", "VALE3", "ITUB4", "BBAS3", "BBDC4"])

def obter_dados_yfinance(tickers):
    df_final = pd.DataFrame()
    for nome, ticker in tickers.items():
        dados = yf.Ticker(ticker).info
        linha = {
            "Ticker": nome,
            "Empresa": dados.get("shortName", ""),
            "Setor": dados.get("sector", ""),
            "Preço Atual": dados.get("currentPrice", ""),
            "P/L": dados.get("trailingPE", ""),
            "ROE (%)": dados.get("returnOnEquity", "") * 100 if dados.get("returnOnEquity") else None,
            "Dividend Yield (%)": dados.get("dividendYield", "") * 100 if dados.get("dividendYield") else None
        }
        df_final = pd.concat([df_final, pd.DataFrame([linha])], ignore_index=True)
    return df_final

if selecionadas:
    tickers_selecionados = {k: empresas[k] for k in selecionadas}
    df = obter_dados_yfinance(tickers_selecionados)

    st.subheader("📊 Tabela de Indicadores")
    st.dataframe(df)

    st.subheader("📈 Comparação de Indicadores")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(df, x="Ticker", y="P/L", title="P/L por Empresa", text_auto=".2s")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(df, x="Ticker", y="ROE (%)", title="ROE (%) por Empresa", text_auto=".2s")
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(df, x="Ticker", y="Dividend Yield (%)", title="Dividend Yield (%) por Empresa", text_auto=".2s", color="Setor")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📌 Agrupamento por Setor (média dos indicadores)")
    if "Setor" in df.columns:
        agrupado = df.groupby("Setor")[["P/L", "ROE (%)", "Dividend Yield (%)"]].mean().reset_index()
        st.dataframe(agrupado)

        fig4 = px.bar(agrupado, x="Setor", y="ROE (%)", title="Média de ROE (%) por Setor", text_auto=".2s")
        st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Selecione ao menos um ativo para visualizar os dados.")
