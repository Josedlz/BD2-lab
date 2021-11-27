import json
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SpanishStemmer

"""
index = 
        {
            ...,
            'miun' : [{'id': 43, 'count': 33}, {...}], 
            'macarena': [{'id' : 5, 'count': 123}, {'id' : 42, 'count': 32}]
            ...,
        }
"""

class SPIMI_Inverter:

    def __init__(self, block, curFileNumber):
        self.index = {} #Inverted Index
        self.block = block
        self.stopwords = {}
        self.curFileNumber = curFileNumber
        self.stemmer = SpanishStemmer()
        self.N = 0
    
    def _lower(self, tokens):
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

    def _normalize(self, tokens):
        """
        This will remove the stopwords.
        """
        processed_tokens = []
        for token in tokens:
            if token not in self.stopwords:
                processed_tokens.append(token)
        return processed_tokens

    def _reduce(self, tokens):
        """
        We do stemming of the words.
        There's no lemmatizer for Spanish :()
        """
        #Stemming
        token_count = {}

        for token in tokens:
            stemmed_token = self.stemmer.stem(token)
            if stemmed_token not in token_count:
                token_count[stemmed_token] = 1
            token_count[stemmed_token] += 1
        return token_count

    def generateDictionary(self, ID: int, content: str):
        """
        Method that will split a document into a list of words
        and add each of them to the self.index. 
        """
        tokens = word_tokenize(content)  #generates token list from content self._lower(tokens)
        tokens = self._normalize(tokens) #removes stopwords
        tokens = self._reduce(tokens)    #stemming

        for token, tf in tokens.items():
            if token not in self.index:
                self.index[token] = []
            self.index[token].append({'id': ID, 'tf': tf})

    def writeBlockToDisk(self):
        """
        Writing the self.index to secondary memory
        """
        fileName = 'block_' + str(self.curFileNumber) + '.json'
        with open('blocks/' + fileName, 'w') as f:
            json.dump(self.index, f)

    def parseNextBlock(self):
        #First we read the stopwords
        with open('stopwords.txt') as stopwords:
            self.stopwords = set(stopwords.read().split('\n'))

        #We populate the index
        for document in self.block:
            self.generateDictionary(document['id'], document['text'])
        
        #We eliminate duplicates and sort entries
        for word in self.index:
            self.index[word] = sorted(self.index[word], key=lambda x: x['id'])
