import os
import json
import math
from nltk.stem.snowball import SpanishStemmer

def readBlock(filenames, k):
    # filePath = os.path.join("proyecto2/invertedindex/files/blocks", filenames[k])
    with open ("proyecto2/invertedindex/files/blocks/"+ filenames[k]) as f:
        return json.load(f)

def BB(word, filenames):
    a = 0
    b = len(filenames)-1
    while a <= b:
        k = int((a+b)/2)
        dic = readBlock(k, filenames)
        if word in dic:
            return dic[word]
        firstElement = next(iter(dic))
        lastElement = next(reversed(dic))
        if lastElement < word:
            a = k + 1
        elif firstElement > word:
            b = k - 1
        else:
            return []
    return []

def seqSearch(word, filenames):
    documents = []
    for k in range((len(filenames))):
        dic = readBlock(filenames, k)
        if word in dic:
            for document in dic[word]:
                documents.append({'id': document['id'], 'tf': document['tf']})
    return documents


def tfidf(df, idf):
    return math.log10(1 + df) * idf

def cosine(consulta):

    filenames = os.listdir("proyecto2/invertedindex/files/blocks")

    stemmer = SpanishStemmer()
    consulta = consulta.split()
    for i in range(len(consulta)):
        consulta[i] = stemmer.stem(consulta[i])

    consulta = { x: consulta.count(x) for x in consulta }

    with open ("proyecto2/invertedindex/files/documentsLength.json") as f:
        length = json.load(f)

    N = len(length)
    scores = {}

    for word in consulta:
        # documents = BB(word)
        documents = seqSearch(word, filenames)
        if len(documents) > 0:
            idf = math.log10(N/(len(documents)))
            consulta[word] = tfidf(consulta[word], idf)
            for document in documents:
                document['tf'] = tfidf(document['tf'], idf)
                if document['id'] not in scores:
                    scores[document['id']] = 0
                scores[document['id']] += consulta[word] * document['tf']

    for document in scores:
        key_id = length.get(str(document), None)
        if key_id:
            scores[document] = scores[document]/length.get(str(document), None)
    
    scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    ans = [e for e in scores]
    # print("ans: ", ans)
    return ans