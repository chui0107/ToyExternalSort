'''
    suppose the RAM is only 3 chars big and the file is 27 chars
'''

import os
from random import shuffle
from math import ceil

memSize = 10
fileSize = 90

def GenerateFile(path):
    list = []
    for i in range(fileSize):
        list.append(i + 1)
            
    shuffle(list)
    
    with open(path,'w') as f:    
        for item in list:
          f.write("%s\n" % item)
                  
class ExternalSort:
    
    def __init__(self):
        self.mChunks = 0
                
    def WriteChunk(self,fileID,list):
        
        with open('chunk' + str(fileID + 1) + '.txt','w') as f:    
            for item in list:
                f.write("%s\n" % item)
                    
    def SortFile(self,path):
        
        self.SortChunk(path)
        self.MergeChunk()
            
    def SortChunk(self,path):
        
        #read way to get the size of the file
        #statinfo = os.stat(path)
        #filesize = statinfo.st_size
        
        self.mFilePath = path
        self.mChunks = fileSize / memSize
        
        #sort each chunk
        with open(path,'r') as f:    

            for i in range(self.mChunks):
                
                chunk = []
                #first step sort each chunk
                for j in range(memSize):
                    data = f.readline()
                    chunk.append(int(data[:len(data) - 1]))
                    
                chunk.sort()
                
                self.WriteChunk(i,chunk)
                
    def MergeChunk(self):
        
        firstNBytes = memSize / (self.mChunks + 1)
        
        outputBuffer = []
        
        outputBufferSize = firstNBytes
        
        outputPath = "output.txt"
        
        outputFile = open(outputPath,'w')
        
        #n way merge                
        import Queue    
        q = Queue.PriorityQueue()
                        
        inputFiles = []
        for i in range(self.mChunks):
            inputFiles.append(open('chunk' + str(i + 1) + '.txt','r'))
            file = inputFiles[i]
            
            data = ''
            for j in range(firstNBytes):
                data += file.readline()
                
            data = data.split('\n')
            dataInt = int(data[0])
            
            q.put((dataInt,i));
            
        while not q.empty():
            
            tuple = q.get()
            outputBuffer.append(tuple[0])
                
            #write the outputBuffer to disk
            if len(outputBuffer) == outputBufferSize:
                for item in outputBuffer:
                    outputFile.write("%s\n" % item)
                    outputFile.flush()
                
                #clear the outputbuffer
                    del outputBuffer[:]
            
            #read # bytes from the top file    
            fileId = tuple[1]
            data = ''
            for j in range(firstNBytes):
                data += inputFiles[fileId].readline()
            
            #EOF of the file
            if data == '':
                continue
                    
            data = data.split('\n')
            dataInt = int(data[0])
            
            q.put((dataInt,fileId));
            
        for file in inputFiles:
            file.close()
            
        outputFile.close() 
                            
        
def main():
    path = "input.txt"
    #GenerateFile(path)
    
    externalSort = ExternalSort()
    externalSort.SortFile(path)
    
    
    
if __name__ == "__main__":
    main()