from data.functions import *
from data.queries import *
import pandas as pd

    
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

def get_data_Finances(data, id, inputDate=None, inputEstablishment=None):
    weeklyFinances = apply_filter_in_dataframe( GET_WEEKLY_FINANCES(id), inputDate, inputEstablishment)
    
    data['weeklyFinances'] = weeklyFinances

    return data

def get_data_Review(data, id, inputDate=None, inputEstablishment=None):
    artistRanking = apply_filter_in_dataframe(GET_ARTIST_RANKING(id), inputDate, inputEstablishment)
    reviewArtistByHouse = apply_filter_in_dataframe(GET_REVIEW_ARTIST_BY_HOUSE(id), inputDate, inputEstablishment)
    averageReviewArtistByHouse = apply_filter_in_dataframe(GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id), inputDate, inputEstablishment)
    reviewHouseByArtist = apply_filter_in_dataframe(GET_REVIEW_HOUSE_BY_ARTIST(id), inputDate, inputEstablishment)
    
    data['artistRanking'] = artistRanking
    data['reviewArtistByHouse'] = reviewArtistByHouse
    data['averageReviewArtistByHouse'] = averageReviewArtistByHouse
    data['reviewHouseByArtist'] = reviewHouseByArtist
    
    return data

def get_data_ShowStatement(data, id, inputDate=None, inputEstablishment=None):
    downloadShowStatement = GET_PROPOSTAS_BY_ID(id)
    
    data['downloadShowStatement'] = downloadShowStatement
    
    return data

def get_data_operational_performace(data, user_id,id):
    try:
        oldShowHistory = operational_old_show_history(id)
        data['oldShowHistory'] = oldShowHistory
    except Exception as e:
        data['oldShowHistory'] = pd.DataFrame()

    try:
        newShowHistory = operational_new_show_history(id)
        data['newShowHistory'] = newShowHistory
    except Exception as e:
        data['newShowHistory'] = pd.DataFrame()

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

