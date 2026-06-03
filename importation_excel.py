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
    "activite_principale": "0910Z,0990Z,1011Z, 1012Z, 1013B, 1020Z, 1031Z, 1032Z, 1039A, 1039B, 1041B, 1042Z, 1051A, 1051D, 1052Z, 1061A, 1061B, 1062Z, 1071A, 1071B, 1071D, 1072Z,1073Z, 1081Z, 1082Z, 1083Z, 1084Z, 1085Z, 1086Z, 1089Z, 1091Z, 1092Z, 1101Z, 1102A, 1102B, 1103Z, 1104Z, 1105Z, 1106Z, 1107A, 1107B, 1310Z, 1320Z, 1330Z, 1391Z, 1392Z, 1393Z, 1394Z, 1395Z, 1396Z, 1399Z, 1411Z, 1412Z, 1413Z, 1414Z, 1419Z, 1420Z, 1431Z, 1439Z, 1511Z, 1512Z, 1520Z, 1610A, 1610B, 1621Z, 1622Z, 1623Z, 1624Z, 1629Z, 1711Z, 1712Z, 1721A, 1721B, 1721C, 1722Z, 1723Z, 1724Z, 1729Z, 1811Z, 1812Z, 1813Z, 1814Z, 1820Z, 2011Z, 2012Z, 2013A, 2013B, 2014Z, 2015Z, 2016Z, 2017Z, 2020Z, 2030Z, 2041Z, 2042Z, 2051Z, 2052Z, 2053Z, 2059Z, 2060Z, 2110Z, 2120Z, 2211Z, 2219Z, 2221Z, 2222Z, 2223Z, 2229A, 2229B, 2311Z, 2312Z, 2313Z, 2314Z, 2319Z, 2320Z, 2331Z, 2332Z, 2341Z, 2342Z, 2343Z, 2344Z, 2349Z, 2351Z, 2352Z, 2361Z, 2362Z, 2363Z, 2364Z, 2365Z, 2369Z, 2370Z, 2391Z, 2399Z, 2410Z, 2420Z, 2431Z, 2432Z, 2433Z, 2434Z, 2441Z, 2442Z, 2443Z, 2444Z, 2445Z, 2446Z, 2451Z, 2452Z, 2453Z, 2454Z, 2511Z, 2512Z, 2521Z, 2529Z, 2530Z, 2540Z, 2550A, 2550B, 2561Z, 2562A, 2562B, 2571Z, 2572Z, 2573A, 2573B, 2591Z, 2592Z, 2593Z, 2594Z, 2599A, 2599B, 2611Z, 2612Z, 2620Z, 2630Z, 2640Z, 2651A, 2651B, 2652Z, 2660Z, 2670Z, 2680Z, 2711Z, 2712Z, 2720Z, 2731Z, 2732Z, 2733Z, 2740Z, 2751Z, 2752Z, 2790Z, 2811Z, 2812Z, 2813Z, 2814Z, 2815Z, 2821Z, 2822Z, 2823Z, 2824Z, 2825Z, 2829A, 2829B, 2830Z, 2841Z, 2849Z, 2891Z, 2892Z, 2893Z, 2894Z, 2895Z, 2896Z, 2899A, 2899B, 2910Z, 2920Z, 2931Z, 2932Z, 3011Z, 3012Z, 3020Z, 3030Z, 3040Z, 3091Z, 3092Z, 3099Z, 3101Z, 3102Z, 3103Z, 3109A, 3109B, 3211Z, 3212Z, 3213Z, 3220Z, 3230Z, 3240Z, 3250A, 3250B, 3291Z, 3299Z, 3311Z, 3312Z, 3313Z, 3314Z, 3315Z, 3316Z, 3317Z, 3319Z, 3320A, 3320B, 3320C, 3320D, 4110A, 4110B, 4110C, 4110D, 4120A, 4120B, 4211Z, 4212Z, 4213A, 4213B, 4221Z, 4222Z, 4291Z, 4299Z, 4311Z, 4312A, 4312B, 4313Z, 4321A, 4321B, 4322A, 4322B, 4329A, 4329B, 4331Z, 4332A, 4332B, 4332C, 4333Z, 4334Z, 4339Z, 4391A, 4391B, 4399A, 4399B, 4399C, 4399D, 4399E, 4611Z, 4612A, 4612B, 4613Z, 4614Z, 4615Z, 4616Z, 4617A, 4617B, 4618Z, 4619A, 4619B, 4621Z, 4622Z, 4623Z, 4624Z, 4631Z, 4632A, 4632B, 4632C, 4633Z, 4634Z, 4635Z, 4636Z, 4637Z, 4638A, 4638B, 4639A, 4639B, 4641Z, 4642Z, 4643Z, 4644Z, 4645Z, 4646Z, 4647Z, 4648Z, 4649Z, 4651Z, 4652Z, 4661Z, 4662Z, 4663Z, 4664Z, 4665Z, 4666Z, 4669A, 4669B, 4669C, 4671Z, 4672Z, 4673A, 4673B, 4674A, 4674B, 4675Z, 4676Z, 4677Z, 4690Z, 4910Z, 4920Z, 4931Z, 4932Z, 4939A, 4939B, 4939C, 4941A, 4941B, 4941C, 4942Z, 4950Z, 5010Z, 5020Z, 5030Z, 5040Z, 5320Z, 5811Z, 5812Z, 5813Z, 5814Z, 5819Z, 5821Z, 5829A, 5829B, 5829C, 5911A, 5911B, 5912Z, 5913A, 5913B, 6110Z, 6120Z, 6130Z, 6190Z, 6201Z, 6202A, 6202B, 6203Z, 6209Z, 6311Z, 6312Z, 6391Z, 6399Z, 6511Z, 6512Z, 6520Z, 7112A, 7112B, 7120B, 7211Z, 7219Z, 7220Z, 7311Z, 7312Z, 7320Z, 7410Z, 7420Z, 7430Z, 7490A, 7490B, 7911Z, 7912Z, 7990Z, 8110Z, 8121Z, 8122Z, 8129A, 8129B, 8130Z, 5229A, 5229B, 6622Z, 7022Z, 8292Z, 8559A, 8690A, 8690B", # Le code NAF ou code APE, un code d'activité suivant la nomenclature de l'INSEE valide en juin 2026 (cf README)
    "tranche_effectif_salarie": "03,11,12,21", # Tranche du nombre de salariés (cf README)
    #"categorie_entreprise" :"", # PME, ETI ou GE
    #"nature_juridique" : "", # Nature de l'entreprise (cf README)
    #"section_activite_principale" : "", #Cf README
    "date_naissance_personne_min" : "1954-01-01", # Les personne de moins de 72 ans (repasser derrière)
    "date_naissance_personne_max" : "1972-01-01", # Les personne de plus de 54 ans (repasser derrière)
    "etab_est_siege" : "true",
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

