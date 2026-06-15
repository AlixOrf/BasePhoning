import requests
import pandas as pd
from pandas import json_normalize
import time

# Ici les éléments que je filtre pour récupérer mes données
base_url = "https://recherche-entreprises.api.gouv.fr/search"
params = {
    "departement": "74", # Le département, pas compliqué c'est le même que le code postal
    "etat_administratif": "A", # Si l'entreprise est active où non
    "est_association": "false", # Si ce n'est pas une assosiation (revérifier derrière)
    "activite_principale": "09.10Z,09.90Z,10.11Z, 10.12Z, 10.13B, 10.20Z, 10.31Z, 10.32Z, 10.39A, 10.39B, 10.41B, 10.42Z, 10.51A, 10.51D, 10.52Z, 10.61A, 10.61B, 10.62Z, 10.71A, 10.71B, 10.71D, 10.72Z,10.73Z, 10.81Z, 10.82Z, 10.83Z, 10.84Z, 10.85Z, 10.86Z, 10.89Z, 10.91Z, 10.92Z, 11.01Z, 11.02A, 11.02B, 11.03Z, 11.04Z, 11.05Z, 11.06Z, 11.07A, 11.07B, 13.10Z, 13.20Z, 13.30Z, 13.91Z, 13.92Z, 13.93Z, 13.94Z, 13.95Z, 13.96Z, 13.99Z, 14.11Z, 14.12Z, 14.13Z, 14.14Z, 14.19Z, 14.20Z, 14.31Z, 14.39Z, 15.11Z, 15.12Z, 15.20Z, 16.10A, 16.10B, 16.21Z, 16.22Z, 16.23Z, 16.24Z, 16.29Z, 17.11Z, 17.12Z, 17.21A, 17.21B, 17.21C, 17.22Z, 17.23Z, 17.24Z, 17.29Z, 18.11Z, 18.12Z, 18.13Z, 18.14Z, 18.20Z, 20.11Z, 20.12Z, 20.13A, 20.13B, 20.14Z, 20.15Z, 20.16Z, 20.17Z, 20.20Z, 20.30Z, 20.41Z, 20.42Z, 20.51Z, 20.52Z, 20.53Z, 20.59Z, 20.60Z, 21.10Z, 21.20Z, 22.11Z, 22.19Z, 22.21Z, 22.22Z, 22.23Z, 22.29A, 22.29B, 23.11Z, 23.12Z, 23.13Z, 23.14Z, 23.19Z, 23.20Z, 23.31Z, 23.32Z, 23.41Z, 23.42Z, 23.43Z, 23.44Z, 23.49Z, 23.51Z, 23.52Z, 23.61Z, 23.62Z, 23.63Z, 23.64Z, 23.65Z, 23.69Z, 23.70Z, 23.91Z, 23.99Z, 24.10Z, 24.20Z, 24.31Z, 24.32Z, 24.33Z, 24.34Z, 24.41Z, 24.42Z, 24.43Z, 24.44Z, 24.45Z, 24.46Z, 24.51Z, 24.52Z, 24.53Z, 24.54Z, 25.11Z, 25.12Z, 25.21Z, 25.29Z, 25.30Z, 25.40Z, 25.50A, 25.50B, 25.61Z, 25.62A, 25.62B, 25.71Z, 25.72Z, 25.73A, 25.73B, 25.91Z, 25.92Z, 25.93Z, 25.94Z, 25.99A, 25.99B, 26.11Z, 26.12Z, 26.20Z, 26.30Z, 26.40Z, 26.51A, 26.51B, 26.52Z, 26.60Z, 26.70Z, 26.80Z, 27.11Z, 27.12Z, 27.20Z, 27.31Z, 27.32Z, 27.33Z, 27.40Z, 27.51Z, 27.52Z, 27.90Z, 28.11Z, 28.12Z, 28.13Z, 28.14Z, 28.15Z, 28.21Z, 28.22Z, 28.23Z, 28.24Z, 28.25Z, 28.29A, 28.29B, 28.30Z, 28.41Z, 28.49Z, 28.91Z, 28.92Z, 28.93Z, 28.94Z, 28.95Z, 28.96Z, 28.99A, 28.99B, 29.10Z, 29.20Z, 29.31Z, 29.32Z, 30.11Z, 30.12Z, 30.20Z, 30.30Z, 30.40Z, 30.91Z, 30.92Z, 30.99Z, 31.01Z, 31.02Z, 31.03Z, 31.09A, 31.09B, 32.11Z, 32.12Z, 32.13Z, 32.20Z, 32.30Z, 32.40Z, 32.50A, 32.50B, 32.91Z, 32.99Z, 33.11Z, 33.12Z, 33.13Z, 33.14Z, 33.15Z, 33.16Z, 33.17Z, 33.19Z, 33.20A, 33.20B, 33.20C, 33.20D, 41.10A, 41.10B, 41.10C, 41.10D, 41.20A, 41.20B, 42.11Z, 42.12Z, 42.13A, 42.13B, 42.21Z, 42.22Z, 42.91Z, 42.99Z, 43.11Z, 43.12A, 43.12B, 43.13Z, 43.21A, 43.21B, 43.22A, 43.22B, 43.29A, 43.29B, 43.31Z, 43.32A, 43.32B, 43.32C, 43.33Z, 43.34Z, 43.39Z, 43.91A, 43.91B, 43.99A, 43.99B, 43.99C, 43.99D, 43.99E, 46.11Z, 46.12A, 46.12B, 46.13Z, 46.14Z, 46.15Z, 46.16Z, 46.17A, 46.17B, 46.18Z, 46.19A, 46.19B, 46.21Z, 46.22Z, 46.23Z, 46.24Z, 46.31Z, 46.32A, 46.32B, 46.32C, 46.33Z, 46.34Z, 46.35Z, 46.36Z, 46.37Z, 46.38A, 46.38B, 46.39A, 46.39B, 46.41Z, 46.42Z, 46.43Z, 46.44Z, 46.45Z, 46.46Z, 46.47Z, 46.48Z, 46.49Z, 46.51Z, 46.52Z, 46.61Z, 46.62Z, 46.63Z, 46.64Z, 46.65Z, 46.66Z, 46.69A, 46.69B, 46.69C, 46.71Z, 46.72Z, 46.73A, 46.73B, 46.74A, 46.74B, 46.75Z, 46.76Z, 46.77Z, 46.90Z, 49.10Z, 49.20Z, 49.31Z, 49.32Z, 49.39A, 49.39B, 49.39C, 49.41A, 49.41B, 49.41C, 49.42Z, 49.50Z, 50.10Z, 50.20Z, 50.30Z, 50.40Z, 53.20Z, 58.11Z, 58.12Z, 58.13Z, 58.14Z, 58.19Z, 58.21Z, 58.29A, 58.29B, 58.29C, 59.11A, 59.11B, 59.12Z, 59.13A, 59.13B, 61.10Z, 61.20Z, 61.30Z, 61.90Z, 62.01Z, 62.02A, 62.02B, 62.03Z, 62.09Z, 63.11Z, 63.12Z, 63.91Z, 63.99Z, 65.11Z, 65.12Z, 65.20Z, 71.12A, 71.12B, 71.20B, 72.11Z, 72.19Z, 72.20Z, 73.11Z, 73.12Z, 73.20Z, 74.10Z, 74.20Z, 74.30Z, 74.90A, 74.90B, 79.11Z, 79.12Z, 79.90Z, 81.10Z, 81.21Z, 81.22Z, 81.29A, 81.29B, 81.30Z, 52.29A, 52.29B, 66.22Z, 70.22Z, 82.92Z, 85.59A, 86.90A, 86.90B", # Le code NAF ou code APE, un code d'activité suivant la nomenclature de l'INSEE valide en juin 2026 (cf README)
    "tranche_effectif_salarie": "03,11,12,21", # Tranche du nombre de salariés (cf README)
    #"nature_juridique" : "", # Nature de l'entreprise (cf README)
    "date_naissance_personne_min" : "1954-01-01", # Les personne de moins de 72 ans (repasser derrière)
    "date_naissance_personne_max" : "1972-01-01", # Les personne de plus de 54 ans (repasser derrière)
    "per_page": 25,
    "page": 1  
}
headers = {"accept": "application/json"}

