'''
Created on Mar 15, 2016

@author: Max
'''
import unittest
import rdflib
# from test.importGame import getGameID, getFirstHalfMove, getLastHalfMove,\
#     changeTypes
 
 
class Test(unittest.TestCase):
 
 
    def setUp(self):
        self.testInFile = open('C:/Users/Max/Documents/RO/Q/00a3e640-c214-4e85-bf06-4a307c668ef7.nt', 'r')
 
 
    def tearDown(self):
        self.testInFile.close()
  
 
    def testTurtleParse(self):
        testGraph = rdflib.Graph()
        inFile = open('C:/Users/Max/Documents/RO/ontoChess.ttl', 'r')
        res = testGraph.parse(inFile, format='n3')
        outFile = open('C:/Users/Max/Documents/RO/ontoChess_test.ttl', 'w')
        outFile.write(res.toTriples(format='n3', encoding='utf8').decode( encoding='utf8'))
        outFile.close()
 
#     def testGetGameID(self):
#         testGameID = getGameID(self.testInFile)
#                 
#         self.assertEqual('http://purl.org/NET/chess/resource/692fe704-01ed-41ce-a935-ceac377e8bee', testGameID)
#         
#     def testGetFirstHalfMove(self):
#         self.assertEqual('http://purl.org/NET/chess/resource/4cc9c06e-3dc1-499a-9f0e-da6c8d0ef500', getFirstHalfMove(self.testInFile))
#         
#     def testGetLastHalfMove(self):
#         self.assertEqual('http://purl.org/NET/chess/resource/8cdb0b5e-9b8e-4953-ab29-15a6faff68e2', getLastHalfMove(self.testInFile) )
#         
#     def testChangeTypes(self):
#         outFile = open('C:/Users/Max/Documents/RO/ontoChess_game_test.ttl', 'w')
#         outFile.write(changeTypes(self.testInFile).toTriples(format='n3', encoding='utf8').decode( encoding='utf8'))
#         outFile.close()
         
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()