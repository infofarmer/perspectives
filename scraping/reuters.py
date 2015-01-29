from BeautifulSoup import BeautifulSoup
import json
import logging
import requests

#from api_keys import api_keys
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='reuters.log', level=logging.WARNING)

class REUTERS(news_interface.NewsOrg):
  '''Methods for interacting with the REUTERS website.'''

  def get_article(self, url):
    '''Implementation for getting an article from REUTERS.

    url: A URL in the www.reuters.* domain.

    Returns: The Article representing the article at that url.
    '''
    soup = BeautifulSoup(requests.get(url).text)
    headline = soup.find('div', attrs={'class': 'column1 gridPanel grid8'}).h1.string
    paragraphs = soup.find('div', attrs={'class': 'column1 gridPanel grid8'}).findAll("p")
    body = ' '.join([p.text.encode('ascii', 'ignore') for p in paragraphs])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.BBC)

  def get_query_results(self, query):
    '''Implementation for keyword searches from REUTERS.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
    'http://www.reuters.com/search?blob=%s'
    % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.findAll('li', attrs={'class': 'searchHeadline'})
    article_urls = [article.a.get('href') for article in articles]
 
    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
    return top_articles


