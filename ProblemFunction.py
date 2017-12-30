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

    @staticmethod
    def compete( firstCandidate, secondCandidate):
        ''' Returns a tuple with the winner solution
        '''
        if firstCandidate.fitness > secondCandidate.fitness:
            return firstCandidate, secondCandidate
        else:
            return secondCandidate, firstCandidate

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
    
        return [0.5] * numBit

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
#   TSP ( traversal salesman problem )
#      

class SolutionForTSP( object ):
    ''' A solution for the given problem, it is composed of a binary value and its fitness value
    '''
    
    def __init__(self, value):

        # note value is list of Route object
        self.value = value
        self.fitness = None
        
    def calculateFitness(self, fitnessFunction):
        self.fitness = fitnessFunction(self.value)

class Route():

    def __init__( self, index, leftTownName, rightTownName, prob, distance ):

        self.index = index
        self.leftTownName = leftTownName
        self.rightTownName = rightTownName
        self.distance = distance
        self.prob = prob
    
    def __repr__( self ):
        return ''# route ( {}{}, prob = {:.4f} ) '.format( self.leftTownName, self.rightTownName, self.prob )

class TSP( BaseProblemFunction ):

    #   Input mapping score
    ScoreList = [1] * 16

    @increaseEvaluateFunctionCountDecorator
    def computeFitness( routeList ):
        ''' %routeList% is list of route
            return value compute from trap problem
        '''
        fitness = 0
        for route in routeList:
            fitness += route.distance
        return fitness

    def compete( firstCandidate, secondCandidate):
        ''' Returns a tuple with the winner solution
        '''
        if firstCandidate.fitness < secondCandidate.fitness:
            return firstCandidate, secondCandidate
        else:
            return secondCandidate, firstCandidate
    
    @staticmethod
    def getRandomRouteList( routeList ):
        #   find start route
        sumProb = sum( [route.prob for route in routeList] )
        randomValue = random()

        
        countProb = 0
        for route in routeList:
            countProb += route.prob / sumProb 
            ynxlog( 1, ' randomValue = {}, countProb = {}'.format( randomValue, countProb) )
            if( randomValue < countProb ):                    
                return route
        raise KeyError( ' do not have candidate. WHY !!!!' )

    @staticmethod
    def getRouteListFromVectorList( vectorTupleList ):
        ''' 
        '''
        selectedRouteList = []
        inAndOutCityMappingDict = {}
        for chooseRoute, routeList in vectorTupleList[:-1]:
            
            blockRouteList = []
            routeWithoutZeroProbList = []
            for route in routeList:
                if( route.prob == 0 ):
                    continue
                routeWithoutZeroProbList.append( route )
            
            randomRoute = TSP.getRandomRouteList( routeWithoutZeroProbList )
            #randomRoute = vectorTupleList[-1][1][0]
            blockRouteList.append( randomRoute )

            #   Initialize for find next route
            firstCity = randomRoute.leftTownName
            lastCity = randomRoute.rightTownName
            currentCity = lastCity
            passedCitySet = set( [randomRoute.leftTownName] )
            
            ynxlog( 1, ' chooseRoute = {}, currentCity = {}'.format( chooseRoute, currentCity) )

            #   Loop to choose next route
            while( len( blockRouteList ) < chooseRoute ):
                
                validRouteList = []

                for route in routeList:

                    if( route.prob == 0 ):
                        continue
                    
                    routeCitySet = set( [route.rightTownName, route.leftTownName] )

                    ynxlog( 1, 'routeCitySet = {}, passedCitySet = {}, currentCity in routeCitySet = {}'.format( routeCitySet, passedCitySet, currentCity in routeCitySet ) )
                    ynxlog( 1, 'routeCitySet.difference( passedCitySet ) = {}'.format( routeCitySet.difference( passedCitySet ) ) ) 

                    #   Check route was connect with current city
                    #       and not connect to passed city
                    if( currentCity in routeCitySet
                        and routeCitySet.difference( passedCitySet ) == routeCitySet ):

                        #   Collect all valid route
                        validRouteList.append( route )
                        break
                    
                ynxlog( 1, 'validRoute = {} '.format( validRouteList ) )

                #   Generate next route
                randomNextRoute = TSP.getRandomRouteList( validRouteList )
                blockRouteList.append( randomNextRoute )

                #   Update passed city and current city
                passedCitySet.add( randomNextRoute )
                if( randomNextRoute.leftTownName == currentCity ):
                    currentCity = randomNextRoute.rightTownName
                    
                else:
                    currentCity = randomNextRoute.leftTownName

                lastCity = currentCity

            selectedRouteList.extend( blockRouteList )
            inAndOutCityMappingDict[firstCity] = lastCity
            inAndOutCityMappingDict[lastCity] = firstCity
        
        ynxlog( 1, ' inAndOutCityMappingDict = {} '.format( inAndOutCityMappingDict ) )

        #   Compute last block for route between block
        routeCount, routeBetweenBlockList = vectorTupleList[-1]
        
        ynxlog( 1, ' routeBetweenBlockList = {} '.format( routeBetweenBlockList ) )
        
        validRouteBetweenBlockList = []
        validCitySet = set(inAndOutCityMappingDict.keys())
        for route in routeBetweenBlockList:

            if( route.prob == 0 ):
                continue
                    
            if( route.rightTownName not in validCitySet 
                or route.leftTownName not in validCitySet ):
                continue
            validRouteBetweenBlockList.append( route )
                   
        randomRoute = TSP.getRandomRouteList( validRouteBetweenBlockList )
        blockRouteList = [randomRoute]

        ynxlog( 1, ' randomRoute = {} {} '.format( randomRoute.leftTownName, randomRoute.rightTownName ) )

        #   Initialize for find next route
        firstCity = inAndOutCityMappingDict[ randomRoute.leftTownName ]
        lastCity = inAndOutCityMappingDict[ randomRoute.rightTownName ]
        currentCity = lastCity
        passedCitySet = set( [ firstCity, randomRoute.leftTownName, randomRoute.rightTownName ] )

        while( len( blockRouteList ) < routeCount - 2 ):

            validRouteList = []

            for route in validRouteBetweenBlockList:
                routeCitySet = set( [route.rightTownName, route.leftTownName] )

                ynxlog( 1, 'routeCitySet = {}, passedCitySet = {}, currentCity in routeCitySet = {}'.format( routeCitySet, passedCitySet, currentCity in routeCitySet ) )
                ynxlog( 1, 'routeCitySet.difference( passedCitySet ) = {}'.format( routeCitySet.difference( passedCitySet ) ) ) 

                #   Check route was connect with current city
                #       and not connect to passed city
                if( currentCity in routeCitySet
                    and routeCitySet.difference( passedCitySet ) == routeCitySet ):

                    #   Collect all valid route
                    validRouteList.append( route )
                    break

            #   Generate next route
            randomNextRoute = TSP.getRandomRouteList( validRouteList )
            blockRouteList.append( randomNextRoute )

            #   Update passed city and current city
            passedCitySet.add( randomNextRoute.rightTownName )
            passedCitySet.add( randomNextRoute.leftTownName )

            if( randomNextRoute.leftTownName == currentCity ):
                currentCity = inAndOutCityMappingDict[ randomNextRoute.rightTownName ]
                    
            else:
                currentCity = inAndOutCityMappingDict[ randomNextRoute.leftTownName ]

            lastCity = currentCity
        
        for route in routeBetweenBlockList:
             routeCitySet = set( [route.rightTownName, route.leftTownName] )
             if( routeCitySet == set( [firstCity, lastCity] ) ):
                 blockRouteList.append( route )
        selectedRouteList.extend( blockRouteList )

        return selectedRouteList


    def generateCandidate( vectorTupleList, maxNumBitInBlock, indexToPropCacheDictList ):
        routeProbVectorList = vectorTupleList[0]
        firstRouteList = TSP.getRouteListFromVectorList( routeProbVectorList )
        secondRouteList = TSP.getRouteListFromVectorList( routeProbVectorList )
        ynxlog( 1, 'firstRouteList = {}'.format( firstRouteList ) )
        ynxlog( 1, 'secondRouteList = {}'.format( secondRouteList ) )
        return SolutionForTSP(firstRouteList), SolutionForTSP(secondRouteList)

    def generateVector( numBit ):
        ''' Create list of block [ ( routeCount, [ routeObject, routeObject,... ]),
                                   ( routeCount, [ routeObject, routeObject,... ]), ... ]
        '''
        numCity = 6
        numBlock = 2
        numCityInBlock = numCity / numBlock
        numRoute = ( numCity - 1 ) / 2 * ( numCity )
        baseProb = 1 / numRoute
        vectorList = [ ( 2, [ Route( index=0, leftTownName='1', rightTownName='2', prob=baseProb, distance=2 ),
                             Route( index=1, leftTownName='1', rightTownName='3', prob=baseProb, distance=1 ),
                             Route( index=2, leftTownName='2', rightTownName='3', prob=baseProb, distance=3 ) ] ),
                      ( 2, [ Route( index=3, leftTownName='4', rightTownName='5', prob=baseProb, distance=3 ),
                             Route( index=4, leftTownName='4', rightTownName='6', prob=baseProb, distance=2 ),
                             Route( index=5, leftTownName='5', rightTownName='6', prob=baseProb, distance=1 ) ] ),
                      ( 2, [ Route( index=6, leftTownName='1', rightTownName='4', prob=baseProb, distance=3 ),
                             Route( index=7, leftTownName='1', rightTownName='5', prob=baseProb, distance=3 ),
                             Route( index=8, leftTownName='1', rightTownName='6', prob=baseProb, distance=4 ),
                             Route( index=9, leftTownName='2', rightTownName='4', prob=baseProb, distance=4 ),
                             Route( index=10, leftTownName='2', rightTownName='5', prob=baseProb, distance=4 ),
                             Route( index=11, leftTownName='2', rightTownName='6', prob=baseProb, distance=4 ),
                             Route( index=12, leftTownName='3', rightTownName='4', prob=baseProb, distance=3 ),
                             Route( index=13, leftTownName='3', rightTownName='5', prob=baseProb, distance=3 ),
                             Route( index=14, leftTownName='3', rightTownName='6', prob=baseProb, distance=3 ) ] ) ]

        #vectorList = [ ( 5, [ Route( index=0, leftTownName='1', rightTownName='2', prob=baseProb, distance=2 ),                             
        #                     Route( index=2, leftTownName='2', rightTownName='3', prob=baseProb, distance=3 ),
        #                     Route( index=3, leftTownName='4', rightTownName='5', prob=baseProb, distance=3 ),
        #                     Route( index=4, leftTownName='4', rightTownName='6', prob=baseProb, distance=2 ),
        #                     Route( index=5, leftTownName='5', rightTownName='6', prob=baseProb, distance=1 ),
        #                     Route( index=6, leftTownName='1', rightTownName='4', prob=baseProb, distance=3 ),
        #                     Route( index=7, leftTownName='1', rightTownName='5', prob=baseProb, distance=3 ),
        #                     Route( index=8, leftTownName='1', rightTownName='6', prob=baseProb, distance=4 ),
        #                     Route( index=9, leftTownName='2', rightTownName='4', prob=baseProb, distance=4 ),
        #                     Route( index=10, leftTownName='2', rightTownName='5', prob=baseProb, distance=4 ),
        #                     Route( index=11, leftTownName='2', rightTownName='6', prob=baseProb, distance=4 ),
        #                     Route( index=12, leftTownName='3', rightTownName='4', prob=baseProb, distance=3 ),
        #                     Route( index=13, leftTownName='3', rightTownName='5', prob=baseProb, distance=3 ),
        #                     Route( index=14, leftTownName='3', rightTownName='6', prob=baseProb, distance=3 ) ] ),
        #              ( 1, [ Route( index=1, leftTownName='1', rightTownName='3', prob=baseProb, distance=1 ) ] ) ]

        return vectorList

    def updateVector( vectorBlockList, winner, loser, populationSize, maxNumBitInBlock ):
        ''' Get all winner, loser routeList by find difference index between winner solution and loser solution                
        '''
        assert( len( winner.value ) == len( loser.value ) ), ' route are not equal :: winner( {} ) != loser( {} )'.format( len( winner.value ), len( loser.value ) )
        winnerRouteList = winner.value
        loserRouteList = loser.value

        winnerRouteIndexList =  [ route.index for route in winnerRouteList ]
        loserRouteIndexList =  [ route.index for route in loserRouteList ]

        ynxlog( 1, ' winner route index = {} '.format( winnerRouteIndexList ) )
        ynxlog( 1, ' loser route index = {} '.format( loserRouteIndexList ) )

        
            
        #   Loop to update prob in route
        for index in range( len( winnerRouteList ) ):

            winnerRoute = winnerRouteList[index]
            loserRoute = loserRouteList[index]

            #   Compute transfer prob
            transferProb = 1.0 / float(populationSize)

            #   clamp to minimum prob
            if( transferProb > loserRoute.prob ):
                transferProb = loserRoute.prob
            
            #   Update probility
            winnerRoute.prob += transferProb
            loserRoute.prob -= transferProb
        
        allRouteList = []
        for count, routeList in  vectorBlockList[0]:
            allRouteList.extend( routeList )
        #ynxlog( 0, ' allRouteList = {}'.format( allRouteList ) )
        #ynxlog( 0, ' sum = {}'.format( sum([route.prob for route in allRouteList ]) ) )

