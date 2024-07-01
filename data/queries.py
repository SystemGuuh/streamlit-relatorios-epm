from data.dbconnect import getDfFromQuery
from data.functions import *
import streamlit as st


def search_artist_id(filter):
    result = getDfFromQuery("""
    SELECT 
    AU.ID,
    AU.LOGIN,
    AU.FULL_NAME,
    TA.CELULAR,
    TA.NOME
    FROM ADMIN_USERS AU
    LEFT JOIN T_ATRACOES TA ON AU.ID = TA.FK_USUARIO
    """ +filter)

    return result

def get_search_user_from_session(id):
    result = getDfFromQuery(f"""
    SELECT 
    AU.ID,
    AU.LOGIN,
    AU.FULL_NAME,
    TA.CELULAR,
    TA.NOME
    FROM ADMIN_USERS AU
    LEFT JOIN T_ATRACOES TA ON AU.ID = TA.FK_USUARIO
    WHERE AU.ID = '{id}'
    """)
    return result

def search_establishment_id(filter):
    result = getDfFromQuery("QUERY"+filter)
    return result.loc[0, 'ID']

@st.cache_data
def showhistory_old_show_history(id):
    query = (f"""
    SELECT
    P.ID AS 'ID DA PROPOSTA',

    CASE 
        WHEN S.DESCRICAO IS NULL THEN "Cancelada"
        ELSE S.DESCRICAO
    END AS 'STATUS DA PROPOSTA',
    CASE WHEN PAL.ID IS NULL THEN C.NAME ELSE CONCAT(C.NAME, ' (', PAL.NOME, ')') END AS ESTABELECIMENTO,
    GC.GRUPO_CLIENTES AS GRUPO,
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'DATA DE INÍCIO', 
    DATE_FORMAT(P.DATA_INICIO, '%H:%i') AS 'HORÁRIO INÍCIO',
    DATE_FORMAT(P.DATA_FIM, '%H:%i') AS 'HORÁRIO FIM',
    CONCAT('R$ ', FORMAT(P.VALOR_BRUTO, 2))  AS 'VALOR BRUTO',
    CONCAT('R$ ', FORMAT(P.VALOR_LIQUIDO, 2)) AS 'VALOR LÍQUIDO',
    CONCAT('R$ ', FORMAT(P.VALOR_ARTISTA_A_RECEBER, 2)) AS 'VALOR A RECEBER ARTISTA',
    CONCAT('R$ ', FORMAT(P.VALOR_ESHOWS_RECEBIMENTO, 2)) AS 'VALOR RECEBIDO ESHOWS',
    SF.DESCRICAO AS 'STATUS FINANCEIRO',
    P.FK_FECHAMENTO AS 'ID DO FECHAMENTO',

    CASE 
        WHEN P.ADIANTAMENTO IS NULL THEN 0
        ELSE P.ADIANTAMENTO
    END AS 'ADIANTAMENTO',

    DATE_FORMAT(P.PREVISAO_PGTO, '%d/%m/%Y') AS 'PREVISÃO DE PAGAMENTO',
    
    CASE 
        WHEN P.DATA_PAGAMENTO IS NULL THEN ""
        ELSE DATE_FORMAT(P.DATA_PAGAMENTO, '%d/%m/%Y')
    END AS 'DATA DO PAGAMENTO',

    DATE_FORMAT(P.PREVISAO_VENCIMENTO_BOLETO, '%d/%m/%Y') AS 'PREVISÃO DE VENCIMENTO DO BOLETO',

    CASE 
        WHEN C.NOTA_FISCAL = 1 THEN 'Sim'
        WHEN C.NOTA_FISCAL = 0 THEN 'Não'
        ELSE ' '
    END AS 'EXIGE NF?',

    CASE 
        WHEN P.FK_NOTA_FISCAL IS NULL THEN ""
        ELSE P.FK_NOTA_FISCAL
    END AS 'ID DA NF',

    CASE 
        WHEN P.FK_STATUS_PROPOSTA = 102 THEN CONCAT(MR.MOTIVO,": ",MRP.DESCRICAO_RECUSA)
    WHEN MCP.FK_PROPOSTA = P.ID THEN CONCAT(MC.TEXTO_MOTIVO,": ",MCP.DESCRICAO_CANCELAMENTO)
    WHEN SPP.FK_PROPOSTA = P.ID THEN CONCAT(SP.TITULO,": ",SPP.SINAL_PROBLEMA_DESCRICAO)
    END AS 'OBSERVAÇÃO MOTIVO',
    CONCAT('https://admin.eshows.com.br/proposta/', P.ID) AS LINK
    
    FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
    LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
    LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
    LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
    LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
    LEFT JOIN T_PALCOS PAL ON PAL.ID = P.FK_PALCOS
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON GC.ID = C.FK_GRUPO
    LEFT JOIN T_MOTIVO_RECUSA_PROPOSTA MRP ON MRP.FK_PROPOSTA = P.ID
    LEFT JOIN T_MOTIVO_RECUSA MR ON MR.ID = MRP.FK_MOTIVO_RECUSA
    LEFT JOIN T_MOTIVO_CANCELAMENTO_PROPOSTA MCP ON MCP.FK_PROPOSTA = P.ID
    LEFT JOIN T_MOTIVO_CANCELAMENTO MC ON MC.ID = MCP.FK_ID_SOLICITACAO_CANCELAMENTO
    LEFT JOIN T_SINAL_PROBLEMA_PROPOSTA SPP ON SPP.FK_PROPOSTA = P.ID
    LEFT JOIN T_SINAL_PROBLEMA SP ON SP.ID = SPP.FK_SINAL_PROBLEMA
    LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    LEFT JOIN T_ATRACAO_BANCOS AB ON (AB.ID = P.FK_ATRACAO_BANCO)


    WHERE (P.TESTE = 0 OR P.TESTE IS NULL) 
        AND C.NAME IS NOT NULL 
        AND A.NOME IS NOT NULL 
        AND P.DATA_INICIO IS NOT NULL
        AND DATE(P.DATA_INICIO) <= CURDATE()
        AND P.DATA_INICIO > DATE_SUB(CURDATE(), INTERVAL 120 DAY)
        AND AU.ID = {id}

    ORDER BY P.DATA_INICIO DESC;
    """)
    
    return getDfFromQuery(query)

