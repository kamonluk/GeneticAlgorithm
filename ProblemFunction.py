#
#   Standard import
#

from random import random
import time
import math
#
#   Local import
#


from YnxLog import ynxlog
from Globals import increaseEvaluateFunctionCount

#
#   Function bodies
#

INFINITY = float( 'inf' )

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
            return sum of bit that is 'A'
        '''
        fitness = 0
        
        for bit in bitStr:
            if bit == 'A':
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
    
    if( bit == 'A' or bit == '0' ):
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
            if bit == 'A':
                oneCount += 1

        #   If all bit is 'A' then fitness is max ( numbit count )       
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

def getFirstLoopList( routeList ):

    if( len( routeList ) == 0 ):
        return []

    firstLoopRouteList = []
    remainCitySet = set(routeList[0:])

    currentCity = routeList[0].rightTownName
    firstCity = routeList[0].leftTownName

    while( currentCity != firstCity ):

        for route in routeList:

            if( route.leftTownName == currentCity ):
                currentCity = route.rightTownName                
                firstLoopRouteList.append( route )
                break
                
            elif( route.rightTownName == currentCity ):
                currentCity = route.leftTownName                
                firstLoopRouteList.append( route )
                break
        
    return firstLoopRouteList
    
def isValidLoopRoute( routeList, numCity ):
    ''' Check all route is one loop
    '''
    return len( getFirstLoopList( routeList ) ) == numCity

class SolutionForTSP( object ):
    ''' A solution for the given problem, it is composed of a binary value and its fitness value
    '''
    
    def __init__(self, value):

        # note value is list of Route object
        self.value = value
        self.fitness = None
        
    def calculateFitness(self, fitnessFunction):
        self.fitness = fitnessFunction(self.value)
        
    def __repr__( self ):
        
        if( len( self.value ) == 0 ):
            return ' empty list '

        routeStrList = []
        remainCitySet = set(self.value[0:])

        currentCity = self.value[0].rightTownName
        
        while( len( routeStrList ) != len( self.value ) ):
            
            for route in remainCitySet:

                if( route.leftTownName == currentCity ):
                    currentCity = route.rightTownName
                    remainCitySet = remainCitySet.difference( set([route]) )
                    routeStrList.append( currentCity )
                    break
                    
                elif( route.rightTownName == currentCity ):
                    currentCity = route.leftTownName
                    remainCitySet = remainCitySet.difference( set([route]) )
                    routeStrList.append( currentCity )
                    break
            
        routeStrList = [self.value[0].rightTownName] + routeStrList
        return ' --> '.join( routeStrList )
        
class Route():

    def __init__( self, index, leftTownName, rightTownName, prob, distance ):

        self.index = index
        self.leftTownName = leftTownName
        self.rightTownName = rightTownName
        self.distance = distance
        self.prob = prob
    
    def __repr__( self ):
        return ' ( {} <--> {} ) {} '.format( self.leftTownName, self.rightTownName, self.prob )

class TSP( BaseProblemFunction ):

    NumCity = 13
    
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
        ynxlog( 1, ' sumProb = {}'.format( sumProb ) )        
        countProb = 0
        for route in routeList:
            countProb += route.prob / sumProb 
            ynxlog( 1, ' randomValue = {}, countProb = {}'.format( randomValue, countProb) )
            if( randomValue < countProb ):
                ynxlog( 1, ' choose route = {}<-->{}'.format( route.leftTownName, route.rightTownName ) )
                return route
        raise KeyError( ' do not have candidate. WHY !!!!' )

    @staticmethod
    def getRouteListFromVectorList( vectorTupleList ):
        ''' 
        '''
        allRouteList = []
        for count, routeList in vectorTupleList:
            allRouteList.extend( routeList )
        debugStr = ''
        ynxlog( 1, ' ***** all route prob graph ***** ' )
        graphRatio = 0.01
        for allRoute in allRouteList:
            #debugStr += ' ({}{},{:.2f})'.format( allRoute.leftTownName, allRoute.rightTownName, allRoute.prob  )            
            ynxlog( 1, ' {}{} = {}'.format( allRoute.leftTownName, allRoute.rightTownName, '||'* int( allRoute.prob/graphRatio ) ) )
        #ynxlog( 0, ' allRouteList = {}'.format( debugStr ) )
        #ynxlog( 0, ' allRouteList = {}'.format( allRouteList ) )
        #ynxlog( 0, ' sum = {}'.format( sum([route.prob for route in allRouteList ]) ) )
            
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
            #currentCity = lastCity
            passedCitySet = set([])
                
            ynxlog( 1, ' chooseRoute = {}, firstCity = {}, lastCity = {}'.format( chooseRoute, firstCity, lastCity) )

            #   Loop to choose next route
            while( len( blockRouteList ) < chooseRoute ):
                
                validRouteList = []

                for route in routeList:

                    #   Skip route that prob is zero
                    if( route.prob == 0 ):
                        continue
                    
                    routeCitySet = set( [route.rightTownName, route.leftTownName] )

                    ynxlog( 1, 'routeCitySet = {}, passedCitySet = {}'.format( routeCitySet, passedCitySet ) )
                    ynxlog( 1, 'routeCitySet.difference( passedCitySet ) = {}'.format( routeCitySet.difference( passedCitySet ) ) ) 

                    #   Skip close loop route
                    if( firstCity in routeCitySet and lastCity in routeCitySet ):
                        continue
                        
                    #   Check route was connect with current city
                    #       and not connect to passed city
                    if( ( firstCity in routeCitySet or lastCity in routeCitySet )
                        and routeCitySet.difference( passedCitySet ) == routeCitySet ):

                        #   Collect all valid route
                        validRouteList.append( route )                        
                    
                ynxlog( 1, 'validRoute = {} '.format( validRouteList ) )

                #   Generate next route
                randomNextRoute = TSP.getRandomRouteList( validRouteList )
                blockRouteList.append( randomNextRoute )

                
                #   Change next city and update passed city and current city
                if( randomNextRoute.leftTownName == firstCity ):
                    firstCity = randomNextRoute.rightTownName
                    passedCitySet.add( randomNextRoute.leftTownName )
                                    
                elif( randomNextRoute.rightTownName == firstCity ):
                    firstCity = randomNextRoute.leftTownName
                    passedCitySet.add( randomNextRoute.rightTownName )
                    
                elif( randomNextRoute.leftTownName == lastCity ):
                    lastCity = randomNextRoute.rightTownName
                    passedCitySet.add( randomNextRoute.leftTownName )
                    
                elif( randomNextRoute.rightTownName == lastCity ):
                    lastCity = randomNextRoute.leftTownName
                    passedCitySet.add( randomNextRoute.rightTownName )
                    
                else:
                    assert( False ), 'Impossible !!!'

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

        while( len( blockRouteList ) < routeCount - 1 ):

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

        if( routeCount > 1 ):
            for route in routeBetweenBlockList:
                 routeCitySet = set( [route.rightTownName, route.leftTownName] )
                 if( routeCitySet == set( [firstCity, lastCity] ) ):
                     blockRouteList.append( route )
        
        selectedRouteList.extend( blockRouteList )
            
        return selectedRouteList

    def generateCandidate( vectorTupleList, maxNumBitInBlock, indexToPropCacheDictList ):
        routeProbVectorList = vectorTupleList[0]

        while( True ):

            try:
                firstRouteList = TSP.getRouteListFromVectorList( routeProbVectorList )
                secondRouteList = TSP.getRouteListFromVectorList( routeProbVectorList )
                break
            except KeyError:
                ynxlog( 0, ' KeyError, cannot gen route' )
        ynxlog( 1, 'firstRouteList = {}'.format( firstRouteList ) )
        ynxlog( 1, 'secondRouteList = {}'.format( secondRouteList ) )
        return SolutionForTSP(firstRouteList), SolutionForTSP(secondRouteList)

    def generateVector( numBit ):
        ''' Create list of block [ ( routeCount, [ routeObject, routeObject,... ]),
                                   ( routeCount, [ routeObject, routeObject,... ]), ... ]
        '''
        numCity = TSP.NumCity
        numBlock = 2
        numCityInBlock = numCity / numBlock
        numRoute = ( numCity - 1 ) / 2 * ( numCity )
        baseProb = 1 / numRoute

        cityNameList = [ 'New York', 'Los Angeles', 'Chicago', 'Minneapolis', 'Denver',
                         'Dallas', 'Seattle', 'Boston', 'San Francisco', 'St. Louis', 'Houston',
                         'Phoenix', 'Salt Lake City' ]
        block1CityName = [ 'New York', 'Boston', 'Chicago', 'Minneapolis' ]
        block2CityName = [ 'Denver', 'Salt Lake City', 'Seattle', 'San Francisco', 'Los Angeles' ]
        block3CityName = [ 'Phoenix', 'Houston', 'Dallas', 'St. Louis' ]
        distanceList = [
                    [   0, 2451,  713, 1018, 1631, 1374, 2408,  213, 2571,  875, 1420, 2145, 1972], # New York
                    [2451,    0, 1745, 1524,  831, 1240,  959, 2596,  403, 1589, 1374,  357,  579], # Los Angeles
                    [ 713, 1745,    0,  355,  920,  803, 1737,  851, 1858,  262,  940, 1453, 1260], # Chicago
                    [1018, 1524,  355,    0,  700,  862, 1395, 1123, 1584,  466, 1056, 1280,  987], # Minneapolis
                    [1631,  831,  920,  700,    0,  663, 1021, 1769,  949,  796,  879,  586,  371], # Denver
                    [1374, 1240,  803,  862,  663,    0, 1681, 1551, 1765,  547,  225,  887,  999], # Dallas
                    [2408,  959, 1737, 1395, 1021, 1681,    0, 2493,  678, 1724, 1891, 1114,  701], # Seattle
                    [ 213, 2596,  851, 1123, 1769, 1551, 2493,    0, 2699, 1038, 1605, 2300, 2099], # Boston
                    [2571,  403, 1858, 1584,  949, 1765,  678, 2699,    0, 1744, 1645,  653,  600], # San Francisco
                    [ 875, 1589,  262,  466,  796,  547, 1724, 1038, 1744,    0,  679, 1272, 1162], # St. Louis
                    [1420, 1374,  940, 1056,  879,  225, 1891, 1605, 1645,  679,    0, 1017, 1200], # Houston
                    [2145,  357, 1453, 1280,  586,  887, 1114, 2300,  653, 1272, 1017,    0,  504], # Phoenix
                    [1972,  579, 1260,  987,  371,  999,  701, 2099,  600, 1162,  1200,  504,   0]] # Salt Lake City

        allCityRouteList = []
        index = 0
        for i in range( len( cityNameList ) - 1 ):
            leftCityName = cityNameList[i]
            
            for j in range( i + 1, len( cityNameList ) ):
                rightCityName = cityNameList[j]
                distance = distanceList[i][j]
                route = Route( index, leftCityName, rightCityName, baseProb, distance )
                allCityRouteList.append( route )

        allRouteSet = set( allCityRouteList )
        firstBlockRouteList = []
        secondBlockRouteList = []
        thirdBlockRouteList = []
        for allRoute in allRouteSet:
            if( allRoute.leftTownName in block1CityName
                and allRoute.rightTownName in block1CityName ):
                firstBlockRouteList.append( allRoute )

        allRouteSet = allRouteSet.difference( set(firstBlockRouteList) )
        
        for allRoute in allRouteSet:
            if( allRoute.leftTownName in block2CityName
                and allRoute.rightTownName in block2CityName ):
                secondBlockRouteList.append( allRoute )

        allRouteSet = allRouteSet.difference( set(secondBlockRouteList) )
        
        for allRoute in allRouteSet:
            if( allRoute.leftTownName in block3CityName
                and allRoute.rightTownName in block3CityName ):
                thirdBlockRouteList.append( allRoute )

        allRouteSet = allRouteSet.difference( set(thirdBlockRouteList) )
                
        ynxlog( 3, ' length = {}'.format( len(allCityRouteList) ) )
##        vectorList = [ ( len( cityNameList ) - 1, allCityRouteList ),
##                       ( 1, allCityRouteList ) ]
        vectorList = [ ( 3, firstBlockRouteList ),
                       ( 4, secondBlockRouteList ),
                       ( 3, thirdBlockRouteList ),
                       ( 3, list( allRouteSet ) ) ]
        
        ynxlog( 3, ' vectorList = {}'.format( vectorList ) )
##        vectorList = [ ( 2, [ Route( index=0, leftTownName='A', rightTownName='B', prob=baseProb, distance=2 ),
##                             Route( index=1, leftTownName='A', rightTownName='C', prob=baseProb, distance=1 ),
##                             Route( index=2, leftTownName='B', rightTownName='C', prob=baseProb, distance=3 ) ] ),
##                      ( 2, [ Route( index=3, leftTownName='D', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=4, leftTownName='D', rightTownName='F', prob=baseProb, distance=2 ),
##                             Route( index=5, leftTownName='E', rightTownName='F', prob=baseProb, distance=1 ) ] ),
##                      ( 2, [ Route( index=6, leftTownName='A', rightTownName='D', prob=baseProb, distance=3 ),
##                             Route( index=7, leftTownName='A', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=8, leftTownName='A', rightTownName='F', prob=baseProb, distance=4 ),
##                             Route( index=9, leftTownName='B', rightTownName='D', prob=baseProb, distance=4 ),
##                             Route( index=10, leftTownName='B', rightTownName='E', prob=baseProb, distance=4 ),
##                             Route( index=11, leftTownName='B', rightTownName='F', prob=baseProb, distance=5 ),
##                             Route( index=12, leftTownName='C', rightTownName='D', prob=baseProb, distance=4 ),
##                             Route( index=13, leftTownName='C', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=14, leftTownName='C', rightTownName='F', prob=baseProb, distance=4 ) ] ) ]

##        vectorList = [ ( 5, [ Route( index=0, leftTownName='A', rightTownName='B', prob=baseProb, distance=2 ),
##                             Route( index=1, leftTownName='A', rightTownName='C', prob=baseProb, distance=1 ),
##                             Route( index=2, leftTownName='B', rightTownName='C', prob=baseProb, distance=3 ),
##                             Route( index=3, leftTownName='D', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=4, leftTownName='D', rightTownName='F', prob=baseProb, distance=2 ),
##                             Route( index=5, leftTownName='E', rightTownName='F', prob=baseProb, distance=1 ),
##                             Route( index=6, leftTownName='A', rightTownName='D', prob=baseProb, distance=3 ),
##                             Route( index=7, leftTownName='A', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=8, leftTownName='A', rightTownName='F', prob=baseProb, distance=4 ),
##                             Route( index=9, leftTownName='B', rightTownName='D', prob=baseProb, distance=4 ),
##                             Route( index=10, leftTownName='B', rightTownName='E', prob=baseProb, distance=4 ),
##                             Route( index=11, leftTownName='B', rightTownName='F', prob=baseProb, distance=5 ),
##                             Route( index=12, leftTownName='C', rightTownName='D', prob=baseProb, distance=4 ),
##                             Route( index=13, leftTownName='C', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=14, leftTownName='C', rightTownName='F', prob=baseProb, distance=4 ) ] ),
##                        ( 1, [ Route( index=0, leftTownName='A', rightTownName='B', prob=baseProb, distance=2 ),
##                             Route( index=1, leftTownName='A', rightTownName='C', prob=baseProb, distance=1 ),
##                             Route( index=2, leftTownName='B', rightTownName='C', prob=baseProb, distance=3 ),
##                             Route( index=3, leftTownName='D', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=4, leftTownName='D', rightTownName='F', prob=baseProb, distance=2 ),
##                             Route( index=5, leftTownName='E', rightTownName='F', prob=baseProb, distance=1 ),
##                             Route( index=6, leftTownName='A', rightTownName='D', prob=baseProb, distance=3 ),
##                             Route( index=7, leftTownName='A', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=8, leftTownName='A', rightTownName='F', prob=baseProb, distance=4 ),
##                             Route( index=9, leftTownName='B', rightTownName='D', prob=baseProb, distance=4 ),
##                             Route( index=10, leftTownName='B', rightTownName='E', prob=baseProb, distance=4 ),
##                             Route( index=11, leftTownName='B', rightTownName='F', prob=baseProb, distance=5 ),
##                             Route( index=12, leftTownName='C', rightTownName='D', prob=baseProb, distance=4 ),
##                             Route( index=13, leftTownName='C', rightTownName='E', prob=baseProb, distance=3 ),
##                             Route( index=14, leftTownName='C', rightTownName='F', prob=baseProb, distance=4 ) ] )
##                       ]
        
        #vectorList = [ ( 5, [ Route( index=0, leftTownName='A', rightTownName='B', prob=baseProb, distance=2 ),                             
        #                     Route( index=2, leftTownName='B', rightTownName='C', prob=baseProb, distance=3 ),
        #                     Route( index=3, leftTownName='D', rightTownName='E', prob=baseProb, distance=3 ),
        #                     Route( index=4, leftTownName='D', rightTownName='F', prob=baseProb, distance=2 ),
        #                     Route( index=5, leftTownName='E', rightTownName='F', prob=baseProb, distance=1 ),
        #                     Route( index=6, leftTownName='A', rightTownName='D', prob=baseProb, distance=3 ),
        #                     Route( index=7, leftTownName='A', rightTownName='E', prob=baseProb, distance=3 ),
        #                     Route( index=8, leftTownName='A', rightTownName='F', prob=baseProb, distance=4 ),
        #                     Route( index=9, leftTownName='B', rightTownName='D', prob=baseProb, distance=4 ),
        #                     Route( index=10, leftTownName='B', rightTownName='E', prob=baseProb, distance=4 ),
        #                     Route( index=11, leftTownName='B', rightTownName='F', prob=baseProb, distance=4 ),
        #                     Route( index=12, leftTownName='C', rightTownName='D', prob=baseProb, distance=3 ),
        #                     Route( index=13, leftTownName='C', rightTownName='E', prob=baseProb, distance=3 ),
        #                     Route( index=14, leftTownName='C', rightTownName='F', prob=baseProb, distance=3 ) ] ),
        #              ( 1, [ Route( index=1, leftTownName='A', rightTownName='C', prob=baseProb, distance=1 ) ] ) ]

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

########################################
#   TSP One max ( traversal salesman problem )
#      

class SolutionForTSPOneMax( SolutionForTSP ):
    ''' A solution for the given problem, it is composed of a binary value and its fitness value
    '''
    def __init__(self, value):
        SolutionForTSP.__init__( self, value )

    def __repr__( self ):

        numRoute = int( ( TSPOneMax.NumCity - 1 ) / 2 * ( TSPOneMax.NumCity ) )
        bitStrList = ['0'] * numRoute
        for route in self.value:
            bitStrList[route.index] = '1'

        reprStr = ''.join( bitStrList )

        if( not math.isinf( self.fitness ) ):
            reprStr += ' route = '
            reprStr += SolutionForTSP.__repr__( self )
        return reprStr
        
class TSPOneMax( BaseProblemFunction ):

    NumCity = 6
    
    @increaseEvaluateFunctionCountDecorator
    def computeFitness( routeList ):
        ''' %routeList% is list of route
            return value compute from trap problem
        '''

        #   For onemax, if route count was equal to num city ( invalid route selection )
        #       make fitness to INFINITY
        if( len( routeList ) != TSPOneMax.NumCity ):
            return INFINITY

        cityNameToCountDict = {}
        
        for route in routeList:

            if( route.leftTownName not in cityNameToCountDict ):
                cityNameToCountDict[ route.leftTownName ] = 1
            else:
                cityNameToCountDict[ route.leftTownName ] += 1
                
            if( route.rightTownName not in cityNameToCountDict ):
                cityNameToCountDict[ route.rightTownName ] = 1
            else:
                cityNameToCountDict[ route.rightTownName ] += 1
                
        #   For onemaax if route value make a loop ( invalid route selection )
        #       make fitness to INFINITY
        for routeCount in cityNameToCountDict.values():
            if( routeCount != 2 ):
                return INFINITY

        #   Check valid loop
        if( not isValidLoopRoute( routeList, TSPOneMax.NumCity ) ):
            return INFINITY
            
        #   Sum distance for route
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

    def generateCandidate( vectorTupleList, maxNumBitInBlock, indexToPropCacheDictList ):
        
        routeProbVectorList = vectorTupleList[0]
        firstRouteList = []
        secondRouteList = []
        for routeProbVector in routeProbVectorList:
            randomValue1 = random()
            randomValue2 = random()
            if( randomValue1 < routeProbVector.prob ):
                firstRouteList.append( routeProbVector )
            if( randomValue2 < routeProbVector.prob ):
                secondRouteList.append( routeProbVector )
        return SolutionForTSPOneMax(firstRouteList), SolutionForTSPOneMax(secondRouteList)

    def generateVector( numBit ):
        ''' Create list of block [ ( routeCount, [ routeObject, routeObject,... ]),
                                   ( routeCount, [ routeObject, routeObject,... ]), ... ]
        '''
        numCity = TSPOneMax.NumCity
        numBlock = 2
        numCityInBlock = numCity / numBlock
        numRoute = ( numCity - 1 ) / 2 * ( numCity )
        baseProb = 0.5

        cityNameList = [ 'New York', 'Los Angeles', 'Chicago', 'Minneapolis', 'Denver',
                         'Dallas', 'Seattle', 'Boston', 'San Francisco', 'St. Louis', 'Houston',
                         'Phoenix', 'Salt Lake City' ]
        block1CityName = [ 'New York', 'Boston', 'Chicago', 'Minneapolis' ]
        block2CityName = [ 'Denver', 'Salt Lake City', 'Seattle', 'San Francisco', 'Los Angeles' ]
        block3CityName = [ 'Phoenix', 'Houston', 'Dallas', 'St. Louis' ]
        distanceList = [
                    [   0, 2451,  713, 1018, 1631, 1374, 2408,  213, 2571,  875, 1420, 2145, 1972], # New York
                    [2451,    0, 1745, 1524,  831, 1240,  959, 2596,  403, 1589, 1374,  357,  579], # Los Angeles
                    [ 713, 1745,    0,  355,  920,  803, 1737,  851, 1858,  262,  940, 1453, 1260], # Chicago
                    [1018, 1524,  355,    0,  700,  862, 1395, 1123, 1584,  466, 1056, 1280,  987], # Minneapolis
                    [1631,  831,  920,  700,    0,  663, 1021, 1769,  949,  796,  879,  586,  371], # Denver
                    [1374, 1240,  803,  862,  663,    0, 1681, 1551, 1765,  547,  225,  887,  999], # Dallas
                    [2408,  959, 1737, 1395, 1021, 1681,    0, 2493,  678, 1724, 1891, 1114,  701], # Seattle
                    [ 213, 2596,  851, 1123, 1769, 1551, 2493,    0, 2699, 1038, 1605, 2300, 2099], # Boston
                    [2571,  403, 1858, 1584,  949, 1765,  678, 2699,    0, 1744, 1645,  653,  600], # San Francisco
                    [ 875, 1589,  262,  466,  796,  547, 1724, 1038, 1744,    0,  679, 1272, 1162], # St. Louis
                    [1420, 1374,  940, 1056,  879,  225, 1891, 1605, 1645,  679,    0, 1017, 1200], # Houston
                    [2145,  357, 1453, 1280,  586,  887, 1114, 2300,  653, 1272, 1017,    0,  504], # Phoenix
                    [1972,  579, 1260,  987,  371,  999,  701, 2099,  600, 1162,  1200,  504,   0]] # Salt Lake City

        allCityRouteList = []
        index = 0
        for i in range( len( cityNameList ) - 1 ):
            leftCityName = cityNameList[i]
            
            for j in range( i + 1, len( cityNameList ) ):
                rightCityName = cityNameList[j]
                distance = distanceList[i][j]
                route = Route( index, leftCityName, rightCityName, baseProb, distance )
                allCityRouteList.append( route )

        vectorList = allCityRouteList
        
        ynxlog( 3, ' vectorList = {}'.format( vectorList ) )

        vectorList = [ Route( index=0, leftTownName='A', rightTownName='B', prob=baseProb, distance=2 ),
                     Route( index=1, leftTownName='A', rightTownName='C', prob=baseProb, distance=1 ),
                     Route( index=2, leftTownName='B', rightTownName='C', prob=baseProb, distance=3 ),
                     Route( index=3, leftTownName='D', rightTownName='E', prob=baseProb, distance=3 ),
                     Route( index=4, leftTownName='D', rightTownName='F', prob=baseProb, distance=2 ),
                     Route( index=5, leftTownName='E', rightTownName='F', prob=baseProb, distance=1 ),
                     Route( index=6, leftTownName='A', rightTownName='D', prob=baseProb, distance=3 ),
                     Route( index=7, leftTownName='A', rightTownName='E', prob=baseProb, distance=3 ),
                     Route( index=8, leftTownName='A', rightTownName='F', prob=baseProb, distance=4 ),
                     Route( index=9, leftTownName='B', rightTownName='D', prob=baseProb, distance=4 ),
                     Route( index=10, leftTownName='B', rightTownName='E', prob=baseProb, distance=4 ),
                     Route( index=11, leftTownName='B', rightTownName='F', prob=baseProb, distance=5 ),
                     Route( index=12, leftTownName='C', rightTownName='D', prob=baseProb, distance=4 ),
                     Route( index=13, leftTownName='C', rightTownName='E', prob=baseProb, distance=3 ),
                     Route( index=14, leftTownName='C', rightTownName='F', prob=baseProb, distance=4 ) ]
        
        return vectorList

    def updateVector( vectorBlockList, winner, loser, populationSize, maxNumBitInBlock ):
        ''' Get all winner, loser routeList by find difference index between winner solution and loser solution                
        '''
        winnerRouteList = winner.value
        loserRouteList = loser.value

        winnerRouteIndexList =  [ route.index for route in winnerRouteList ]
        loserRouteIndexList =  [ route.index for route in loserRouteList ]

        ynxlog( 1, ' winner route index = {} '.format( winnerRouteIndexList ) )
        ynxlog( 1, ' loser route index = {} '.format( loserRouteIndexList ) )

        #   Compute transfer prob
        transferProb = 1.0 / float(populationSize)
            
        #   Loop to update prob in route
        for winnerRoute in winnerRouteList:
            
            #   Update probility
            winnerRoute.prob = min( 1.0, winnerRoute.prob + transferProb )

        #   Loop to update prob in route
        for loserRoute in loserRouteList:
            
            #   Update probility
            loserRoute.prob = max( 0.0, loserRoute.prob - transferProb )

        ynxlog( 0, ' allRouteList = {}'.format( vectorBlockList[0] ) )
##        ynxlog( 0, ' sum = {}'.format( sum([route.prob for route in allRouteList ]) ) )



