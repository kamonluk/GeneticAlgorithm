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
    shelveObj = shelve.open( 'data/{}BitCandidate_{}.shelve'.format( numBit, problemFunctionClass.Name ) )    
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
    numSample = 5
    populationSize = 10
    populationSizeList = [10,100,500,1000,2000,5000,10000,12000,15000,20000]#range( 500, 501, 10 )
    #populationSizeList = [4]
    generations = 10000
    numGene = 1
    doInfGen = False
    
    #   Choose problem HERE
    problemClass = ProblemFunction.TSPOneMax
    
    #   Call write candidate to shelve
    writeCandidateShelve( maxNumBitInBlock, problemClass )

    #   List for collect fucntion evaluation count
    #       ( list of integer )
    functEvalList = []

    #   Loop for every pop size sample
    for populationSize in populationSizeList:
        
        #   Loop to generate result for each sample
        for sample in range( numSample ):

            argumentDict = { 'generations' : generations,
                             'size' : numBit,
                             'populationSize' : populationSize,
                             'problemFunctionClass' : problemClass,
                             'numGene' : numGene,
                             'maxNumBitInBlock' : maxNumBitInBlock,
                             'sample' : sample,
                             'doInfGen' : doInfGen }
            
            fucntionEvaluationCount = CompactGA.run( **argumentDict )
            functEvalList.append( fucntionEvaluationCount )
    
    ynxlog( 0, ' AVERAGE = {}'.format( np.average( functEvalList ) ) )
    ynxlog( 0, functEvalList )
