#
#   Global variable
#

# for set level of print 
Verbosity = 0

#
#   Function bodies
#

def ynxlog( verbosity, message ):
    if( Verbosity >= verbosity ):
        print( message )
