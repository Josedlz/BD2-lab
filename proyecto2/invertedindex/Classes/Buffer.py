import os 
import json

from Classes.IndexedOrderedDict import IndexedOrderedDict
from helpers.system import getSize

class Buffer:
    def __init__(self, dictionary):
        self.filePath = ''
        self.dictionary = IndexedOrderedDict(dictionary=dictionary)

    def __getitem__(self, index):
        word, postingList = (self.dictionary.get(index))
        return word, postingList

    def load(self, document_name):
        path = 'proyecto2/invertedindex/'
        filePath = os.path.join(path, document_name) 
        if self.filePath != filePath:
            self.filePath = filePath
            with open(filePath) as f:
               buffer = json.load(f) 
               self.dictionary = IndexedOrderedDict(buffer)

    def isComplete(self):
        return not self.dictionary.hasNext()

    def getFilePath(self):
        return self.filePath

    def getLength(self):
        return self.dictionary.getLength()

    def getMemorySize(self):
        return getSize(self.dictionary)
