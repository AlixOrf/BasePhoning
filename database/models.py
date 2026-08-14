from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from database.database import Base


class Entreprise(Base):
    __tablename__ = "entreprises"

    id = Column(Integer, primary_key=True, autoincrement=True)

    siren = Column(String(9), unique=True, nullable=False, index=True)

    nom = Column(String)

    établissements = Column(Integer)

    activite_principale = Column(String)

    categorie_entreprise = Column(String)

    date_creation = Column(Date)

    etat_administratif = Column(String)

    nature_juridique = Column(String)

    section_activite_principale = Column(String)

    tranche_effectif_salarie = Column(String)

    dirigeant_nom = Column(String)

    dirigeant_prenoms = Column(String)

    dirigeant_annee_de_naissance = Column(Integer)

    dirigeant_date_de_naissance = Column(Date)

    dirigeant_qualite = Column(String)

    dirigeant_type_dirigeant = Column(String)

    dirigeant_siren = Column(String)

    dirigeant_denomination = Column(String)

    etab_activite_principale = Column(String)

    etab_adresse = Column(String)

    etab_code_postal = Column(String)

    etab_latitude = Column(Float)

    etab_libelle_commune = Column(String)

    etab_longitude = Column(Float)

    ca_recent = Column(String)

    resultat_net_recent = Column(String)

    recherche_google = Column(String)

    telephone = Column(String)

    traite = Column(String)

    CONSULTANT = Column(String)
   
    NUMCONSULTANT = Column(String)
   
    TOTAL_APPELS = Column(String)
   
    DATE_APPEL = Column(String)
   
    DUREE = Column(String)
   
    ACCORD = Column(String)
   
    DESACCORD = Column(String)
   
    ECHEC = Column(String)
   
    OPERATEUR = Column(String)
   
    COMMENTAIRE = Column(String)
   
    R1RETRAITE = Column(String)
   
    R1CA = Column(String)
   
    R1EFFECTIF = Column(String)
   
    R1PORTABLE = Column(String)
   
    R1DATE = Column(String)
   
    R1HEURE = Column(String)
   
    R1REMARQUES = Column(String)

    nombre_etablissements = Column(Integer)

    etab_caractere_employeur = Column(String)

    etab_commune = Column(String)

    etab_epci = Column(String)

    etab_est_siege = Column(String)

    etab_liste_enseignes = Column(String)