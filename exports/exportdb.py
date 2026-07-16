from datetime import datetime

import pandas as pd

from database.database import SessionLocal
from database.models import Entreprise


def exporter(fichier, entreprises, personne):

    data = []

    session = SessionLocal()

    try:

        for e in entreprises:

            data.append({

                "siren": e.siren,
                "nom": e.nom,
                "établissements": e.établissements,
                "activite_principale": e.activite_principale,
                "categorie_entreprise": e.categorie_entreprise,
                "date_creation": e.date_creation,
                "etat_administratif": e.etat_administratif,
                "nature_juridique": e.nature_juridique,
                "section_activite_principale": e.section_activite_principale,
                "tranche_effectif_salarie": e.tranche_effectif_salarie,
                "dirigeant_nom": e.dirigeant_nom,
                "dirigeant_prenoms": e.dirigeant_prenoms,
                "dirigeant_annee_de_naissance": e.dirigeant_annee_de_naissance,
                "dirigeant_date_de_naissance": e.dirigeant_date_de_naissance,
                "dirigeant_qualite": e.dirigeant_qualite,
                "dirigeant_type_dirigeant": e.dirigeant_type_dirigeant,
                "dirigeant_siren": e.dirigeant_siren,
                "dirigeant_denomination": e.dirigeant_denomination,
                "etab_activite_principale": e.etab_activite_principale,
                "etab_adresse": e.etab_adresse,
                "etab_code_postal": e.etab_code_postal,
                "etab_latitude": e.etab_latitude,
                "etab_libelle_commune": e.etab_libelle_commune,
                "etab_longitude": e.etab_longitude,
                "ca_recent": e.ca_recent,
                "resultat_net_recent": e.resultat_net_recent,
                "recherche_google": e.recherche_google,
                "telephone": e.telephone,
                "traite": e.traite

            })

            entreprise = session.query(Entreprise).filter_by(
                siren=e.siren
            ).first()

            if entreprise:

                entreprise.traite = f"traité par {personne}"

        session.commit()

    finally:

        session.close()

    df = pd.DataFrame(data)

    df.to_excel(
        fichier,
        index=False
    )