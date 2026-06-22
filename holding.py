import requests
import pandas as pd
from pandas import json_normalize
import time

# Lecture du fichier
df_pm = pd.read_excel("entreprises_siren_74_V12pm.xlsx")

# Liste des SIREN à rechercher
sirens = (
    df_pm["dirigeant_siren"]
    .dropna()
    .astype(str)
    .str.replace(".0", "", regex=False)
    .unique()
)

base_url = "https://recherche-entreprises.api.gouv.fr/search"
headers = {"accept": "application/json"}

all_results = []

print("DÉBUT DE LA RÉCUPÉRATION")

for i, siren in enumerate(sirens, start=1):
    print(f"{i}/{len(sirens)} : {siren}")

    try:
        r = requests.get(
            base_url,
            headers=headers,
            params={"q": siren},
            timeout=20
        )

        if r.status_code != 200:
            print(f"Erreur HTTP {r.status_code}")
            continue

        data = r.json()
        results = data.get("results", [])

        if results:
            all_results.append(results[0])

        time.sleep(0.2)

    except Exception as e:
        print(f"Erreur sur {siren} : {e}")

print(f"Total entreprises récupérées : {len(all_results)}")

# Création du DataFrame
df_raw = pd.DataFrame(all_results)

# On explose 'siege'
if "siege" in df_raw.columns:
    siege_df = json_normalize(df_raw["siege"]).add_prefix("siege_")
    df_raw = pd.concat(
        [df_raw.drop(columns=["siege"]), siege_df],
        axis=1
    )

# On explose 'dirigeants'
if "dirigeants" in df_raw.columns:
    df_raw = df_raw.explode("dirigeants").reset_index(drop=True)

    dirigeants_df = json_normalize(
        df_raw["dirigeants"].apply(
            lambda x: x if isinstance(x, dict) else {}
        )
    ).add_prefix("dirigeant_")

    df_raw = pd.concat(
        [df_raw.drop(columns=["dirigeants"]), dirigeants_df],
        axis=1
    )

# On explose 'matching_etablissements'
if "matching_etablissements" in df_raw.columns:
    df_raw = df_raw.explode("matching_etablissements").reset_index(drop=True)

    etab_df = json_normalize(
        df_raw["matching_etablissements"].apply(
            lambda x: x if isinstance(x, dict) else {}
        )
    ).add_prefix("etab_")

    df_raw = pd.concat(
        [df_raw.drop(columns=["matching_etablissements"]), etab_df],
        axis=1
    )

# On explose 'finances'
if "finances" in df_raw.columns:
    finances_df = json_normalize(df_raw["finances"]).add_prefix("finances_")

    df_raw = pd.concat(
        [df_raw.drop(columns=["finances"]), finances_df],
        axis=1
    )

# On explose 'complements'
if "complements" in df_raw.columns:
    complements_df = json_normalize(
        df_raw["complements"]
    ).add_prefix("complements_")

    df_raw = pd.concat(
        [df_raw.drop(columns=["complements"]), complements_df],
        axis=1
    )

# Suppression des doublons
if "siren" in df_raw.columns:
    df_raw = df_raw.drop_duplicates(subset="siren")

# Export
output_file = "entreprises_siren_74_V14.xlsx"
df_raw.to_excel(output_file, index=False)

print(f"Fichier créé : {output_file}")