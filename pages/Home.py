import streamlit as st
import pandas as pd

from utils.components import *
from utils.functions import *
from utils.user import logout
from data.get_data import *

# modularização das páginas
from menu.general_dash import GeneralDashPage
from menu.finances import FinancesPage
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
    #user_id = st.session_state['user_data']["data"]["user_id"]
    #user_name = st.session_state['user_data']["data"]['full_name']
    user_id = 12345
    user_name = "Nome Usuário"

    if 'Search' not in st.session_state:
        st.session_state['Search'] = {'id': None}

    # Header
    with st.container(border=True):
        row1 = st.columns([2, 3, 1, 0.5, 0.5])
        with row1[0]:
            st.markdown("<p style='padding-top:0.4em'></p>", unsafe_allow_html=True)
            search_user = modalSearchComponent()
            
            if not search_user.empty and st.session_state['Search']['id'] is None:
                if search_user.shape[0] > 1:
                    modalChooseResultComponent(search_user)
                else:
                    st.session_state['Search']['id'] = search_user['ID'].loc[0]
            elif st.session_state['Search']['id'] is not None:
                search_user = search_user_from_session(st.session_state['Search']['id'])
                
            
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
    if not search_user.empty and st.session_state['Search']['id'] is not None:
        searchUserDataComponent(search_user)

    data = initialize_data(user_id)
    # Body
    tab1, tab2, tab3 = st.tabs(["OPERACIONAL", "HISTÓRICO DE SHOWS", "FINANCEIRO"])
    with tab1:
        #try:
            if not search_user.empty:
                search_user_id = search_user['ID'].loc[0]
                data = get_data_operational_performace(data, search_user_id)
                page = OperationalPerformacePage(data)
                page.render()
        #except Exception as e:
        #    st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab2:
        try:
            data = get_data_Finances(data, user_id, inputDate, inputEstablishment)
            page = FinancesPage(data)
            page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab3:
        try:
            data = get_data_Review(data, user_id, inputDate, inputEstablishment)
            page = ReviewPage(data)
            page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')

else:
    st.switch_page("main.py")
