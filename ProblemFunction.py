#
#   Standard import
#

from random import random

#
#   Local import
#


from YnxLog import ynxlog
from Globals import increaseEvaluateFunctionCount

#
#   Function bodies
#

def increaseEvaluateFunctionCountDecorator( function ):
    ''' To increase EvaluateFunctionCount
    '''   

    def increaseCountFunc( *args, **kwargs ):

        returnValue = function( *args, **kwargs )
        
        increaseEvaluateFunctionCount()
        
        return returnValue
    
    return increaseCountFunc

def binarySearch(objectList, target):
    lower = 0
    upper = len(objectList) - 1
    while lower < upper:   # use < instead of <=
        
        mid = lower + (upper - lower) // 2
        
        midObj = objectList[mid]
        val = midObj.prob
        
        if( upper - 1 == lower ):
          if( target < objectList[lower].prob ):
            return lower
          else:
            return upper
            
        if val > target:
          upper = mid
              
        elif val < target:
          lower = mid
#
#   Class definition
#

class Obj:
    def __init__(self, val, weight, prob ):
        self.val = val
        self.weight = weight
        self.prob = prob
    def __repr__(self):
        return 'val = {}, weight = {}, prob = {}'.format( self.val, self.weight, self.prob )
    
########################################
#   Solution
#

class Solution(object):
    ''' A solution for the given problem, it is composed of a binary value and its fitness value
    '''
    
    def __init__(self, value):
        self.value = value
        self.fitness = None
        
    def calculateFitness(self, fitnessFunction):
        self.fitness = fitnessFunction(self.value)
        
class SolutionForTrap(object):
    ''' A solution for the given problem, it is composed of a binary value and its fitness value
    '''
    
    def __init__(self, value, numBit, indexList):
        self.value = value
        self.fitness = None
        self.numBit = numBit
        self.indexList = indexList
        
    def calculateFitness(self, fitnessFunction):
        self.fitness = fitnessFunction(self.value)
        return 
        fitnessList = []
        valueBlockCount = int( len(self.value)/self.numBit )
        for i in range( valueBlockCount ):
            fitnessList.append( fitnessFunction(self.value[i * self.numBit: (i+1) * self.numBit] ) )
        if( len(self.value)%self.numBit > 0 ):
            fitnessList.append( fitnessFunction(self.value[valueBlockCount * self.numBit: ]) )
                         
        self.fitness = sum( fitnessList )

########################################
#   Base
#

class BaseProblemFunction( object ):

    @staticmethod    
    def computeFitness( inputBit ):
        raise NotImplemented( ' not implemented yet ' )

    @staticmethod
    def generateCandidate( vectorBlock, maxNumBitInBlock, indexToPropCacheDictList ):
        raise NotImplemented( ' not implemented yet ' )

    @staticmethod
    def generateVector( numBit ):
        raise NotImplemented( ' not implemented yet ' )
    
    @staticmethod
    def updateVector( vectorBlock, winnerValue, loserValue, populationSize, maxNumBitInBlock ):
        raise NotImplemented( ' not implemented yet ' )

########################################
#   SumOfBits
#

class SumOfBits( BaseProblemFunction ):

    @increaseEvaluateFunctionCountDecorator
    def computeFitness( bitStr ):
        ''' %bitStr% is '10100111010'
            return sum of bit that is '1'
        '''
        fitness = 0
        
        for bit in bitStr:
            if bit == '1':
               fitness += 1
       
        return fitness

########################################
#   Sphere
#

class Sphere( BaseProblemFunction ):

    @increaseEvaluateFunctionCountDecorator
    def computeFitness( bitStr ):
        ''' %bitArrayList% is list of BitArray
            return sum of sqr float from bitstr
        '''
        fitness = 0
        
        for bitArray in bitArrayList:
            fitness += ( bitArray.float**2 )
            
        return fitness

########################################
#   Rosenbrock
#

class Rosenbrock( BaseProblemFunction ):   

    @increaseEvaluateFunctionCountDecorator
    def computeFitness( bitArrayList ):
        ''' %bitArrayList% is list of BitArray
            return value compute from rosenbrock
        '''    
        ynxlog( 1, 'bitArrayList[0].float = {}'.format( bitArrayList[0].float ) )
        ynxlog( 1, 'bitArrayList[1].float = {}'.format( bitArrayList[1].float ) )
        
        firstComputeValue = bitArrayList[0].float*bitArrayList[0].float - bitArrayList[1].float
        ynxlog( 1, 'firstComputeValue = {}, pow = {}'.format( firstComputeValue, pow(firstComputeValue, 2)  ) )
        
        secondComputeValue = 1 - bitArrayList[0].float
        ynxlog( 1, 'secondComputeValue = {}, pow = {}'.format( secondComputeValue, pow(secondComputeValue, 2) ) )

        fitness = 100 * pow(firstComputeValue, 2) + pow(secondComputeValue, 2)
        
        return fitness

