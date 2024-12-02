import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

file_path = "Od/Dados/user_behavior_dataset342.csv"
df = pd.read_csv(file_path)

st.title("Dashboard Interativo: Comportamento de Uso de Dispositivos")

st.write("### Dados Brutos")
st.dataframe(df)

st.sidebar.header("Filtros")
sistema_operacional = st.sidebar.multiselect(
    "Sistema Operacional",
    options=df["Sistema Operacional"].unique(),
    default=df["Sistema Operacional"].unique(),
)

gênero = st.sidebar.multiselect(
    "Gênero",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
)

df_filtered = df[
    (df["Sistema Operacional"].isin(sistema_operacional)) &
    (df["Gender"].isin(gênero))
]

st.write(f"### Dados Filtrados ({len(df_filtered)} registros)")
st.dataframe(df_filtered)

st.write("### Visualizações")

st.write("**Distribuição por Sistema Operacional**")
fig, ax = plt.subplots()
df_filtered["Sistema Operacional"].value_counts().plot.bar(ax=ax, color='skyblue')
ax.set_title("Número de Usuários por Sistema Operacional")
ax.set_ylabel("Quantidade")
st.pyplot(fig)

st.write("**Relação entre Tempo de Tela Ligada e Drenagem de Bateria**")
fig, ax = plt.subplots()
scatter = ax.scatter(
    df_filtered["Tempo de tela ligada (horas/dia)"],
    df_filtered["Drenagem da bateria (mAh/dia)"],
    c=df_filtered["Idade"],
    cmap='viridis',
    alpha=0.7
)
ax.set_xlabel("Tempo de Tela Ligada (horas/dia)")
ax.set_ylabel("Drenagem de Bateria (mAh/dia)")
ax.set_title("Dispersão: Tempo de Tela Ligada vs. Drenagem de Bateria")
fig.colorbar(scatter, ax=ax, label="Idade")
st.pyplot(fig)

st.write("**Uso de Dados por Idade**")
fig, ax = plt.subplots()
df_filtered.groupby("Idade")["Uso de dados (MB/dia)"].mean().plot(ax=ax, marker='o')
ax.set_title("Média de Uso de Dados por Idade")
ax.set_ylabel("Uso de Dados (MB/dia)")
ax.set_xlabel("Idade")
st.pyplot(fig)

st.write("### Estatísticas Descritivas")
st.write(df_filtered.describe())
