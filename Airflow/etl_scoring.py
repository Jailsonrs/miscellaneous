import pandas as pd
import psycopg2
import cx_Oracle
from sqlalchemy import create_engine
import numpy as np
import boto3
from datetime import datetime, timedelta
import itertools
import requests as re
import json
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
import aiohttp
import asyncio
from airflow import DAG
import os


def consulta_api1(pid):
  api_token = 
  headers = {'Content-Type': 'application/json',
  'Authorization': 'Bearer {0}'.format(api_token)}
    URL = #endpoint
     r = re.get(url = URL,headers= headers)
return(r)


def consulta():
  connection = cx_Oracle.connect("", uid, pwd, encoding="UTF-8")   
  query = """
  SELECT DISTINCT C.id as contractid
  ,i.installmentvalue
  ,P.ID as personid        
  ,P.NAME
  ,P.DOCUMENT
  ,floor(months_between(sysdate, birthdate) /12) as idade
  ,P.PHONENUMBER1
  ,P.REGISTRATIONDATE
  ,floor(sysdate  - TRUNC(P.REGISTRATIONDATE)) as  dias_cadastro
  ,C.CONTRACTDATE
  ,CL.loanstatus
  ,fd.marginloan as MARGINLOAN
  ,CL.LOANTYPE
  ,p.enrollment as ENROLLMENT
  ,i.paidinstallments
  ,CL.NOMINALRATEPERMONTH
  ,P.REGISTRATIONDATE
  ,l.OPERATIONSTEPTYPE
  FROM alias.PERSON P
  INNER JOIN alias.CONTRACT C ON C.PERSONID = P.ID
  INNER JOIN alias.PERSONFINANCIALDATA fd ON p.id = fd.PERSONID
  INNER JOIN alias.CONTRACTLOAN CL ON CL.CONTRACTID = C.ID
  INNER JOIN alias.OPERATIONSTEPLOG l ON l.CONTRACTID = C.ID 
  INNER JOIN (select PERSONID, MAX(PAIDINSTALLMENTS) as paidinstallments, INSTALLMENTVALUE from alias.loanhistory
  GROUP BY INSTALLMENTVALUE, PERSONID) i on i.PERSONID = P.ID
  WHERE 1=1
  AND REGISTRATIONDATE >= to_date('2018-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND REGISTRATIONDATE <= to_date('2020-10-31:00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND FD.MARGINLOAN >= 20
  --AND LOANTYPE <> 'FUTUREMARGIN'
  --AND l.OPERATIONSTEPTYPE NOT IN ('PORT_REFUSED_FRAUD','REFUSED_FRAUD', 'REFUSED_NOT_LITERATE','PORT_REFUSED_NOT_LITERATE')
  AND floor(months_between(sysdate, birthdate) /12) < 76 and floor(months_between(sysdate, birthdate) /12) > 20
  AND P.REGISTRATIONSTATUS IN ('COMPLETE')
  AND (P.AGREEMENTID != 2)
  AND P.AGREEMENTID = 42
  AND (P.REGISTRATIONSTATUS IS NOT NULL AND P.REGISTRATIONSTATUS != 'OPENED')
  AND P.ENROLLMENT IS NOT NULL
  
  """
  contrato = pd.read_sql_query(query, connection)
  
  connection.close()
  return(contrato)

  def scoring(contrato):
    contrato['taxa_intervalo'] = pd.cut(contrato['NOMINALRATEPERMONTH'],bins = [0, 0.0130, 0.0150, 0.0170, 0.0200, 3])
    contrato = contrato[contrato['PAIDINSTALLMENTS']>0]
    contrato['parcelas_intervalo'] =pd.cut(contrato['PAIDINSTALLMENTS'],bins = [0, 6, 12, 80])
    contrato = contrato[contrato['DIAS_CADASTRO']>=2]
    contrato['dias_intervalo'] = pd.cut(contrato['DIAS_CADASTRO'],bins = [2,7,15,30,10000])

    tax = contrato['taxa_intervalo'].cat.categories.astype(str)
    par = contrato['parcelas_intervalo'].cat.categories.astype(str)
    di  = contrato['dias_intervalo'].cat.categories.astype(str)

    taxa_df = pd.DataFrame({'tax':contrato['taxa_intervalo'].cat.categories.astype(str)})
    taxa_df['score_taxa'] = pd.DataFrame({'score':[18,6,12,24,30]})       
    taxa_df['tax'] = taxa_df['tax'].astype(str)

    dias_df = pd.DataFrame({'dia':contrato['dias_intervalo'].cat.categories.astype(str)})
    dias_df['score_dias'] = pd.DataFrame({'score_dias':[20,15,10,5]})       
    dias_df['dia']= dias_df['dia'].astype(str)

    par_df = pd.DataFrame({'parc':contrato['parcelas_intervalo'].cat.categories.astype(str)})
    par_df['score_parcelas'] = pd.DataFrame({'score_parceloas':[9,6,3]})       
    par_df['parc']= par_df['parc'].astype(str)

    contrato['dias_intervalo'] = contrato['dias_intervalo'].apply(lambda x: str(x)).astype(str)
    contrato['parcelas_intervalo'] = contrato['parcelas_intervalo'].astype(str)
    contrato['taxa_intervalo'] = contrato['taxa_intervalo'].astype(str)

    contrato = contrato.merge(taxa_df,left_on = 'taxa_intervalo', right_on = 'tax')

    contrato = contrato.merge(par_df,left_on = 'parcelas_intervalo', right_on = 'parc')

    contrato = contrato.merge(dias_df,left_on = 'dias_intervalo', right_on = 'dia')

    contrato = contrato.drop(['tax','parc','dia'],axis='columns')

    contrato['escore'] = contrato.apply(lambda x:x.iloc[21] + x.iloc[22] + x.iloc[23], axis=1)
    return(contrato)


    def data_wrangling(consulta):
      escores_person = consulta[['PERSONID','LOANTYPE','INSTALLMENTVALUE','NAME' \
      ,'IDADE','ENROLLMENT','PHONENUMBER1','MARGINLOAN','DOCUMENT','escore']] \
      .groupby(['PERSONID','NAME','IDADE','LOANTYPE','DOCUMENT','ENROLLMENT' \
       ,'PHONENUMBER1','escore']).agg(['min','mean','max','sum','count'])
      return(escores_person)

