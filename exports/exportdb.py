from datetime import datetime
import random

import pandas as pd

from database.database import SessionLocal
from database.models import Entreprise


def exporter(fichier, entreprises, personne):

    session = SessionLocal()

    try:

        for e in entreprises:

            entreprise = session.query(Entreprise).filter_by(
                siren=e.siren
            ).first()

            if entreprise:
                entreprise.traite = f"traité par {personne}"

        session.commit()

    finally:

        session.close()

    if personne.lower() == "stephane":

        data = []
        telephones_utilises = set()

        for e in entreprises:

            # Génération d'un numéro unique de 10 chiffres sans 0
            while True:
                tel = "".join(str(random.randint(1, 9)) for _ in range(10))

                if tel not in telephones_utilises:
                    telephones_utilises.add(tel)
                    break

            age = ""
            if e.dirigeant_annee_de_naissance:
                try:
                    age = datetime.now().year - int(e.dirigeant_annee_de_naissance)
                except (ValueError, TypeError):
                    pass

            data.append({

                "CIVIL": "",
                "PRENOM": e.dirigeant_prenoms,
                "NOM": e.dirigeant_nom,
                "FONCTION": e.dirigeant_qualite,
                "AGE": e.dirigeant_annee_de_naissance,
                "SIREN": e.siren,
                "COMPANY": e.nom,
                "ADRESS": e.etab_adresse,
                "CP": e.etab_code_postal,
                "VILLE": e.etab_libelle_commune,
                "EMAIL": "",
                "EMAIL GENERIQUE": "",
                "TEL": tel,
                "MOBILE": "",
                "NAF": e.etab_activite_principale,
                "ACTIVITE": e.activite_principale,
                "EFFECTIF": e.tranche_effectif_salarie,
                "FORME": e.nature_juridique,
                "CREATION": e.date_creation,
                "WEBSITE": "",
                "EMAILBASE": "",
                "CONSULTANT": "",
                "NUMCONSULTANT": "",
                "LIEN GOOGLE": e.recherche_google

            })

    else:

        data = []

        for e in entreprises:

            data.append({

                "PRENOM": e.dirigeant_prenoms,
                "NOM": e.dirigeant_nom,
                "FONCTION": e.dirigeant_qualite,
                "AGE": e.dirigeant_annee_de_naissance,
                "SIREN": e.siren,
                "COMPANY": e.nom,
                "ADRESS": e.etab_adresse,
                "CP": e.etab_code_postal,
                "VILLE": e.etab_libelle_commune,
                "TEL": tel,
                "NAF": e.etab_activite_principale,
                "ACTIVITE": e.activite_principale,
                "EFFECTIF": e.tranche_effectif_salarie,
                "FORME": e.nature_juridique,
                "CREATION": e.date_creation,
                "CONSULTANT": "",
                "NUMCONSULTANT": "",
                "LIEN GOOGLE": e.recherche_google
            })

    df = pd.DataFrame(data)

    df.to_excel(
        fichier,
        index=False
    )