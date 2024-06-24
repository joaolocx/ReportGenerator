import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(f"Connection to {db_name} DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


st.header("Gerador Automático de Relatórios")
st.write("Esse gerador vai auxiliar na busca de dados do sistema")
st.sidebar.title("Filtros")
bd_user = st.sidebar.text_input(label="Usuário: ")
bd_pass = st.sidebar.text_input(label="Senha: ", type="password")
locxre = create_connection("locx-readonly.cy9zpcnfbawx.us-east-1.rds.amazonaws.com", bd_user, bd_pass, "locx")
cur = locxre.cursor()

colunas_select = st.sidebar.multiselect(
    label='Colunas',
    options=[
        'Todas', 'id', 'APP', 'Marca', 'Cliente', 'Tipo de Projeto', 'Escopo de projeto', 'Unidade', 'Contrato', 'Bandeira', 'Indice contrato', 
        'Inicio contrato', 'Fim contrato', 'Data Reajuste', 'Fase', 'Etiqueta', 'Motivo', 'Tipo de Imóvel', 'Aluguel', 'Saving', 'FEE', 
        'FEE POTENCIAL', 'Proprietario', 'CPF/CNPJ', 'Rua', 'Número', 'Bairro', 'Complemento', 'Cidade', 'Estado', 'CEP', 'Área construínda', 
        'Área externa', 'Área terreno', 'Negociador', 'Back Office', 'Front Office', 'Analista de Projeto', 'Gerente de Contas', 'Squad', 
        'Nivel', 'Data de importação', 'Data da Caixa de Entrada', 'Data da Negociação Não Iniciada', 'Data da Negociação em Andamento', 
        'Data Aguardando Informações Cliente Negociação', 'Data Nova Abordagem Programada', 'Data Proposta em Análise pelo Locador', 
        'Data Aguardando Aprovação Cliente', 'Data da Negociação Aceita locx', 'Data da Elaboração de Minuta', 'Data da Elaboração de Minuta Locx', 
        'Data do Ajuste de Minuta Locx', 'Data da Coleta de Dados', 'Data Aguardando Informações Cliente Formalização', 
        'Data Minuta Aguardando Chancela LocX', 'Data Minuta Aguardando Chancela de Dados', 'Data Minuta Aguardando Chancela Locador', 
        'Data Minuta Aguardando Chancela Cliente', 'Data Aguardando Assinatura do Locador', 'Data Aguardando Assinatura do Cliente', 
        'Data Aguardando Link de Assinatura', 'Data Aguardando Input da Minuta', 'Data da negociação Pausada', 'Data da Formalização Declinada', 
        'Data do Contrato Assinado', 'Data do Contrato Não Elegível', 'Data da Negociação Recusada', 'Data da Prévia Enviada ao Cliente', 
        'Data da Negociação Faturada', 'Valor a considerar', 'Desconto temporario valor final', 'Desconto %', 'Desconto % recebível', 
        'Desconto temporario inicio', 'Desconto temporario fim', 'Prazo de Desconto', 'Prazo desconto recebível', 'Negociacao de Reajuste valor base', 
        'Negociacao de Reajuste desconto', 'Reajuste data Inicio', 'Reajuste data final', 'Prazo Reajuste', 'DiscountFee', 'Negociacao de reajuste tipo', 
        'Troca indice antigo', 'Troca indice novo', 'Troca indice troca definitiva', 'Troca indice fim', 'Troca indice inicio', 'Prazo de Indice', 
        'Reducao valor base', 'Reducao valor final', 'Reducao inicio', 'Reducao fim', 'Reducao Percentual', 'Redução % recebível', 'Prazo Redução', 
        'Prazo Redução recebível', 'Renovacao valor base', 'Renovacao inicio', 'Renovacao fim', 'Prazo de Renovacao', 'Analista acionamento', 
        'Acionamento', 'Data acionamento', 'Tempo acionamento', 'Data de agendamento do retorno', 'Data Limite', 'LEAD TIME', 'LEAD PROJETO', 
        'LEAD CAIXA DE ENTRADA', 'LEAD NEGOCIAÇÃO', 'LEAD FORMALIZAÇÃO', 'LEAD ASSINATURA', 'Cod Auxiliar', 'Segmento'
    ],
    default='Todas'
)

# st.sidebar.subheader("Data da Negociação Aceita")
# aceita_ini = st.sidebar.date_input(label='De: ', format='DD/MM/YYYY')
# aceita_fim = st.sidebar.date_input(label='Até: ', format='DD/MM/YYYY')
negociadores_select = st.sidebar.multiselect(
    label="Negociadores",
    options=[
        "Todos",
        "JOÃO OLIVEIRA",
        "DAIANA CAROLINA GONCALVES",
        "JULIANA ALMEIDA",
        "FERNANDA FREITAS",
        "THAMIRES ALVES OLIVEIRA",
        "WALDEMAR DA COSTA",
        "FERNANDO ANTONIO COUTINHO JUNIOR",
        "LORRAINE CRISTINA NAVES RESENDE",
        "ANALISTA BPO",
        "ALINE TRINDADE ROCHA",
        "MARIELA SANTOS MILAGRE",
        "MARLA RUANA",
        "CAROLINA STEFANE CAETANO DA SILVA",
        "WELINTON PAULO DOS REIS",
        "RAFAEL CARVALHO",
        "ROSANIA CARVALHO",
        "ADRIANA OLIVEIRA REIS",
        "BRAZ PEREIRA DE CAMARGOS",
        "JESSÉ MUNIZ",
        "DAYANE SAAR"
    ],
    default="Todos"
)

fases_select = st.sidebar.multiselect(
    label="Fases",
    options=[
        "Todas",
        "Caixa de Entrada",
        "Negociação",
        "Formalização",
        "Chancela",
        "Assinatura",
        "Pausado",
        "Financeiro",
        "Concluído"  
    ],
    default="Todas"
)

import_ini = st.sidebar.date_input(label="Importação Início: ",format="DD/MM/YYYY")
import_end = st.sidebar.date_input(label="Importação Fim: ",format="DD/MM/YYYY")

botao_gerar = st.sidebar.button(label="Gerar")

# Construir a cláusula SELECT
if 'Todas' in colunas_select:
    colunas = '*'
else:
    colunas = ', '.join([f'`{c}`' for c in colunas_select])

negociadores = ", ".join([f'"{n}"' for n in negociadores_select])
fases = ", ".join([f'"{f}"' for f in fases_select])

# Construir a consulta SQL
query = f"""
with sv as (
SELECT
        ne1.id,
        nc.rent * (1 - (nrd.finalValue / nrd.BaseValue)) * IF(nrd.Term >= 12, 12, nrd.Term) AS desco,
		nc.rent * (1 - (nrr.finalValue / nrr.BaseValue))*
            IF((IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))>=12,12,(IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))) AS red
            
from negotiations ne1
left join product_contracts pc on pc.id=ne1.ProductContractsId
left join product_contract_commercial_premises pccp1 on pccp1.ProductContractId=pc.id and pccp1.NegotiationType = 2 
left join product_contract_commercial_premises pccp2 on pccp2.ProductContractId=pc.id and pccp2.NegotiationType = 1
left join product_contract_commercial_premises pccp on pccp.ProductContractId=pc.id and pccp.NegotiationType = 3
left join entities en on en.id=pc.EntitiesId
left join entity_segmentations eseg on eseg.id=en.EntitySegmentationsId
left join negotiation_contracts nc on nc.id=ne1.NegotiationContractsId
left join properties p on p.id=nc.PropertiesId
left join cities c on c.id=p.CitiesId
left join states s on s.id=c.StatesId
left join units un on un.id=nc.UnitsId
left join readjustment_types rt on rt.id=nc.ReadjustmentTypesId
left join properties_entities pe on pe.PropertiesId = p.Id	
left join entities ep on ep.id = pe.EntitiesId
left join negotiation_rent_discounts nrd on ne1.id=nrd.NegotiationsId and nrd.deletedat is null
left join negotiation_rent_reductions nrr on ne1.id=nrr.NegotiationsId and nrr.deletedat is null
left join negotiation_contract_renewals ncr on ne1.id=ncr.NegotiationsId and ncr.deletedat is null
left join negotiation_readjustment_index_discounts nrid on ne1.id=nrid.NegotiationsId and nrid.deletedat is null
left join negotiation_readjustment_type_changes nrtc on ne1.id=nrtc.NegotiationsId and nrtc.deletedat is null
left join readjustment_indexes ri1 on ri1.id=nrtc.ReadjustmentIndexId
left join readjustment_types rt1 on rt1.id=ri1.ReadjustmentTypesId
left join readjustment_indexes ri2 on ri2.id=nrtc.PrevReadjustmentIndexId
left join readjustment_types rt2 on rt2.id=ri2.ReadjustmentTypesId
left join entity_squads es on es.id = ne1.EntitySquadsId
left join negotiation_types nt on nt.id = pccp.NegotiationType
left join entities ng on ng.id =ne1.ResponsibleEntitiesId
left join entities bk on bk.id =ne1.BackofficeEntitiesId
left join entities fo on fo.id =ne1.FormalizationResponsibleEntitiesId
left join entities ap on ap.id = ne1.ProjectResponsibleEntitiesId
left join negotiation_status ns on ns.id = ne1.NegotiationStatusId
left join negotiation_rationales nr on nr.id = ne1.NegotiationRationalesId
left join type_projects tp on tp.id=ne1.TypeProjectsId
left join project_scopes ps on ps.id=ne1.ProjectScopesId
left join products pdt on pdt.id=pc.ProductsId
left join entities_entity_customer_portfolios eecp on eecp.EntitiesId = nc.EntitiesId
left join customer_portfolios cp on cp.id = eecp.CustomerPortfoliosId and cp.IsDisabled = 0
left join entities cs on cs.id=cp.ManagerId
left join property_types pt on pt.id=p.PropertyTypesId
left join brands bd on bd.id = nc.BrandsId  

where ne1.DeletedAt is null and ((tp.name<>"Laudo" and tp.name<>"Broker opinion") or tp.name is null) and bd.name="RAIA DROGASIL"
group by ne1.id
order by ne1.id desc
), dados as(
select ne.id, 
if(ne.NegotiationMobile =1,"SIM","NÃO") as 'APP',
bd.name 'Marca',
en.name 'Cliente',
CASE
    WHEN bd.name IN ('ALIFE NINO', 'AMERICAN TOWER', 'AMIL', 'ATHENA', 'BMG', 'BONSONO', 'BOTOCLINIC', 'CENCOSUD', 'CHILLI BEANS', 'CLARO', 'DAKI', 'DASA', 'DMTOP', 'DOMINOS', 'DROGA CLARA', 'EDP ENERGIAS DO BRASIL', 'EDP ESPÍRITO SANTO', 'EDP SÃO PAULO', 'FARMÁCIAS INDEPENDENTE', 'FREE BAHIA', 'GPA', 'HAPVIDA', 'HELP!', 'ITAPUÃ CALÇADOS', 'LABI EXAMES', 'LEV BICICLETAS', 'LOGGI', 'LOPES SUPERMERCADOS', 'MAGAZINE LUIZA', 'MASTERCELL', 'MEDSÊNIOR', 'MRV', 'ORTOBOM', 'PETZ', 'RAIA DROGASIL', 'RIBERCRED', 'RODOBENS', 'TBSA', 'TIM') THEN 'ativo'
    WHEN bd.name IN ('AMERICANAS', 'BANCO MERCANTIL', 'BOTICÁRIO', 'CABANA BURGER', 'CLARO LOJAS', 'COMUNICARE', 'DROGARIA MODERNA', 'EMBRACON', 'EXCLUSIVA COLCHÕES', 'GRUPO CASAS BAHIA', 'GRUPO OPTY', 'GRUPO WEBBY', 'HABIB''S', 'HERMES PARDINI', 'HIGHLINE', 'IHS', 'LOJAS SILVA', 'PERNAMBUCANAS', 'PMP FARMARCIAS', 'POSTO IPIRANGA', 'QMC', 'RODRIGUES COLCHÕES', 'SBA', 'SOLAR MAGAZINE', 'SUPERFRIO', 'TENDA CONSTRUTORA', 'VAMOS SORRIR', 'VIBRA ENERGIA', 'YDUQS', 'ZAMP') THEN 'inativo'
    ELSE 'não identificado'
END AS 'status',
tp.name 'Tipo de Projeto',
ps.name 'Escopo de projeto',
un.Name 'Unidade',
nc.ContractNumber 'Contrato',
nc.ContractFlag 'Bandeira',
rt.name 'Indice contrato',
nc.start 'Inicio contrato',
nc.end 'Fim contrato',
date_format(nc.NextReadjustment, '%Y-%m-01') 'Data Reajuste',
(select nps.Name from negotiations ne3
left join negotiation_phase_setting nps on nps.NegotiationPhase = ne3.Phase
where ne3.id = ne.id
) as 'Fase',
ns.name 'Etiqueta',
nr.name 'Motivo',
CASE when ns.name like '%CLIENTE%' OR nr.name like '%CLIENTE%' THEN 'CLIENTE'
ELSE 'LOCX'
END AS 'Responsabilidade',
pt.name 'Tipo de Imóvel',
replace(cast(nc.rent as decimal(10,2)),'.',',') 'Aluguel',  
replace(cast(ne.saving as decimal(10,2)),'.',',') 'Saving',
REPLACE(
    CAST(
        CASE 
            WHEN bd.name = 'AMERICAN TOWER' AND ne.id > 14000 THEN
                CASE 
                    WHEN 1 - (nrr.finalValue / nrr.BaseValue) IS NOT NULL THEN
                        2700 + (2700 * 0.05 * ((1 - (nrr.finalValue / nrr.BaseValue)) * 100))
                    WHEN ncr.BaseValue > nc.rent THEN
                        CASE 
                            WHEN (ncr.BaseValue - nc.rent) / nc.rent > 0.0999 THEN 2700 * 0.8
                            ELSE 2700 * 0.9
                        END
                    ELSE
                        CASE 
                            WHEN nrid.Term IS NOT NULL THEN
                                CASE 
                                    WHEN nrid.Term > 12 THEN 2700
                                    ELSE 2700 * 0.5
                                END
                            ELSE 0
                        END
                END
            WHEN bd.name = 'RAIA DROGASIL' THEN
                CASE 
                    WHEN nrr.finalValue IS NOT NULL THEN
                        CASE 
                            WHEN (IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))   <= 12 THEN
                                CASE 
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.02 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.1 THEN sv.red * 0.05
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.10 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.11 THEN sv.red * 0.055
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.11 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.12 THEN sv.red * 0.06
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.12 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.13 THEN sv.red * 0.065
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.13 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.14 THEN sv.red * 0.07
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.14 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.15 THEN sv.red * 0.075
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.15 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.16 THEN sv.red * 0.08
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.16 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.17 THEN sv.red * 0.085
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.17 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.18 THEN sv.red * 0.09
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.18 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.19 THEN sv.red * 0.095
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.19 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.200 THEN sv.red * 0.1
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.200 THEN sv.red * 0.13
                                END
                            WHEN (IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))   >= 13 AND (IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))   <= 18 THEN
                                CASE 
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.02 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.100 THEN sv.red * 0.055
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.10 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.110 THEN sv.red * 0.06
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.11 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.120 THEN sv.red * 0.065
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.12 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.130 THEN sv.red * 0.07
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.13 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.140 THEN sv.red * 0.075
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.14 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.150 THEN sv.red * 0.08
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.15 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.160 THEN sv.red * 0.085
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.16 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.170 THEN sv.red * 0.09
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.17 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.180 THEN sv.red * 0.095
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.18 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.190 THEN sv.red * 0.1
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.19 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.200 THEN sv.red * 0.105
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.200 THEN sv.red * 0.13
                                END
                            WHEN (IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))   >= 19 AND (IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))   < 24 THEN
                                CASE 
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.02 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.100 THEN sv.red * 0.06
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.10 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.110 THEN sv.red * 0.065
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.11 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.120 THEN sv.red * 0.07
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.12 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.130 THEN sv.red * 0.075
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.13 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.140 THEN sv.red * 0.08
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.14 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.150 THEN sv.red * 0.085
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.15 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.160 THEN sv.red * 0.09
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.16 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.170 THEN sv.red * 0.095
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.17 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.180 THEN sv.red * 0.1
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.18 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.190 THEN sv.red * 0.105
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.19 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.200 THEN sv.red * 0.11
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.200 THEN sv.red * 0.13
                                END
                            WHEN (IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))   >= 24 AND (IF(ncr.start is Null, IF(nc.end < nrr.start, (select pccp1.TermLimit from product_contract_commercial_premises pccp1 where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1))   <= 30 THEN
                                CASE 
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.02 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.100 THEN sv.red * 0.065
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.10 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.110 THEN sv.red * 0.07
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.11 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.120 THEN sv.red * 0.075
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.12 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.130 THEN sv.red * 0.08
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.13 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.140 THEN sv.red * 0.085
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.14 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.150 THEN sv.red * 0.09
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.15 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.160 THEN sv.red * 0.95
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.16 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.170 THEN sv.red * 0.1
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.17 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.180 THEN sv.red * 0.105
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.18 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.190 THEN sv.red * 0.11
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.19 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.200 THEN sv.red * 0.115
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.200 THEN sv.red * 0.13
                                END
                            ELSE 
                                CASE
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.02 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.100 THEN sv.red * 0.075
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.10 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.110 THEN sv.red * 0.08
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.11 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.120 THEN sv.red * 0.085
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.12 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.130 THEN sv.red * 0.09
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.13 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.140 THEN sv.red * 0.095
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.14 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.150 THEN sv.red * 0.1
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.15 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.160 THEN sv.red * 0.105
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.16 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.170 THEN sv.red * 0.11
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.17 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.180 THEN sv.red * 0.115
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.18 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.190 THEN sv.red * 0.12
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.19 AND (1 - (nrr.finalValue / nrr.BaseValue)) <= 0.200 THEN sv.red * 0.125
                                    WHEN (1 - (nrr.finalValue / nrr.BaseValue)) > 0.200 THEN sv.red * 0.13
                                END
                        END
                    ELSE
                        CASE 
                            WHEN nrd.finalValue IS NOT NULL THEN
                                CASE 
                                    WHEN nrd.Term <= 12 THEN
                                        CASE 
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.02 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.100 THEN desco * 0.055
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.101 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.201 THEN desco * 0.065
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) > 0.201 THEN desco * 0.105
                                        END
                                    WHEN nrd.Term >= 13 AND nrd.Term <= 18 THEN
                                        CASE 
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.02 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.100 THEN desco * 0.06
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.101 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.201 THEN desco * 0.07
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) > 0.201 THEN desco * 0.11
                                        END
                                    WHEN nrd.Term >= 19 AND nrd.Term <= 24 THEN
                                        CASE 
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.02 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.100 THEN desco * 0.065
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.101 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.201 THEN desco * 0.075
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) > 0.201 THEN desco * 0.115
                                        END
                                    ELSE
                                        CASE 
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.02 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.100 THEN desco * 0.07
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) >= 0.101 AND (1 - (nrd.finalValue / nrd.BaseValue)) <= 0.201 THEN desco * 0.08
                                            WHEN (1 - (nrd.finalValue / nrd.BaseValue)) > 0.201 THEN desco * 0.12
                                        END
                                END
                            ELSE 0
                        END
                END
            ELSE ne.fee
        END
    AS DECIMAL(10,2)),
    '.',
    ','
) AS 'FEE',
IF(bd.name="TBSA",850,
replace(cast((IF(bd.name="RAIA DROGASIL" or bd.name="LEV BICICLETAS" or bd.name="BOTOCLINIC" or bd.name="VAMOS SORRIR" or bd.name="MASTERCELL" or bd.name="BOTICÁRIO" or bd.name="GRUPO WEBBY" or bd.name="PMP FARMACIAS" or bd.name="CABANA BURGER" or bd.name="EXCLUSIVA COLCHÕES" or bd.name="CLARO LOJAS",
(replace(cast(((nc.rent*0.2*24)*0.2) as decimal(10,2)),'.',','))
,
IF(bd.name="CLARO" or bd.name="QMC" or bd.name="TIM",
(replace(cast(((nc.rent*0.2*12)*0.2) as decimal(10,2)),'.',','))
,
IF(bd.name="AMERICAN TOWER",
(replace(cast((2700+(2700*0.05*25)) as decimal(10,2)),'.',','))
,
IF(bd.name="GRUPO CASAS BAHIA",
IF((nrd.Term is null and nrr.BaseValue is null) or (nrd.Term is null and nrr.BaseValue is not null),
((replace(cast(nc.rent as decimal(10,2)),'.',','))*(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null) as decimal (10,2))/100)*(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null) as decimal (10,2))/100)*((select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null))),
((replace(cast(nc.rent as decimal(10,2)),'.',','))*(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 3 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null) as decimal (10,2))/100)*(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 3 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null) as decimal (10,2))/100)*((select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 3 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null))))
,
IF(bd.name="AMIL",
IF(nc.rent<=5000, 6782.99, IF(nc.rent<=10000, 7082.93, IF(nc.rent<=25000, 7848.84, 9383.68)))
,
((replace(cast(nc.rent as decimal(10,2)),'.',','))*(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null) as decimal (10,2))/100)*(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null) as decimal (10,2))/100)*((select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId and pccp.DeletedAt is null))))))))) as decimal (10,2)), ".",",")) as 'FEE POTENCIAL',


ep.name 'Proprietario',
ep.cpfcnpj as 'CPF/CNPJ',
p.street as 'Rua',
p.number as 'Número',
p.Neighborhood as 'Bairro', 
p.complement as 'Complemento',
c.Name as 'Cidade', 
s.name as 'Estado',
p.zipcode as 'CEP',
replace(cast(p.InternalArea as decimal(10,2)),'.',',') as 'Área construínda',
replace(cast(p.ExternalArea as decimal(10,2)),'.',',') as 'Área externa',
replace(cast(p.AllotmentArea as decimal(10,2)),'.',',') as 'Área terreno',
ng.name 'Negociador',
bk.name 'Back Office',
fo.name 'Front Office',
ap.name 'Analista de Projeto',
min(cp.name) 'Gerente de Contas',
es.name as 'Squad',
ne.Level 'Nivel',

ne.createdat 'Data de importação',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =10 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Caixa de Entrada',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and nh.NegotiationStatusId=76 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Negociação Não Iniciada',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and nh.NegotiationStatusId=77 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Negociação em Andamento',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and nh.NegotiationStatusId=80 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Aguardando Informações Cliente Negociação',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and nh.NegotiationStatusId=78 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Nova Abordagem Programada',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and nh.NegotiationStatusId=79 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Proposta em Análise pelo Locador',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and nh.NegotiationStatusId=81 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Aguardando Aprovação Cliente',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and nh.NegotiationStatusId=82 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Negociação Aceita locx',


(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and nh.NegotiationStatusId=84 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Elaboração de Minuta',

(select max(nhr.createdAt)
from negotiation_history_rationale nhr
left join negotiations ne1 on ne1.id=nhr.NegotiationsId
where nhr.NegotiationRationalesId=10 and ne1.id=ne.id and nhr.DeletedAt is null) 'Data da Elaboração de Minuta Locx',

(select max(nhr.createdAt)
from negotiation_history_rationale nhr
left join negotiations ne1 on ne1.id=nhr.NegotiationsId
where nhr.NegotiationRationalesId=13 and ne1.id=ne.id and nhr.DeletedAt is null) 'Data do Ajuste de Minuta Locx',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and nh.NegotiationStatusId=83 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Coleta de Dados',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and nh.NegotiationStatusId=98 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Aguardando Informações Cliente Formalização',

(select max(nhr.createdAt)
from negotiation_history_rationale nhr
left join negotiations ne1 on ne1.id=nhr.NegotiationsId
where nhr.NegotiationRationalesId=21 and ne1.id=ne.id and nhr.DeletedAt is null) 'Data Minuta Aguardando Chancela LocX',

(select max(nhr.createdAt)
from negotiation_history_rationale nhr
left join negotiations ne1 on ne1.id=nhr.NegotiationsId
where nhr.NegotiationRationalesId=20 and ne1.id=ne.id and nhr.DeletedAt is null) 'Data Minuta Aguardando Chancela de Dados',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =40 and nh.NegotiationStatusId=87 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Minuta Aguardando Chancela Locador',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =40 and nh.NegotiationStatusId=88 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Minuta Aguardando Chancela Cliente',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and ne.NegotiationRationalesId=22 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Aguardando Assinatura do Locador',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and ne.NegotiationRationalesId=23 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Aguardando Assinatura do Cliente',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and nh.NegotiationStatusId=90 and ne.NegotiationRationalesId=24 and ne1.id=ne.id and nh.DeletedAt is null) 'Data Aguardando Link de Assinatura',

(select max(nhr.createdAt)
from negotiation_history_rationale nhr
left join negotiations ne1 on ne1.id=nhr.NegotiationsId
where nhr.NegotiationRationalesId=25 and ne1.id=ne.id and nhr.DeletedAt is null) 'Data Aguardando Input da Minuta',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =60 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da negociação Pausada',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and nh.NegotiationStatusId=85 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Formalização Declinada',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =70 and nh.NegotiationStatusId=92 and ne1.id=ne.id and nh.DeletedAt is null) 'Data do Contrato Assinado',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =70 and nh.NegotiationStatusId=93 and ne1.id=ne.id and nh.DeletedAt is null) 'Data do Contrato Não Elegível',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =70 and nh.NegotiationStatusId=94 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Negociação Recusada',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =80 and nh.NegotiationStatusId=95 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Prévia Enviada ao Cliente',

(select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =80 and nh.NegotiationStatusId=96 and ne1.id=ne.id and nh.DeletedAt is null) 'Data da Negociação Faturada',

replace(cast(nrd.BaseValue as decimal(10,2)),'.',',') 'Valor a considerar',
replace(cast(nrd.FinalValue as decimal(10,2)),'.',',')'Desconto temporario valor final',
replace(1-(nrd.finalValue/nrd.BaseValue),'.',',') 'Desconto %',
IF(replace((1-(nrd.finalValue/nrd.BaseValue)),'.',',') > (replace(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 3 and pccp1.ProductContractId = pccp.ProductContractId) as decimal (10,2))/100,'.',',')),(replace(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 3 and pccp1.ProductContractId = pccp.ProductContractId) as decimal (10,2))/100,'.',',')),replace(1-(nrd.finalValue/nrd.BaseValue),'.',',')) as 'Desconto % recebível',
nrd.start 'Desconto temporario inicio',
nrd.end 'Desconto temporario fim',
nrd.Term 'Prazo de Desconto',
IF(nrd.term > (select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 3 and pccp1.ProductContractId = pccp.ProductContractId), (select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 3 and pccp1.ProductContractId = pccp.ProductContractId), nrd.term) as 'Prazo desconto recebível',

replace(cast(nrid.BaseValue as decimal(10,2)),'.',',') 'Negociacao de Reajuste valor base',

replace(cast(nrid.Discount as decimal(10,2)),'.',',') 'Negociacao de Reajuste desconto',

nrid.start 'Reajuste data Inicio',
nrid.end 'Reajuste data final',
nrid.Term 'Prazo Reajuste',
replace((nrid.DiscountFee/100),'.',',') 'DiscountFee',
case negotiationReadjustmentType when 2  then 'Futuro' when 1  then 'Atual/Retroativo' end as 'Negociacao de reajuste tipo',
rt1.name 'Troca indice antigo',
rt2.name 'Troca indice novo',
case nrtc.IsDefinitive when 1 then 'Sim' end as 'Troca indice troca definitiva',
nrtc.start 'Troca indice fim',
nrtc.end 'Troca indice inicio',
nrtc.Term 'Prazo de Indice',
replace(cast(nrr.BaseValue as decimal(10,2)),'.',',') 'Reducao valor base',
replace(cast(nrr.FinalValue as decimal(10,2)),'.',',') 'Reducao valor final',
nrr.start 'Reducao inicio',
IF(nrr.start is not null, if( ncr.End is Null,nc.end, ncr.end), "") as 'Reducao fim',
replace(1-(nrr.finalValue/nrr.BaseValue),'.',',') 'Reducao Percentual',
IF(replace((1-(nrr.finalValue/nrr.BaseValue)),'.',',') > (replace(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId) as decimal (10,2))/100,'.',',')),(replace(cast((select pccp1.DiscountLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId) as decimal (10,2))/100,'.',',')),replace(1-(nrr.finalValue/nrr.BaseValue),'.',',')) as 'Redução % recebível',
IF(ncr.start is Null, 
IF(nc.end < nrr.start, 
(select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),
TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), 
TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1) as 'Prazo Redução',

IF(
IF(ncr.start is Null, 
IF(nc.end < nrr.start, 
(select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),
TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), 
TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1)>(select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),(select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),IF(ncr.start is Null, 
IF(nc.end < nrr.start, 
(select pccp1.TermLimit from product_contract_commercial_premises pccp1
where pccp1.NegotiationType = 2 and pccp1.ProductContractId = pccp.ProductContractId),
TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(nc.end, '%Y-%m-01'))+1), 
TIMESTAMPDIFF(month, date_format(nrr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1)) as 'Prazo Redução recebível',


replace(cast(ncr.BaseValue as decimal(10,2)),'.',',')'Renovacao valor base',
ncr.start 'Renovacao inicio',
ncr.end 'Renovacao fim',
TIMESTAMPDIFF(month, date_format(ncr.start, '%Y-%m-01'), date_format(ncr.end, '%Y-%m-01'))+1 'Prazo de Renovacao',



(select enthist.Name from contract_notes ctn 
left join entities enthist on enthist.id=ctn.EntitiesId 
where ctn.negotiationcontractsid=nc.id and ctn.DeletedAt is null 
order by ctn.id desc limit 1) as 'Analista acionamento',

(select ctn.Note from contract_notes ctn 
left join contract_note_types ctnt on ctnt.id=ctn.contractnotetypesid 
where ctn.negotiationcontractsid=nc.id and ctn.DeletedAt is null 
order by ctn.id desc limit 1) as 'Acionamento',

(select ctn.UpdatedAt from contract_notes ctn 
where ctn.negotiationcontractsid=nc.id and ctn.DeletedAt is null 
order by ctn.id desc limit 1) as 'Data acionamento',

(select DATEDIFF (now(),(select ctn.UpdatedAt from contract_notes ctn 
where ctn.negotiationcontractsid=nc.id and ctn.DeletedAt is null 
order by ctn.id desc limit 1))) as 'Tempo acionamento',

(select ScheduledDate from negotiation_schedules ngs1
left join negotiations ne1 on ne1.id = ngs1.NegotiationsId
where ngs1.DeletedAt is null
and ne1.id = ne.id
order by ngs1.ScheduledDate desc limit 1) as 'Data de agendamento do retorno',

cast(ne.Deadline as date) as 'Data Limite',
if(ns.name='CONTRATO ASSINADO' or ns.name='CONTRATO NÃO ELEGÍVEL' or ns.name='NEGOCIAÇÃO RECUSADA' or ns.name='NEGOCIAÇÃO FATURADA' or ns.name='NEGOCIAÇÃO NÃO REMUNERADA' or ns.name='PRÉVIA ENVIADA AO CLIENTE' or ns.name='UNIDADE COM PENDÊNCIA',0,
if((select nps.Name from negotiations ne3
left join negotiation_phase_setting nps on nps.NegotiationPhase = ne3.Phase where ne3.id = ne.id) = "Assinatura",
(select coalesce((select abs (DATEDIFF (now(),(select max(nhr.createdAt) from negotiation_history_rationale nhr left join negotiations ne1 on ne1.id=nhr.NegotiationsId where ne1.id=ne.id and nhr.DeletedAt is null)))),
(select abs (DATEDIFF (now(),(select max(nh.createdAt) from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId where ne1.id=ne.id and nh.DeletedAt is null and nh.phase=50)))))),
(select coalesce(
(select abs (DATEDIFF (now(),(select max(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where (
nh.phase =10 or 
nh.phase =60 or 
(nh.phase =20 and nh.NegotiationStatusId=76) or
(nh.phase =20 and nh.NegotiationStatusId=77) or 
(nh.phase =20 and nh.NegotiationStatusId=80) or  
(nh.phase =20 and nh.NegotiationStatusId=78) or 
(nh.phase =20 and nh.NegotiationStatusId=79) or  
(nh.phase =20 and nh.NegotiationStatusId=81) or  
(nh.phase =20 and nh.NegotiationStatusId=82) or 
(nh.phase =30 and nh.NegotiationStatusId=84) or  
(nh.phase =30 and nh.NegotiationStatusId=83) or  
(nh.phase =30 and nh.NegotiationStatusId=98) or 
(nh.phase =40 and nh.NegotiationStatusId=86) or  
(nh.phase =40 and nh.NegotiationStatusId=87) or  
(nh.phase =40 and nh.NegotiationStatusId=88) or  
(nh.phase =30 and nh.NegotiationStatusId=85) or  
(nh.phase =70 and nh.NegotiationStatusId=94)) 
and ne1.id=ne.id and nh.DeletedAt is null)))),
(select abs (DATEDIFF (now(), ne.createdat))))))) 'LEAD TIME',

if(ns.name='CONTRATO ASSINADO' or ns.name='CONTRATO NÃO ELEGÍVEL' or ns.name='NEGOCIAÇÃO RECUSADA' or ns.name='NEGOCIAÇÃO FATURADA' or ns.name='NEGOCIAÇÃO NÃO REMUNERADA' or ns.name='PRÉVIA ENVIADA AO CLIENTE' or ns.name='UNIDADE COM PENDÊNCIA',
(select abs (DATEDIFF ((select max(nh.createdAt)
from negotiation_history nh
left join negotiations ne1 on ne1.id=nh.NegotiationsId
where ((nh.phase =70 and nh.NegotiationStatusId=92) or (nh.phase =70 and nh.NegotiationStatusId=93) or (nh.phase =70 and nh.NegotiationStatusId=94))  and ne1.id=ne.id and nh.DeletedAt is null), ne.createdat)))
, (select abs (DATEDIFF (now(), ne.createdat)))) as 'LEAD PROJETO',

if(ns.name='CONTRATO ASSINADO' or ns.name='CONTRATO NÃO ELEGÍVEL' or ns.name='NEGOCIAÇÃO RECUSADA' or ns.name='NEGOCIAÇÃO FATURADA' or ns.name='NEGOCIAÇÃO NÃO REMUNERADA' or ns.name='PRÉVIA ENVIADA AO CLIENTE' or ns.name='UNIDADE COM PENDÊNCIA',
if((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and ne1.id=ne.id and nh.DeletedAt is null) is null,
(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where ((nh.phase =70 and nh.NegotiationStatusId=92) or (nh.phase =70 and nh.NegotiationStatusId=93) or (nh.phase =70 and nh.NegotiationStatusId=94)) and ne1.id=ne.id and nh.DeletedAt is null), ne.createdat)))
,(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where (nh.phase=20 or (nh.phase =70 and nh.NegotiationStatusId=92) or (nh.phase =70 and nh.NegotiationStatusId=93) or (nh.phase =70 and nh.NegotiationStatusId=94)) and ne1.id=ne.id and nh.DeletedAt is null), ne.createdat))))
,(select coalesce(
(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and ne1.id=ne.id and nh.DeletedAt is null), ne.createdat))),
(select abs (DATEDIFF (now(), ne.createdat)))))) 'LEAD CAIXA DE ENTRADA',

if(ns.name='CONTRATO ASSINADO' or ns.name='CONTRATO NÃO ELEGÍVEL' or ns.name='NEGOCIAÇÃO RECUSADA' or ns.name='NEGOCIAÇÃO FATURADA' or ns.name='NEGOCIAÇÃO NÃO REMUNERADA' or ns.name='PRÉVIA ENVIADA AO CLIENTE' or ns.name='UNIDADE COM PENDÊNCIA',
if((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and ne1.id=ne.id and nh.DeletedAt is null) is null, 0 ,
(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where (nh.phase =30 or (nh.phase =70 and nh.NegotiationStatusId=92) or (nh.phase =70 and nh.NegotiationStatusId=93) or (nh.phase =70 and nh.NegotiationStatusId=94)) and ne1.id=ne.id and nh.DeletedAt is null), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and ne1.id=ne.id and nh.DeletedAt is null)))))
,(select coalesce(
(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and ne1.id=ne.id and nh.DeletedAt is null), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and ne1.id=ne.id and nh.DeletedAt is null)))),
(select abs (DATEDIFF (now(), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =20 and ne1.id=ne.id and nh.DeletedAt is null))))))) 'LEAD NEGOCIAÇÃO',

if(ns.name='CONTRATO ASSINADO' or ns.name='CONTRATO NÃO ELEGÍVEL' or ns.name='NEGOCIAÇÃO RECUSADA' or ns.name='NEGOCIAÇÃO FATURADA' or ns.name='NEGOCIAÇÃO NÃO REMUNERADA' or ns.name='PRÉVIA ENVIADA AO CLIENTE' or ns.name='UNIDADE COM PENDÊNCIA',
if((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where (nh.phase =30 or nh.phase=40) and ne1.id=ne.id and nh.DeletedAt is null) is null, 0 ,
(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where (nh.phase =50 or (nh.phase =70 and nh.NegotiationStatusId=92) or (nh.phase =70 and nh.NegotiationStatusId=93) or (nh.phase =70 and nh.NegotiationStatusId=94)) and ne1.id=ne.id and nh.DeletedAt is null), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and ne1.id=ne.id and nh.DeletedAt is null)))))
,(select coalesce(
(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and ne1.id=ne.id and nh.DeletedAt is null), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and ne1.id=ne.id and nh.DeletedAt is null)))),
(select abs (DATEDIFF (now(), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =30 and ne1.id=ne.id and nh.DeletedAt is null))))))) 'LEAD FORMALIZAÇÃO',

if(ns.name='CONTRATO ASSINADO' or ns.name='CONTRATO NÃO ELEGÍVEL' or ns.name='NEGOCIAÇÃO RECUSADA' or ns.name='NEGOCIAÇÃO FATURADA' or ns.name='NEGOCIAÇÃO NÃO REMUNERADA' or ns.name='PRÉVIA ENVIADA AO CLIENTE' or ns.name='UNIDADE COM PENDÊNCIA',
if((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and ne1.id=ne.id and nh.DeletedAt is null) is null, 0 ,
(select abs (DATEDIFF ((select max(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where ((nh.phase =70 and nh.NegotiationStatusId=92) or (nh.phase =70 and nh.NegotiationStatusId=93) or (nh.phase =70 and nh.NegotiationStatusId=94)) and ne1.id=ne.id and nh.DeletedAt is null), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and ne1.id=ne.id and nh.DeletedAt is null)))))
,(select coalesce(
(select abs (DATEDIFF ((select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =70 and ne1.id=ne.id and nh.DeletedAt is null), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and ne1.id=ne.id and nh.DeletedAt is null)))),
(select abs (DATEDIFF (now(), (select min(nh.createdAt)
from negotiation_history nh left join negotiations ne1 on ne1.id=nh.NegotiationsId
where nh.phase =50 and ne1.id=ne.id and nh.DeletedAt is null))))))) 'LEAD ASSINATURA',

nc.AuxiliarId 'Cod Auxiliar',

eseg.Name 'Segmento'

from negotiations ne
left join product_contracts pc on pc.id=ne.ProductContractsId
left join product_contract_commercial_premises pccp1 on pccp1.ProductContractId=pc.id and pccp1.NegotiationType = 2 
left join product_contract_commercial_premises pccp2 on pccp2.ProductContractId=pc.id and pccp2.NegotiationType = 1
left join product_contract_commercial_premises pccp on pccp.ProductContractId=pc.id and pccp.NegotiationType = 3
left join entities en on en.id=pc.EntitiesId
left join entity_segmentations eseg on eseg.id=en.EntitySegmentationsId
left join negotiation_contracts nc on nc.id=ne.NegotiationContractsId
left join properties p on p.id=nc.PropertiesId
left join cities c on c.id=p.CitiesId
left join states s on s.id=c.StatesId
left join units un on un.id=nc.UnitsId
left join readjustment_types rt on rt.id=nc.ReadjustmentTypesId
left join properties_entities pe on pe.PropertiesId = p.Id	
left join entities ep on ep.id = pe.EntitiesId
left join negotiation_rent_discounts nrd on ne.id=nrd.NegotiationsId and nrd.deletedat is null
left join negotiation_rent_reductions nrr on ne.id=nrr.NegotiationsId and nrr.deletedat is null
left join negotiation_contract_renewals ncr on ne.id=ncr.NegotiationsId and ncr.deletedat is null
left join negotiation_readjustment_index_discounts nrid on ne.id=nrid.NegotiationsId and nrid.deletedat is null
left join negotiation_readjustment_type_changes nrtc on ne.id=nrtc.NegotiationsId and nrtc.deletedat is null
left join readjustment_indexes ri1 on ri1.id=nrtc.ReadjustmentIndexId
left join readjustment_types rt1 on rt1.id=ri1.ReadjustmentTypesId
left join readjustment_indexes ri2 on ri2.id=nrtc.PrevReadjustmentIndexId
left join readjustment_types rt2 on rt2.id=ri2.ReadjustmentTypesId
left join entity_squads es on es.id = ne.EntitySquadsId
left join negotiation_types nt on nt.id = pccp.NegotiationType
left join entities ng on ng.id =ne.ResponsibleEntitiesId
left join entities bk on bk.id =ne.BackofficeEntitiesId
left join entities fo on fo.id =ne.FormalizationResponsibleEntitiesId
left join entities ap on ap.id = ne.ProjectResponsibleEntitiesId
left join negotiation_status ns on ns.id = ne.NegotiationStatusId
left join negotiation_rationales nr on nr.id = ne.NegotiationRationalesId
left join type_projects tp on tp.id=ne.TypeProjectsId
left join project_scopes ps on ps.id=ne.ProjectScopesId
left join products pdt on pdt.id=pc.ProductsId
left join entities_entity_customer_portfolios eecp on eecp.EntitiesId = nc.EntitiesId
left join customer_portfolios cp on cp.id = eecp.CustomerPortfoliosId and cp.IsDisabled = 0
left join entities cs on cs.id=cp.ManagerId
left join property_types pt on pt.id=p.PropertyTypesId
left join brands bd on bd.id = nc.BrandsId
left join sv on sv.id=ne.id

where ne.DeletedAt is null and ((tp.name<>"Laudo" and tp.name<>"Broker opinion") or tp.name is null) 
group by ne.id
)
SELECT {colunas} FROM dados where cast(`Data de importação` as date) between '{import_ini}' and '{import_end}' and (Negociador in ({negociadores}) or "Todos" in ({negociadores})) and (Fase in ({fases}) or "Todas" in ({fases}))
"""
if botao_gerar:
    # st.write(query)
    cur.execute(query)
    result = cur.fetchall()

    collumns = [desc[0] for desc in cur.description]
    dados_retornados = pd.DataFrame(result, columns=collumns)
    if dados_retornados is not None:
        st.write(dados_retornados)
    else:
        st.warning("Informe os dados de conexão")


