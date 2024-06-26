import streamlit as st
import pandas as pd
from data.queries import *

# Filtro de estabelecimento dataframes
def apply_filter_artist_in_dataframe(df, artist):
    if artist is not None:
        try:
            df = df[df['ESTABELECIMENTO'] == artist]
        except:
            return df
    return df

# Chamas as funções de filtro
def apply_filter_in_dataframe(df, artist):
    df = apply_filter_artist_in_dataframe(df, artist)
    return df

# Gerando dados de reclamações por artista
def get_report_artist(df):
    df['QUANTIDADE'] = df.groupby('ARTISTA')['ARTISTA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['ARTISTA'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    df_grouped['RANKING'] = df_grouped['QUANTIDADE'].rank(method='first', ascending=False).astype(int)
    df_grouped = df_grouped.reset_index(drop=True)

    return df_grouped

# Agrupa dataframe por semana e cria um campo quantidade para colocar valores
def get_report_artist_by_week(df):
    df['QUANTIDADE'] = df.groupby('SEMANA')['SEMANA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['SEMANA'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    return df_grouped

# Agrupa por ocorrência
def get_report_by_occurrence(df):
    df['QUANTIDADE'] = df.groupby(['TIPO'])['ARTISTA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['TIPO'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    return df_grouped