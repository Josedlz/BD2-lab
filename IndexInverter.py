import os
import json
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SpanishStemmer

class IndexInverter:
    def __init__(self):
        self.index = {}
        self.stopwords = {}
        if not self.loadIndex():
            self.readDocuments()
            self.writeIndex()
    
    def loadIndex(self):
        """We check if there's already an index at hand.
           Returns a boolean that's true if there is one and 
           false otherwise."""
        index_filename = "inverted_index.json"
        if os.path.exists(index_filename):
            with open(index_filename, 'r') as index:
                self.index = json.load(index)
                return True
        return False

    def _normalize(self, tokens):
        """
        This will remove the stopwords.
        """
        processed_tokens = set()
        for token in tokens:
            if token not in self.stopwords:
                processed_tokens.add(token)
        return processed_tokens

    def _reduce(self, tokens):
        """
        We do stemming of the words.
        There's no lemmatizer for Spanish :()
        """
        #Stemming
        stemmer = SpanishStemmer()
        processed_tokens = set()
        for token in tokens:
            processed_tokens.add(stemmer.stem(token))
        return processed_tokens

    def _tokenize(self, file, content):
        """
        Method that will split a document into a list of words
        and add each of them to the self.index. 
        """
        tokens = word_tokenize(content)
        tokens = self._normalize(tokens)
        tokens = self._reduce(tokens)

        for token in tokens:
            if token in self.index:
                self.index[token].append(file)
            else:
                self.index[token] = [file]

    def readDocuments(self):
        #First we read the stopwords
        with open('stopwords.txt') as stopwords:
            self.stopwords = set(stopwords.read().split('\n'))

        #We populate the index
        for root, folder, files in os.walk(os.getcwd()):
            for file in files:
                if file != 'stopwords.txt' and file.startswith('libro'):
                    with open(file) as document:
                        content = document.read()
                        self._tokenize(file, content)
        
        #We eliminate duplicates and sort entries
        for word in self.index:
            self.index[word] = sorted(set(self.index[word]))
        
    def writeIndex(self):
        """
        Writing the self.index to secondary memory
        """
        with open('inverted_index.json', 'w') as f:
            json.dump(self.index, f)


    def retrieve(self, query):
        pass

if __name__ == '__main__':
    ii = IndexInverter()
    query = input()
    ii.retrieve(query)
