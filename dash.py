import streamlit as st
import pandas as pd 
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao
#Isso garante que o Python execute o Streamlit diretamente, independentemente do caminho do sistema.***** python -m streamlit run dash.py *****

# PRIMEIRA CONSULTA / ATUALIZAÇÕES DOS DADOS 
# CONSULTA OS DADOS
query = "SELECT * FROM tb_carro"

# CARREGAR OS DADOS 
df = conexao(query)

# BOTÃO PARA ATUALIZAR
if st.button("Atualizar Dados"):
    df = conexao(query)

# ESTRUTURA LATERAL DE FILTROS
st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada",  # NOME DO SELETOR
                               options=df["marca"].unique(),  # OPÇÃO DO DF
                               default=df["marca"].unique()  # as marcas pré-definidas
                               )

modelo = st.sidebar.multiselect("Modelo Selecionado",  # NOME DO SELETOR
                               options=df["modelo"].unique(),  # OPÇÃO DO DF
                               default=df["modelo"].unique()  # os modelos pré-definidos
                               )

ano = st.sidebar.multiselect("Ano Selecionado",  # NOME DO SELETOR
                               options=df["ano"].unique(),  # OPÇÃO DO DF
                               default=df["ano"].unique()  # os anos pré-definidos
                               )

valor = st.sidebar.multiselect("Valor Selecionado",  # NOME DO SELETOR
                               options=df["valor"].unique(),  # OPÇÃO DO DF
                               default=df["valor"].unique()  # os valores pré-definidos
                               )

cor = st.sidebar.multiselect("Cor Selecionada",  # NOME DO SELETOR
                               options=df["cor"].unique(),  # OPÇÃO DO DF
                               default=df["cor"].unique()  # as cores pré-definidas
                            )

numero_vendas = st.sidebar.multiselect("Número de Vendas Selecionado",  # NOME DO SELETOR
                               options=df["numero_vendas"].unique(),  # OPÇÃO DO DF
                               default=df["numero_vendas"].unique()  # vendas pré-definidas
                                        )                                
    
# Aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas))
]

# EXIBIR VALORES MÉDIOS - ESTATÍSTICAS
def Home():
    with st.expander("Tabela"):  # CRIA UMA CAIXA EXPANSÍVEL COM UM TÍTULO
        mostrar_dados = st.multiselect('Filtrar Colunas:', df_selecionado.columns.tolist(), default=df_selecionado.columns.tolist())

        # VERIFICAR SE O USUÁRIO SELECIONOU COLUNAS PARA EXIBIR
        if mostrar_dados: 
            st.write(df_selecionado[mostrar_dados])  # Exibir os dados filtrados pelas colunas selecionadas

    # VERIFICAR SE O DATAFRAME FILTRADO (df_selecionado) NÃO ESTÁ VAZIO
    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()

        # Exibir as estatísticas
        #st.write(f"**Total de Vendas:** {venda_total}")
        #st.write(f"**Média de Vendas:** {venda_media}")
        #st.write(f"**Mediana de Vendas:** {venda_mediana}")

        # Exibir as estatísticas
        total1, total2, total3 = st.columns(3, gap= "large")

        with total1:
            st.info("Valor Total de Vendas dos Carros", icon="📊")
            st.metric(label="total", value=f"{venda_total:,.0f}")
        
        with total2:
            st.info("Valor Total de Vendas dos Carros", icon="📊")
            st.metric(label="Media", value=f"{venda_media:,.0f}")

        with total3:
            st.info("Valor Total de Vendas dos Carros", icon="📊")
            st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")

    else:
        st.warning("Nenhum dados disponinel com os filtros selecionados")
#inseri uma linha divisoria para separar as secoes 
    st.markdown("""--------""")

def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dados disponivel para gerar graficos ")
        #INTERROMPE A FUNCAO PQ NAO MOTIVOS PRA CONTINUA EXECUTANDO SE N TEM DADOS
        return
    
    ### ###
    """ CRIAR DOS GRAFICOS
    4 ABAS -> GRAFICOS DE BARRAS, GRAFICO DE LINHAS, GRAFICO PIZZA E DISPERSAO
    """
    graf1, graf2, graf3, graf4 = st.tabs(["Graficos de Barras", "Graficos de Linhas", "Graficos de Pizza", "Graficos de Dispersao"])





    
# Chamar a função Home para renderizar os dados
Home()
