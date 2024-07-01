import streamlit as st
import pandas as pd

from utils.components import *
from utils.functions import *
from utils.user import logout
from data.get_data import *

# modularização das páginas
from menu.general_dash import GeneralDashPage
from menu.show_history import ShowHistory
from menu.reviews import ReviewPage
from menu.operational_performance import OperationalPerformacePage
from menu.show_statement import ShowStatementPage

st.set_page_config(
    page_title="Home | Projetos Eshows",
    page_icon="./assets/imgs/eshows-logo100x100.png",
    layout="wide",
)

function_hide_sidebar()
function_fix_tab_echarts()

if 'loggedIn' not in st.session_state:
    st.switch_page("main.py")

if st.session_state['loggedIn']:
    user_id = st.session_state['user_data']["data"]["user_id"]
    user_name = st.session_state['user_data']["data"]['full_name']
    

    if 'Search' not in st.session_state:
        st.session_state['Search'] = {'ID': None,
        'FULL_NAME' : None,
        'NOME' : None,
        'LOGIN' : None,
        'CELULAR' : None
        }

    # Header
    with st.container(border=True):
        row1 = st.columns([2, 3, 1, 0.5, 0.5])
        with row1[0]:
            st.markdown("<p style='padding-top:0.4em'></p>", unsafe_allow_html=True)
            search_user = modalSearchComponent()
            
            # lógica salvar o id do usuário buscado na sessão ou trocar caso feita outra busca
            if not search_user.empty:
                if search_user.shape[0] > 1:
                    modalChooseResultComponent(search_user)
                else:
                    st.session_state['Search']['ID'] = search_user['ID'].loc[0]
                    st.session_state['Search']['FULL_NAME'] = str(search_user['FULL_NAME'].loc[0])
                    st.session_state['Search']['NOME'] = str(search_user['NOME'].loc[0])
                    st.session_state['Search']['LOGIN'] = str(search_user['LOGIN'].loc[0])
                    st.session_state['Search']['CELULAR'] = str(search_user['CELULAR'].loc[0])
            elif st.session_state['Search']['ID'] is not None and search_user.empty:
                search_user = search_user_from_session(st.session_state['Search']['ID'])
                
        with row1[1]:
            st.markdown("<h2 style='text-align: center;'>Informações dos projetos</h2>", unsafe_allow_html=True)
        
        with row1[3]:
            st.image("./assets/imgs/eshows100x100.png")
        
        with row1[4]:
            st.markdown("<p style='padding-top:0.4em'></p>", unsafe_allow_html=True)
            if st.button("Logout"):
                logout()
                st.switch_page("main.py")
    
    # Nav
    if not search_user.empty: searchUserDataComponent(search_user)

    data = initialize_data(user_id)
    # Body
    tab1, tab2, tab3 = st.tabs(["OPERACIONAL", "HISTÓRICO DE SHOWS", "FINANCEIRO"])
    search_user_id = st.session_state['Search']['ID']
    with tab1:
        try:
            if st.session_state['Search']['ID'] is not None:
                data = get_data_operational_performace(data, user_id, search_user_id)
                page = OperationalPerformacePage(data)
                page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab2:
        #try:
            data = get_data_ShowHistory(data, user_id, search_user_id)
            page = ShowHistory(data)
            page.render()
        #except Exception as e:
        #    st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab3:
        try:
            data = get_data_Review(data, user_id, inputDate, inputEstablishment)
            page = ReviewPage(data)
            page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')

else:
    st.switch_page("main.py")
