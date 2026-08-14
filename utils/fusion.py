import pandas as pd
from pathlib import Path

# ==========================================================
# CONFIGURATION
# ==========================================================

dossier = Path("finaux")
fichier_sortie = dossier / "00.xlsx"

# ==========================================================
# LECTURE DES 95 FICHIERS
# ==========================================================

fichiers = []

for i in range(1, 96):
    fichier = dossier / f"{i:02d}.xlsx"

    if fichier.exists():
        fichiers.append(fichier)
    else:
        print(f"⚠️ Fichier manquant : {fichier}")

# ==========================================================
# FUSION
# ==========================================================

print(f"\nNombre de fichiers trouvés : {len(fichiers)}")

df_liste = []

for fichier in fichiers:
    print(f"Lecture : {fichier.name}")

    df = pd.read_excel(fichier)
    df_liste.append(df)

# Fusion de tous les fichiers
df_final = pd.concat(df_liste, ignore_index=True)

# ==========================================================
# EXPORT
# ==========================================================

df_final.to_excel(fichier_sortie, index=False)

print("\n========================================")
print("Fusion terminée !")
print(f"Fichiers fusionnés : {len(fichiers)}")
print(f"Nombre de lignes : {len(df_final)}")
print(f"Fichier créé : {fichier_sortie}")
print("========================================")