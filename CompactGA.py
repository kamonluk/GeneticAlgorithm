#
#   Standard import
#

import time
import shelve

from collections import OrderedDict

from math import floor, pow, isnan, log2

#
#   Local import
#

from YnxLog import ynxlog
from Globals import getEvaluateFunctionCount, resetEvaluateFunctionCount

#
#   Global variable
#

useDict = False
indexToPropCacheDict = {}


#
#   Function bodies
#

def generate_candidate_simple(vector):
    ''' Generate a new candidate solution based on the probability vector
    '''
    value = ""
    
    for p in vector:
        value += "0" if random() < p else "1"

    return Solution(value)

def generate_candidate(vectorList, valueSize):
    '''
    Generate a new candidate solution based on the probability vector
    '''
    valueList = []
    count = 0
    while (count < valueSize):
        value = ""   

        for p in vectorList[count]:
            value += "0" if random() < p else "1" #for_sphere
#            value += "1" if random() < p else "0"

        bitArrayValue = BitArray (bin = value)
   
        #if xi range for sphere model and step func: [-5.12, 5.12], rosenbrock func: [-2.048, 2.048]
        #if bitArrayValue.float < -2.048 or bitArrayValue.float > 2.048:
        if bitArrayValue.float < -5.12 or bitArrayValue.float > 5.12:
            continue
        
        if isnan(bitArrayValue.float):
            ynxlog( 0, 'WARNING!!!  candidate bitarray float is nan = {}'.format( bitArrayValue.bin ) )
            continue
            
        valueList.append(bitArrayValue)
          
        count += 1
    
    return Solution(valueList)

def generate_vector_simple(size):
    ''' Initializes a probability vector with given size
    '''  
    return [0.5] * size

def generate_vector(size, numGene):
    ''' Initializes a probability vector with given size
    '''  
    vectorList = []
    
    for i in range( numGene ):
        vector = [0.5]*size
        vectorList.append( vector )
    
    return vectorList

#waring MOVE THIS TO ProblemFunction when need to use
##def update_vector_onemax(vector, winner, loser, populationSize):
##    for i in range(len(vector)):
##        if winner[i] != loser[i]:
##            if winner[i] == '0':
##                vector[i] += 1.0 / float(populationSize)
##            else:
##                vector[i] -= 1.0 / float(populationSize)
##
##def update_vector_sphere(vectorList, winnerValue, loserValue, populationSize):
##    updateCount = 0
##    
##    for index, vector in enumerate( vectorList ):
##        winner = winnerValue[index].bin
##        loser = loserValue[index].bin
##        for i in range(len(vector)):
##            if winner[i] != loser[i]:
##
##                if( winner[i] == '0' ):
##                    vector[i] += 1.0 / float(populationSize)
##                       
##                else:
##                    vector[i] -= 1.0 / float(populationSize)
##
##        print ( 'update vector[{}] = {}'.format( index, vector) )
##           
##def update_vector_rosenbrock(vectorList, winnerValue, loserValue, populationSize):
##    updateCount = 0
##    BestBitArrayStr = '00111111100000000000000000000000'
##
##    for index, vector in enumerate( vectorList ):
##        winner = winnerValue[index].bin
##        loser = loserValue[index].bin
##        for i in range(len(vector)):
##            if winner[i] != loser[i]:
##
##                if( winner[i] == '1' and BestBitArrayStr[i] == '1' ):
##                    vector[i] += 1.0 / float(populationSize)
##                        
##                elif( winner[i] == '0' and BestBitArrayStr[i] == '0' ):
##                    vector[i] -= 1.0 / float(populationSize)
##
##        print ( 'update vector[{}] = {}'.format( index, vector) )
## 
##def update_vector_step(vectorList, winner, loser, populationSize):
##    updateCount = 0
##    winnerValue = winner.value
##    loserValue = loser.value
##    for index, vector in enumerate( vectorList ):
##        winner = winnerValue[index].bin
##        loser = loserValue[index].bin
##        for i in range(len(vector)):
##            if winner[i] != loser[i]:
##
##                if( winner[i] == '0' ):
##                    vector[i] += 1.0 / float(populationSize)
##                        
##                else:
##                    vector[i] -= 1.0 / float(populationSize)
##
##        print ( 'update vector[{}] = {}'.format( index, vector) )