@st.cache_data     
def showhistory_new_show_history(id):
    return getDfFromQuery(f"""
    SELECT
    P.ID AS 'ID DA PROPOSTA',

    CASE 
        WHEN S.DESCRICAO IS NULL THEN "Cancelada"
        ELSE S.DESCRICAO
    END AS 'STATUS DA PROPOSTA',
    CASE WHEN PAL.ID IS NULL THEN C.NAME ELSE CONCAT(C.NAME, ' (', PAL.NOME, ')') END AS ESTABELECIMENTO,
    GC.GRUPO_CLIENTES AS GRUPO,
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'DATA DE INÍCIO', 
    DATE_FORMAT(P.DATA_INICIO, '%H:%i') AS 'HORÁRIO INÍCIO',
    DATE_FORMAT(P.DATA_FIM, '%H:%i') AS 'HORÁRIO FIM',
    CONCAT('R$ ', FORMAT(P.VALOR_BRUTO, 2))  AS 'VALOR BRUTO',
    CONCAT('R$ ', FORMAT(P.VALOR_LIQUIDO, 2)) AS 'VALOR LÍQUIDO',
    CONCAT('R$ ', FORMAT(P.VALOR_ARTISTA_A_RECEBER, 2)) AS 'VALOR A RECEBER ARTISTA',
    CONCAT('R$ ', FORMAT(P.VALOR_ESHOWS_RECEBIMENTO, 2)) AS 'VALOR RECEBIDO ESHOWS',
    SF.DESCRICAO AS 'STATUS FINANCEIRO',
    P.FK_FECHAMENTO AS 'ID DO FECHAMENTO',

    CASE 
        WHEN P.ADIANTAMENTO IS NULL THEN 0
        ELSE P.ADIANTAMENTO
    END AS 'ADIANTAMENTO',

    DATE_FORMAT(P.PREVISAO_PGTO, '%d/%m/%Y') AS 'PREVISÃO DE PAGAMENTO',
    
    CASE 
        WHEN P.DATA_PAGAMENTO IS NULL THEN ""
        ELSE DATE_FORMAT(P.DATA_PAGAMENTO, '%d/%m/%Y')
    END AS 'DATA DO PAGAMENTO',

    DATE_FORMAT(P.PREVISAO_VENCIMENTO_BOLETO, '%d/%m/%Y') AS 'PREVISÃO DE VENCIMENTO DO BOLETO',

    CASE 
        WHEN C.NOTA_FISCAL = 1 THEN 'Sim'
        WHEN C.NOTA_FISCAL = 0 THEN 'Não'
        ELSE ' '
    END AS 'EXIGE NF?',

    CASE 
        WHEN P.FK_NOTA_FISCAL IS NULL THEN ""
        ELSE P.FK_NOTA_FISCAL
    END AS 'ID DA NF',

    CASE 
        WHEN P.FK_STATUS_PROPOSTA = 102 THEN CONCAT(MR.MOTIVO,": ",MRP.DESCRICAO_RECUSA)
    WHEN MCP.FK_PROPOSTA = P.ID THEN CONCAT(MC.TEXTO_MOTIVO,": ",MCP.DESCRICAO_CANCELAMENTO)
    WHEN SPP.FK_PROPOSTA = P.ID THEN CONCAT(SP.TITULO,": ",SPP.SINAL_PROBLEMA_DESCRICAO)
    END AS 'OBSERVAÇÃO MOTIVO',
    CONCAT('https://admin.eshows.com.br/proposta/', P.ID) AS LINK

    FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
    LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
    LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
    LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
    LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
    LEFT JOIN T_PALCOS PAL ON PAL.ID = P.FK_PALCOS
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON GC.ID = C.FK_GRUPO
    LEFT JOIN T_MOTIVO_RECUSA_PROPOSTA MRP ON MRP.FK_PROPOSTA = P.ID
    LEFT JOIN T_MOTIVO_RECUSA MR ON MR.ID = MRP.FK_MOTIVO_RECUSA
        LEFT JOIN T_MOTIVO_CANCELAMENTO_PROPOSTA MCP ON MCP.FK_PROPOSTA = P.ID
        LEFT JOIN T_MOTIVO_CANCELAMENTO MC ON MC.ID = MCP.FK_ID_SOLICITACAO_CANCELAMENTO
    LEFT JOIN T_SINAL_PROBLEMA_PROPOSTA SPP ON SPP.FK_PROPOSTA = P.ID
        LEFT JOIN T_SINAL_PROBLEMA SP ON SP.ID = SPP.FK_SINAL_PROBLEMA
    LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO

    WHERE P.TESTE = 0 
        AND C.NAME IS NOT NULL 
        AND A.NOME IS NOT NULL 
        AND P.DATA_INICIO IS NOT NULL
        AND DATE(P.DATA_INICIO) >= CURDATE()
        AND A.FK_USUARIO = {id}
        

    ORDER BY P.DATA_INICIO DESC 
    """)

