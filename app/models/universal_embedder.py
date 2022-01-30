from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import numpy as np
from nltk.tokenize.punkt import PunktSentenceTokenizer
sent_tokenizer = PunktSentenceTokenizer()

tokenizer = AutoTokenizer.from_pretrained("microsoft/mpnet-base")
embed_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


def conversational_embedder(utterances):
    """
    ues - lists of strings which are parts of an utterance for each utterance
          Example: ues = [["part1_ue1", "part2_ue1"], ["part1_ue2", "part2_ue2", "part3_ue2"],...]
    ue - list of input strings for 1 utterance
         Example: ue1 = ["part1_ue1", "part2_ue1"]
    input_str - part of an utterance - string input which the model will process
         Example: input_str = "part1_ue1"
    sent - sentence
    """
    ues = []
    for utterance in utterances:

        ue = []
        token_counter = 0
        input_str = ""

        for start, end in sent_tokenizer.span_tokenize(utterance):
            sent = utterance[start:end]
            if token_counter + len(tokenizer(sent)['input_ids']) < 128:
                input_str += sent + " "
                token_counter += len(tokenizer(sent)['input_ids'])
            else:
                # we append the previous input_srt to our list which contains parts of the current utterance
                if input_str.strip():
                    ue.append(input_str.strip())
                # theoretically there could be very rare cases when length of 1 sentence exceeds 128 tokens,
                # but the model itself is able to process Max Sequence Length of 384 tokens,
                # although it was trained on shorter sentences and during training developers truncated the input
                input_str = sent + " "
                token_counter = len(tokenizer(sent)['input_ids'])

        # in the loop above last input_str was not added to the list containing parts of the current utterance, so we add it
        if input_str.strip(): ue.append(input_str.strip())
        ues.append(ue)

    # we are doing this to encode an array of all strings which is much faster compared to encoding separate strings in the loop
    num_sent_per_ues = [len(s) for s in ues]

    embeddings = embed_model.encode(np.concatenate(ues).ravel())

    # initializing an array which will hold the final embeddings, it's much faster than ordinary appending to the list,
    # because it is numpy-way
    output = np.zeros((len(utterances), embeddings.shape[1]))
    prev_num = 0

    for i, num_sent in enumerate(num_sent_per_ues):
        output[i] = (embeddings[prev_num:prev_num + num_sent].mean(axis=0))
        prev_num += num_sent

    return output