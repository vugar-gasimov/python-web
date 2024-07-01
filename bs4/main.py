from bs4 import BeautifulSoup

import requests

URL = "https://news.ycombinator.com/news"
STATIC_URL = "https://appbrewery.github.io/news.ycombinator.com/"

response = requests.get(STATIC_URL)

yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")
# print(soup.title)
all_storylinks = soup.find_all(name="a", class_="storylink")
article_texts = []
article_links = []
for link in all_storylinks:
    text = link.getText()
    article_texts.append(text)
    link = link.get("href")
    article_links.append(link)
    
article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name='span',  class_="score")]
    # print(text, link, article_upvote)
# print(article_texts, article_links, article_upvotes)
    
# print(int(article_upvotes[0].split()[0]))
highest_vote=0
index_of_highest_voted_article = 0
for i, vote in enumerate(article_upvotes):
    if vote > highest_vote:
        highest_vote = vote
        index_of_highest_voted_article = i
        
print("Article with the highest vote:")
print("Title:", article_texts[index_of_highest_voted_article])
print("Link:", article_links[index_of_highest_voted_article])
print("Upvotes:", highest_vote)
# largest_number = max(article_upvotes)
# largest_index = article_upvotes.index(largest_number)
# print(artice_texts[largest_index])