########################################
#   Step
#

class Step( BaseProblemFunction ):

    @increaseEvaluateFunctionCountDecorator
    def computeFitness( bitArrayList ):
        ''' %bitArrayList% is list of BitArray
            return value compute from floor of float value
        ''' 
        fitness = 0
        
        for bitArray in bitArrayList:
            tmp = floor( bitArray.float )
            if tmp >= 0:
                fitness += tmp
            else:
                fitness -= tmp
                
        return fitness

########################################
#   Hiff
#

#   t func
def transformFunc( firstBit, secondBit ):
    
    if( firstBit != secondBit 
        or firstBit == None ):
        return None
        
    return firstBit

#   T func
def hierarchyFunc( bitStr, numBlock ):
    
    if( bitStr == None or len( bitStr ) == 1 ):
        return bitStr

    strLength = len( bitStr )    

    bitPerBlock = int( strLength/numBlock )
    firstBlock = bitStr[:bitPerBlock]
    secondBlock = bitStr[bitPerBlock:]

    return transformFunc( hierarchyFunc( firstBlock, numBlock ), 
                          hierarchyFunc( secondBlock, numBlock ) )

#   f func
def fitnessFunc( bit ):
    
    if( bit == '1' or bit == '0' ):
        return 1
    else:
        return 0

#   F func
def getSumFitness( bitStr, numBlock ):
    
    if( bitStr == None or len( bitStr ) == 1 ):
        return fitnessFunc( bitStr )    

    strLength = len( bitStr )    

    bitPerBlock = int( strLength/numBlock )

    firstBlock = bitStr[:bitPerBlock]
    secondBlock = bitStr[bitPerBlock:]

    return len(bitStr) * fitnessFunc( hierarchyFunc(bitStr, numBlock) ) \
            + getSumFitness(firstBlock, numBlock) \
            + getSumFitness(secondBlock, numBlock)

class Hiff( BaseProblemFunction ):
    
    @increaseEvaluateFunctionCountDecorator
    def computeFitness( bitStr ):
        ''' %bitArrayList% is list of BitArray
            return value compute from floor of float value
        ''' 
        numBlock = 2 # k
        fitness = getSumFitness( bitStr, numBlock )
                
        return fitness

    def generateCandidate( vectorTupleList, maxNumBitInBlock, indexToPropCacheDictList ):

        fullBitResultValue1 = ''
        fullBitResultValue2 = ''
        indexList1 = []
        indexList2 = []
        for vectorIndex, vectorTuple in enumerate( vectorTupleList ):

            randomCandidate1 = random ()
            randomCandidate2 = random ()   
                 
            #ynxlog( 5, '    randomCandidate1 = {}'.format( randomCandidate1 ) )
            #ynxlog( 5, '    randomCandidate2 = {}'.format( randomCandidate2 ) )

            candidateIndex1 = binarySearch( vectorTuple, randomCandidate1 )
                
            candidateObject1 = vectorTuple[candidateIndex1]        
            fullBitResultValue1 += candidateObject1.val
            indexList1.append( candidateIndex1 )

            candidateIndex2 = binarySearch( vectorTuple, randomCandidate2 )
            
            candidateObject2 = vectorTuple[candidateIndex2]        
            fullBitResultValue2 += candidateObject2.val
            indexList2.append( candidateIndex2 )

        return SolutionForTrap(fullBitResultValue1, maxNumBitInBlock, indexList1), SolutionForTrap(fullBitResultValue2, maxNumBitInBlock, indexList2)

    def generateVector( numBit ):
    
        maxValue = int( pow( 2, numBit ) )
        DefaultProbValue = 1.0 / float (maxValue)
        valueObjectList = []
        blockValueToProbValueDict = dict()

        for value in range( maxValue ):        
            string = '{1:0{0:}b}'.format( numBit, value )
            
            valueObjectList.append( Obj( string, DefaultProbValue, ( value + 1 )/float( maxValue ) ) )
        
        ynxlog( 5, 'valueObjectList = {}'.format( valueObjectList ) )

        return tuple( valueObjectList )

    def updateVector( vectorBlockList, winner, loser, populationSize, maxNumBitInBlock ):

        for index, vectorBlock in enumerate( vectorBlockList ):
        
            winObjIndex = winner.indexList[index]        
            winObj = vectorBlock[winObjIndex]

            loseObjIndex = loser.indexList[index]
            loseObj = vectorBlock[loseObjIndex]

            startIndex = min( winObjIndex, loseObjIndex )
            endIndex = max( winObjIndex, loseObjIndex )
            
            sumProb = vectorBlock[startIndex].prob - vectorBlock[startIndex].weight
            
            transferVector = 1.0 / float(populationSize)
            
            if loseObj.weight < transferVector:            
                transferVector = loseObj.weight
           
            winObj.weight += transferVector
            loseObj.weight -= transferVector  
            
            for i in range( startIndex, endIndex + 1 ):
                sumProb += vectorBlock[i].weight
                vectorBlock[i].prob = sumProb