@st.cache_data
def operational_explore_stages(id):
    result = getDfFromQuery(f"""
    SELECT
    CI.ID AS 'ID DA INDICAÇÃO',
    DATE_FORMAT(CI.CREATED_AT, '%d/%m/%Y') AS 'DATA DE CRIAÇÃO',
    CASE
        WHEN CI.FEEDBACK = 1 THEN 'Positivo'
        WHEN CI.FEEDBACK = 0 THEN 'Negativo'
        ELSE 'Pendente'
    END AS FEEDBACK,

    CASE 
        WHEN MR.MOTIVO  IS NULL THEN ' '
        ELSE MR.MOTIVO 
    END AS 'MOTIVO DA RECUSA',
    C.NAME AS ESTABELECIMENTO,
    GC.NOME AS 'GRUPO',
    AD.NUMERO_SHOWS AS 'SHOWS REALIZADOS',
    DATE_FORMAT(CI.LAST_UPDATE, '%d/%m/%Y') AS 'ÚLTIMA ATUALIZAÇÃO'

    FROM 
    T_CANDIDATO_INDICACAO CI
    LEFT JOIN T_COMPANIES C ON CI.FK_INDICACAO_CASA = C.ID
    LEFT JOIN T_ATRACOES A ON CI.FK_ATRACAO = A.ID
    LEFT JOIN T_ATRACOES_DADOS AD ON A.ID = AD.FK_ATRACAO
    LEFT JOIN T_MOTIVO_RECUSA_EXPLORAR_PALCOS MR ON MR.ID = CI.FK_MOTIVO_RECUSA
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON C.FK_GRUPO = GC.ID
    LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO

    WHERE 
    # C.ID NOT IN (102,632,633,343)
    # AND 
    C.ACTIVE = 1
    AND C.EXPLORAR_CONTRATANTES = 1
    AND A.FK_USUARIO = {id}

    GROUP BY CI.ID 
    """)
    return result

