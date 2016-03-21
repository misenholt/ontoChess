'''
Created on Mar 15, 2016

@author: Max
'''
import rdflib
from rdflib.term import URIRef, Literal
import re
import uuid
from rdflib.namespace import RDF

hasState = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasState')
rdfType = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
chessGame = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#ChessGame')
hasFirstHalfMove = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasFirstHalfMove')
hasHalfMove = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasHalfMove')
nextHalfMove = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#nextHalfMove')
partOf = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#partOf')
sameAs = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#sameAs')
hasLocation = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasLocation')
hasColour = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasColour')
hasLocationStr = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasLocationStr')
        
file = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
file_inv = 'abcdefgh'
rank = [1,2,3,4,5,6,7,8]
rank_inv = [1,2,3,4,5,6,7,8]

class Colour():
    white = 'white'
    black = 'black'
    
class Shape():
    king = 'King'
    queen = 'Queen'
    bishop = 'Bishop'
    knight = 'Knight'
    rook = 'Rook'
    pawn = 'Pawn'
    
class StateInconsistency(Exception):
    pass

def loadGames(fileName):
    g = rdflib.Graph()
    g.parse(fileName, format='n3')
    
    return g
    
def getIDs(graph):
    gameIDs = []
    
    for subj, pred, obj in graph.triples( (None, rdfType, chessGame)):
        gameIDs.append(subj)
            
    return gameIDs

def addHasHalfMove(graph):
    
    gameIDs = getIDs(graph)

    for gameID in gameIDs:
        
        move = graph.value( subject=gameID, predicate=hasFirstHalfMove )
    
        while(move is not None):
            graph.add( (gameID, hasHalfMove, move) )
            move = graph.value(subject=move, predicate=nextHalfMove)
            
    return graph

    
#     def __init__(self, inStr):
#         if inStr.lower() not in self.shapeMap:
#             raise Exception
#         self.val = inStr.lower()
#     
#     def __str__(self):
#         return self.val
#     
#     def __eq__(self, shape):
#         return self.val == shape.val
        