########################################
#   Trap
#

class Trap( BaseProblemFunction ):

    @increaseEvaluateFunctionCountDecorator
    def computeFitness( bitStr ):
        ''' %bitStr% is '10100111010'
            return value compute from trap problem
        '''
        fitness = 0
        oneCount = 0
        
        fitnessLow = len( bitStr ) - 1
        
        for bit in bitStr:
            if bit == '1':
                oneCount += 1

        #   If all bit is '1' then fitness is max ( numbit count )       
        if oneCount == len( bitStr ):
            fitness = float( oneCount )

        #   fitness is compute from max - 1 - one count
        else:
            fitness = fitnessLow - oneCount
            
        return fitness

    def generateCandidate( vectorTupleList, maxNumBitInBlock, indexToPropCacheDictList ):

        fullBitResultValue1 = ''
        fullBitResultValue2 = ''
        indexList1 = []
        indexList2 = []
        for vectorIndex, vectorTuple in enumerate( vectorTupleList ):

            randomCandidate1 = random ()
            randomCandidate2 = random ()   
                 
            #ynxlog( 5, '    randomCandidate1 = {}'.format( randomCandidate1 ) )
            #ynxlog( 5, '    randomCandidate2 = {}'.format( randomCandidate2 ) )

            candidateIndex1 = binarySearch( vectorTuple, randomCandidate1 )
                
            candidateObject1 = vectorTuple[candidateIndex1]        
            fullBitResultValue1 += candidateObject1.val
            indexList1.append( candidateIndex1 )

            candidateIndex2 = binarySearch( vectorTuple, randomCandidate2 )
            
            candidateObject2 = vectorTuple[candidateIndex2]        
            fullBitResultValue2 += candidateObject2.val
            indexList2.append( candidateIndex2 )

        return SolutionForTrap(fullBitResultValue1, maxNumBitInBlock, indexList1), SolutionForTrap(fullBitResultValue2, maxNumBitInBlock, indexList2)

    def generateVector( numBit ):
    
        maxValue = int( pow( 2, numBit ) )
        DefaultProbValue = 1.0 / float (maxValue)
        valueObjectList = []
        blockValueToProbValueDict = dict()

        for value in range( maxValue ):        
            string = '{1:0{0:}b}'.format( numBit, value )
            
            valueObjectList.append( Obj( string, DefaultProbValue, ( value + 1 )/float( maxValue ) ) )
        
        ynxlog( 5, 'valueObjectList = {}'.format( valueObjectList ) )

        return tuple( valueObjectList )

    def updateVector( vectorBlockList, winner, loser, populationSize, maxNumBitInBlock ):

        for index, vectorBlock in enumerate( vectorBlockList ):
        
            winObjIndex = winner.indexList[index]        
            winObj = vectorBlock[winObjIndex]

            loseObjIndex = loser.indexList[index]
            loseObj = vectorBlock[loseObjIndex]

            startIndex = min( winObjIndex, loseObjIndex )
            endIndex = max( winObjIndex, loseObjIndex )
            
            sumProb = vectorBlock[startIndex].prob - vectorBlock[startIndex].weight
            
            transferVector = 1.0 / float(populationSize)
            
            if loseObj.weight < transferVector:            
                transferVector = loseObj.weight
           
            winObj.weight += transferVector
            loseObj.weight -= transferVector  
            
            for i in range( startIndex, endIndex + 1 ):
                sumProb += vectorBlock[i].weight
                vectorBlock[i].prob = sumProb
            
