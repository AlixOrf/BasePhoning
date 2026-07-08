from PySide6.QtGui import QStandardItemModel, QStandardItem


class EntrepriseTableModel(QStandardItemModel):

    HEADERS = [
        "SIREN",
        "Nom",
        "Commune",
        "Téléphone",
        "Traité",
        "Departement"
    ]

    def __init__(self):
        super().__init__()

        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)

    def charger(self, entreprises):

        self.setRowCount(0)

        for e in entreprises:

            ligne = [
                QStandardItem(str(e.siren)),
                QStandardItem(str(e.nom)),
                QStandardItem(str(e.etab_libelle_commune)),
                QStandardItem("" if e.telephone is None else str(e.telephone)),
                QStandardItem(str(e.traite)),
                QStandardItem(str(e.etab_code_postal)),
            ]

            for item in ligne:
                item.setEditable(False)

            self.appendRow(ligne)