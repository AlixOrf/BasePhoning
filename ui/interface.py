from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)

from database.crud import recuperer_toutes_les_entreprises


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Base Entreprises")
        self.resize(1300, 700)

        # Widget principal
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # ======================
        # Barre de recherche
        # ======================

        recherche_layout = QHBoxLayout()

        recherche_layout.addWidget(QLabel("Recherche :"))

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Nom ou SIREN...")
        recherche_layout.addWidget(self.recherche)

        self.btn_recherche = QPushButton("Rechercher")
        recherche_layout.addWidget(self.btn_recherche)

        layout.addLayout(recherche_layout)

        # ======================
        # Tableau
        # ======================

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "SIREN",
            "Nom",
            "Commune",
            "Téléphone",
            "Traité"
        ])

        layout.addWidget(self.table)

        # ======================
        # Boutons
        # ======================

        boutons = QHBoxLayout()

        self.btn_import = QPushButton("Importer")
        self.btn_export = QPushButton("Exporter")
        self.btn_ajouter = QPushButton("Ajouter")
        self.btn_modifier = QPushButton("Modifier")
        self.btn_supprimer = QPushButton("Supprimer")

        boutons.addWidget(self.btn_import)
        boutons.addWidget(self.btn_export)

        boutons.addStretch()

        boutons.addWidget(self.btn_ajouter)
        boutons.addWidget(self.btn_modifier)
        boutons.addWidget(self.btn_supprimer)

        layout.addLayout(boutons)

        # Chargement des données
        self.charger_entreprises()

    def charger_entreprises(self):

        entreprises = recuperer_toutes_les_entreprises()

        self.table.setRowCount(len(entreprises))

        for ligne, e in enumerate(entreprises):

            self.table.setItem(
                ligne,
                0,
                QTableWidgetItem(str(e.siren))
            )

            self.table.setItem(
                ligne,
                1,
                QTableWidgetItem(str(e.nom))
            )

            self.table.setItem(
                ligne,
                2,
                QTableWidgetItem(str(e.etab_libelle_commune))
            )

            self.table.setItem(
                ligne,
                3,
                QTableWidgetItem("" if e.telephone is None else str(e.telephone))
            )

            self.table.setItem(
                ligne,
                4,
                QTableWidgetItem("Oui" if e.traite else "Non")
            )

        self.table.resizeColumnsToContents()