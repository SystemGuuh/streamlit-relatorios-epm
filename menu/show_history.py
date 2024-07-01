# menu/finances.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildShowHistory(oldShowHistory, newShowHistory):

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
