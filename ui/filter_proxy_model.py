from PySide6.QtCore import QSortFilterProxyModel, Qt


class FilterProxyModel(QSortFilterProxyModel):

    def __init__(self):
        super().__init__()

        # Recherche globale
        self.global_filter = ""

        # Filtres Excel par colonne
        # Exemple :
        # {
        #   1: ["Renault", "Peugeot"],
        #   2: ["Paris"]
        # }
        self.column_filters = {}


    # ======================
    # Recherche globale
    # ======================

    def setGlobalFilter(self, text):

        self.global_filter = text.lower().strip()

        self.invalidateFilter()



    # ======================
    # Filtre colonne Excel
    # ======================

    def setColumnFilter(self, column, values):

        print("FILTRE RECU :", column, values)

        if values:
            self.column_filters[column] = values

        elif column in self.column_filters:
            del self.column_filters[column]

        self.invalidateFilter()



    # ======================
    # Application filtres
    # ======================

    def filterAcceptsRow(
        self,
        source_row,
        source_parent
    ):

        model = self.sourceModel()


        # ----------------------
        # Recherche globale
        # ----------------------

        if self.global_filter:

            trouve = False


            for column in range(
                model.columnCount()
            ):

                index = model.index(
                    source_row,
                    column,
                    source_parent
                )

                valeur = model.data(
                    index
                )


                if valeur is not None and self.global_filter in str(valeur).lower():

                    trouve = True
                    break


            if not trouve:
                return False



        # ----------------------
        # Filtres Excel colonnes
        # ----------------------

        for column, valeurs in self.column_filters.items():

            index = model.index(
                source_row,
                column,
                source_parent
            )


            valeur = model.data(
                index
            )


            if valeur is None:
                return False


            if str(valeur) not in valeurs:

                return False



        return True