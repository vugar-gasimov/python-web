import requests
from bs4 import BeautifulSoup
# import re

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

response = requests.get(URL)

website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
print(soup.title)
all_articles = []
# all_numbers=[]
all_titles = soup.find_all(name="h3", class_="title")
for title in all_titles:
    text = title.getText()
    all_articles.append(text)
for article in reversed(all_articles):
    print(article)
    # article_number = article.split()[0]
    # clean_number = re.sub(r'\D', '', article_number)
    # clean_number_int = int(clean_number)
    # all_numbers.append(clean_number_int)

