'''
Created on Mar 15, 2016

@author: Max
'''
import rdflib
from rdflib.term import URIRef
import os


# def getTypes(inFile, g=None):
#     if g is None:
#         g = rdflib.Graph()
#         g.parse(inFile, format='n3')
#         
#     retSet = set()
#     
#     for subj, pred, obj in g:
#         if str(pred) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
#             retSet.add(str(obj))
#     
#     return retSet



def importGames(inDir, graph):
    MAX_GAMES = 11
    count = 0
     
    for inFileName in os.listdir(path=inDir):
        game = Game(inDir+inFileName)

        for triple in game.gameGraph:
            graph.add(triple)
             
        count += 1
        if count > MAX_GAMES:
            break
             
    return graph

def importOntology(ontoFileName, graph):
    graph.parse(ontoFileName, format='turtle')
    
    return graph

class Game(object):
    
    
    def __init__(self, inFileName):
        inFile = open(inFileName, 'r')
        self.importGame(inFile)
    
    def importGame(self, inFile):
        self.gameGraph = rdflib.Graph()
            
        self.gameGraph.parse(inFile, format='n3')
        
        self.gameGraph = self.changeTypes()
        
        self.addFirstLast()
        

    def changeTypes(self):
    
        #read in map file
        mapFile = open('typeMap', 'r')
        typeMap = {}
        for s in mapFile:
            k, v = s.split('\t')
            typeMap[k.strip()] = v.strip()
            
        outGraph = rdflib.Graph()
        for subj, pred, obj in self.gameGraph:
            if str(subj) in typeMap.keys():
                subj = URIRef(typeMap[str(subj)])
                
            if str(pred) in typeMap.keys():
                pred = URIRef(typeMap[str(pred)])
                
            if str(obj) in typeMap.keys():
                obj = URIRef(typeMap[str(obj)])
            
            outGraph.add( (subj, pred, obj))
        
        return outGraph
    
    
    
    def addFirstLast(self):
        gameID = self.getGameID()
        firstMoveID = self.getFirstHalfMove()
        lastMoveID = self.getLastHalfMove()
        
        print(gameID)
        game = URIRef(gameID)
        firstMove = URIRef(firstMoveID)
        lastMove = URIRef(lastMoveID)
        
        self.gameGraph.add( (game, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasFirstHalfMove'), firstMove))
        self.gameGraph.add( (game, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasLastHalfMove'), lastMove))
        

    def getGameID(self):
        
        retVal = None
        
        for subj, pred, obj in self.gameGraph:
            if str(obj) == 'http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#ChessGame' and str(pred) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                retVal = str(subj)
                
        return retVal
    
    def getFirstHalfMove(self):
            
        retVal = None
        
        for subj, pred, obj in self.gameGraph:
            if str(obj) == 'http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#FirstMove' and str(pred) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                retVal = str(subj)
                
        return retVal
    
    def getLastHalfMove(self):
            
        retVal = None
        
        for subj, pred, obj in self.gameGraph:
            if str(obj) == 'http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#LastMove' and str(pred) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                retVal = str(subj)
                
        return retVal
    

if __name__ == '__main__':
    graph = rdflib.Graph()
    graph = importOntology('C:/Users/Max/Documents/RO/ontoChess/ontoChess.ttl', graph)
    graph = importGames('C:/Users/Max/Documents/RO/ontoChess/test_data/', graph)
    outFile = open('C:/Users/Max/Documents/RO/ontoChess/ontoChess_res.ttl', 'w')
    outFile.write(graph.serialize(format='n3', encoding='utf8').decode( encoding='utf8'))
    outFile.close()