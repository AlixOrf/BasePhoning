import pandas as pd
import os

# Fichiers
FICHIER_ENTREE = "entreprises_siren_95_V8.xlsx"
DOSSIER_SORTIE = "finaux"
FICHIER_SORTIE = os.path.join(DOSSIER_SORTIE, "95.xlsx")

# Création du dossier si nécessaire
os.makedirs(DOSSIER_SORTIE, exist_ok=True)

# Lecture du fichier
df = pd.read_excel(FICHIER_ENTREE)

# Renommage de la colonne
df = df.rename(columns={"nom_complet": "nom"})
df = df.rename(columns={"nombre_etablissements_ouverts": "établissements"})

# Conversion de la date
if "date_creation" in df.columns:
    df["date_creation"] = pd.to_datetime(
        df["date_creation"],
        errors="coerce"
    )

# Conversion de la date
if "dirigeant_date_de_naissance" in df.columns:
    df["dirigeant_date_de_naissance"] = pd.to_datetime(
        df["dirigeant_date_de_naissance"],
        errors="coerce"
    )


# Écriture Excel avec format de date
with pd.ExcelWriter(
    FICHIER_SORTIE,
    engine="openpyxl",
    datetime_format="dd/mm/yyyy"
) as writer:
    df.to_excel(writer, index=False)

print(f"Fichier créé : {FICHIER_SORTIE}")