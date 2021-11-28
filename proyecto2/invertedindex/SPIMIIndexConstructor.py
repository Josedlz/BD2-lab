from Classes.Buffer import Buffer
from helpers.sorting import mergeLists
from helpers.system import getSize

import os 
import json
import logging

from SPIMI_Inverter import SPIMI_Inverter   

class SPIMIIndexConstructor:
    def __init__(self):
        #Average block size
        self.blockSize = 0

        self.outputBlocks = None
        self.outputBlockIterator = 0

        self.bufferA = Buffer({})
        self.bufferB = Buffer({})

        self.outputBuffer = {}

    def dumpBuffer(self):
        path =  self.outputBlocks[self.outputBlockIterator]['filePath']
        print("Writing", path)
        with open(path, 'w') as out:
            json.dump(self.outputBuffer, out)
    
    def isLastBlock(self):
        return self.outputBlockIterator == (len(self.outputBlocks) - 1)

    def getLeftOutputBlockSize(self):
        return self.outputBlocks[self.outputBlockIterator]['sizeLeft']
    
    def advanceOutputBlock(self):
        if self.outputBlockIterator < len(self.outputBlocks):
            self.outputBlockIterator += 1
            self.outputBuffer.clear()
    
    def decreaseSizeOutputBlock(self, amount):
        self.outputBlocks[self.outputBlockIterator]['sizeLeft'] -= amount

    def _loadBlocksMetadata(self, blocksToMerge):
        self.outputBlockIterator = 0
        metaData = []
        for blockFile in blocksToMerge:
            blockFileMod = blockFile.rstrip('.json') + '_temp.json'
            blockMetaData = {}
            blockMetaData['filePath'] = blockFileMod
            blockMetaData['sizeLeft'] = os.path.getsize(blockFile)
            metaData.append(blockMetaData) 
        self.outputBlocks = metaData

    def _loadBuffers(self, documentA, documentB):
        self.bufferA.load(documentA)
        self.bufferB.load(documentB)
    
    def _addPostingList(self, word, postingList):
        postingListSize = getSize(postingList)
        isLastBlock = self.isLastBlock()
        sizeLeft = self.getLeftOutputBlockSize()
        ratio = sizeLeft // postingListSize

        if ratio >= 1 or isLastBlock:
            self.decreaseSizeOutputBlock(postingListSize)
            self.outputBuffer[word] = postingList
        else:
            lastIndex = ratio*(len(postingList)-1)
            if lastIndex != 0:
                self.outputBuffer[word] = postingList[:lastIndex]
            self.dumpBuffer()
            self.advanceOutputBlock() #if it's last it won't move
            self.outputBuffer[word] = postingList[lastIndex:]

    def _sortBuffers(self):
        """
        I will iterate and constantly check three things
        1. Output buffer has not reached its max size yet
        2. Both buffers still have a current word
        3. Both buffers still have elements in the posting list
        of the current word that aren't assigned
        """
        i = 0
        j = 0

        n1 = self.bufferA.getLength()
        n2 = self.bufferB.getLength()

        while i < n1 and j < n2:
            wordA, postingListA = self.bufferA[i]
            wordB, postingListB = self.bufferB[j]

            if wordA == wordB:
                mergedPostingList = mergeLists(postingListA, postingListB)
                self._addPostingList(wordA, mergedPostingList)

            elif wordA < wordB:
                self._addPostingList(wordA, postingListA)

            else:
                self._addPostingList(wordB, postingListB)

            i += 1
            j += 1
        
        while i < n1:
            wordA, postingListA = self.bufferA[i]
            self._addPostingList(wordA, postingListA)
            i += 1
            
        while j < n2:
            wordB, postingListB = self.bufferB[j]
            self._addPostingList(wordB, postingListB)
            j += 1

        self.dumpBuffer()
        self.outputBuffer.clear()
        return

    def merge(self, documents, l, m, r):
        L = documents[l : m+1]
        R = documents[m+1 : r+1]
        logging.info("Merging blocks:", L, "and", R)
        print("Merging blocks:", L, "and", R)

        self._loadBlocksMetadata(L + R)
        for left, right in zip(L, R):
            logging.info("Comparing:", left, "and", right)
            print("Comparing:", left.lstrip('proyecto2/invertedindex/files/blocks/'), "and", right.lstrip('proyecto2/invertedindex/files/blocks/'))
            self._loadBuffers(left, right)
            self._sortBuffers()

        print("Merged blocks:", L, "and", R)
        
        #Clear the temporary files        
        print("Clearing temporary files")
        mergedBlocks = L + R
        for mergedBlock in mergedBlocks:
            blockFileMod = mergedBlock.rstrip('.json') + '_temp.json'
            with open(blockFileMod, 'r') as f:
                content = json.load(f)
            with open(mergedBlock, 'w') as out:
                json.dump(content, out)

                os.remove(blockFileMod) # one file at a time

    def mergeBlocks(self, documents, l, r):
        if l >= r:
            return 
        m = (l + r - 1) // 2
        self.mergeBlocks(documents, l, m)
        self.mergeBlocks(documents, m+1, r)
        self.merge(documents, l, m, r)

    def generate(self):
        """
        This method iterates over the documents by chunks
        of size documentSize.

        For each chunk of string, it creates a Pandas DataFrame. 

        Then it creates a dictionary using the document ID and the 
        content of the document. This is passed to an instance of the 
        Index Inverter class, using the same instance until its index 
        attribute exceeds blockSize.

        When this happens, we save the index created so far into a block
        of secondary memory, and then we free the memory of the Index Inverter
        class for it to keep iterating over the documents.
        """       

        root = os.getcwd()
        data_path = 'proyecto2/invertedindex/files/data_elecciones'
        path = os.path.join(root, data_path)

        for curFileNumber, file in enumerate(os.listdir(path)):
            with open(os.path.join(path, file), 'r') as f:
                data = json.load(f)
                spimi = SPIMI_Inverter(data, curFileNumber)   
                spimi.parseNextBlock()
                spimi.writeBlockToDisk()
    
if __name__ == '__main__':
    bsbi = SPIMIIndexConstructor()
    #bsbi.generate()
    path = 'proyecto2/invertedindex/files/blocks'
    files = []
    for i in range(8):
        files.append(os.path.join(path, f"block_{i}.json"))
    bsbi.mergeBlocks(files, 0, len(files)-1)
    print("termine bitch")