# On refiltre assos & service public au cas où
for col in ["complements_est_association", "complements_est_service_public"]:
    if col not in df_raw.columns:
        df_raw[col] = "FAUX"

mask_exclude = (
    (df_raw["complements_est_association"] == "VRAI") |
    (df_raw["complements_est_service_public"] == "VRAI")
)
df_raw = df_raw[~mask_exclude].reset_index(drop=True)

# On enlève les colonnes inutiles
cols_to_drop = [
    "sigle","annee_categorie_entreprise","date_fermeture","date_mise_a_jour","date_mise_a_jour_insee","date_mise_a_jour_rne","statut_diffusion","etab_date_fermeture","etab_etat_administratif","etab_liste_id_organisme_formation","etab_liste_rge","etab_liste_uai","etab_region","etab_siret","etab_statut_diffusion_etablissement","complements_collectivite_territoriale","complements_convention_collective_renseignee","complements_liste_idcc","complements_liste_finess_juridique","complements_egapro_renseignee","complements_est_achats_responsables","complements_est_alim_confiance","complements_est_bio","complements_est_entrepreneur_individuel","complements_liste_id_organisme_formation","complements_identifiant_association","complements_statut_entrepreneur_spectacle","complements_collectivite_territoriale.code","complements_collectivite_territorialaire.code_insee","complements_collectivite_territoriale.elus","complements_collectivite_territoriale.niveau"
]

df_raw = df_raw.drop(columns=[c for c in cols_to_drop if c in df_raw.columns], errors="ignore")

# On enlève les doublons (il devrait pas en avoir)
if "siren" in df_raw.columns:
    df_raw = df_raw.drop_duplicates(subset="siren", keep="first")

# Et on exporte
output_file = "entreprises_siren_74_V1.xlsx"
df_raw.to_excel(output_file, index=False)

print(f"Fichier créé : {output_file}")