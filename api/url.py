import pandas as pd
import urllib.parse

# === Charger le fichier existant ===
df = pd.read_excel("entreprises_siren_74_V2.xlsx")

# === Colonnes utilisées ===
col_nom = "nom_complet"
col_commune = "etab_libelle_commune"

# === Construire la requête texte ===
df["recherche_google"] = (
    df[col_nom].fillna("") + " " + df[col_commune].fillna("")
).str.strip()

# === Encoder pour URL Google ===
df["recherche_google"] = df["recherche_google"].apply(
    lambda x: "https://www.google.com/search?q=" + urllib.parse.quote_plus(x)
)

# === Sauvegarde ===
df.to_excel("entreprises_siret_74_V3.xlsx", index=False)

print("Fichier exporté : entreprises_siret_74_V3.xlsx")
