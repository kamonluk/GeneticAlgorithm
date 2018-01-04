#
#   Standard import
#
import sys
import shelve
import math
#   Bokeh plot graph
#from bokeh.plotting import figure, output_file, show

#   Numpy
import numpy as np

#
#   Local import
#

import SimpleGA
import CompactGA
import ProblemFunction

from YnxLog import ynxlog

#
#   Helper function
#

def writeCandidateShelve( numBit, problemFunctionClass ):   
    ''' Generate candidate to dict and write to shelve
        For optimize generate candidate
    '''
    vector = problemFunctionClass.generateVector( numBit )
    shelveObj = shelve.open( '{}BitCandidate.shelve'.format( numBit ) )
    shelveObj['vector'] = vector
    shelveObj.close()

#
#   Main 
#
#print( math.average( [3,2] ) )
if __name__ == '__main__':

    #   Initialize value
    numBit = 8
    maxNumBitInBlock = 8
    numSample = 1
    populationSize = 100
    generations = 1000000
    numGene = 1

    #   Choose problem HERE
    problemClass = ProblemFunction.TSPOneMax
    
    #   Call write candidate to shelve
    writeCandidateShelve( maxNumBitInBlock, problemClass )
    #sys.exit( 0 )

    #   List for collect fucntion evaluation count
    #       ( list of integer )
    functEvalList = []
    
    #   Loop to generate result for each sample
    for sample in range( numSample ):

        argumentDict = { 'generations' : generations,
                         'size' : numBit,
                         'populationSize' : populationSize,
                         'problemFunctionClass' : problemClass,
                         'numGene' : numGene,
                         'maxNumBitInBlock' : maxNumBitInBlock,
                         'sample' : sample }
        
        fucntionEvaluationCount = CompactGA.run( **argumentDict )
        functEvalList.append( fucntionEvaluationCount )
    
    ynxlog( 0, ' AVERAGE = {}'.format( np.average( functEvalList ) ) )
    ynxlog( 0, functEvalList )
