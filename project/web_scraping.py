import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# URL of the webpage to summarize
url = 'https://www.dawn.com/news/1805010/upheaval-in-top-judiciary-as-justice-ijazul-ahsan-resigns-a-day-after-justice-naqvi'
def web_scraping(url):
    try:
        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, 'html.parser')
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # fetch text from main (change the below code to filter page)
        if soup.main:
            return soup.main.get_text()
        elif soup.article:
            return soup.article.get_text()
        else:
            return soup.body.get_text()
    except:
        print('something wrong')
        return None
        
# print(web_scraping(url))

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False