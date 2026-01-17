import pandas as pd  # On utilise pandas pour gérer les tableaux de données
import sys  # On utilise sys pour passer des arguments aux autres scripts
import os  # On utilise os pour vérifier si les fichiers existent
import subprocess  # On utilise subprocess pour lancer un autre script python (visualisation.py) automatiquement

# Définition des noms de fichiers par défaut
INPUT_FILE = "donnees.json"  # Le fichier source
OUTPUT_FILE = "donnees_filtrees.json"  # Le fichier résultat après filtre

def main():
    # on vérifie si le fichier d'entrée existe ( pour la sécurité)
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur: {INPUT_FILE} manquant.")  # Affiche une erreur si absent
        return
    # Lit le fichier JSON 
    df = pd.read_json(INPUT_FILE)
    # On montre à l'utilisateur quels types de DUT sont présents dans les données
    print("DUTs disponibles :")
    # On nettoie la colonne 'Dut' : on enlève les cases vides, les doublons et on trie par ordre alphabétique
    duts = sorted(df['Dut'].dropna().unique())
    # On affiche juste les 10 premiers pour ne pas encombrer la console
    print(", ".join(duts[:10]) + "...")

    df_filtered = df
    
    # On ne garde que les colonnes Passage et Obtention
    group_keys = ["Dut", "Dut_lib", "Série ou type de Bac", "Rgp_lib"]
    # On va construire la liste finale des colonnes à garder 
    cols_to_keep = []
    # On regarde chaque colonne du tableau filtré
    for col in df_filtered.columns:
        if col in group_keys or "Obtention" in col or "Passage" in col:
            cols_to_keep.append(col)            
    # On applique ce filtre de colonnes au tableau 
    df_filtered = df_filtered[cols_to_keep]

    # le résultat est sauvegarder dans un nouveau fichier JSON
    df_filtered.to_json(OUTPUT_FILE, orient='records', indent=4) # orient='records' garde le format liste d'objets, indent=4 rend le fichier lisible
    print(f"Données filtrées sauvegardées dans {OUTPUT_FILE} ({len(df_filtered)} lignes).")
    # Lance automatiquement le script de visualisation sur ce nouveau fichier filtré
    print("Lancement de la visualisation...")
    # C'est l'équivalent de taper "python3 visualisation.py donnees_filtrees.json" dans le terminal, plus efficase
    subprocess.run([sys.executable, "visualisation.py", OUTPUT_FILE])

if __name__ == "__main__":
    main()# On appelle notre fonction pour l'exécuter
