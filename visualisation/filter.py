import pandas as pd  # Importe pandas pour gérer les tableaux de données
import sys  # Importe sys pour passer des arguments aux autres scripts
import os  # Importe os pour vérifier si les fichiers existent
import subprocess  # Importe subprocess pour lancer un autre script python (visualisation.py)

# Définition des noms de fichiers par défaut
INPUT_FILE = "donnees.json"  # Le fichier source
OUTPUT_FILE = "donnees_filtrees.json"  # Le fichier résultat après filtre

def main():
    # Vérifie si le fichier d'entrée existe
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur: {INPUT_FILE} manquant.")  # Affiche une erreur si absent
        return

    # Lit le fichier JSON
    df = pd.read_json(INPUT_FILE)
    # Affiche un aperçu des codes DUT disponibles pour aider l'utilisateur
    print("DUTs disponibles :")
    # Prend la colonne 'Dut', enlève les vides, garde les valeurs uniques et trie
    duts = sorted(df['Dut'].dropna().unique())
    # Affiche les 10 premiers pour ne pas inonder l'écran
    print(", ".join(duts[:10]) + "...")


    # On ne filtre PAS les lignes : on garde tous les étudiants de tous les DUT par défaut.
    # C'est ici qu'on pourrait ajouter df_filtered = df[df['Dut'] == 'INFO'] si on voulait restreindre.
    df_filtered = df
    
    # --- FILTRAGE DES COLONNES (Automatique) ---
    # On ne garde que les colonnes pertinentes (Passage/Obtention).
    group_keys = ["Dut", "Dut_lib", "Série ou type de Bac", "Rgp_lib"]
    
    # On va construire la liste finale des colonnes à garder
    cols_to_keep = []
    # On regarde chaque colonne du tableau filtré
    for col in df_filtered.columns:
        # On garde la colonne SI :
        # 1. C'est une clé de groupe (nom, bac...)
        # 2. OU si le nom contient "Obtention"
        # 3. OU si le nom contient "Passage"
        if col in group_keys or "Obtention" in col or "Passage" in col:
            cols_to_keep.append(col)
            
    # On applique ce filtre de colonnes au tableau
    df_filtered = df_filtered[cols_to_keep]

    # Sauvegarde le résultat dans un nouveau fichier JSON
    # orient='records' garde le format liste d'objets, indent=4 rend le fichier lisible
    df_filtered.to_json(OUTPUT_FILE, orient='records', indent=4)
    print(f"Données filtrées sauvegardées dans {OUTPUT_FILE} ({len(df_filtered)} lignes).")

    # Lance automatiquement le script de visualisation sur ce nouveau fichier
    print("Lancement de la visualisation...")
    # C'est l'équivalent de taper "python visualisation.py donnees_filtrees.json" dans le terminal
    subprocess.run([sys.executable, "visualisation.py", OUTPUT_FILE])

if __name__ == "__main__":
    main()  # Point d'entrée du script
