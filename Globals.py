#
#   Global variable
#

EvaluateFunctionCount = 0

#
#   Function bodies
#

def getEvaluateFunctionCount():
    global EvaluateFunctionCount
    return EvaluateFunctionCount

def resetEvaluateFunctionCount():
    global EvaluateFunctionCount
    EvaluateFunctionCount = 0

def increaseEvaluateFunctionCount():
    global EvaluateFunctionCount
    EvaluateFunctionCount += 1

