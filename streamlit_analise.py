import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações  iniciais
st.set_page_config(page_title="Dashboard - Coleta de Lixo", page_icon="♻️", layout="wide")

# Carregar dados
df_soma = pd.read_excel('./.streamlit/somas_total_2013_2024.xlsx')
df_tipos = pd.read_excel('./.streamlit/tipo_residuos_total.xlsx')

df_tipos_melt = df_tipos.melt(id_vars='tipo_residuo', 
    value_vars=['total_2013', 'total_2014', 'total_2015', 'total_2016', 'total_2017', 'total_2018', 'total_2019', 'total_2020', ], 
    var_name='ano', 
    value_name='Distribuição tipo de lixo')

def aplicar_estilo():
    with open("./.streamlit/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
aplicar_estilo()
# FILTROS
# Sidebar   
st.sidebar.header("Selecione os Filtros")


tipo_residuo = st.sidebar.multiselect(
    "Tipos de resíduo",
    # Seleciona os 10 maiores tipos de resíduos com base em uma coluna numérica relevante
    options=df_tipos.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Define como padrão os mesmos 10 maiores tipos
    default=df_tipos.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Chave única
    key='tipo'
)



# Filtrar o Dataframe com as opções selecionadas
df_selecao = df_tipos.query("tipo_residuo in @tipo_residuo")
df_selecao_tipos_melt = df_tipos_melt.query("tipo_residuo in @tipo_residuo")

# Graficos e na função da página
def Home():
    st.title('Coleta de lixo de 2013 a 2024')

    total_vendas = df_soma['soma_total_em_KT'].sum()
    media = df_soma['soma_total_em_KT'].mean()
    mediana = df_soma['soma_total_em_KT'].median()

    total1, total2, total3= st.columns(3)
    with total1:
        # Apresentrar indicadores rápidos
        st.metric('Total coletado', value=f"{total_vendas:.2f}")
    with total2:
        st.metric('Média de coleta', value=f"{media:.2f}")
    with total3:
        st.metric('Mediana de coleta', value=f"{mediana:.2f}")

    st.markdown('- - -')



def Graficos():
    # Criar um grafico de barras
    # Mostrando a quant de produtos por lojas

    fig_barras = px.bar(
        df_selecao,
        x="total_anos",
        y="tipo_residuo",
        color="tipo_residuo",
        title="Quantidade de Resíduos por ano"
    )
    #Grafico de linha
    # Total de vendas por Loja

    fig_linha = px.line(
        df_soma.groupby(["ano"]).sum(numeric_only=True).reset_index(),
        x= 'ano',
        y='soma_total_em_KT',
        title='Total de lixo coletado de 2013 a 2024'

    )

    fig_barras_empilhadas = px.bar(
        df_selecao_tipos_melt,
        x='ano',
        y='Distribuição tipo de lixo',
        color="tipo_residuo",
        title='Distribuição de Lixo por Tipo de 2013 a 2020',
        labels={'Distribuição tipo de lixo': 'Quantidade de Lixo'},
        barmode='stack'

        # inserir nota falando do pq n tem até 2024 e apelação tipo (pq vc acha q ta faltando?)
    )

    graf1, graf2 = st.columns(2)
    with graf1:
        st.plotly_chart(fig_barras,  use_container_width=True )
    with graf2:
        st.plotly_chart(fig_linha,  use_container_width=True )

    graf3, = st.columns(1)
    with graf3:
        st.plotly_chart(fig_barras_empilhadas, use_container_width=True)


def sideBar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title="Menu",
            options=['Home', 'Gráficos'],
            icons=['house', 'bar-chart'],
            default_index=0
        )

    if selecionado == 'Home':
        Home()
        Graficos()
    elif selecionado == 'Gráficos':
        Graficos()

sideBar()

# python -m streamlit run analise.py



