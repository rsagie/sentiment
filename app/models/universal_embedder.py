from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import numpy as np
from nltk.tokenize.punkt import PunktSentenceTokenizer
sent_tokenizer = PunktSentenceTokenizer()

tokenizer = AutoTokenizer.from_pretrained("microsoft/mpnet-base")
embed_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def conversational_embedder(utterances):
    ues = []
    for utterance in utterances:
        sentences = []
        token_counter = 0
        sentence = ""
        for start, end in sent_tokenizer.span_tokenize(utterance):
            sent = utterance[start:end]
            if token_counter + len(tokenizer(sent)['input_ids']) < 128:
                sentence += sent + " "
                token_counter += len(tokenizer(sent)['input_ids'])
            else:
                if sentence.strip(): sentences.append(sentence.strip())
                sentence = sent + " "
                token_counter = len(tokenizer(sent)['input_ids'])

        if sentence.strip(): sentences.append(sentence.strip())
        ues.append(sentences)
    num_sent_per_ues = [len(s) for s in ues]
    embeddings = embed_model.encode(np.array(sentences).flatten())
    output = np.zeros((len(utterances), embeddings.shape[1]))
    prev_num = 0
    for i, num_sent in enumerate(num_sent_per_ues):
        output[i] = (embeddings[prev_num:prev_num + num_sent].mean(axis=0))
        prev_num += num_sent
    return output