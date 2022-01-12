import os
import requests

URL = 'http://34.134.67.245:9080/sentiment'

def get_sentiment(article):
    return requests.post(URL, headers={
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }, json={
        'input_text': article
    }).json()['labels'][0]['value']

def get_txt_files(dir):
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if (os.path.isdir(path)): yield from get_txt_files(path)
        else: yield path

if __name__ == '__main__':
    for article in get_txt_files('bulk sentiment/data'):
        print(article, get_sentiment(open(article, 'r').read()))
    pass