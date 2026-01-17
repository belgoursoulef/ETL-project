import csv
import json
import os

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

if __name__ == "__main__":
    # On utilise le nom du fichier généré par votre script extract.py
    csv_to_json('fr-esr-parcours-et-reussite-des-bacheliers-en-dut.csv', 'donnees.json')