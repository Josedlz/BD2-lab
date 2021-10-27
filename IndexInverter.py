import os
import json
import time
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SpanishStemmer

class IndexInverter:
    def __init__(self):
        """
        self.index: Inverted Index
        """
        self.index = {}
        self.stopwords = {}
        self.stemmer = SpanishStemmer()
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
    
    def _lower(self, tokens):
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

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
        processed_tokens = set()
        for token in tokens:
            processed_tokens.add(self.stemmer.stem(token))
        return processed_tokens

    def _tokenize(self, file, content):
        """
        Method that will split a document into a list of words
        and add each of them to the self.index. 
        """
        tokens = word_tokenize(content)  #generates token list from content
        self._lower(tokens)
        tokens = self._normalize(tokens) #removes stopwords
        tokens = self._reduce(tokens)    #stemming

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

    def queryAND(self, A, B):
        i = 0
        j = 0
        result = []
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                i += 1
            elif A[i] > B[j]:
                j += 1
            else:
                result.append(A[i])
                i += 1
                j += 1
        return result

    def queryOR(self, A, B):
        i = 0
        j = 0
        result = []
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                result.append(A[i])
                i += 1
            else:
                result.append(B[j])
                j += 1

        while i < len(A):
            if not result:
                result.append(A[i])
            if A[i] != result[-1]:
                result.append(A[i])
            i += 1

        while j < len(B):
            if not result:
                result.append(B[j])
            elif B[j] != result[-1]:
                result.append(B[j])
            j += 1
        
        result = sorted(set(result))
        return result
    
    def queryANDNOT(self, A, B):
        i = 0
        j = 0
        result = []
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                result.append(A[i])
                i += 1
            elif A[i] > B[j]:
                j += 1
            else:
                i += 1
                j += 1
        return result

    def retrieve(self, query):
        if not query:
            return []
        query = query.rstrip(')')
        query = query.lstrip('(')

        if ' AND ' in query:
            A = query.split(' AND ')[0]
            B = ''.join(query.split(' AND ')[1:])
            if not B:
                return []
            if B[0] == '(' and B[-1] == ')':
                return self.queryAND(self.retrieve(B), self.retrieve(A))
            return self.queryAND(self.retrieve(A), self.retrieve(B))

        if ' OR ' in query:
            A = query.split(' OR ')[0]
            B = ''.join(query.split(' OR ')[1:])
            if not B:
                return A
            if B[0] == '(' and B[-1] == ')':
                return self.queryOR(self.retrieve(B), self.retrieve(A))
            return self.queryOR(self.retrieve(A), self.retrieve(B))

        if ' AND-NOT ' in query:
            A = query.split(' AND-NOT ')[0]
            B = ''.join(query.split(' AND-NOT ')[1:])
            if not B:
                return A
            if B[0] == '(' and B[-1] == ')':
                return self.queryANDNOT(self.retrieve(B), self.retrieve(A))
            return self.queryANDNOT(self.retrieve(A), self.retrieve(B))

        query = query.lower()
        if query in self.stopwords:
            return []
        query = self.stemmer.stem(query)
        return self.index.get(query, [])


if __name__ == '__main__':
    ii = IndexInverter()
    #query = input()
    start = time.time()
    query = "(Jinetes OR Muerte OR Luz) AND-NOT Gandalf"
    end = time.time()
    print("Recovered:", ii.retrieve(query), "\nTime taken:", (end - start)*1e6, "microseconds")
