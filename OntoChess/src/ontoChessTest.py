'''
Created on Mar 19, 2016

@author: Max
'''
import unittest
from test.processGames import loadGames, addHasHalfMove, parseHalfMoveRecord,\
    addMadeBy, addGameState
from rdflib.term import URIRef
import re


class Test(unittest.TestCase):


    def setUp(self):
        halfMoveRecord = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#halfMoveRecord')
        madeBy = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#madeBy')
        self.graph = loadGames('C:/Users/Max/Documents/RO/ontoChess.ttl')
        self.graph = addHasHalfMove(self.graph)
        self.graph = addMadeBy(self.graph)
        self.graph = addGameState(self.graph)
        
        self.halfMoveRecords = []
        
        for moveURI, pred, moveRecord in self.graph.triples( (None, halfMoveRecord, None)):
            playercolour = self.graph.value(subject=moveURI, predicate=madeBy) 
            self.halfMoveRecords.append((moveRecord, playercolour))


    def tearDown(self):
        pass



    def testParseHalfMoveRecord(self):
        for halfMoveRecord, playercolour in self.halfMoveRecords:
#             print(playercolour)
            parseHalfMoveRecord(halfMoveRecord, playercolour, self.graph)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()