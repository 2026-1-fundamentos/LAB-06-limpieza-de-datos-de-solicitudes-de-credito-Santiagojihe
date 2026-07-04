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

df['tipo_de_emprendimiento']=df['tipo_de_emprendimiento'].replace({'nan':np.nan,'':np.nan})
df['barrio']=df['barrio'].replace({'nan':np.nan,'':np.nan})

# candidate filters
for allowed in [None, ['microempresarial','agropecuaria','credioportuno','empresarial ed.','juridica y cap.semilla','fomento agropecuario','soli-diaria','solidaria','ayacucho formal'], ['microempresarial','agropecuaria','credioportuno']]:
    t=df.copy()
    t=t.dropna(subset=['tipo_de_emprendimiento','barrio'])
    t=t.drop_duplicates()
    if allowed is not None:
        t=t[t['línea_credito'].isin(allowed)]
    print('allowed', allowed, 'rows', len(t))
    print(t['línea_credito'].value_counts().to_string())
    print('---')