@st.cache_data
def operational_oportunities(id):
    result = getDfFromQuery(f"""
    SELECT
    TC.NAME AS ESTABELECIMENTO,
    CASE
    WHEN C.CREATED_AT = "0000-00-00 00:00:00" THEN NULL
    ELSE DATE_FORMAT(C.CREATED_AT, '%d/%m/%Y')
    END AS 'DATA DE CANDIDATURA',
    DATE_FORMAT(O.DATA_INICIO, '%d/%m/%Y') AS 'DATA DO SHOW', 
    DATE_FORMAT(O.DATA_INICIO, '%H:%i') AS 'HORÁRIO INÍCIO',
    C.FK_OPORTUNIDADE AS 'ID OPORTUNIDADE',
    CASE
        WHEN O.FINALIZADA = 1 THEN 'Cancelada'
    ELSE SO.DESCRICAO 
    END AS 'DESCRIÇÃO',
    CASE
        WHEN EMM.DESCRICAO IS NULL THEN ' '
        ELSE  EMM.DESCRICAO
    END AS 'ESTILO 1',
    CASE
        WHEN EMMM.DESCRICAO IS NULL THEN ' '
        ELSE  EMMM.DESCRICAO
    END AS 'ESTILO 2',
    CASE
        WHEN EMMMM.DESCRICAO IS NULL THEN ' '
        ELSE  EMMMM.DESCRICAO
    END AS 'ESTILO 3',
    O.CIDADE AS 'CIDADE',
    AD.NUMERO_SHOWS AS 'NÚEMRO DE SHOWS',
    EM.DESCRICAO AS 'ESTILO DO ARTISTA',
    SC.DESCRICAO AS 'STATUS DO CANDIDATO'

    FROM
    T_CANDIDATOS C
    LEFT JOIN T_ATRACOES A ON C.FK_ATRACAO = A.ID
    LEFT JOIN T_STATUS_CANDIDATO SC ON SC.ID = C.FK_STATUS_CANDIDATO
    LEFT JOIN T_OPORTUNIDADES O ON O.ID = C.FK_OPORTUNIDADE
    LEFT JOIN T_STATUS_OPORTUNIDADE SO ON SO.ID = O.FK_STATUS_OPORTUNIDADE
    LEFT JOIN T_ATRACOES_DADOS AD ON A.ID = AD.FK_ATRACAO
    LEFT JOIN T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID
    LEFT JOIN T_ESTILOS_MUSICAIS EMM ON O.FK_ESTILO_INTERESSE_1 = EMM.ID
    LEFT JOIN T_ESTILOS_MUSICAIS EMMM ON O.FK_ESTILO_INTERESSE_2 = EMMM.ID
    LEFT JOIN T_ESTILOS_MUSICAIS EMMMM ON O.FK_ESTILO_INTERESSE_3 = EMMMM.ID
    INNER JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    INNER JOIN T_COMPANIES TC ON TC.ID = O.FK_CONTRATANTE

    WHERE  
    O.FK_OCASIAO <> 106
    AND A.FK_USUARIO = {id}

    GROUP BY C.ID
    ORDER BY O.DATA_INICIO DESC
    """)
    return result

