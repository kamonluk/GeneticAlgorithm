
import shelve

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
sampleNum = 1
numBit = 8
#pop_size = 1000000#100000
startSample = 0
maxSample = 5
sample = 0
i=0
evaluateFunctionCountList = []
print( ' numbit = ', numBit )
#print( ' pop_size = ', pop_size )
#for i in range( startSample, maxSample ):
populationSizeList = [10,100,500,1000,2000,5000,10000,12000,15000,20000]
avgCorrectBitList = []
for pop_size in populationSizeList:


    sumCorrectBit = 0
    sampleCount = 0
    for sample in range( maxSample ):
        shelveObj = shelve.open( 'data/{}bit_{}pop_backup_sample{}_ProblemTSPOneMax.shelve'.format( numBit, pop_size, sample ) )
        #print( [ keys for keys in shelveObj.keys()] )
        #try:
        #print( ' round : ', i + 1 )
####        print( '**************************** ')
##        print( '    pop_size = ', pop_size )
##        print( '    sample = ', sample )        
##        print( '    eval count = ', shelveObj['EvaluateFunctionCount'] )
##        print( '    generation = ', shelveObj['generation'] )
##        print( '    bestValue  = ', shelveObj['bestValue'] )
##        print( '    bestFitness  = ', shelveObj['bestFitness'] )
##        print( '    correctBitCount  = ', shelveObj['correctBitCount'] )
        try:
            sumCorrectBit += shelveObj['correctBitCount']
            sampleCount += 1
        except KeyError:
            continue
        shelveObj.close()
    avgCorrectBitList.append( sumCorrectBit / float(sampleCount) )

    print( '    pop_size = ', pop_size, ' avgCorrectBit = ', sumCorrectBit / float(maxSample) )
    
##    bestFunc = lambda data: data =='000'
##    bestValueList = list( filter( bestFunc, chunks( shelveObj['bestValue'], 3 ) ) )
##    print( '    000 blocks count  = ', len( bestValueList ) )
##    print( '    111 blocks count  = ', 10 - len( bestValueList ) )
##    
##    evaluateFunctionCountList.append( shelveObj['SolutionForTrap.evaluateFunctionCount'] )
    #except:
    #    continue
    
    
    #print( '    numbit = ', numBit )
    
print( avgCorrectBitList )    
    
#print( 'eval list = ', evaluateFunctionCountList )
#print( ' average eval = ', float( sum( evaluateFunctionCountList ) )/ len(evaluateFunctionCountList )  )
