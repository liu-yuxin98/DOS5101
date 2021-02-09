# Author liu yuxin
# 2021/02/06
import BasicVariableandFucforsimulation as SG
import pandas as pd
import math

# this module contains some functions to find the best operating profit for the next year
# given actions as As ,EVENTS as ES, calculate OP and after try go back to the original condition
# based on current As, Es calculate the As and Es till Endyear
# return OPValues from year0 to year6
def Trycases(Endyear,As,Es):
     # calculate till year
    SG.CurrentSituationforYear(Endyear, As, Es)
    OPvalues = int(sum(SG.ValueOperatingprofit))
    return OPvalues

#  only take one action in each round and calculate the total results

# in order to find which actions are better than else, get OriginalAs,OriginalEs for future go back
def CompareActions(Startyear,OriginalAs,OriginalEs,times):
    As = OriginalAs.copy()
    Opvalues = [[0]*times]*17 # record opearting values

    for i in range(0,17):
        for j in range(Startyear,7):
            As[j][0] = i  # from startyear to year 6 only take action i
        opFori = [0]*times  # store action i 's operating value
        for t in range(times):
            Es = SG.generateRandomEvents()
            opFori[t] = Trycases(6,As,Es)
        Opvalues[i] = opFori.copy()
    # go back
    Trycases(6, OriginalAs, OriginalEs)

    res = [[i,0] for i in range(17)]
    for i in range(17):
        res[i][1] = int(sum(Opvalues[i])/times)
    print('Use different EVENTS combination for '+str(times)+ ' times.')
    for i in range(len(res)):
        print('only take Action ' + str(i) +' for 6 years, total Opearting Profit  is '+str(res[i]))
    name = ['ActionID','TotalOperatingProfit']
    test = pd.DataFrame(columns=name, data=res)
    #print(test)
    #test.to_csv('C:/Users/Lenovo/Desktop/Fri-DOS5101/Simulation/EveryRound/1Action_Round2.csv')
    return res


# if calculate the best two combination of year3 than year should be 3
# find which two actions taken together can increase value the most
def findBestTwoCombination(Startyear,OriginalAsInNumber,OriginalEsInNumber,times):
    As = OriginalAsInNumber.copy()
    c1 = [4,16]
    c2 = [12,13]
    # get all kinds of combination and store them as (i,j) in CombinationList
    CombinationList = []
    for i in range(0,16):
        for j in range(i+1,17):
            if [i,j] != c1 and [i,j]!= c2:
                CombinationList.append((i,j))
    # values stores Total Operating Values of 6 years for each (i,j) combination
    values = [[0]*times for i in range(len(CombinationList))]
    for i in range(len(CombinationList)):
        for j in range(Startyear,7):
            # from year year to year 6 only takes action (CombinationList[i][0],CombinationList[i][1])
            As[j][0] = CombinationList[i][0]
            As[j][1] = CombinationList[i][1]
        for t in range(times):
            Es = SG.generateRandomEvents()
            values[i][t] = Trycases(6,As,Es)

    # go back to currrent condition
    Trycases(6,OriginalAsInNumber,OriginalEsInNumber)

    # get profit
    AvgTotalOperatingProfit = [[0] for i in range(len(values))]
    for i in range(len(values)):
        AvgTotalOperatingProfit[i] = int(sum(values[i])/times)
    dictValues =  dict(zip(CombinationList,AvgTotalOperatingProfit))
    name = ['ActionCombination', 'TotalOperatingProfit']
    output = [[ CombinationList[i] ,AvgTotalOperatingProfit[i]  ] for i in range(len(values))]
    test = pd.DataFrame(columns=name, data=output)
    print(test)
    # test.to_csv('C:/Users/Lenovo/Desktop/Fri-DOS5101/Simulation/ActionCombinationPerformance.csv')
    return None

# find which three actions taken together can increase value the most
def findBestThreeCombination(Startyear,OriginalAsInNumber,OriginalEsInNumber,times):
    As = OriginalAsInNumber.copy()
    # store each combination of (i,j,k) in CombinationList
    CombinationList = []
    for i in range(15):
        for j in range(i+1,16):
            for k in range(j+1,17):
                conflit =( (i,j)==(4,16) or (i,k)==(4,16) or (j,k)==(4,16) or
                           (i,j)==(12,13) or (i,k)==(12,13) or (j,k)==(12,13))
                if not conflit:
                    CombinationList.append((i, j, k))

    values = [[0] * times for i in range(len(CombinationList))]

    for i in range(len(CombinationList)):
        for j in range(Startyear, 7):
            # only take actions (i,j,k) from year to 6 to see the Operating Profit
            As[j][0] = CombinationList[i][0]
            As[j][1] = CombinationList[i][1]
            As[j][2] = CombinationList[i][2]
        for t in range(times):
            Es = SG.generateRandomEvents()
            values[i][t] = Trycases(6, As, Es)

    # go back to current situation
    Trycases(6, OriginalAsInNumber, OriginalEsInNumber)

    # get profit
    AvgTotalOperatingProfit = [[0] for i in range(len(values))]
    for i in range(len(values)):
        AvgTotalOperatingProfit[i] = int(sum(values[i]) / times)
    dictValues = dict(zip(CombinationList, AvgTotalOperatingProfit))
    name = ['ActionCombination', 'TotalOperatingProfit']
    output = [[CombinationList[i], AvgTotalOperatingProfit[i]] for i in range(len(values))]
    test = pd.DataFrame(columns=name, data=output)
    #print(test)
    # test.to_csv('C:/Users/Lenovo/Desktop/Fri-DOS5101/Simulation/3ActionCombination_forRound2.csv')



