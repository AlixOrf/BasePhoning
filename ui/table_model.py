from PySide6.QtGui import QStandardItemModel, QStandardItem


class EntrepriseTableModel(QStandardItemModel):

    HEADERS = [
        "SIREN",
        "Nom",
        "Commune",
        "Téléphone",
        "Traité",
        "Code Postal",
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

                QStandardItem(str(e.siren)),
                QStandardItem(e.nom or ""),
                QStandardItem(e.etab_libelle_commune or ""),
                QStandardItem(e.telephone or ""),
                QStandardItem(e.traite or ""),
                QStandardItem(e.etab_code_postal or ""),

            ]

            for item in ligne:
                item.setEditable(False)

            self.appendRow(ligne)

    def get_entreprise(self, row):

        if row < 0 or row >= len(self.entreprises):
            return None

        return self.entreprises[row]