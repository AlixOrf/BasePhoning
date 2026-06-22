import requests
import pandas as pd
from pandas import json_normalize
import time

# Lecture du fichier de départ
df_principal = pd.read_excel("entreprises_siren_74_V12pm.xlsx")

colonnes_dirigeant = [
    "dirigeant_nom",
    "dirigeant_prenoms",
    "dirigeant_annee_de_naissance",
    "dirigeant_date_de_naissance",
    "dirigeant_qualite",
    "dirigeant_nationalite",
    "dirigeant_siren",
    "dirigeant_type_dirigeant"
]

for col in colonnes_dirigeant:
    if col in df_principal.columns:
        df_principal[col] = df_principal[col].astype("object")

# Uniformisation du SIREN dirigeant
df_principal["dirigeant_siren"] = (
    df_principal["dirigeant_siren"]
    .fillna("")
    .astype(str)
    .str.replace(".0", "", regex=False)
)

base_url = "https://recherche-entreprises.api.gouv.fr/search"
headers = {"accept": "application/json"}

tour = 1

while True:

    print(f"\n----- TOUR {tour} -----")

    # Lignes dont le dirigeant est une personne morale
    masque_pm = (
        df_principal["dirigeant_type_dirigeant"]
        .fillna("")
        .str.lower()
        .eq("personne morale")
    )

    nb_pm = masque_pm.sum()

    print(f"{nb_pm} personnes morales restantes")

    # Fin si plus aucune personne morale
    if nb_pm == 0:
        break

    # SIREN à rechercher
    sirens = (
        df_principal.loc[masque_pm, "dirigeant_siren"]
        .dropna()
        .astype(str)
        .str.replace(".0", "", regex=False)
        .unique()
    )

    all_results = []

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

            results = r.json().get("results", [])

            if results:
                all_results.append(results[0])

            time.sleep(0.2)

        except Exception as e:
            print(f"Erreur sur {siren} : {e}")

    if len(all_results) == 0:
        print("Aucun résultat trouvé.")
        break

    df_raw = pd.DataFrame(all_results)

    # Déplier les dirigeants
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

    # On garde uniquement les colonnes utiles
    colonnes_utiles = [
        "siren",
        "dirigeant_nom",
        "dirigeant_prenoms",
        "dirigeant_annee_de_naissance",
        "dirigeant_date_de_naissance",
        "dirigeant_qualite",
        "dirigeant_nationalite",
        "dirigeant_siren",
        "dirigeant_type_dirigeant"
    ]

    colonnes_existantes = [
        c for c in colonnes_utiles if c in df_raw.columns
    ]

    df_infos = df_raw[colonnes_existantes].copy()

    # Uniformisation du SIREN
    df_infos["siren"] = (
        df_infos["siren"]
        .fillna("")
        .astype(str)
        .str.replace(".0", "", regex=False)
    )

    # Création d'un dictionnaire de recherche
    infos_dict = (
        df_infos
        .drop_duplicates(subset="siren")
        .set_index("siren")
        .to_dict("index")
    )

    # Mise à jour uniquement des lignes concernées
    for index, row in df_principal.loc[masque_pm].iterrows():

        siren = row["dirigeant_siren"]

        if siren not in infos_dict:
            continue

        infos = infos_dict[siren]

        for colonne in [
            "dirigeant_nom",
            "dirigeant_prenoms",
            "dirigeant_annee_de_naissance",
            "dirigeant_date_de_naissance",
            "dirigeant_qualite",
            "dirigeant_nationalite",
            "dirigeant_siren",
            "dirigeant_type_dirigeant"
        ]:

            if colonne in infos:
                df_principal.at[index, colonne] = infos[colonne]

    tour += 1

# Export final
df_principal.to_excel(
    "entreprises_siren_74_final.xlsx",
    index=False
)

print("\nTerminé.")
print("Fichier créé : entreprises_siren_74_final.xlsx")