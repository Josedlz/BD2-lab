import nltk

class IndexInverter:
    def __init__(self, block_id):
        self.index = {}
        pass
    def tokenize(self):
        """
        Method that will split a document into a list of words
        and add each of them to the self.index. 
        """
        pass
    def normalize(self):
        """
        This will remove the stopwords. For this we can use
        nltk.stopwords module
        """
        pass
    def reduction(self):
        """
        We do stemming and lemmatization of the words.
        For this we also use the nltk modules.
        """
        pass
    def generateIndex(self):
        """
        Writing the self.index to secondary memory
        """
        pass

if __name__ == '__main__':
    pass
