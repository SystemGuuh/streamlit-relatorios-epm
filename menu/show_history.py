# menu/finances.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildShowHistory(oldShowHistory, newShowHistory):
    
    # Concatenar as colunas ESTABELECIMENTO
    df_combined = pd.concat([oldShowHistory['ESTABELECIMENTO'], newShowHistory['ESTABELECIMENTO']], ignore_index=True)
    # Transformar em um DataFrame
    df_combined = pd.DataFrame(df_combined, columns=['ESTABELECIMENTO'])

    row1 = st.columns([2.5,2.5,5])
    with row1[0]:
        filterData = filterCalendarComponent()
    with row1[1]:
        filterEstablishment = filterEstablishmentComponent(df_combined)
    
    oldShowHistory = function_apply_filter_date_establishment(oldShowHistory, filterData, filterEstablishment)
    newShowHistory = function_apply_filter_date_establishment(newShowHistory, filterData, filterEstablishment)

    tab = st.tabs(["Shows Antigos", "Shows Futuros"])
    with tab[0]:
        container1 = st.container(border=True)
        with container1: 
            plotDataframe(oldShowHistory, "Histórico de shows antigos")

    with tab[1]:
        container1 = st.container(border=True)
        with container1: 
            plotDataframe(newShowHistory, "Histórico de shows futuros")

class ShowHistory(Page):
    def render(self):
        buildShowHistory(self.data['oldShowHistory'],
                      self.data['newShowHistory'],)
