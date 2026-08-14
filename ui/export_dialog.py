from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QPushButton,
    QHBoxLayout
)


class ExportDialog(QDialog):

    def __init__(self, nb_entreprises, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Export")
        self.resize(350, 170)

        # ==========================================================
        # LAYOUT PRINCIPAL
        # ==========================================================

        layout = QVBoxLayout(self)

        # ==========================================================
        # TEXTE
        # ==========================================================

        texte = QLabel(
            f"{nb_entreprises} entreprises seront exportées.\n\n"
            "Qui va traiter ces entreprises ?"
        )

        layout.addWidget(texte)

        # ==========================================================
        # CHOIX DE LA PERSONNE
        # ==========================================================

        self.alain = QRadioButton("Alain")
        self.stephane = QRadioButton("Stéphane")
        self.autre = QRadioButton("Autre")

        layout.addWidget(self.alain)
        layout.addWidget(self.stephane)
        layout.addWidget(self.autre)

        # ==========================================================
        # BOUTONS
        # ==========================================================

        boutons = QHBoxLayout()

        annuler = QPushButton("Annuler")
        exporter = QPushButton("Exporter")

        boutons.addStretch()
        boutons.addWidget(annuler)
        boutons.addWidget(exporter)

        layout.addLayout(boutons)

        # ==========================================================
        # SIGNALS
        # ==========================================================

        annuler.clicked.connect(self.reject)
        exporter.clicked.connect(self.accept)

    # ==========================================================
    # RÉCUPÉRATION DU CHOIX
    # ==========================================================

    def get_personne(self):

        if self.alain.isChecked():
            return "Alain"

        if self.stephane.isChecked():
            return "Stephane"

        if self.autre.isChecked():
            return "Autre"

        return None