from collections import OrderedDict
from typing import Union

class IndexedOrderedDict:
    """
    This is a read-only data structure that will
    store a dictionary with sorted keys. You
    are also able to index it (0-based indexing). 
    
    It holds a counter that gets automatically
    increased each time you use the method
    getCurrent().
    """
    def __init__(self, dictionary):
        self.sortedDict = OrderedDict(sorted(dictionary.items()))
        self.keys = list(self.sortedDict.keys())
        self.max = len(self.keys)
        self.i = 0

    def getCurrent(self) -> Union[int, bool]:
        if self.i < (self.max - 1):
            word = self.keys[self.i]
            result = self.sortedDict[word]
            self.i += 1
            return word, result
        return False, []

    def get(self, pos: int) -> Union[int, bool]:
        if pos < (self.max - 1):
            word = self.keys[self.i]
            result = self.sortedDict[word]
            return word, result
        return False, []

    def hasNext(self) -> bool:
        return self.i < (self.max - 1)
    
    def getLength(self):
        return self.max
