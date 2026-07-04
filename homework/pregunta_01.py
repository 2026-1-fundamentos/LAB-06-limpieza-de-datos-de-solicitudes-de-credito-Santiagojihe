import pandas as pd
import os

def pregunta_01():
    """
    Realice la limpieza de los datos y guarde el resultado.
    """
    # 1. Cargar los datos (nota: la ruta relativa es desde la raíz del proyecto)
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")
    
    # Eliminar la columna de índice defectuosa si existe
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # 2. Limpieza de columnas de texto
    cols_texto = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "línea_credito"]
    for col in cols_texto:
        df[col] = df[col].astype(str).str.lower()
        df[col] = df[col].str.replace("_", " ", regex=False)
        df[col] = df[col].str.replace("-", " ", regex=False)
        df[col] = df[col].str.replace(r"\s+", " ", regex=True)
        df[col] = df[col].str.strip()
        df[col] = df[col].replace({'nan': pd.NA, 'none': pd.NA, '': pd.NA})

    # 3. Limpieza de la columna monetaria
    df["monto_del_credito"] = df["monto_del_credito"].astype(str)
    df["monto_del_credito"] = df["monto_del_credito"].str.replace("$", "", regex=False)
    df["monto_del_credito"] = df["monto_del_credito"].str.replace(",", "", regex=False)
    df["monto_del_credito"] = df["monto_del_credito"].str.strip()
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")

    # 4. Limpieza de fechas
    df["fecha_de_beneficio"] = pd.to_datetime(df["fecha_de_beneficio"], dayfirst=True, format="mixed", errors="coerce")

    # Normalizar numéricas extra
    df["estrato"] = pd.to_numeric(df["estrato"], errors="coerce")
    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors="coerce")

    # 5. Eliminar valores nulos y duplicados
    df = df.dropna()
    df = df.drop_duplicates()

    # 6. Guardar el archivo limpio
    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)

if __name__ == "__main__":
    pregunta_01()