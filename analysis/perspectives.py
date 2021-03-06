'''Get perspectives from different articles.'''

from scraping import logger
import re

import compare_articles
import extract_keywords
from scraping import aljazeera, bbc, cbc, cnn, globe_and_mail, guardian, \
                     huff_post, jpost, ny_post, ny_times, reuters, \
                     russia_today, times_of_israel, todays_zaman, usa_today

AL_JAZEERA = aljazeera.AlJazeera()
BBC = bbc.BBC()
CBC = cbc.CBC()
CNN = cnn.CNN()
GLOBE_AND_MAIL = globe_and_mail.GlobeAndMail()
GUARDIAN = guardian.Guardian()
HUFF_POST = huff_post.HuffPost()
JPOST = jpost.JPost()
NY_POST = ny_post.NYPost()
NY_TIMES = ny_times.NYTimes()
REUTERS = reuters.Reuters()
RT = russia_today.RussiaToday()
TIMES_OF_ISRAEL = times_of_israel.TimesOfIsrael()
TODAYS_ZAMAN = todays_zaman.TodaysZaman()
USA_TODAY = usa_today.USAToday()

NEWS_ORGS = [AL_JAZEERA, BBC, CBC, CNN, GLOBE_AND_MAIL, GUARDIAN, HUFF_POST,
            JPOST, NY_POST, NY_TIMES, REUTERS, RT, TIMES_OF_ISRAEL,
            TODAYS_ZAMAN, USA_TODAY]


def get_perspectives(url):
  '''Get different perspectives on the topic covered by article.

  Args:
    url: A string.

  Returns:
    A JSON-encoded string representing other articles with different
    perspectives than the original article.

    Format: a list of Article.to_dict()s, each with an additional 'sentences'
    attribute. 'sentences' contains a list of sentences with semantically
    different words that were extracted from the corresponding article's body.
  '''
  article = url_to_article(url)
  if article:
    article_topic = extract_keywords.extract_keywords(article.headline)
    related_articles = query_all_news_orgs(article_topic)
    return compare_articles.compare.to_all_articles(article, related_articles)

def query_all_news_orgs(query):
  '''Get the top articles for the given query from all supported news orgs.

  Args:
    query: A string of keywords.

  Returns:
    A list of Articles.
  '''
  top_articles = []
  for news_org in NEWS_ORGS: #TODO: parallelize
    try:
      top_articles.extend(news_org.get_query_results(query))
    except TypeError as e:
      logger.log.error('Error getting query results for %s: %s' %
                       (str(news_org), e))
  return top_articles

def url_to_article(url):
  '''Returns the Article at url if the url is supported.

  Args:
    url: A string.

  Returns:
    The Article that is scraped from url, if the url corresponds to an article
    on a supported news org page. Otherwise, None.
  '''
  try:
    if re.search(r'.*aljazeera\.com/((opinions)|(articles)|(news))/.+', url):
      return AL_JAZEERA.get_article(url)
    elif re.search(r'.*bbc\..+', url):
      return BBC.get_article(url)
    elif re.search(r'.*cbc\.ca/news/.+', url):
      return CBC.get_article(url)
    elif re.search(r'.*cnn\.com/.+', url):
      return CNN.get_article(url)
    elif re.search(r'.*theglobeandmail\.com/.+', url):
      return GLOBE_AND_MAIL.get_article(url)
    elif re.search(r'.*theguardian\.com/.+', url):
      return GUARDIAN.get_article(url)
    elif re.search(r'.*huffingtonpost\.c.+/.+', url):
      return HUFF_POST.get_article(url)
    elif re.search(r'.*jpost\.com/.+', url):
      return JPOST.get_article(url)
    elif re.search(r'.*nypost\.com/.+', url):
      return NY_POST.get_article(url)
    elif re.search(r'.*nytimes\.com/.+', url):
      return NY_TIMES.get_article(url)
    elif re.search(r'.*reuters\.com/.+', url):
      return REUTERS.get_article(url)
    elif re.search(r'.*rt\.com/.+', url):
      return RT.get_article(url)
    elif re.search(r'.*timesofisrael\.com/.+', url):
      return TIMES_OF_ISRAEL.get_article(url)
    elif re.search(r'.*todayszaman\.com/.+', url):
      return TODAYS_ZAMAN.get_article(url)
    elif re.search(r'.*usatoday\.com/story/.+', url):
      return USA_TODAY.get_article(url)
    else:
      logger.log.info("Didn't regexp match for %s" % url)
  except Exception as e:
    logger.log.info("Hit exception getting article for %s: %s" % (url, e))
    return None
