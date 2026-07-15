from PySide6.QtCore import QSortFilterProxyModel


class FilterProxyModel(QSortFilterProxyModel):

    def __init__(self):
        super().__init__()

        self.global_filter = ""
        self.column_filters = {}

    # ======================
    # Recherche globale
    # ======================

    def setGlobalFilter(self, text):

        self.global_filter = text.lower().strip()
        self.invalidateFilter()

    # ======================
    # Filtre colonne
    # ======================

    def setColumnFilter(self, column, values):

        if values is None:
            values = []

        if len(values) == 0:
            self.column_filters.pop(column, None)
        else:
            self.column_filters[column] = set(values)

        self.invalidateFilter()

    # ======================
    # Filtrage
    # ======================

    def filterAcceptsRow(self, source_row, source_parent):

        model = self.sourceModel()

        # ------------------
        # Recherche globale
        # ------------------

        if self.global_filter:

            trouve = False

            for column in range(model.columnCount()):

                index = model.index(source_row, column, source_parent)
                valeur = model.data(index)

                if valeur is not None and self.global_filter in str(valeur).lower():
                    trouve = True
                    break

            if not trouve:
                return False

        # ------------------
        # Filtres colonnes
        # ------------------

        for column, valeurs in self.column_filters.items():

            index = model.index(source_row, column, source_parent)

            valeur = model.data(index)

            if valeur is None or str(valeur).strip() == "":
                valeur = "(Vide)"
            else:
                valeur = str(valeur)

            if valeur not in valeurs:
                return False

        return True