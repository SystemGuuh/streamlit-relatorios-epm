import pandas as pd
import streamlit as st
from io import BytesIO
from utils.functions import *
from data.queries import *

# Esconde a sidebar caso de problema no config
def function_hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

# resolve o bug de carregamento dos gráficos de echart
def function_fix_tab_echarts():
    streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 300px;} 
   </style>
    """
    return st.markdown(streamlit_style, unsafe_allow_html=True)

# função para procurar usuários:
def function_search_user(search):
    if any(value for value in search.values() if value):
        if search['ArtistId']: return search_artist_id("WHERE TA.ID = '" + str(search['ArtistId']) + "'")
        if search['ArtistName']: return search_artist_id("WHERE TA.NOME = '" + str(search['ArtistName']) + "'")
        if search['ArtistEmail']: return search_artist_id("WHERE AU.LOGIN = '" + str(search['ArtistEmail']) + "'")
        if search['ArtistPhone']: return search_artist_id("WHERE TA.CELULAR = '" + str(search['ArtistPhone']) + "'")
        if search['EstablishmentId']: return search_establishment_id()
        if search['EstablishmentName']: return search_establishment_id()
        if search['EstablishmentEmail']: return search_establishment_id()
        if search['EstablishmentPhone']: return search_establishment_id()
    else:
        st.markdown('<p style="color:#B22222;">*Preencha pelo menos um campo.</p>', unsafe_allow_html=True)
        return pd.DataFrame()

# conta o checkin e checkout para a tela de Desempenho Operacional
def transform_show_statement(df):
    # Filtrar apenas as linhas que têm "Checkout Realizado" ou "Checkin Realizado" na coluna "STATUS_PROPOSTA"
    df_filtered = df
    
    # Inicializar colunas para armazenar a contagem
    df_filtered['CHECKIN_REALIZADO'] = 0
    df_filtered['CHECKOUT_REALIZADO'] = 0

    # Atualizar as colunas com base no valor de 'STATUS_PROPOSTA'
    df_filtered.loc[df_filtered['STATUS_PROPOSTA'] == 'Checkin Realizado', 'CHECKIN_REALIZADO'] = 1
    df_filtered.loc[df_filtered['STATUS_PROPOSTA'] == 'Checkout Realizado', 'CHECKOUT_REALIZADO'] = 1

    # Agrupar por 'ARTISTA' e contar o número de ocorrências
    grouped = df_filtered.groupby('ARTISTA').agg({
        'STATUS_PROPOSTA': 'size',  # Conta o número de ocorrências (número de shows)
        'CHECKIN_REALIZADO': 'sum',
        'CHECKOUT_REALIZADO': 'sum'
    }).reset_index()

    grouped['CHECKIN_REALIZADO'] = (((grouped['CHECKIN_REALIZADO'] + grouped['CHECKOUT_REALIZADO'])*100)/grouped['STATUS_PROPOSTA']).map("{:.2f}%".format)
    grouped['CHECKOUT_REALIZADO'] = ((grouped['CHECKOUT_REALIZADO']*100)/grouped['STATUS_PROPOSTA']).map("{:.2f}%".format)
    
    # Renomear as colunas para refletir o que foi pedido
    grouped.rename(columns={
        'STATUS_PROPOSTA': 'NÚMERO DE SHOWS',
        'CHECKIN_REALIZADO': 'PORCENTAGEM DE CHECKIN(%)',
        'CHECKOUT_REALIZADO': 'PORCENTAGEM DE CHECKOUT(%)'
    }, inplace=True)

    return grouped.sort_values(by='NÚMERO DE SHOWS', ascending=False)

# Função para converter o arquivo para excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


