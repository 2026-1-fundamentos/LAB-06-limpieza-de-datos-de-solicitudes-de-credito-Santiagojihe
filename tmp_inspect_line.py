import pandas as pd
import numpy as np

path='files/input/solicitudes_de_credito.csv'
df=pd.read_csv(path, sep=';').drop(columns=['Unnamed: 0'])
for col in ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','línea_credito']:
    df[col]=df[col].astype(str).str.strip()
for col in ['sexo','tipo_de_emprendimiento','línea_credito']:
    df[col]=df[col].str.lower()
for col in ['idea_negocio','barrio']:
    df[col]=df[col].str.lower()
    df[col]=df[col].str.replace('_',' ', regex=False)
    df[col]=df[col].str.replace(r'\s+',' ', regex=True)
    df[col]=df[col].str.strip()

print(df['línea_credito'].value_counts(dropna=False).to_string())
print('---')
print(df['tipo_de_emprendimiento'].value_counts(dropna=False).to_string())
