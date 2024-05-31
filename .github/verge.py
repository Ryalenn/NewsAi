import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import dateparser
import os

# Fonction pour récupérer le contenu HTML
def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

# Fonction pour trouver les articles récents et filtrer par date
def find_recent_articles(url, date_limit=None):
    html_content = get_html_content(url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []

    # Trouver tous les articles sur la page
    all_articles = soup.find_all('div', class_='duet--content-cards--content-card')

    for article in all_articles:
        article_data = {}  # Initialisation en dehors de la boucle

        # Extraire le titre et le lien de l'article
        title_tag = article.find('h2', class_='font-polysans')
        if title_tag:
            link_tag = title_tag.find('a')
            if link_tag and link_tag['href']:
                title = title_tag.get_text(strip=True)
                link = link_tag['href']
                # Ajouter le préfixe au lien
                link = "https://www.theverge.com" + link
                article_data['title'] = title
                article_data['link'] = link
                article_data['check'] = "no"

                # Extraire et formater la date
                date_tag = article.find('time', datetime=True)
                if date_tag:
                    date_str = date_tag.get_text(strip=True)
                    # Filtrer les articles avec "UTC", "MINUTES", "HOUR", ou "HOURS" dans la date
                    if any(keyword in date_str for keyword in ["UTC", "MINUTES", "HOUR", "HOURS"]):
                        try:
                            # Convertir la date relative en datetime absolu
                            absolute_date = dateparser.parse(date_str)
                            if not absolute_date:
                                continue  # Passer à l'article suivant si la conversion échoue
                            article_data['date'] = absolute_date.strftime("%d/%m/%Y")
                        except ValueError:
                            # En cas d'erreur de conversion, ignorer l'article
                            continue
                        articles.append(article_data)

    return articles

def main():
    main_url = "https://www.theverge.com/ai-artificial-intelligence"  # Remplacez example.com par l'URL réelle
    # Date limite au format (année, mois, jour)
    date_limit = datetime.now() - timedelta(days=1)

    articles = find_recent_articles(main_url, date_limit)

    # Charger les données existantes du fichier JSON s'il existe
    existing_articles = []
    if os.path.exists('articles_after_date.json'):
        with open('articles_after_date.json', 'r') as infile:
            existing_articles = json.load(infile)

    # Ajouter les nouveaux articles aux articles existants
    existing_articles.extend(articles)

    # Enregistrer toutes les données (nouvelles et existantes) dans le fichier JSON
    with open('articles_after_date.json', 'w') as outfile:
        json.dump(existing_articles, outfile, indent=4)

if __name__ == "__main__":
    main()
