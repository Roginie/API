import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

# Consulta os dados
query = "SELECT * FROM tb_carro"
df = conexao(query)

# Botão para atualizar os dados
if st.button("Atualizar Dados"):
    df = conexao(query)

# Estrutura lateral de filtros
st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada",
                               options=df["marca"].unique(),
                               default=df["marca"].unique())

modelo = st.sidebar.multiselect("Modelo Selecionado",
                                options=df["modelo"].unique(),
                                default=df["modelo"].unique())

ano = st.sidebar.multiselect("Ano Selecionado",
                             options=df["ano"].unique(),
                             default=df["ano"].unique())

valor = st.sidebar.multiselect("Valor Selecionado",
                               options=df["valor"].unique(),
                               default=df["valor"].unique())

cor = st.sidebar.multiselect("Cor Selecionada",
                             options=df["cor"].unique(),
                             default=df["cor"].unique())

numero_vendas = st.sidebar.multiselect("Número de Vendas Selecionado",
                                       options=df["numero_vendas"].unique(),
                                       default=df["numero_vendas"].unique())

# Aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas))
]

# Exibir valores médios e estatísticas
def Home():
    with st.expander("Tabela"):
        mostrar_dados = st.multiselect('Filtrar Colunas:', df_selecionado.columns.tolist(), default=df_selecionado.columns.tolist())
        if mostrar_dados:
            st.write(df_selecionado[mostrar_dados])

    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()

        total1, total2, total3 = st.columns(3, gap="large")

        with total1:
            st.info("Valor Total de Vendas", icon="📊")
            st.metric(label="Total", value=f"{venda_total:,.0f}")

        with total2:
            st.info("Média de Vendas", icon="📊")
            st.metric(label="Média", value=f"{venda_media:,.0f}")

        with total3:
            st.info("Mediana de Vendas", icon="📊")
            st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")

    else:
        st.warning("Nenhum dado disponível com os filtros selecionados")

    st.markdown("""--------""")

# Função para os gráficos
def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dado disponível para gerar gráficos.")
        return

    graf1, graf2, graf3, graf4, graf5 = st.tabs(["Gráfico de Barras", "Gráfico de Linhas", "Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico Horizontal"])


    with graf1:
        st.write("Gráfico de Barras")
        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
        fig_valores = px.bar(investimento,
                             x=investimento.index,
                             y="valor",
                             orientation="h",
                             title="<b>Valores de Carros</b>",
                             color_discrete_sequence=["#0083b3"])
        st.plotly_chart(fig_valores, use_container_width=True)

    with graf2:
        st.write("Gráfico de Linhas")
        dados = df_selecionado.groupby("marca")[["valor"]].sum()
        fig_valores2 = px.line(dados,
                               x=dados.index,
                               y="valor",
                               title="<b>Valor por Marca</b>")
        st.plotly_chart(fig_valores2, use_container_width=True)

    with graf3:
        st.write("Gráfico de Pizza")
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]

        fig_valores3 = px.pie(dados2,
                              values="valor",
                              names=dados2.index,
                              title="<b>Distribuição de valores por Marca</b>")
        st.plotly_chart(fig_valores3, use_container_width=True)

    with graf4:
        st.write("Gráfico de Dispersão")
        fig_valores4 = px.scatter(df_selecionado,
                                  x="marca",
                                  y="valor",
                                  size="numero_vendas",
                                  color="cor",
                                  title="<b>Dispersão de Valores por Marca</b>")
        st.plotly_chart(fig_valores4, use_container_width=True)

    with graf5:
        st.write("Gráfico de Barras Horizontais")
        dados_barras = df_selecionado.groupby("marca").sum()[["valor"]]
        fig_horizontais = px.bar(dados_barras,
                             x="valor",
                             y=dados_barras.index,
                             orientation='h',
                             title="<b>Valores por Marca - Barras Horizontais</b>")
        st.plotly_chart(fig_horizontais, use_container_width=True)




def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    object = 200000
    percentual = round((valorAtual / object * 100))


    if percentual > 100:
        st.subheader("Valores Antingidos!!!")

    else:
        st.write(f"Voce tem {percentual}% de {object}. Corra atras filhao!")

        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, tex="Alvo %")

#***************MENU LATERAL****************

def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home", "progresso"],
        icons=["house", "eye"], menu_icon="cast",
        default_index=0)

    if selecionado == "Home":
        st.subheader(f"Pagina:{selecionado}")
        Home()
        graficos(df_selecionado)

    if selecionado == "progresso":
        st.subheader(f"Pagina:{selecionado}")
        barraprogresso()
        graficos(df_selecionado)




menuLateral()
