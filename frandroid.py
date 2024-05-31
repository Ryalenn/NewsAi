import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# Fonction pour récupérer le contenu HTML
def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

# Fonction pour trouver les articles récents dans les balises <ul>
def find_recent_articles(url, date_limit=None):
    html_content = get_html_content(url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []

    for ul in soup.find_all('ul'):
        for article in ul.find_all('li', class_='post-card'):
            title_tag = article.find('p', class_='post-card__title')
            date_tag = article.find('p', class_='post-card__date')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                article_data = {'title': title, 'link': link}  # Ajout du lien de l'article
                article_data['check'] = "no"
                if date_tag:
                    # Extraire la date brute
                    date_str = date_tag.get_text(strip=True)
                    # Supprimer les 7 premiers caractères et les 11 derniers
                    date_str_cleaned = date_str[11:-7].strip()
                    # Reformater la date au format "dd/mm/yyyy"
                    article_data['date'] = datetime.strptime(date_str_cleaned, "%d/%m/%Y").strftime("%d/%m/%Y")
                    article_date = datetime.strptime(article_data['date'], "%d/%m/%Y")
                    print(article_date)
                    if date_limit and article_date < date_limit:
                        continue  # Passer à l'article suivant si la date est antérieure à la limite
                articles.append(article_data)

    return articles

def main():
    main_url = "https://www.frandroid.com/culture-tech/intelligence-artificielle"
    # Date limite au format (année, mois, jour)
    date_limit = datetime(2024, 5, 25)

    articles = find_recent_articles(main_url, date_limit)

    if os.path.exists('.github/articles_after_date.json'):
        with open('.github/articles_after_date.json', 'r') as infile:
            print("11111   fichier json rempli")
            existing_articles = json.load(infile)
        articles.extend(existing_articles)    

    with open('.github/articles_after_date.json', 'w') as outfile:
        print("22222   fichier json rempli")
        json.dump(articles, outfile, indent=4)

if __name__ == "__main__":
    main()
