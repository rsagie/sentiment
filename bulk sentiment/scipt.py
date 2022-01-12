import os
import requests

URL = 'http://localhost:9080/api/v0/pipeline'


def pipeline(input_text):
    return requests.post(URL, headers={
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }, json={
        'text': input_text,
        'input_type': 'article',
        "steps": [
            {"skill": "entities", "params": {}},
            {"skill": "custom", "params": {"url": "http://34.134.67.245:9080/sentiment", "auth_key": "password"},
             "cond": {"entities": {"$contains": "Trump"}}}]
    }
                         )
def get_txt_files(dir):
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if (os.path.isdir(path)):
            yield from get_txt_files(path)
        else:
            # print(f"Article name: {path}")
            yield path


def print_website_sentiment(website):
    print(f"Web site: {website}")
    for article in get_txt_files(f'./data/{website}'):
        article_sentiment = pipeline(input_text=open(article, 'r').read()).json()
        labels = article_sentiment.get("output")[0].get("labels")
        sentiment = None
        for label in labels:
            type = label.get('type')
            if type == 'custom':
                sentiment = label.get('value')
        if sentiment:
            print(f"Sentiment:{sentiment}")
        else:
            print("Skipped not interesting")


if __name__ == '__main__':
    print_website_sentiment(website= 'cnn')
    print("\n")
    print_website_sentiment(website= 'fox')