DELAY = 1  # Délais en secondes entre chaque requête sinon ça bloque

all_results = []
seen_sirens = set()

print("DÉBUT DE LA RÉCUPÉRATION")

while True:
    print(f"Page {params['page']}...")

    try:
        r = requests.get(base_url, headers=headers, params=params, timeout=20)
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau : {e}")
        break

    # Vérification HTTP
    if r.status_code != 200:
        print(f"Erreur HTTP {r.status_code}")
        print(r.text[:300])
        break

    # Vérification JSON
    try:
        data = r.json()
    except Exception:
        print("Réponse non JSON")
        print(r.text[:300])
        break

    results = data.get("results", [])

    if not results:
        print("Plus de résultats.")
        break

    # Déduplication SIREN
    new_results = []
    for company in results:
        siren = company.get("siren")
        if siren and siren not in seen_sirens:
            seen_sirens.add(siren)
            new_results.append(company)

    if not new_results:
        print("Aucun nouvel établissement trouvé, arrêt.")
        break

    all_results.extend(new_results)
    params["page"] += 1

    time.sleep(DELAY)

print(f"Total entreprises uniques récupérées : {len(all_results)}")

# Ici on a récupéré les données, maintenant ménage !
df_raw = pd.DataFrame(all_results)

# On explose 'siege'
if "siege" in df_raw.columns:
    df_raw = df_raw.explode("siege").reset_index(drop=True)
    siege_df = json_normalize(
        df_raw["siege"].apply(lambda x: x if isinstance(x, dict) else {})
    ).add_prefix("siege_")
    df_raw = pd.concat([df_raw.drop(columns=["siege"]), siege_df], axis=1)