def run( generations, size, populationSize,
         problemFunctionClass, numGene,
         maxNumBitInBlock, sample):
    ''' Run this compact GA 
    '''

    ynxlog( 0, 'run ...' )
    
    #
    #   Load prob vector
    #
    
    numBlock = int(size / maxNumBitInBlock)
    lastNumBit = size % maxNumBitInBlock
    vectorBlock = []     
    
    startTime = time.time()

    #   Open shelve to load vector
    shelveObj = shelve.open( '{}BitCandidate.shelve'.format( maxNumBitInBlock ) )    
    initializeBitVector = shelveObj['vector']
    shelveObj.close()
    
    for i in range(numBlock):
        
        vector = initializeBitVector
        vectorBlock.append(vector)

    if lastNumBit > 0:
        vectorBlock.append(generate_vector_trap(lastNumBit))     

    endTime = time.time()

    ynxlog( 1, '    gen vector time = {:.8f}'.format( endTime - startTime ) )
    
    #
    #   Set up before loop
    #   
    
    #   Open shelve to write result
#    shelveObj = shelve.open( '{}bit_{}pop_backup_sample{}.shelve'.format( size, populationSize, sample ) )

    #   Initialize variable
    sumTime = 0
    generationIndex = 0
    bestfitgen = -1
    best = None
    indexToPropCacheDictList = []
    
#warning Change to use this for loop until given generation number
    #for generationIndex in range(generations):    
    while ( True ):
    #for generationIndex in range(1):   
        
        startAllTime = time.time()

        #
        #   Generate candidate
        #
        
        startGenCanTime = startAllTime

        firstCandidate, secondCandidate = problemFunctionClass.generateCandidate(vectorBlock, maxNumBitInBlock, indexToPropCacheDictList)
        ynxlog( 1, ' first = {}, second = {}'.format( firstCandidate.value, secondCandidate.value ) ) 
        
        endGenCanTime = time.time()

        #
        #   Compute fitness
        #

        startCalFitTime = time.time()

        #   calculate fitness for each candidate
        firstCandidate.calculateFitness( problemFunctionClass.computeFitness )
        secondCandidate.calculateFitness( problemFunctionClass.computeFitness )

        endCalFitTime = time.time()

        #
        #   Compete and update the best candidate
        #

        startCompeteTime = time.time()
        
        #   let them compete, so we can know who is the best of the pair
        winner, loser = problemFunctionClass.compete( firstCandidate, secondCandidate )

        endCompeteTime = time.time()

        ynxlog( 2, ' winner = {}, loser = {}'.format( winner.value, loser.value ) )
        ynxlog( 0, ' winner fitness = {}, loser fitness = {}'.format( winner.fitness, loser.fitness ) )
        
        #   Update best candidate
        if best:
            best, winner = problemFunctionClass.compete( winner, best )            
        else:
            best = winner

        #
        #   Update probability vector
        #
        
        startUpVecTime = time.time()

        #   updates the probability vector based on the success of each bit
        problemFunctionClass.updateVector(vectorBlock, winner, loser, populationSize, maxNumBitInBlock)
        
        endUpVecTime = time.time()

        #
        #   Check result and print information
        #

        endAllTime = endUpVecTime
        sumTime += ( endAllTime - startAllTime )
        
        if( bestfitgen == -1 and winner.fitness == size ):
            bestfitgen = generationIndex + 1

        ynxlog( 1, '    gen candidate time = {}'.format( endGenCanTime - startGenCanTime ) )
        ynxlog( 1, '    cal fitness time = {}'.format( endCalFitTime - startCalFitTime ) )
        ynxlog( 1, '    compete time = {}'.format( endCompeteTime - startCompeteTime ) )
        ynxlog( 1, '    update vec time = {}'.format( endUpVecTime - startUpVecTime ) )
        ynxlog( 1, '    generation time = {}'.format( endAllTime - startAllTime ) )        
        ynxlog( 0, " sample: %d generation: %d best value: %s best fitness: %f" % ( sample + 1, generationIndex + 1, best, float(best.fitness)))
        ynxlog( 0, '    avg bin time = {}'.format( sumTime / ( generationIndex + 1 ) ) )
        ynxlog( 0, ' {} '.format( '='*50 ) )
        
        generationIndex += 1

        #   Stop if fitness is the best 
        #if( best.fitness == size ):
        #if( best.fitness == ( log2( size ) + 1 ) * size ):
        if( best.fitness == 7293 ):
        #if( best.fitness == ( ( log2( maxNumBitInBlock ) + 1 ) * maxNumBitInBlock ) * numBlock ):
            break

    #   Write result to shelve
    functEvalValue = getEvaluateFunctionCount()
##    shelveObj['EvaluateFunctionCount'] = functEvalValue
##    shelveObj['generation'] = generationIndex
##    shelveObj['vectorBlock'] = vectorBlock
##    shelveObj['bestValue'] = best.value
##    shelveObj.close()

    ynxlog( 1, 'best fitness found in gen = {} '.format( bestfitgen ) )
    ynxlog( 0, ' EvaluateFunctionCount = {}'.format( functEvalValue ) )
    
    #   Reset value after end this sample
    resetEvaluateFunctionCount()

    return functEvalValue
