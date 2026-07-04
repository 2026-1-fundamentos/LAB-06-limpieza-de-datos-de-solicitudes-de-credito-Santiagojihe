import pandas as pd
import numpy as np

path='files/input/solicitudes_de_credito.csv'
df=pd.read_csv(path, sep=';').drop(columns=['Unnamed: 0'])

def norm(s):
    if pd.isna(s):
        return np.nan
    s=str(s).strip().lower()
    s=s.replace('_',' ')
    s=' '.join(s.split())
    return s

for col in ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','línea_credito']:
    df[col]=df[col].apply(norm)

valid_types={'comercio','servicio','industria','agropecuaria'}
valid_sex={'masculino','femenino'}

print('rows with valid type', df['tipo_de_emprendimiento'].isin(valid_types).sum())
print('rows with valid type+nonempty barrio', (df['tipo_de_emprendimiento'].isin(valid_types) & df['barrio'].notna().astype(bool) & (df['barrio']!='')).sum())
print('rows with valid type+nonempty barrio+valid sex', (df['tipo_de_emprendimiento'].isin(valid_types) & df['barrio'].notna().astype(bool) & (df['barrio']!='') & df['sexo'].isin(valid_sex)).sum())
print('rows with valid type+sex+nonempty barrio and not duplicated on selected subset')
subset=['sexo','tipo_de_emprendimiento','idea_negocio','barrio','estrato','comuna_ciudadano','fecha_de_beneficio','monto_del_credito','línea_credito']
mask=(df['tipo_de_emprendimiento'].isin(valid_types) & df['barrio'].notna().astype(bool) & (df['barrio']!='') & df['sexo'].isin(valid_sex))
print(mask.sum())
print(df.loc[mask, 'tipo_de_emprendimiento'].value_counts().to_dict())
print(df.loc[mask, 'sexo'].value_counts().to_dict())
# after dropping duplicates by subset
print('after dedup', df.loc[mask].drop_duplicates(subset=subset).shape[0])
print(df.loc[mask].drop_duplicates(subset=subset)['sexo'].value_counts().to_dict())
print(df.loc[mask].drop_duplicates(subset=subset)['tipo_de_emprendimiento'].value_counts().to_dict())
