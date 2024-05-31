import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse as parse_date
import dateparser
import os

# Fonction pour récupérer le contenu HTML
def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

# Fonction pour trouver les articles récents
def find_recent_articles(url, date_limit=None):
    html_content = get_html_content(url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []

    # Filtrer les articles qui ont le lien de l'IA
    ai_articles = soup.find_all('a', href=lambda href: href and "https://techcrunch.com/category/artificial-intelligence/" in href)

    for ai_article in ai_articles:
        article_data = {}  # Initialisation en dehors de la boucle
        # Extraire le titre et le lien de l'article
        title_tag = ai_article.find_next('h2', class_='wp-block-post-title')
        if title_tag:
            link_tag = title_tag.find('a')
            if link_tag and link_tag['href']:
                title = title_tag.get_text(strip=True)
                link = link_tag['href']
                article_data['title'] = title
                article_data['link'] = link
                article_data['check'] = "no"

                # Extraire et formater la date
                date_tag = ai_article.find_next('div', class_='wp-block-tc23-post-time-ago')
                if date_tag:
                    date_str = date_tag.get_text(strip=True)
                    #print("Date string:", date_str)
                    try:
                        # Convertir la date relative en datetime absolu
                        absolute_date = dateparser.parse(date_str)
                        #print("Absolute date:", absolute_date)
                        if not absolute_date:
                            continue  # Passer à l'article suivant si la conversion échoue
                        article_data['date'] = absolute_date.strftime("%d/%m/%Y")
                    except ValueError:
                        # En cas d'erreur de conversion, ignorer l'article
                        continue
                articles.append(article_data)

    #print(articles)
    return articles

def main():
    main_url = "https://techcrunch.com/"
    # Date limite au format (année, mois, jour)
    date_limit = datetime(2024, 5, 25)

    articles = find_recent_articles(main_url, date_limit)
    #print(articles)

    # Charger les données existantes du fichier JSON s'il existe
    if os.path.exists('articles_after_date.json'):
        with open('articles_after_date.json', 'r') as infile:
            existing_articles = json.load(infile)
        articles.extend(existing_articles)

    # Enregistrer toutes les données (nouvelles et existantes) dans le fichier JSON
    with open('articles_after_date.json', 'w') as outfile:
        json.dump(articles, outfile, indent=4)

if __name__ == "__main__":
    main()
