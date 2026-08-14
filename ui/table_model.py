from PySide6.QtGui import QStandardItemModel, QStandardItem


class EntrepriseTableModel(QStandardItemModel):

    HEADERS = [
        "Activité principale",
        "Catégorie entreprise",
        "Nature juridique",
        "Section activité principale",
        "Tranche effectif salarié",
        "Dirigeant année de naissance",
        "Étab. activité principale",
        "Étab. code postal",
        "Étab. commune",
        "Téléphone",
        "Traité",
    ]

    def __init__(self):
        super().__init__()

        self.entreprises = []

        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)

    def charger(self, entreprises):

        self.clear()

        self.entreprises = entreprises

        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)

        for e in entreprises:

            ligne = [

                QStandardItem(e.activite_principale or ""),
                QStandardItem(e.categorie_entreprise or ""),
                QStandardItem(e.nature_juridique or ""),
                QStandardItem(e.section_activite_principale or ""),
                QStandardItem(e.tranche_effectif_salarie or ""),
                QStandardItem(str(e.dirigeant_annee_de_naissance or "")),
                QStandardItem(e.etab_activite_principale or ""),
                QStandardItem(e.etab_code_postal or ""),
                QStandardItem(e.etab_libelle_commune or ""),
                QStandardItem(e.telephone or ""),
                QStandardItem(e.traite or ""),
            ]

            for item in ligne:
                item.setEditable(False)

            self.appendRow(ligne)

    def get_entreprise(self, row):

        if row < 0 or row >= len(self.entreprises):
            return None

        return self.entreprises[row]