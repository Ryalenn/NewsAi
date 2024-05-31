import cohere
import json
import requests
from bs4 import BeautifulSoup
import time
import os 
import httpx

# Fonction pour récupérer le contenu HTML avec timeout
def get_html_content(url, timeout=20):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return None

# Fonction pour extraire le texte pertinent
def extract_relevant_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    relevant_text = ' '.join([para.get_text() for para in paragraphs])
    return relevant_text

def summarize_text(prompt, relevant_text, retry_count=3, retry_delay=10):
    co = cohere.Client(api_key="ENqgUcGs1sB0DBMbrMnfrSjiDf264vcbcpAZbiMz")
    
    for attempt in range(retry_count):
        try:
            response = co.chat(
                model="command-r-plus",
                message=f"{prompt}\n\n{relevant_text}"
            )
            print(response.text)
            return response.text
        except (requests.exceptions.RequestException, httpx.ConnectTimeout) as e:
            print(f"Erreur lors de l'appel à l'API Cohere: {e}")
            if attempt < retry_count - 1:
                print(f"Nouvelle tentative dans {retry_delay} secondes...")
                time.sleep(retry_delay)
            else:
                print("Échec après plusieurs tentatives.")
                return None

def main():
    # Charger les URLs depuis le fichier JSON
    with open('articles_after_date.json', 'r') as file:
        articles = json.load(file)

    prompt = "Résumez le texte suivant en vous concentrant sur les points importants pour quelqu'un travaillant dans le domaine de l'IA. Fournissez ensuite un titre pertinent pour l'article, suivi de son résumé. Assurez-vous que le titre est fourni seul, sans la mention 'Titre:', A la fin du titre ajoute la balise '##', ta réponse prend donc la forme Titre ## Resumé : "

    summaries = []  # Liste pour stocker les résumés

    for article in articles:
        if article.get('check') == 'no':
            url = article['link']
            html_content = get_html_content(url)
            if html_content:
                relevant_text = extract_relevant_text(html_content)
                summary = summarize_text(prompt, relevant_text)
                if summary:
                    # Extraire le titre et le contenu du résumé
                    split_summary = summary.split("##")
                    if len(split_summary) >= 2:
                        title = split_summary[0].strip()
                        body = split_summary[1].strip()
                        article['check'] = 'yes'
                        summaries.append({
                            "title": title,
                            "link": url,
                            "body": body
                        })
                    # Mettre à jour l'article avec le résumé
                    with open('articles_after_date.json', 'w') as outfile:
                        json.dump(articles, outfile, indent=4)
            # Pause de 8 secondes entre les appels API pour respecter les limites de taux
            time.sleep(8)

    # Ajouter les nouveaux résumés au fichier JSON sans écraser les données existantes
    if os.path.exists('summaries.json'):
        with open('summaries.json', 'r') as infile:
            existing_summaries = json.load(infile)
        summaries.extend(existing_summaries)

    with open('summaries.json', 'w') as outfile:
        json.dump(summaries, outfile, indent=4)

if __name__ == "__main__":
    main()