# start from year1 and find best actions to make total to the best
# start from year year to find the optimized actions for the following n years
# repeat time times to eliminate fluctuation
# given CurrenActions for year year
# ChooseActions is a list of good actions to select from( this has been calculated to find the good actions from all
# actions to reduce running times
def findBestactionsForfuturetwoYears(Startyear,CurrentActions,ChooseActions,Events,time):

    # get all the three-combination from the CurrentActions eg threeactions[i] = (4,5,8)
    threeactions = []
    end = len(ChooseActions)-3+1
    for a1 in range( end ):
        for a2 in range(a1+1,end+1):
            for a3 in range(a2+1,end+2):
                threeactions.append((ChooseActions[a1],ChooseActions[a2],ChooseActions[a3]))

    # store combination infon  for two yearsin form ((4,5,8),(4,7,8)) -> means (4,5,8) for year (4,7,8) for year+1
    CombineActions = []

    for i in range(len(threeactions)):
        for j in range(len(threeactions)):
            CombineActions.append( ( threeactions[i] , threeactions[j] ) )

    As = CurrentActions.copy()

    # go through all the possible actions to find the best solution
    OPvalues = [[0] * time for i in range(len(CombineActions))]

    for i in range(len(CombineActions)):
        for j in range(3):
            As[Startyear][j] = CombineActions[i][0][j]
            As[Startyear+1][j] = CombineActions[i][1][j]
        for t in range(time):
             Es = SG.generateRandomEvents()
             OPvalues[i][t] = Trycases(6, As, Es)

    # go back to current situation
    Trycases(6, CurrentActions, Events)

    # OUTPUT  RESULTS
    AvgTotalOperatingProfit = [[0] for i in range(len(OPvalues))]
    for i in range(len(OPvalues)):
        AvgTotalOperatingProfit[i] = int(sum(OPvalues[i]) / time)
    dictValues = dict(zip(CombineActions, AvgTotalOperatingProfit))
    name = ['ActionCombination', 'TotalOperatingProfit']
    output = [[CombineActions[i], AvgTotalOperatingProfit[i]] for i in range(len(OPvalues))]
    test = pd.DataFrame(columns=name, data=output)
    print(test)
    #test.to_csv('C:/Users/Lenovo/Desktop/Fri-DOS5101/Simulation/EveryRound/6ActionCombination_Round2.csv')


# start from StartYear ,given CurrentActions , Events all in numbe matrix , repeat time times
def findBestActionsForNextYear(Startyear,CurrentActions,Events):
    bestActions = [0,0,0]
    # As to store actions in number
    As = CurrentActions.copy()
    maxOP = 0
    for i in range(15):
        for j in range(i+1,16):
            for k in range(j+1,17):
                conflit = ((i, j) == (4, 16) or (i, k) == (4, 16) or (j, k) == (4, 16) or
                           (i, j) == (12, 13) or (i, k) == (12, 13) or (j, k) == (12, 13))
                if not conflit:
                    As[Startyear] = [i,j,k]
                    ijkOP  = Trycases(6,As,Events)
                    if maxOP< ijkOP:
                        maxOP  = ijkOP
                        bestActions = [i,j,k]

    print(maxOP)
    print(bestActions)
    return maxOP,bestActions



if __name__ == "__main__":
    # current actions before year 2
    CurrentActions =[
          [0, 0, 0],
          [4, 11, 13],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]
    ChooseActions = [4,5,6,7,8,9,11,12,14]
    Events = [0,2,0,0,0,0,0]
    Startyear = 2 # start from current year 2 to find the best actions for 2,3 year
    times = 1 # repeat time
    n = 2 # find the best actions for the next two years
    maxop, bestactions = findBestActionsForNextYear(Startyear,CurrentActions,Events)


    # CompareActions(Startyear,CurrentActions,Events,times)
    # findBestTwoCombination(Startyear,CurrentActions,Events,times)
    # findBestThreeCombination(Startyear,CurrentActions,Events,times)
    # findBestactionsForfuturetwoYears(Startyear, CurrentActions, ChooseActions,Events, times)


















