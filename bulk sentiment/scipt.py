import os
import requests

URL = 'https://stage-studio.oneai.com/api/v0/pipeline'

def pipeline(input_text, skills):
    return requests.post(URL, headers={
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }, json={
        'text': input_text,
        'steps': [
            {
                'skill': skill,
                'id': id + 1,
                'inupt': id
            } for id, skill in enumerate(skills)
        ],
        'input_type': 'article'
    })

def get_txt_files(dir):
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if (os.path.isdir(path)): yield from get_txt_files(path)
        else: yield path

if __name__ == '__main__':
    for article in get_txt_files('bulk sentiment/data'):
        print(article, pipeline(
            open(article, 'r').read(),
            ['summarize', 'article-topics']
        ).__dict__)
        break
    pass