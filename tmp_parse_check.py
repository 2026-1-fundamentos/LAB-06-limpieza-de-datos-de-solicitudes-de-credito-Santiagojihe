import pandas as pd
import numpy as np
import re

path='files/input/solicitudes_de_credito.csv'
df=pd.read_csv(path, sep=';').drop(columns=['Unnamed: 0'])


def parse_money(x):
    if pd.isna(x):
        return np.nan
    s=str(x).strip().replace('$','').replace('.','').replace(',','').replace(' ','')
    if s in {'', 'nan', 'none'}:
        return np.nan
    try:
        return float(s)
    except Exception:
        return np.nan

# normalize text
for col in ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','línea_credito']:
    df[col] = df[col].astype(str).str.strip()
for col in ['sexo','tipo_de_emprendimiento','línea_credito']:
    df[col] = df[col].str.lower()
for col in ['idea_negocio','barrio']:
    df[col] = df[col].str.lower()
    df[col] = df[col].str.replace('_',' ', regex=False)
    df[col] = df[col].str.replace(r'\s+',' ', regex=True)
    df[col] = df[col].str.strip()

df['monto_del_credito'] = df['monto_del_credito'].apply(parse_money)
print('missing monto', df['monto_del_credito'].isna().sum())
print('monto <=0', (df['monto_del_credito']<=0).sum())
print('monto categories', df[df['monto_del_credito'].isna()].head(20).to_string())
print('rows with missing monto by line', df[df['monto_del_credito'].isna()]['línea_credito'].value_counts().to_string())
