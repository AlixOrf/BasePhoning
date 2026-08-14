import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FICHIER_EXCEL = BASE_DIR / "finaux" / "00.xlsx"

from database.database import SessionLocal
from database.models import Entreprise


# =========================
# IMPORT
# =========================

def importer_excel(fichier):

    df = pd.read_excel(fichier)

    session = SessionLocal()

    ajoutes = 0
    maj = 0

    try:

        for _, ligne in df.iterrows():

            donnees = ligne.to_dict()

            # -------------------------
            # [NON-DIFFUSIBLE] -> vide
            # -------------------------

            for cle, valeur in donnees.items():

                if valeur == "[NON-DIFFUSIBLE]":
                    donnees[cle] = None

            # -------------------------
            # Conversion des dates
            # -------------------------

            if pd.notna(donnees.get("date_creation")):
                donnees["date_creation"] = pd.to_datetime(
                    donnees["date_creation"]
                ).date()
            else:
                donnees["date_creation"] = None

            if pd.notna(donnees.get("dirigeant_date_de_naissance")):
                donnees["dirigeant_date_de_naissance"] = pd.to_datetime(
                    donnees["dirigeant_date_de_naissance"]
                ).date()
            else:
                donnees["dirigeant_date_de_naissance"] = None

            # -------------------------
            # NaN -> None
            # -------------------------

            for cle, valeur in donnees.items():

                if pd.isna(valeur):
                    donnees[cle] = None

            # -------------------------
            # Recherche SIREN
            # -------------------------

            entreprise = (
                session.query(Entreprise)
                .filter_by(siren=str(donnees["siren"]))
                .first()
            )

            if entreprise:

                # Mise à jour

                for cle, valeur in donnees.items():

                    if hasattr(entreprise, cle):
                        setattr(entreprise, cle, valeur)

                maj += 1

            else:

                # Nouvelle entreprise

                donnees["siren"] = str(donnees["siren"])

                session.add(Entreprise(**donnees))

                ajoutes += 1

        session.commit()

        print("Import terminé.")
        print(f"Ajoutées : {ajoutes}")
        print(f"Mises à jour : {maj}")

    except Exception as e:

        session.rollback()
        print(e)

    finally:

        session.close()


if __name__ == "__main__":
    importer_excel(FICHIER_EXCEL)