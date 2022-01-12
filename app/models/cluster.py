# This is a sample Python script.
from numpy import dot
from numpy.linalg import norm

from app.api.pipeline.output_model import SkillOutput
from app.common import CustomModel, Label

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from app.models.universal_embedder import conversational_embedder

phrase_break_threshold = 0.1
phrase_merge_threshold = 0.25
cluster_break_threshold = 0.3
cluster_merge_threshold = 0.45
max_elements_per_operation = 500


def get_embedding(text):
    return conversational_embedder([text])[0]


def cosine_distance(a, b):
    return 1 - (dot(a, b) / (norm(a) * norm(b)))


def cluster_texts(texts):
    phrases = []
    clusters = []
    for text in texts[:max_elements_per_operation]:
        phrase = cluster_text_to_phrase(text, phrases)
        if phrase.parent is None:
            cluster_phrase(phrase, clusters)
    # sort phrases in clusters, biggest to smallest
    for c in clusters:
        c.children.sort(key=lambda x: x.count, reverse=True)
    # sort clusters from biggest to smallest
    clusters.sort(key=lambda x: x.count, reverse=True)

    return clusters


class Phrase:
    count = 0
    text = None
    tightness = 0
    embedding = None
    parent = None


def cluster_text_to_phrase(text, phrases):
    # get embedding for text
    text_embed = get_embedding(text)
    best = None
    best_distance = 0
    for p in phrases:
        distance = cosine_distance(text_embed, p.embedding)
        if distance < phrase_break_threshold:
            best = p
            best_distance = distance

        if distance < phrase_merge_threshold:
            if best is None or distance < best_distance:
                best = p
                best_distance = distance

    if best is None:
        best = Phrase()
        best.count = 1
        best.text = text
        best.tightness = 0
        best.embedding = text_embed
        best.parent = None
        phrases.append(best)
    else:
        best.count += 1
        best.tightness = max(best.tightness, best_distance)
        best.parent.count += 1
        best.parent.children.append(best)
    return best


class Cluster:
    count = 0
    text = None
    tightness = 0
    embedding = None
    center_phrase = None
    children = []


def cluster_phrase(phrase, clusters):
    best = None
    best_distance = 0
    for cluster in clusters:
        distance = cosine_distance(phrase.embedding, cluster.embedding)
        if distance < cluster_break_threshold:
            best = cluster
            best_distance = distance

        if distance < cluster_merge_threshold:
            if best is None or distance < best_distance:
                best = cluster
                best_distance = distance

    if best is None:
        best = Cluster()
        best.text = phrase.text
        best.center_phrase = phrase
        best.embedding = phrase.embedding
        best.tightness = 0
        best.children = [phrase]
        clusters.append(best)
    else:
        best.tightness = max(best.tightness, best_distance)
        best.children.append(phrase)

    best.count += phrase.count
    phrase.parent = best
    return best


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


def test():
    # with open("C:\\Users\\Amit\\Downloads\\3800_queries_clean.txt", encoding="utf8") as file:
    #     lines = file.readlines()
    # print(lines[0])
    # print(lines[1])

    cluster_texts(["hello", "good morning"])


async def cluster_texts_api(req_body: CustomModel):
    input_texts = []
    label_type = req_body.params.get('type')
    for label in req_body.labels:
        if label.type == label_type:
            input_texts.append(label.span_text.strip())
    clusters = cluster_texts(input_texts)
    clusters_count = 0
    elements = []
    for cluster in clusters:
        element = {
            'count': cluster.count,
            'text': cluster.text
        }
        elements.append(element)
        clusters_count = clusters_count + cluster.count
    value_dict = {'count': clusters_count, 'elements': elements}
    label = Label(type="cluster", name=label_type, span=None, value=str(value_dict),
                  output_spans=[],
                  input_spans=None, span_text=None)
    skill_output: SkillOutput = SkillOutput(labels=[label])
    return skill_output


test()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
