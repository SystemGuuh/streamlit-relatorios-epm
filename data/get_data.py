from data.functions import *
from data.queries import *
import pandas as pd

#user_id -> id do usário que fez login
#id -> id do usuário buscado

def get_geral_information_and_finances(id):
    return GET_PROPOSTAS_BY_ID(id)

def search_user_from_session(id):
    return get_search_user_from_session(id)

# Inicializa os valores de data
def initialize_data(id):

    # Dicionário com dados de entrada
    data = {
        'oldShowHistory': pd.DataFrame(),
        'newShowHistory': pd.DataFrame(),
        'exploreStages': pd.DataFrame(),
        'oportunites': pd.DataFrame(),
        'casting': pd.DataFrame(),
        'favorite': pd.DataFrame(),
        'generalFinances':pd.DataFrame(),
        'financeDash':pd.DataFrame(),
        'averageReviewHouseByArtist':pd.DataFrame(),
        'ByOccurrence':pd.DataFrame(),
        'downloadShowStatement':pd.DataFrame(),
        'showStatement':pd.DataFrame(),
        'weeklyFinances':pd.DataFrame(),
        'artistRanking':pd.DataFrame(),
        'reviewArtistByHouse':pd.DataFrame(),
        'averageReviewArtistByHouse':pd.DataFrame(),
        'reviewHouseByArtist':pd.DataFrame(),
        'operationalPerformace':pd.DataFrame(),
        'ByWeek':pd.DataFrame(),
        'allOperationalPerformaceByOccurrenceAndDate':pd.DataFrame(),
        'id':id
    }

    return data

def get_data_GeneralDash(data, id, inputDate=None, inputEstablishment=None):
    generalFinances = apply_filter_in_dataframe(GET_WEEKLY_FINANCES(id), inputDate, inputEstablishment)
    financeDash = apply_filter_in_dataframe(GET_GERAL_INFORMATION_AND_FINANCES(id), inputDate, inputEstablishment)
    averageReviewHouseByArtist = apply_filter_in_dataframe(GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id), inputDate, inputEstablishment)
    ByOccurrence = apply_filter_in_dataframe(get_report_by_occurrence(GET_ALL_REPORT_ARTIST_BY_OCCURRENCE_AND_DATE(id)), inputDate, inputEstablishment)
    showStatement = apply_filter_in_dataframe(GET_PROPOSTAS_BY_ID(id), inputDate, inputEstablishment)
    showStatement['DIA_DA_SEMANA'] = showStatement['DIA_DA_SEMANA'].apply(translate_day)
    financeDash['DIA_DA_SEMANA'] = financeDash['DIA_DA_SEMANA'].apply(translate_day)
    
    data['generalFinances'] = generalFinances
    data['financeDash'] = financeDash
    data['averageReviewHouseByArtist'] = averageReviewHouseByArtist
    data['ByOccurrence'] = ByOccurrence
    data['showStatement'] = showStatement
    
    return data

def get_data_ShowHistory(data, user_id,id):
    try:
        oldShowHistory = showhistory_old_show_history(id)
        data['oldShowHistory'] = oldShowHistory
    except Exception as e:
        data['oldShowHistory'] = pd.DataFrame()

    try:
        newShowHistory = showhistory_new_show_history(id)
        data['newShowHistory'] = newShowHistory
    except Exception as e:
        data['newShowHistory'] = pd.DataFrame()

    return data

def get_data_operational_performace(data, user_id,id):
    try:
        exploreStages = operational_explore_stages(id)
        data['exploreStages'] = exploreStages
    except Exception as e:
        data['exploreStages'] = pd.DataFrame()

    try:
        oportunites = operational_oportunities(id)
        data['oportunites'] = oportunites
    except Exception as e:
        data['oportunites'] = pd.DataFrame()

    try:
        casting = operational_casting(id)
        data['casting'] = casting
    except Exception as e:
        data['casting'] = pd.DataFrame()

    try:
        favorite = operational_favorite(id)
        data['favorite'] = favorite
    except Exception as e:
        data['favorite'] = pd.DataFrame()

    try:
        financeDash = operational_general_information_and_finance(id)
        data['financeDash'] = financeDash
    except Exception as e:
        data['financeDash'] = pd.DataFrame()

    try:
        ByOccurrence = get_report_by_occurrence(operational_report_by_occurence_and_date(id))
        data['ByOccurrence'] = ByOccurrence
    except Exception as e:
        data['ByOccurrence'] = pd.DataFrame()

    try:
        allOperationalPerformaceByOccurrenceAndDate = operational_performance(id)
        data['allOperationalPerformaceByOccurrenceAndDate'] = allOperationalPerformaceByOccurrenceAndDate
    except Exception as e:
        data['allOperationalPerformaceByOccurrenceAndDate'] = pd.DataFrame()

    try:
        operationalPerformace = get_report_artist(allOperationalPerformaceByOccurrenceAndDate)
        data['operationalPerformace'] = operationalPerformace
    except Exception as e:
        data['operationalPerformace'] = pd.DataFrame()

    try:
        ByWeek = get_report_artist_by_week(allOperationalPerformaceByOccurrenceAndDate)
        data['ByWeek'] = ByWeek
    except Exception as e:
        data['ByWeek'] = pd.DataFrame()
    
    return data

