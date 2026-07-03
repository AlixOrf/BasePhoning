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