# On explose 'dirigeants'
if "dirigeants" in df_raw.columns:
    df_raw = df_raw.explode("dirigeants").reset_index(drop=True)
    dirigeants_df = json_normalize(
        df_raw["dirigeants"].apply(lambda x: x if isinstance(x, dict) else {})
    ).add_prefix("dirigeant_")
    df_raw = pd.concat([df_raw.drop(columns=["dirigeants"]), dirigeants_df], axis=1)

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

# On exploser 'complements'
if "complements" in df_raw.columns:
    complements_df = json_normalize(df_raw["complements"]).add_prefix("complements_")
    df_raw = pd.concat(
        [df_raw.drop(columns=["complements"]), complements_df],
        axis=1
    )

# On refiltre au cas où
for col in ["complements_est_association", "complements_est_service_public"]:
    if col not in df_raw.columns:
        df_raw[col] = "FAUX"

df_raw["etab_est_siege"] = (
    df_raw["etab_est_siege"]
    .astype(str)
    .str.strip()
    .str.upper()
)

mask_exclude = (
    (df_raw["complements_est_association"] == "VRAI") |
    (df_raw["complements_est_service_public"] == "VRAI") |
    (df_raw["complements_est_ess"] == "VRAI") |
    (df_raw["complements_est_administration"] == "VRAI") |
    (df_raw["etab_est_siege"] == "FALSE") |
    (df_raw["dirigeant_annee_de_naissance"] < "1954") |
    (df_raw["dirigeant_annee_de_naissance"] > "1972")
)
df_raw = df_raw[~mask_exclude].reset_index(drop=True)


# On enlève les doublons (il devrait pas en avoir)
if "siren" in df_raw.columns:
    df_raw = df_raw.drop_duplicates(subset="siren", keep="first")

# Et on exporte
output_file = "entreprises_siren_74_V10.xlsx"
df_raw.to_excel(output_file, index=False)

print(f"Fichier créé : {output_file}")