class GameState():
    
    def __init__(self, graph, gameURI, prevState=None, move=None):
        self.URI = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#{}'.format(uuid.uuid4()))
        graph.add( (self.URI, RDF.type, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#GameState')) )
        graph.add( (gameURI, hasState, self.URI))
        if prevState is None or move is None:
            self.createStartingState(graph)
            graph.add( (self.URI, RDF.type, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#StartingState')) )
        else:
            #TODO: handle move
            pass
            
            
    def createStartingState(self, graph):
        PieceState(graph, self, 1, 'a', colour=Colour.white, shape=Shape.rook)
        PieceState(graph, self, 1, 'b', colour=Colour.white, shape=Shape.knight)
        PieceState(graph, self, 1, 'c', colour=Colour.white, shape=Shape.bishop)
        PieceState(graph, self, 1, 'd', colour=Colour.white, shape=Shape.queen)
        PieceState(graph, self, 1, 'e', colour=Colour.white, shape=Shape.king)
        PieceState(graph, self, 1, 'f', colour=Colour.white, shape=Shape.bishop)
        PieceState(graph, self, 1, 'g', colour=Colour.white, shape=Shape.knight)
        PieceState(graph, self, 1, 'h', colour=Colour.white, shape=Shape.rook)
        PieceState(graph, self, 2, 'a', colour=Colour.white, shape=Shape.pawn)
        PieceState(graph, self, 2, 'b', colour=Colour.white, shape=Shape.pawn)
        PieceState(graph, self, 2, 'c', colour=Colour.white, shape=Shape.pawn)
        PieceState(graph, self, 2, 'd', colour=Colour.white, shape=Shape.pawn)
        PieceState(graph, self, 2, 'e', colour=Colour.white, shape=Shape.pawn)
        PieceState(graph, self, 2, 'f', colour=Colour.white, shape=Shape.pawn)
        PieceState(graph, self, 2, 'g', colour=Colour.white, shape=Shape.pawn)
        PieceState(graph, self, 2, 'h', colour=Colour.white, shape=Shape.pawn)
        
        PieceState(graph, self, 8, 'a', colour=Colour.black, shape=Shape.rook)
        PieceState(graph, self, 8, 'b', colour=Colour.black, shape=Shape.knight)
        PieceState(graph, self, 8, 'c', colour=Colour.black, shape=Shape.bishop)
        PieceState(graph, self, 8, 'd', colour=Colour.black, shape=Shape.queen)
        PieceState(graph, self, 8, 'e', colour=Colour.black, shape=Shape.king)
        PieceState(graph, self, 8, 'f', colour=Colour.black, shape=Shape.bishop)
        PieceState(graph, self, 8, 'g', colour=Colour.black, shape=Shape.knight)
        PieceState(graph, self, 8, 'h', colour=Colour.black, shape=Shape.rook)
        PieceState(graph, self, 7, 'a', colour=Colour.black, shape=Shape.pawn)
        PieceState(graph, self, 7, 'b', colour=Colour.black, shape=Shape.pawn)
        PieceState(graph, self, 7, 'c', colour=Colour.black, shape=Shape.pawn)
        PieceState(graph, self, 7, 'd', colour=Colour.black, shape=Shape.pawn)
        PieceState(graph, self, 7, 'e', colour=Colour.black, shape=Shape.pawn)
        PieceState(graph, self, 7, 'f', colour=Colour.black, shape=Shape.pawn)
        PieceState(graph, self, 7, 'g', colour=Colour.black, shape=Shape.pawn)
        PieceState(graph, self, 7, 'h', colour=Colour.black, shape=Shape.pawn)
    

class PieceState():
    
    def __init__(self, graph, gameState, rank, file, colour=None, shape=None, piece=None):
        if piece is None:
            if colour is None or shape is None:
                raise Exception
            else:
                piece = Piece(graph, colour, shape)
                
        self.URI = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#{}'.format(uuid.uuid4()))
        graph.add( (self.URI, RDF.type, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#PieceState')) )
        graph.add( (self.URI, sameAs, piece.URI) )
        graph.add( (self.URI, partOf, gameState.URI) )
        loc = Loc(rank=rank, file=file)
        graph.add( (self.URI, hasLocation, loc.URI) )
        
    
# class PieceLoc():
#     
#     def __init__(self, piece, loc):
#         self.piece = piece
#         self.loc = loc
#         
#     def setLoc(self, loc):
#         self.loc = loc
#         
#     def getLoc(self):
#         return self.loc
#     
#     def getPiece(self):
#         return self.piece
    
class Piece():
    
    def __init__(self, graph, colour, shape):
        self.URI = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#{}'.format(uuid.uuid4()))
        graph.add( (self.URI, RDF.type, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#{}'.format(shape))) )
        graph.add( (self.URI, RDF.type, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#GamePiece')) )
        #TODO: change hasColour to hasOwner with instance of player
        graph.add( (self.URI, hasColour, Literal(colour)))
        self.colour = colour
        self.shape = shape
        
    def __eq__(self, piece):
        return self.colour == piece.colour and self.shape == piece.shape

class Loc():
    
    '''
    rank should be an integer 1<=x<=8
    file should be a character in [a-h] 
    '''
    def __init__(self, locStr='', rank=None, file=None): 
        self.URI = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#{}'.format(uuid.uuid4()))
        graph.add( (self.URI, RDF.type, URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#Location')) )
        if rank is not None and file is not None:
            locStr = '{}{}'.format(file, rank)
        graph.add( (self.URI, hasLocationStr, Literal(locStr)))
        if rank is None or file is None:
            if not len(locStr) == 2:
                print(locStr)
                raise Exception
            self.file = locStr[0]
            self.rank = locStr[1]
        else:
            self.rank = rank
            self.file = file
        
    def equals(self, loc):
        return self.file == loc.file and self.rank == loc.rank
    
    def __str__(self):
        return '{}{}'.format(self.file, self.rank)
    
    
def addGameState(graph):
    
    gameURIs = getIDs(graph)

    for gameURI in gameURIs:
        GameState(graph, gameURI)
#         for triple in gameState.toTriples():
#             graph.add(triple)
#         link up gameState to game as game state and as starting state
        
        
        move = graph.value( subject=gameURI, predicate=hasFirstHalfMove )
        print(move)
    
#         while(move is not None):
#             
# #             get half move record
#             rec = getHalfMoveRecord(graph, move)
#             
#             
# #             parse half move record
#             move = parseHalfMoveRecord(rec)
#             
#             GameState(graph, gameURI, prevState=gameState, move=move)
#             
# #             link up game states
#             
#                 
#             move = graph.value(subject=move, predicate=nextHalfMove)

    return graph

def getHalfMoveRecord(graph, move):
    halfMoveRecord = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#halfMoveRecord')
    return graph.value(subject=move, predicate=halfMoveRecord)



def parseHalfMoveRecord(halfMoveRecord, playerColour, graph):
    pieceMap = {'K':'king', 'Q':'queen', 'B':'bishop', 'N':'knight', 'R':'rook'}
    capture = False
    shape = None
    toLoc = None
    fromLoc = None
    piece2 = None
    toLoc2 = None
    fromLoc2 = None
    print(halfMoveRecord)
    print(playerColour)
    if halfMoveRecord.startswith('O'):
        colourRank = {'white':1, 'black':8}
        shape = Shape('king')
        fromLoc = Loc(file='e', rank=colourRank[str(playerColour)])
        piece2 = Shape('rook')
        toLoc2 = fromLoc
        if len(halfMoveRecord) < 4:
            fromLoc2 = Loc(file='h', rank=colourRank[str(playerColour)])
        else:
            fromLoc2 = Loc(file='a', rank=colourRank[str(playerColour)])
            
        toLoc = fromLoc2
        
    else:
        if halfMoveRecord[0].isupper():
            shape = Shape(pieceMap[halfMoveRecord[0]])
            if halfMoveRecord[1] == 'x':
                capture = True
        else:
            shape = Shape('pawn')
            if halfMoveRecord[0] == 'x':
                capture = True
        
        m = re.search('.*([a-z][0-9]).*', halfMoveRecord)
        toLoc = Loc(m.group(1))
        
        fromLoc = getFromLoc(graph, Piece(playerColour, shape), toLoc)
    
    capStr = ''
    if capture:
        capStr = 'capture at '
        
    print('{} {} in {} to {}{}'.format(playerColour, shape, fromLoc, capStr, toLoc))
    if piece2 is not None:
        print('{} {} in {} to {}{}'.format(playerColour, piece2, fromLoc2, capStr, toLoc2))
    print('')
    
def addMadeBy(graph):
    hasFirstHalfMove = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#hasFirstHalfMove')
    madeBy = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#madeBy')
    nextHalfMove = URIRef('http://www.semanticweb.org/max/ontologies/2016/2/ontoChess#nextHalfMove')
    
    gameIDs = getIDs(graph)
    
    players = [Literal('white'), Literal('black')]
    playerPointer = 0

    for gameID in gameIDs:
        
        move = graph.value( subject=gameID, predicate=hasFirstHalfMove )
    
        while(move is not None):
            player = players[playerPointer]
            
            graph.add( (move, madeBy, player) )
            
            playerPointer = (playerPointer+1)%2
            
            move = graph.value(subject=move, predicate=nextHalfMove)
            
    return graph

def getThreats(graph, loc, shape):
    threatCandidates = []
    
    if shape == Shape('king'):
        pass
#     TODO
        
    threats = []
    
    return threats

def getFromLoc(graph, toLoc, piece):
    threats = getThreats(graph, toLoc, piece.shape)
    fromLoc = None
    
    for threat in threats:
        if piece.colour == threat.piece.colour:
            fromLoc = threat.loc
            
    return fromLoc

if __name__ == '__main__':
    graph = loadGames('C:/Users/Max/Documents/RO/ontoChess/ontoChess_res.ttl')
    graph = addHasHalfMove(graph)
    graph = addMadeBy(graph)
    graph = addGameState(graph)
    graph.serialize('C:/Users/Max/Documents/RO/ontoChess/ontoChess_test.ttl', format='turtle')

        