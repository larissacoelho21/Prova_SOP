import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")
st.title("📊 Dashboard Financeiro - Amostra")

df = pd.read_csv("MS_Financial Sample.csv", sep=';', on_bad_lines='skip', encoding='utf-8-sig')
df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes

# Limpa e converte valores numéricos
for col in ['Sales', 'Profit', 'COGS']:
    df[col] = df[col].astype(str).str.replace(',', '').str.replace('$', '').str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Visão geral
st.header("📌 Primeiras linhas dos dados")
st.dataframe(df.head())

# Filtros
st.sidebar.header("🔎 Filtros")
segment_filter = st.sidebar.multiselect("Segmento:", options=sorted(df['Segment'].unique()), default=sorted(df['Segment'].unique()))
country_filter = st.sidebar.multiselect("País:", options=sorted(df['Country'].unique()), default=sorted(df['Country'].unique()))

# Aplicar filtros
filtered_df = df[(df['Segment'].isin(segment_filter)) & (df['Country'].isin(country_filter))]

# Verifica se há dados
if filtered_df.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros atuais.")
    st.stop()

# KPIs
st.header("📈 Indicadores Principais")
col1, col2, col3 = st.columns(3)
col1.metric("Receita Total", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Lucro Total", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Custo Total", f"${filtered_df['COGS'].sum():,.0f}")

# Gráficos
st.subheader("💼 Receita por Segmento")
fig_segment = px.bar(
    filtered_df.groupby('Segment', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False),
    x='Segment', y='Sales', title='Receita por Segmento', text_auto='.2s'
)
st.plotly_chart(fig_segment, use_container_width=True)

st.subheader("🌍 Receita por País")
fig_country = px.bar(
    filtered_df.groupby('Country', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False),
    x='Country', y='Sales', title='Receita por País', text_auto='.2s'
)
st.plotly_chart(fig_country, use_container_width=True)

st.subheader("📊 Lucro vs Receita por País")
scatter_data = filtered_df[['Sales', 'Profit', 'COGS', 'Country', 'Product']].dropna()
fig_scatter = px.scatter(
    scatter_data,
    x="Sales", y="Profit", color="Country",
    size="COGS", hover_name="Product",
    title="Lucro vs Receita (tamanho = Custo)"
)
st.plotly_chart(fig_scatter, use_container_width=True) 



