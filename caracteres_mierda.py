import json
import os

def es_basura(word):
    if len(word) == 1:
        return True
    basura = {'q', 'pq', ':', '@', '¿', '?', 
            'xq', 'k','rt'}

    mega_basura = {',', '.', '(', ')', 
            '/', '\\', '!', '¡', '',
            '%', "'", "//", "t.co", "\uh"}

    for mb in mega_basura:
        if mb in word:
            return True

    if word in basura or mega_basura:
        return True
    
    return False

if __name__ == '__main__':
    dump = 'stopwords.txt'
    stopwords = {}
    files = os.listdir('blocks')
    for file in files:
        with open(file, 'r') as f:
            temp = json.load(f)
        for word in temp:
            if es_basura(word):
                stopwords.add(word)

    with open(dump, "w") as f:
        for word in stopwords:
            f.write(dump)