#para cada pessoa libera portabildiade

def liberar_portabilidade(pid):
  r=[]
  URL = #endpoint
  api_token = #bearer
  headers = {'Content-Type': 'application/json',
  'Authorization': 'Bearer {0}'.format(api_token)}
  r.append(re.post(url = URL, headers= headers, json = {"unlockList":[str(pid)]}))
  return(r)   

#ese nao tiver oportunidade eu excluo
def verificar_oportunidade(dados):
  URL = #endpoint
  api_token = #bearer

  headers = {'Content-Type': 'application/json',
  'Authorization': 'Bearer {0}'.format(api_token)}

  payload = {"document": "" + dados.DOCUMENT, "enrollment": "" + dados.ENROLLMENT}
    # sending get request and saving the response as response object
    r = re.post(url = URL, headers= headers, json = payload)

    response = r.json()["resource"]
    return(response)  

    def data_tos3(**kwargs):
    aakid= ##creds3
    asak=#creds3
    client_bucket = boto3.client(
      "s3",
      aws_access_key_id=aakid,
      aws_secret_access_key=asak,
      region_name="us-east-1")
    dta = data_wrangling(scoring(consulta()))
    #dta = data_wrangling(dta)
    dta.columns = dta.columns.map('_'.join).str.strip('_')
    dta.reset_index(inplace=True)  
    URL = #ENDPOINT
    api_token = #Bearer'
    headers = {'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(api_token)}

    for ind,i in dta.iterrows():
      payload = {"document": "" + i.DOCUMENT, "enrollment": "" + i.ENROLLMENT}
        # sending get request and saving the response as response object
        r = re.post(url = URL, headers= headers, json = payload)
        response = r.json()["resource"]
        rangesForItem = response['rangesForNew']['rangeItem']
        if((response['rangesForNew'] == None or len(response['rangesForNew']['rangeItem'])==0) or rangesForItem == None):
          if(response['rangesForPortability'] == [] or response['rangesForPortability'] == None ):
            dta = dta.drop([ind])
          elif(len(pd.DataFrame(response['rangesForPortability']).rangeItem) == 0):
            dta = dta.drop([ind])
            liberar_portabilidade(i['PERSONID'])
            resp = consulta_in100(i['PERSONID'])
            if(resp.json()["resource"] == False):
              dta = dta.drop([ind])
              dta.to_csv('/home/git/producao/dags/buffer_scoring_opportunity.csv',index=False,header=False,encoding='utf-8')
              client_bucket.upload_file('/home/git/producao/dags/buffer_scoring_opportunity.csv',\
                'buffer-redshift','buffer_scoring_opportunity.csv')
              os.remove('/home/git/producao/dags/buffer_scoring_opportunity.csv')        


default_args = {
'owner': 'jrs',
'depends_on_past': False,
'start_date': datetime(2020, 4, 13,0,0), 
'email_on_failure': True,
'email_on_retry': False,
'retries': 0,
'retry_delay': timedelta(hours=24)
}

dag = DAG('dag_oportunidades_escores', default_args = default_args,   schedule_interval = '40 * * * *', catchup = False)


t1 = PythonOperator(
  task_id='etl',
  python_callable = data_tos3,
  provide_context = True,
  dag=dag)

t2 = PostgresOperator(
  task_id='s3_to_redshift',
  postgres_conn_id='redshift',
  sql="""BEGIN;
  ### CREDENCIAIS

  COMMIT;""",
  dag=dag)


t1 >> t2