@st.cache_data
def operational_casting(id):
    result = getDfFromQuery(f"""
    SELECT
    C.ID AS ID,
    C.NAME AS ESTABELECIMENTO

    FROM T_CASTING CAST
    INNER JOIN T_ATRACOES A ON A.ID = CAST.FK_ATRACAO
    INNER JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    INNER JOIN T_COMPANIES C ON C.ID = CAST.FK_CONTRATANTE

    WHERE A.FK_USUARIO = {id}

    """)
    return result

@st.cache_data
def operational_favorite(id):
    result = getDfFromQuery(f"""
    SELECT
    C.ID AS ID,
    C.NAME AS ESTABELECIMENTO,
    F.ID AS 'ID FAVORITO'

    FROM T_FAVORITO F
    INNER JOIN T_ATRACOES A ON A.ID = F.FK_ATRACAO
    INNER JOIN T_COMPANIES C ON C.ID = F.FK_CONTRATANTE
    INNER JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO

    WHERE 
    F.FAVORITE = 1
    AND A.FK_USUARIO = {id}

    """)
    return result

@st.cache_data
def operational_performance(id):
    df = getDfFromQuery(f"""
                            SELECT
                            A.FK_USUARIO AS ID,
                            A.NOME AS ARTISTA,
                            DATE(OA.DATA_OCORRENCIA) AS DATA,
                            DATE_ADD(DATE(OA.DATA_OCORRENCIA), INTERVAL(2-DAYOFWEEK(OA.DATA_OCORRENCIA)) DAY) AS SEMANA,
                            TIPO.TIPO AS TIPO,
                            EM.DESCRICAO AS ESTILO,
                            C.NAME AS ESTABELECIMENTO
                            
                            FROM 
                            T_OCORRENCIAS_AUTOMATICAS OA
                            LEFT JOIN T_PROPOSTAS P ON P.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_PROPOSTAS'
                            LEFT JOIN T_NOTAS_FISCAIS NF ON NF.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND NF.TIPO = 'NF_UNICA'
                            LEFT JOIN T_NOTAS_FISCAIS NF2 ON NF2.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND (NF2.TIPO = 'NF_SHOW_ANTECIPADO' OR NF2.TIPO = 'NF_SHOW_SOZINHOS')
                            INNER JOIN T_ATRACOES A ON A.ID = OA.FK_ATRACAO
                            INNER JOIN T_TIPOS_OCORRENCIAS TIPO ON TIPO.ID = OA.FK_TIPO_OCORRENCIA
                            LEFT JOIN T_FECHAMENTOS F ON F.ID = NF.FK_FECHAMENTO
                            LEFT JOIN T_PROPOSTAS P2 ON P2.ID = NF2.FK_PROPOSTA
                            LEFT JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE OR C.ID = F.FK_CONTRATANTE OR C.ID = P2.FK_CONTRANTE)
                            LEFT JOIN T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID
                            
                            WHERE
                            A.FK_USUARIO = {id} 
                            AND C.ID NOT IN (102,343,632,633)
                            AND A.ID NOT IN (12166)
                            AND OA.DATA_OCORRENCIA >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    """)

    return df

