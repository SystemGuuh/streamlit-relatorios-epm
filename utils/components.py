import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date
from streamlit_echarts import st_echarts
from utils.functions import *
from decimal import Decimal
import calendar

# resolve o bug de carregamento dos gráficos de echart
def fix_tab_echarts():
    streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 300px;} 
   </style>
    """

    return st.markdown(streamlit_style, unsafe_allow_html=True)

# Esconde a sidebar caso de problema no config
def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def plotDataframe(df, name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    st.dataframe(df, hide_index=True, use_container_width=True)

def plotPizzaChart(labels, sizes, name):
    chart_key = f"{labels}_{sizes}_{name}_"
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    
    # Preparar os dados para o gráfico
    data = [{"value": size, "name": label} for size, label in zip(sizes, labels)]
    
    options = {
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: {c} ({d}%)" 
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "top": "top", 
            "textStyle": {
                "color": "orange"
            }
        },
        "grid": {  # Adicionado para organizar o layout
            "left": "50%", 
            "right": "50%", 
            "containLabel": True
        },
        "series": [
            {
                "name": "Quantidade",
                "type": "pie",
                "radius": "75%",
                "center": ["75%", "45%"],  # Posiciona o gráfico no meio verticalmente
                "data": data,
                "label": {
                    "show": False  # Ocultar os textos nas fatias
                },
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }
    
    st_echarts(options=options, height="300px", key=chart_key)

def plotBarChart(df, xValue, yValue,name):
    chart_key = f"{xValue}_{yValue}_{name}"
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)

    if yValue == 'VALOR_GANHO_BRUTO':
        df = df.rename(columns={'VALOR_GANHO_BRUTO': 'VALOR INVESTIDO'})
        yValue = 'VALOR INVESTIDO'

    if yValue == 'VALOR_BRUTO':
        df = df.rename(columns={'VALOR_BRUTO': 'VALOR INVESTIDO'})
        yValue = 'VALOR INVESTIDO'
    
    if df[xValue].dtype == 'object':
        # Tentar converter os valores para o tipo datetime
        try:
            df_sorted = df.sort_values(by=xValue)
            df_sorted[xValue] = pd.to_datetime(df_sorted[xValue])
            df_sorted[xValue] = df_sorted[xValue].dt.strftime('%d/%m/%Y')
        except ValueError:
            df_sorted = df

    options = {
        "xAxis": {
            "type": "category",
            "data": df_sorted[xValue].tolist(),
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": yValue,
                "data": df_sorted[yValue].tolist(),
                "type": "bar",
                "itemStyle": {
                    "color": "#ff6600"
                },
                "barWidth": "50%"  # Ajuste a largura das colunas aqui
            }
        ],
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "legend": {
            "data": [yValue],
            "textStyle": {
                "color": "#808080"
            }
        }
    }
    
    st_echarts(options=options, height="300px", key=chart_key)

# Modal de busca
def modalSearchComponent():
    with st.popover("Buscar", use_container_width=False):
        search = {}
        with st.expander("Artista"):
            search['ArtistId'] = st.text_input(label='Buscar artista por id', placeholder="Buscar por ID", value=None, max_chars=255, label_visibility="collapsed")
            search['ArtistName'] = st.text_input(label='Buscar artista por nome',placeholder="Buscar por Nome", value=None, max_chars=255, label_visibility="collapsed")
            search['ArtistEmail'] = st.text_input(label='Buscar artista por email', placeholder="Buscar por E-mail", value=None, max_chars=255, label_visibility="collapsed")
            search['ArtistPhone'] = st.text_input(label='Buscar artista por telefone', placeholder="Buscar por Telefone", value=None, max_chars=255, label_visibility="collapsed")
            
        with st.expander("Estabelecimento"):
            search['EstablishmentId'] = st.text_input(label='Buscar estabelecimento por id', placeholder="Buscar por ID", value=None, max_chars=255, label_visibility="collapsed")
            search['EstablishmentName'] = st.text_input(label='Buscar estabelecimento por nome', placeholder="Buscar por Nome", value=None, max_chars=255, label_visibility="collapsed")
            search['EstablishmentEmail'] = st.text_input(label='Buscar estabelecimento por email', placeholder="Buscar por E-mail", value=None, max_chars=255, label_visibility="collapsed")
            search['EstablishmentPhone'] = st.text_input(label='Buscar estabelecimento por telefone', placeholder="Buscar por Telefone", value=None, max_chars=255, label_visibility="collapsed")

        if st.button("Procurar"):
                return function_search_user(search)
        else:
            return pd.DataFrame()

# Modal para quando há mais de um resultado de busca
@st.experimental_dialog("Opa, mais de um resultado encontrado!")
def modalChooseResultComponent(result):
    st.write('Escolha um:')
    for index, row in result.iterrows():
        if st.button(f"ID: {row['ID']} | Nome: {row['NOME']}", key=index):
            st.session_state['Search']['ID'] = row['ID']
            st.session_state['Search']['FULL_NAME'] = str(row['FULL_NAME'])
            st.session_state['Search']['NOME'] = str(row['NOME'])
            st.session_state['Search']['LOGIN'] = str(row['LOGIN'])
            st.session_state['Search']['CELULAR'] = str(row['CELULAR'])
            st.rerun()

# Mostra os dados do artista buscado na nav
def searchUserDataComponent(user):
    with st.container(border=True):
        row1 = st.columns([2.5,2.5,2.5,2.5, 0.5])

        with row1[0]:
            st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Nome: {str(user['FULL_NAME'].loc[0])}</p>", unsafe_allow_html=True)
        with row1[1]:
            st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Projeto: {str(user['NOME'].loc[0])}</p>", unsafe_allow_html=True)
        with row1[2]:
            st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>E-mail: {str(user['LOGIN'].loc[0])}</p>", unsafe_allow_html=True)
        with row1[3]:
            st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Celular: {str(user['CELULAR'].loc[0])}</p>", unsafe_allow_html=True)
        with row1[4]:
            if st.button('X'):
                st.session_state['Search']['ID'] = None
                st.session_state['Search']['FULL_NAME'] = None
                st.session_state['Search']['NOME'] = None
                st.session_state['Search']['LOGIN'] = None
                st.session_state['Search']['CELULAR'] = None
                st.rerun()

def filterReportType(df):
    df = df.sort_values(by='TIPO')
    option = st.selectbox("Tipo de ocorrência:",(df['TIPO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def filterReportArtist(df):
    df = df.sort_values(by='ARTISTA')
    option = st.selectbox("Buscar artista:",(df['ARTISTA'].unique()),
            index=None, placeholder="Selecione um artista")
    return option

def buttonDowloadDash(df, name):
    button_key = f"_{name}_"
    st.download_button(
    label='Baixar em Excel',
    data=to_excel(df),
    file_name=f"{name}.xlsx",
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    key=button_key
    )
