import requests
import json
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Votre token API Diffbot
API_TOKEN = '4d5aab0fe994bbcfc7af548d1e9c9c62'

@retry(
    stop=stop_after_attempt(5),  # Arrêter après 5 tentatives
    wait=wait_exponential(multiplier=1, min=4, max=10),  # Attendre de façon exponentielle entre les retries
    retry=retry_if_exception_type(requests.exceptions.RequestException)  # Retry en cas de RequestException
)
def get_article_list(url):
    api_url = f'https://api.diffbot.com/v3/list?token={API_TOKEN}&url={url}'
    
    response = requests.get(api_url, timeout=10)  # Augmenter le délai d'attente à 10 secondes
    response.raise_for_status()  # Lever une exception si le statut de la réponse est une erreur
    return response.json()  # Obtenir le JSON

def filter_articles(articles, existing_urls):
    filtered_articles = []
    for item in articles:
        for article in item.get('items', []):
            # Convertir la date de publication en objet datetime
            published_date_str = article.get('date')
            if not published_date_str:
                continue  # Ignorer les articles sans date de publication
            
            # Parser la date dans le format 'Thu, 30 May 2024 23:00:00 GMT'
            published_date = datetime.strptime(published_date_str, '%a, %d %b %Y %H:%M:%S GMT')
            # Calculer la différence entre maintenant et la date de publication
            time_difference = datetime.now() - published_date
            
            # Garder les articles publiés il y a moins de 48 heures et dont le lien n'existe pas déjà
            if time_difference < timedelta(hours=48):
                article_url = article.get('link', '')
                if article_url and article_url not in existing_urls:
                    filtered_articles.append({
                        'title': article.get('post-card__title', ''),
                        'link': article_url,
                        'image': article.get('image', ''),
                        'date': published_date_str,  # Conserver la date sous forme de chaîne
                        'check': 'no'  # Ajouter la clé 'check' avec la valeur 'no'
                    })
                    existing_urls.add(article_url)  # Ajouter le lien à la liste des liens existants
    return filtered_articles

def save_to_json(data):
    with open('articles.json', 'r+') as file:
        try:
            # Charger les données existantes
            existing_data = json.load(file)
        except json.JSONDecodeError:
            # S'il n'y a pas encore de données dans le fichier, initialiser existing_data à une liste vide
            existing_data = []
        
        # Créer un ensemble de toutes les URL existantes dans les données existantes
        existing_urls = set(article['link'] for article in existing_data)
        
        # Filtrer les nouveaux articles pour ne conserver que ceux dont l'URL n'existe pas déjà
        filtered_data = [article for article in data if article['link'] not in existing_urls]
        
        # Fusionner les nouveaux articles filtrés avec les données existantes
        existing_data.extend(filtered_data)
        
        # Rembobiner le pointeur de fichier au début du fichier
        file.seek(0)
        
        # Écrire les données fusionnées dans le fichier JSON
        json.dump(existing_data, file, indent=4)
        # Tronquer le fichier après la fin des données pour supprimer les anciennes données en excès
        file.truncate()

# Exemple d'URL de site de news
urls = [
    'https://www.frandroid.com/culture-tech/intelligence-artificielle',
    'https://www.theverge.com/ai-artificial-intelligence'
    'https://www.forbes.com/ai/'
]

existing_urls = set()

new_articles = []

for url in urls:
    print(f"Fetching articles from {url}")
    try:
        articles_data = get_article_list(url)
        if articles_data:
            articles = filter_articles(articles_data.get('objects', []), existing_urls)
            new_articles.extend(articles)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch articles from {url} after several retries. Error: {e}")

# Enregistrer les nouveaux articles dans le fichier JSON
save_to_json(new_articles)
