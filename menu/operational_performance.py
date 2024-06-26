# menu/operational_performance.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildOperationalPerformace(oldShowHistory, newShowHistory, exploreStages, oportunites, casting, favorite, operationalPerformace, ByOccurrence, ByWeek, allOperationalPerformaceByOccurrenceAndDate, financeDash):
    tab= st.tabs(["Histórico de shows", "Explorar palcos", "Artístico", "Resumos de ocorrências", "Extrato de ocorrências"])
    
    with tab[0]:
        plotDataframe(oldShowHistory, "Histórico de shows antigos")
        plotDataframe(newShowHistory, "Histórico de shows futuros")

    with tab[1]:
        plotDataframe(exploreStages, "Explorar palcos do artista")
        plotDataframe(oportunites, "Oportunidades do artista")

    with tab[2]:
        plotDataframe(casting, "Casting do artista")
        plotDataframe(favorite, "Casas em que o artista está favoritado")
        
    with tab[3]:
        container1 = st.container(border=True)
        container2 = st.container(border=True)
        with container1: 
            row1 = st.columns(2)
            with row1[0]:
                plotPizzaChart(ByOccurrence['TIPO'], ByOccurrence['QUANTIDADE'], "Tipos de Ocorrências")
                plotBarChart(ByWeek, 'SEMANA', 'QUANTIDADE', "Quantidade de ocorrêcias por semana")
            with row1[1]:
                st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>Ranking de artistas com mais ocorrências</h5>", unsafe_allow_html=True)
                st.dataframe(operationalPerformace[['RANKING','ARTISTA', 'ESTILO','QUANTIDADE']].reset_index(drop=True), hide_index=True,use_container_width=True, height=735)

        with container2:    
            plotDataframe(transform_show_statement(financeDash), "Quantidade de checkin e checkout por artista")
    
    with tab[4]:
        # removendo valores e reodernando o dataset
        allOperationalPerformaceByOccurrenceAndDate.drop(columns=['SEMANA'], inplace=True)
        allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[['ARTISTA', 'ESTILO','ESTABELECIMENTO','DATA','TIPO']]
        allOperationalPerformaceByOccurrenceAndDate['DATA'] = allOperationalPerformaceByOccurrenceAndDate['DATA'].apply(lambda x: x.strftime('%d/%m/%Y') if not pd.isnull(x) else None)
        
        row1 = st.columns(6)
        with row1[0]:
            type = filterReportType(allOperationalPerformaceByOccurrenceAndDate)
        with row1[1]:
            art = filterReportArtist(allOperationalPerformaceByOccurrenceAndDate)
        with row1[5]:
            st.write('') # alinhar botão
            st.write('') # alinhar botão
            buttonDowloadDash(allOperationalPerformaceByOccurrenceAndDate, "Extrato-de-Ocorrencias")
        container = st.container(border=True)
        with container:
            if type is not None:
                allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[allOperationalPerformaceByOccurrenceAndDate['TIPO']==type]
            if art is not None:
                allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[allOperationalPerformaceByOccurrenceAndDate['ARTISTA']==art]

            plotDataframe(allOperationalPerformaceByOccurrenceAndDate, "Relatório completo de ocorrências")
    pass

class OperationalPerformacePage(Page):
    def render(self):
        buildOperationalPerformace(
                                   self.data['oldShowHistory'],
                                   self.data['newShowHistory'],
                                   self.data['exploreStages'],
                                   self.data['oportunites'],
                                   self.data['casting'],
                                   self.data['favorite'],
                                   self.data['operationalPerformace'],  
                                   self.data['ByOccurrence'], 
                                   self.data['ByWeek'],  
                                   self.data['allOperationalPerformaceByOccurrenceAndDate'], 
                                   self.data['financeDash'])
