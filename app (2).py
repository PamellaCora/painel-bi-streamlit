
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel BI - Asimov", layout="wide")

st.title("Painel de Análise de Dados - Asimov")

# Carregando os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dataset_asimov.csv")

df = carregar_dados()

st.subheader("Visualização da Tabela de Dados")
st.dataframe(df)

# Filtros dinâmicos
colunas_numericas = df.select_dtypes(include='number').columns.tolist()
colunas_categoricas = df.select_dtypes(exclude='number').columns.tolist()

with st.sidebar:
    st.header("Filtros")
    filtros = {}
    for col in colunas_categoricas:
        valores = df[col].dropna().unique().tolist()
        selecao = st.multiselect(f"{col}", valores, default=valores)
        filtros[col] = selecao

    df_filtrado = df.copy()
    for col, selecao in filtros.items():
        df_filtrado = df_filtrado[df_filtrado[col].isin(selecao)]

st.subheader("Gráficos")

if colunas_numericas:
    col1, col2 = st.columns(2)

    with col1:
        col_x = st.selectbox("Eixo X (Numérico)", colunas_numericas, key="x1")
        col_y = st.selectbox("Eixo Y (Numérico)", colunas_numericas, key="y1")
        fig1 = px.scatter(df_filtrado, x=col_x, y=col_y, title=f"Dispersão: {col_x} vs {col_y}")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        col_hist = st.selectbox("Histograma de", colunas_numericas, key="hist")
        fig2 = px.histogram(df_filtrado, x=col_hist, title=f"Histograma de {col_hist}")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("O dataset não possui colunas numéricas para visualização gráfica.")