@st.cache_data
def operational_report_by_occurence_and_date(id):
    df = getDfFromQuery(f"""
                            SELECT
                            A.FK_USUARIO AS ID,
                            A.NOME AS ARTISTA,
                            DATE(OA.DATA_OCORRENCIA) AS DATA,
                            DATE_ADD(DATE(OA.DATA_OCORRENCIA), INTERVAL(2-DAYOFWEEK(OA.DATA_OCORRENCIA)) DAY) AS SEMANA,
                            TIPO.TIPO AS TIPO,
                            EM.DESCRICAO AS ESTILO,
                            C.NAME AS ESTABELECIMENTO

                            FROM 
                            T_OCORRENCIAS_AUTOMATICAS OA
                            LEFT JOIN T_PROPOSTAS P ON P.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_PROPOSTAS'
                            LEFT JOIN T_NOTAS_FISCAIS NF ON NF.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND NF.TIPO = 'NF_UNICA'
                            LEFT JOIN T_NOTAS_FISCAIS NF2 ON NF2.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND (NF2.TIPO = 'NF_SHOW_ANTECIPADO' OR NF2.TIPO = 'NF_SHOW_SOZINHOS')
                            INNER JOIN T_ATRACOES A ON A.ID = OA.FK_ATRACAO
                            INNER JOIN T_TIPOS_OCORRENCIAS TIPO ON TIPO.ID = OA.FK_TIPO_OCORRENCIA
                            LEFT JOIN T_FECHAMENTOS F ON F.ID = NF.FK_FECHAMENTO
                            LEFT JOIN T_PROPOSTAS P2 ON P2.ID = NF2.FK_PROPOSTA
                            LEFT JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE OR C.ID = F.FK_CONTRATANTE OR C.ID = P2.FK_CONTRANTE)
                            LEFT JOIN T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID

                            WHERE A.FK_USUARIO = {id} 
                            AND C.ID NOT IN (102,343,632,633)
                            AND A.ID NOT IN (12166)
                            AND OA.DATA_OCORRENCIA >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    """)

    return df

@st.cache_data
def operational_general_information_and_finance(id): 
    df =getDfFromQuery(f"""
                        SELECT
                        A.FK_USUARIO AS ID,
                        A.NOME AS ARTISTA,
                        C.NAME AS ESTABELECIMENTO,
                        S.DESCRICAO AS STATUS_PROPOSTA,
                        SF.DESCRICAO AS STATUS_FINANCEIRO,
                        P.DATA_INICIO AS DATA_INICIO,
                        P.DATA_FIM AS DATA_FIM,
                        CONCAT(
                        TIMESTAMPDIFF(HOUR, P.DATA_INICIO, P.DATA_FIM), 'h ',
                        TIMESTAMPDIFF(MINUTE, P.DATA_INICIO, P.DATA_FIM) % 60, 'm ',
                        TIMESTAMPDIFF(SECOND, P.DATA_INICIO, P.DATA_FIM) % 60, 's'
                        ) AS DURACAO,
                        DAYNAME(P.DATA_INICIO) AS DIA_DA_SEMANA,
                        P.VALOR_BRUTO,
                        P.VALOR_LIQUIDO,
                        F.ID AS ID_FECHAMENTO,
                        F.DATA_INICIO AS INICIO_FECHAMENTO,
                        F.DATA_FIM AS FIM_FECHAMENTO
                        FROM T_PROPOSTAS P
                        INNER JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
                        INNER JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
                        LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
                        INNER JOIN T_FECHAMENTOS F ON F.ID = P.FK_FECHAMENTO
                        LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
                        WHERE 
                        A.FK_USUARIO = {id}
                        AND P.FK_STATUS_PROPOSTA IN (100,101,103,104)
                        AND A.ID NOT IN (12166)
                        ORDER BY
                        P.DATA_INICIO ASC
                        """)
    
    return df


