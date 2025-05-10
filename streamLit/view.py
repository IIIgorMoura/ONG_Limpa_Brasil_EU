# pip install streamlit streamlit-option-menu
# comando execução: python -m streamlit run view.py

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Análise dos últimos anos de coleta de lixo', page_icon='♻️', layout='wide')

df = pd.read_excel('../DBs_tratados/somas_total_2013_2024.xlsx')

st.sidebar.header('Selecione os Filtros')

df_selecao = df.query('`ID Loja` in @lojas and Produto in @produtos')

def Home():
    st.title('Faturamento das Lojas')

    # # graficos e função da página
    # total_vendas = df['Quantidade'].sum()
    # media = df['Quantidade'].mean()
    # mediana = df['Quantidade'].median()

    # # trabalhar com colunas ou paginações usa st.columns
    # total1,total2,total3 = st.columns(3) # o numero deve ser == a quant de variaveis

    # # na coluna.. vai ter..
    # with total1:
    #     # .metric = indicadores rápidos
    #         # principais infos visíveis de forma rápida
    #         # aqueles indicadores tipo cards de info, total de venda = 400.000
    #         # cards rápidos
    #     st.metric('Total Vendido', value=int(total_vendas)) # da para colocar icones
        
    # with total2:
    #     st.metric('Média por Produto', value=f'{media:.1f}') # 1 num dps da ,

    # with total3:
    #     st.metric('Mediana', value=int(mediana))

    # st.markdown('---') # traçado para dar respiro visual na página

# mesmo padrão do matplotlib
def Graficos():
    # graph Bar, qnt prods/loja
    fig_barras = px.bar(
        df, # AJUSTAR PARA _SELEÇÃO
        x='Produto', 
        y='Quantidade', 
        color='ID Loja', # cada loja vai ter uma cor diferente
        barmode='group', # diferenciar lojas por cor (agrupando, msm loja, msm cor)
        title='Quantidade de Produtos Vendidos por Loja'
    )

    # graph linha com total de vendas por loja
    # fig_linha = px.line(
    #     df.groupby(['ID Loja']).sum(numeric_only=True).reset_index(),
    #     x='ID Loja',
    #     y='Quantidade',
    #     title='Total de Vendas por Loja'
    # )

    # graphs lado a lado usa: .columns tmb
    graf1 = st.columns(1)
    with graf1:
        st.plotly_chart(fig_barras, use_container_width=True)
    # with graf2:
    #     st.plotly_chart(fig_linha, use_container_width=True)

# se for usar varias telas
def sidebar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title='Menu',
            options=['Home', 'Gráficos'],
            icons=['house','bar-chart'], # icons/emojis padrão
            default_index=0
        )

    if selecionado == 'Home':
        Home()
        Graficos()
    elif selecionado == 'Graficos':
        Graficos()

sidebar()