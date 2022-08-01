import string
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Criar lista das 24 horas
horas = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

# Obter dia de ontem
yesterday = datetime.now() - timedelta(1)
dia = datetime.strftime(yesterday, '%Y-%m-%d')
dia = [dia]

### Air Temperature


dias_horas = []

for hora in horas:
    result = [s + '_' + hora for s in dia]
    dias_horas.append(result)
    
dias_horas = [item for sublist in dias_horas for item in sublist]

df = pd.DataFrame()

for x in dias_horas:
    url = "http://coastsense.colabatlantic.com/output/temp_lisboa/json/lx_temp_{}.json".format(x)
    resp = requests.get(url)
    txt = resp.json()
    results = pd.DataFrame(txt['addressPoints'])
    results['Date_Hour'] = x
    df = df.append(results, ignore_index=True)
    
# Rename column
df = df.rename(columns={0: "lat", 1: "lon", 2: "Value"})


### Thermal Amplitude



dias_horas = []

for hora in horas:
    result = [s + '_' + hora for s in dia]
    dias_horas.append(result)
    
dias_horas = [item for sublist in dias_horas for item in sublist]

df_termal = pd.DataFrame()

for x in dias_horas:
    url = "http://coastsense.colabatlantic.com/output/temp_lisboa/json/lx_temp_avg_{}.json".format(x)
    resp = requests.get(url)
    txt = resp.json()
    results = pd.DataFrame(txt['addressPoints'])
    results['Date_Hour'] = x
    df_termal = df_termal.append(results, ignore_index=True)
    
    
# Rename column
df_termal = df_termal.rename(columns={0: "lat", 1: "lon", 2: "Value"})




# Get today date now to file name when export to csv or excel with encoding utf8
df.to_csv((datetime.now()+timedelta(hours=1)).strftime('data_sources/data_transformed/air_temperature-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)
df_termal.to_csv((datetime.now()+timedelta(hours=1)).strftime('data_sources/data_transformed/air_temperature-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)
