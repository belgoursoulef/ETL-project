import pandas as pd  # Importe la bibliothèque pandas pour manipuler les données (tableaux)
import requests  # Importe la bibliothèque requests pour envoyer des requêtes internet (API)
import webbrowser  # Importe le module pour ouvrir le navigateur web automatiquement
import os  # Importe le module pour interagir avec le système d'exploitation (fichiers)
import sys  # Importe le module pour récupérer les arguments de la ligne de commande

# Définit le fichier JSON d'entrée : soit celui donné en argument, soit 'donnees_filtrees.json' par défaut
# Cela garantit qu'on visualise les données filtrées si on lance le script directement.
JSON_FILE = sys.argv[1] if len(sys.argv) > 1 else "donnees_filtrees.json"

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

def main():
    # Vérifie si le fichier de données existe
    if not os.path.exists(JSON_FILE):
        return print(f"File {JSON_FILE} not found.")  # Arrête tout si le fichier n'est pas là

    # 1. Chargement et Traitement des Données
    df = pd.read_json(JSON_FILE)  # Lit le fichier JSON et le met dans un tableau pandas
    
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

if __name__ == "__main__":
    main()  # Lance la fonction principale si on exécute ce script