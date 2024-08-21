import random

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from hf_model_wrappers import hf_summarize

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the description
    description = soup.find('div', class_='author-description').get_text(strip=True)
    
    # Optionally, keep only the first 500 characters if needed
    # article_text = article_text[:500]
    
    return description

def scrape_news(urls):
    all_news = []
    for url, structure in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if structure == 'test':
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract the title
                    title = soup.find('h3', class_='author-title').get_text(strip=True)

                    all_news.append({'title': title, 'url': url})

            else:
                print(f"Failed to retrieve data from {url}")
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")

    return all_news

if __name__ == "__main__": # for testing purposes
    urls = [
        ('http://quotes.toscrape.com/author/Albert-Einstein/', 'test'),
        ('http://quotes.toscrape.com/author/J-K-Rowling/', 'test'),
        ('http://quotes.toscrape.com/author/Jane-Austen/', 'test'),
        ('http://quotes.toscrape.com/author/Marilyn-Monroe/', 'test'),
        ('http://quotes.toscrape.com/author/Andre-Gide/', 'test'),
        ('http://quotes.toscrape.com/author/Thomas-A-Edison/', 'test'),
        ('http://quotes.toscrape.com/author/Eleanor-Roosevelt/', 'test'),
        ('http://quotes.toscrape.com/author/Elie-Wiesel/', 'test'),
        ('http://quotes.toscrape.com/author/Douglas-Adams/', 'test'),
        ('http://quotes.toscrape.com/author/Dr-Seuss/', 'test'),
    ]

    news_articles = scrape_news(urls) # scrape all links

    print("Authors profiles retrieved: ")
    for article in news_articles:
        print(f"Title: {article['title']}, URL: {article['url']}")
   
    selected_article = random.choice(news_articles)
    article_title = selected_article['title']
    article_url = selected_article['url']
    article_text = fetch_article_content(article_url)
    summary = hf_summarize.bart_large_cnn(article_title + " " + article_text)

    print("\r")
    print("Random author profile retrieved: ")
    print(selected_article)
    print("Full author bio: ", article_text)
    print("Bio summary: ", summary)
