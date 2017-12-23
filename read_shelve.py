
import shelve

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
sampleNum = 1
numBit = 30
#pop_size = 1000000#100000
startSample = 0
maxSample = 50
sample = 0
i=0
evaluateFunctionCountList = []
print( ' numbit = ', numBit )
#print( ' pop_size = ', pop_size )
#for i in range( startSample, maxSample ):
for pop_size in ( 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300 ):
    
    shelveObj = shelve.open( '{}bit_{}pop_backup_sample{}.shelve'.format( numBit, pop_size, sample ) )
    #print( [ keys for keys in shelveObj.keys()] )
    #try:
    #print( ' round : ', i + 1 )
    print( '**************************** ')
    print( '    pop_size = ', pop_size )
    print( '    eval count = ', shelveObj['SolutionForTrap.evaluateFunctionCount'] )
    print( '    generation = ', shelveObj['generation'] )
    print( '    bestValue  = ', shelveObj['bestValue'] )

    bestFunc = lambda data: data =='000'
    bestValueList = list( filter( bestFunc, chunks( shelveObj['bestValue'], 3 ) ) )
    print( '    000 blocks count  = ', len( bestValueList ) )
    print( '    111 blocks count  = ', 10 - len( bestValueList ) )
    
    evaluateFunctionCountList.append( shelveObj['SolutionForTrap.evaluateFunctionCount'] )
    #except:
    #    continue
    shelveObj.close()
    
    #print( '    numbit = ', numBit )
    
    
print( 'eval list = ', evaluateFunctionCountList )
#print( ' average eval = ', float( sum( evaluateFunctionCountList ) )/ len(evaluateFunctionCountList )  )
