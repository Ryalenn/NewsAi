import json
from datetime import datetime, timedelta

def load_json(file_path):
    """Charge le fichier JSON depuis le chemin spécifié."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_path):
    """Enregistre les données JSON dans le fichier spécifié."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def filter_articles_by_date(articles, max_age_hours=48):
    """Filtre les articles pour ne conserver que ceux publiés dans les dernières max_age_hours heures."""
    threshold_date = datetime.now() - timedelta(hours=max_age_hours)
    filtered_articles = [
        article for article in articles
        if datetime.strptime(article['date'], '%a, %d %b %Y %H:%M:%S GMT') > threshold_date
    ]
    return filtered_articles

def update_files(file_paths, max_age_hours=48):
    """Met à jour les fichiers JSON spécifiés en supprimant les articles plus vieux que max_age_hours heures."""
    for file_path in file_paths:
        print(f"Processing {file_path}...")
        
        # Charger les articles depuis le fichier JSON
        articles = load_json(file_path)
        
        # Filtrer les articles par date
        filtered_articles = filter_articles_by_date(articles, max_age_hours)
        
        # Sauvegarder les articles filtrés dans le même fichier JSON
        save_json(filtered_articles, file_path)
        
        print(f"Updated {file_path} with filtered articles.")

def main():
    file_paths = ['articles.json', 'summaries.json']  # Chemins vers vos fichiers JSON
    
    update_files(file_paths)

if __name__ == "__main__":
    main()
