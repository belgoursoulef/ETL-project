import pandas as pd
import requests
import webbrowser
import os
import sys
import csv
import json

# =============================================================================
# PARTIE 1 : EXTRACTION
# =============================================================================
url="https://www.data.gouv.fr/api/1/datasets/r/18e77311-5d8f-424d-b73e-defc8f446ef6"

#Traite les données sur la page web 
r = requests.get(url, stream=True)

r.encoding = "utf-8"
#Vérification du fonctionnement du lien
if r.status_code == 200:
    
    #Ouverture du fichier en mode écriture binaire ('wb')
    with open(f"fr-esr-parcours-et-reussite-des-bacheliers-en-dut.csv",'wb') as f:
        #On écrit le contenu téléchargé dans le fichier 
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
        print("Téléchargement terminé !")
else :
    print("Erreur lors du téléchargement, code:",r.status_code)


df = pd.read_csv("fr-esr-parcours-et-reussite-des-bacheliers-en-dut.csv", sep=";")
#mots contenu dans les entêtes ciblées
col_clear = df.columns[df.columns.str.contains('Id|sigle|ou')]
# Suppression des entêtes ciblées
df = df.drop(columns=col_clear)
#Remplace tout le reste par 0
df = df.fillna(0)
#Supprimer les doublons
df = df.drop_duplicates()

#Sauvegarder le fichier propre 
df.to_csv('fr-esr-parcours-et-reussite-des-bacheliers-en-dut.csv', index=False)


# =============================================================================
# PARTIE 2 : TRANSFORMATION 
# =============================================================================

def csv_to_json(csv_file, json_file):
    """Convertit le fichier CSV en JSON."""
    data = []
    
    if not os.path.exists(csv_file):
        print(f"Erreur : Le fichier {csv_file} est introuvable.")
        return

    # Lecture du CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        # Note : Les fichiers de data.gouv.fr utilisent souvent le point-virgule ';'
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            data.append(row)

    # Écriture du JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Transformation terminée : {json_file} créé avec {len(data)} lignes.")

# Exécution directe de la transformation
csv_to_json('fr-esr-parcours-et-reussite-des-bacheliers-en-dut.csv', 'donnees.json')


# =============================================================================
# PARTIE 3 : VISUALISATION 
# =============================================================================
# Note: On définit les fonctions ici pour qu'elles soient utilisables par le filtre plus bas.

def generate_chart_url(labels, data, label_name, chart_type):
    """Fonction qui configure et demande le graphique à l'API."""
    # Création de la configuration JSON pour QuickChart (format standard Chart.js)
    qc_config = {
        "type": chart_type,  # Définit le type de graphique (barre, ligne, etc.)
        "data": {  # Contient les données du graphique
            "labels": labels,  # Les noms sur l'axe X (ex: types de DUT)
            "datasets": [{  # Liste des séries de données
                "label": label_name,  # Le titre de la série
                "data": data,  # Les valeurs numériques (axe Y)
                # Une liste de couleurs qui se répète pour colorier les barres
                "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"] * 5
            }]
        },
        "options": {"title": {"display": True, "text": label_name}}  # Affiche le titre du graphique
    }
    
    # Envoie la demande à l'API QuickChart via Internet
    resp = requests.post("https://quickchart.io/chart/create", json={"chart": qc_config})
    
    # Si la réponse est bonne (code 200), on retourne l'URL de l'image, sinon rien
    return resp.json().get("url") if resp.status_code == 200 else None

def visualisation_main(target_file="donnees_filtrees.json"):
    print(f"\n--- VISUALISATION --- (Fichier: {target_file})")
    
    # Vérifie si le fichier de données existe
    if not os.path.exists(target_file):
        return print(f"File {target_file} not found.")  # Arrête tout si le fichier n'est pas là

    # 1. Chargement et Traitement des Données
    df = pd.read_json(target_file)  # Lit le fichier JSON et le met dans un tableau pandas
    
    # Cherche une colonne qui peut servir de catégorie (Groupe)
    # On regarde si une des colonnes classiques ("Dut_lib", etc.) est présente
    group_col = next((c for c in ["Dut_lib", "Dut", "Série ou type de Bac", "Rgp_lib"] if c in df.columns), None)
    
    if group_col:
        print(f"Grouping by: {group_col}")  # Affiche la colonne choisie pour le groupe
        # Regroupe les lignes qui ont la même valeur dans 'group_col' et additionne les chiffres
        df_grouped = df.groupby(group_col).sum(numeric_only=True)
    else:
        # Si aucune colonne de groupe n'est trouvée
        print("No grouping criteria found. Using first 10 rows.")
        # On prend juste les 10 premières lignes de chiffres
        df_grouped = df.select_dtypes(include='number').head(10)
        # On utilise la première colonne comme étiquette
        df_grouped.index = df[df.columns[0]].head(10)

    # 2. Génération des Graphiques et Ouverture
    
    # Boucle sur chaque colonne numérique du tableau groupé
    for i, col in enumerate(df_grouped.columns):
        # Logique demandée : Si c'est une "Obtention", on met des barres
        if "Obtention" in col:
            chart_type = 'bar'
        else:
            # Pour tout le reste (dont "Passage"), on met des lignes
            chart_type = 'line'
        
        print(f"Generating {chart_type} for {col}...")  # Affiche ce qu'on est en train de faire
        
        # Trie les données du plus grand au plus petit et garde le Top 20 pour que le graphique reste lisible
        series = df_grouped[col].sort_values(ascending=False).head(20)
        
        # Appelle notre fonction pour créer l'URL du graphique
        url = generate_chart_url(series.index.tolist(), series.values.tolist(), col, chart_type)
        
        # Si on a bien reçu une URL
        if url:
            print(f"Opening chart: {url}")  # On l'affiche
            webbrowser.open(url)  # Et on l'ouvre directement dans le navigateur


# =============================================================================
# PARTIE 4 : FILTRAGE
# =============================================================================
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
    # MODIFICATION POUR LE SCRIPT TOUT-EN-UN : Appel direct de la fonction au lieu de subprocess
    visualisation_main(OUTPUT_FILE)

if __name__ == "__main__":
    main()
