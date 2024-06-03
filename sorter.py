import json
from datetime import datetime

def load_json(file_path):
    """Charge le fichier JSON depuis le chemin spécifié."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_path):
    """Enregistre les données JSON dans le fichier spécifié."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def sort_articles_by_date(articles):
    """Trie les articles du plus récent au plus ancien."""
    return sorted(articles, key=lambda x: datetime.strptime(x['date'], '%a, %d %b %Y %H:%M:%S GMT'), reverse=True)

def main():
    input_file_path = 'summaries.json'  # Chemin vers votre fichier JSON d'entrée
    output_file_path = 'sorted_summaries.json'  # Chemin vers le fichier JSON de sortie

    # Charger les articles depuis le fichier JSON
    articles = load_json(input_file_path)

    # Trier les articles par date
    sorted_articles = sort_articles_by_date(articles)

    # Sauvegarder les articles triés dans un nouveau fichier JSON
    save_json(sorted_articles, output_file_path)

    print(f"Articles triés et enregistrés dans {output_file_path}")

if __name__ == "__main__":
    main()
