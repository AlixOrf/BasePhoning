import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analyse des dirigeants")

# Upload du fichier Excel
fichier = st.file_uploader(
    "Choisis un fichier Excel",
    type=["xlsx", "xls"]
)

if fichier is not None:

    # Lecture Excel
    df = pd.read_excel(fichier)

    # =========================
    # CAMEMBERT : traite
    # =========================
    if "traite" in df.columns:

        st.subheader("Répartition de la colonne 'traite'")

        repartition = df["traite"].fillna("Valeur vide").value_counts()

        fig1, ax1 = plt.subplots(figsize=(6, 6))

        ax1.pie(
            repartition,
            labels=repartition.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax1.set_title("Répartition des traitements")
        ax1.axis("equal")

        st.pyplot(fig1)

        st.dataframe(
            repartition.reset_index().rename(
                columns={"index": "Valeur", "count": "Nombre"}
            )
        )

    # =========================
    # CAMEMBERT : type dirigeant
    # =========================
    if "dirigeant_type_dirigeant" in df.columns:

        st.subheader("Répartition des types de dirigeants")

        repartition_dirigeant = (
            df["dirigeant_type_dirigeant"]
            .fillna("Valeur vide")
            .value_counts()
        )

        fig2, ax2 = plt.subplots(figsize=(6, 6))

        ax2.pie(
            repartition_dirigeant,
            labels=repartition_dirigeant.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax2.set_title("Type de dirigeant")
        ax2.axis("equal")

        st.pyplot(fig2)

    # =========================
    # HISTOGRAMME : année naissance
    # =========================
    if "dirigeant_annee_de_naissance" in df.columns:

        st.subheader("Répartition des années de naissance")

        annees = pd.to_numeric(
            df["dirigeant_annee_de_naissance"],
            errors="coerce"
        ).dropna()

        # Comptage par année
        repartition_annees = (
            annees.astype(int)
            .value_counts()
            .sort_index()
        )

        fig3, ax3 = plt.subplots(figsize=(14, 6))

        ax3.bar(
            repartition_annees.index,
            repartition_annees.values
        )

        ax3.set_title("Nombre de dirigeants par année de naissance")
        ax3.set_xlabel("Année de naissance")
        ax3.set_ylabel("Nombre de dirigeants")

        # Affiche une graduation tous les 5 ans
        ax3.set_xticks(
            repartition_annees.index[::5]
        )

        plt.xticks(rotation=45)

        st.pyplot(fig3)

        st.write(
            f"Nombre de dirigeants avec année renseignée : {len(annees):,}"
        )

        # =========================
        # SECTEURS ACTIVITE
        # =========================
        if "section_activite_principale" in df.columns:

            st.subheader("Top secteurs d'activité")

            data = (
                df["section_activite_principale"]
                .fillna("Inconnu")
                .value_counts()
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(10,6))

            ax.barh(
                data.index[::-1],
                data.values[::-1]
            )

            ax.set_title("10 secteurs les plus représentés")

            st.pyplot(fig)

        # =========================
        # TRANCHE EFFECTIF
        # =========================
        if "tranche_effectif_salarie" in df.columns:

            st.subheader("Répartition des effectifs salariés")

            data = (
                df["tranche_effectif_salarie"]
                .fillna("Inconnu")
                .value_counts()
            )

            fig, ax = plt.subplots(figsize=(10,5))

            ax.bar(
                data.index,
                data.values
            )

            ax.tick_params(axis='x', rotation=45)

            st.pyplot(fig)

        # =========================
        # FORMES JURIDIQUES
        # =========================
        if "nature_juridique" in df.columns:

            st.subheader("Formes juridiques")

            data = (
                df["nature_juridique"]
                .fillna("Inconnu")
                .value_counts()
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(10,6))

            ax.barh(
                data.index[::-1],
                data.values[::-1]
            )

            st.pyplot(fig)

        # =========================
        # CARTE DES ETABLISSEMENTS
        # =========================
        if (
            "etab_latitude" in df.columns
            and "etab_longitude" in df.columns
        ):

            st.subheader("Carte des établissements")

            carte = df[
                [
                    "etab_latitude",
                    "etab_longitude"
                ]
            ].copy()

            carte.columns = [
                "lat",
                "lon"
            ]

            carte["lat"] = pd.to_numeric(
                carte["lat"],
                errors="coerce"
            )

            carte["lon"] = pd.to_numeric(
                carte["lon"],
                errors="coerce"
            )

            carte = carte.dropna()

            st.map(carte)