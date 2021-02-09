# Author liu yuxin
# 2021/02/05
import math
import tkinter
import random

# ----------------------Variables needs for the simualtion ---------------------------------
# Market
Number_of_units_sold = [5000]*7
Unit_price = [20000]*7
# Production
Number_of_factories = [1]*7
Each_factory_has_depreciation_of = 1000000 # fixed
Depreciation_period = 6  # fixed
Number_of_additional_new_machines_introduced = [0]*7
Each_new_machinery_had_depreciation_of = [200000]*7
Raw_materials_inventory_value = 0.1 # fixed

# COGS
COGS = [0.3]*7

# Finished goods inventory
Inventory_obsolescence = 0.01 # fixed
Inventory_holding = [1]*7
FG_Inventory_holding = [1]*7
FG_Inventory_holding_cost= 0.1  # fixed

# Raw materials inventory
Constant_Inventory_obsolescence = 0.01 # fixed
Raw_Inventory_holding = [1]*7
Raw_Inventory_holding_cost = 0.1 # fixed

Logistics_cost = [0.08]*7
R_D = [0.05]*7
SG_A = [0.35]*7

# change values of each values  in  each round
Delta_Number_of_units_sold = 0  # %x
Delta_Unit_price = 0
Delta_Number_of_factories = 0
Delta_Number_of_additional_new_machines_introduced = 0
Delta_Each_new_machinery_had_depreciation_of = 0
Delta_COGS = 0
Delta_FG_Inventory_holding = 0
Delta_Raw_Inventory_holding = 0
Delta_Logistics_cost = 0
Delta_R_D = 0
Delta_SG_A = 0

# Store every rounds' values
ValueRevenue = [100000000]*7
ValueCOGS = [30000000]*7
ValueGrossProfit = [70000000]*7
ValueR_D = [5000000]*7
ValueSG_A = [35000000]*7
ValueLogistics = [8000000]*7
ValueDepreciation = [1000000]*7
ValueFGInventory = [100000000]*7
ValueRawMterialsInventory = [10000000.0]*7
ValueInventoryholdingCost = [11000000.0]*7
ValueInventoryObsolescence = [1100000.0]*7
ValueOperatingprofit =  [ 8900000.0]*7



# ------------------------------------- basic func to calculate the variables --------------------------

# calculate Revenue in year i
def getRevenue(i):
    ValueRevenue[i] = Number_of_units_sold[i]*Unit_price[i]
    return  ValueRevenue[i]

# calculate COGS in year i
def getCOCS(i):
    ValueCOGS[i] = COGS[i]* getRevenue(i)
    return ValueCOGS[i]

# calculate Gross profit in year i
def getGross_profit(i):
    ValueGrossProfit[i] = getRevenue(i) - getCOCS(i)
    return  ValueGrossProfit[i]

# calculate R&D in year i
def getR_D(i):
    ValueR_D[i] = getRevenue(i)*R_D[i]
    return ValueR_D[i]

# calculate SG&A in year i
def getSG_A(i):
    ValueSG_A[i] = SG_A[i]*getRevenue(i)
    return ValueSG_A[i]

# calculate Logistics in year i
def getLogistics(i):
    ValueLogistics[i] = Logistics_cost[i]*getRevenue(i)
    return ValueLogistics[i]

# calculate Depreciation in year i
def getDepreciation(i):
    ValueDepreciation[i] = Each_factory_has_depreciation_of*Number_of_factories[i]+ \
           Number_of_additional_new_machines_introduced[i]*Each_new_machinery_had_depreciation_of[i]
    return ValueDepreciation[i]

# calculate FG inventory in year i
def getFG_inventory(i):
    ValueFGInventory[i] = getRevenue(i)*FG_Inventory_holding[i]
    return ValueFGInventory[i]

# calculate Raw materials inventory in year i
def getRaw_materials_inventory(i):
    if i ==0:
        ValueRawMterialsInventory[i] = getRevenue(i)*Raw_materials_inventory_value
    else:
        ValueRawMterialsInventory[i] = getRevenue(i)*Raw_Inventory_holding[i]*Raw_materials_inventory_value
    return ValueRawMterialsInventory[i]


# calculate Inventory holding cost in year i
def getInventory_holding_cost(i):
    ValueInventoryholdingCost[i] = getFG_inventory(i)*FG_Inventory_holding_cost+\
                                   getRaw_materials_inventory(i)*Raw_Inventory_holding_cost
    return ValueInventoryholdingCost[i]

# calculateInventory_obsolescence(1%) in year i
def getInventory_obsolescence(i):
    ValueInventoryObsolescence[i] =(getFG_inventory(i)+getRaw_materials_inventory(i))*Inventory_obsolescence
    return  ValueInventoryObsolescence[i]

# calculate Operating_profit in year i
def getOperating_profit(i):
    ValueOperatingprofit[i] = getGross_profit(i)-getR_D(i)-getSG_A(i)-\
           getLogistics(i)-getDepreciation(i)-\
           getInventory_holding_cost(i)-getInventory_obsolescence(i)
    return ValueOperatingprofit[i]


# renew all values for year i
def RenewData(i):
    getRevenue(i)
    getCOCS(i)
    getGross_profit(i)
    getR_D(i)
    getSG_A(i)
    getLogistics(i)
    getDepreciation(i)
    getFG_inventory(i)
    getRaw_materials_inventory(i)
    getInventory_holding_cost(i)
    getInventory_obsolescence(i)
    getOperating_profit(i)



# Chances of EVENT
Event1Cards = 8
Event2Cards = 8
Event3Cards = 9
Event4Cards = 8
Event5Cards = 8
Event6Cards = 9
TotalCards = Event1Cards+Event2Cards+Event3Cards+Event4Cards+Event5Cards+Event6Cards


# -------------------------------------Events func--------------------------


# do nothing
def EVENT0(i,Actions):
    return None

# Demand surges for EVs globally.
# Those who took Action 10 have a 20% increase in sales.
# Those that did not take Action 10 have no impact
def EVENT1(i,Actions):
    if action10 in Actions:
        global Delta_Number_of_units_sold
        Delta_Number_of_units_sold += 0.2

# Strategic suppliers run of capacity due to high demand.
# Those who took Action 2 have no impact.
# Those who did not take Action 2 have a 15% decrease in sales
def EVENT2(i,Actions):
    if action2 not in Actions:
        global Delta_Number_of_units_sold
        Delta_Number_of_units_sold -= 0.15

# Disease epidemic causes showrooms to be locked down.
# Those who did not take Action 15 have a decrease in sales by 15%.
# Those who took action 15 are not affected
def EVENT3(i,Actions):
    if action15 not in Actions:
        global Delta_Number_of_units_sold
        Delta_Number_of_units_sold -= 0.15

#Labour strikes at low cost countries cause disruptions to backoffice work.
# Those who took action 8 have their SG&A increase by 3%.
# Those who did not take action 8 have no impact.
def EVENT4(i,Actions):
    if action8 in Actions:
        global Delta_SG_A
        Delta_SG_A += 0.03

#Trade tariffs are imposed on imports from overseas.
# Those who took Action 5  are not affected.
# Those who did not take action 5 have a 20% increase in logistics cost
def EVENT5(i,Actions):
    if action5 not in Actions:
        global Delta_Logistics_cost
        Delta_Logistics_cost += 0.2

# Competitors such as Apple and Google introduce new cars at low cost in order to sell  services.
# Those who did not take Action 6 have their sales drop by 15%.
# Those who took Action 6 are not affected.
def EVENT6(i,Actions):
    if action6 not in Actions:
        global Delta_Number_of_units_sold
        Delta_Number_of_units_sold -= 0.15


# ------------------------------------- actions func--------------------------------

# Do nothing
def action0():
    return None

#Invest into new production sites overseas to increase sales
# Delay effects! Increase factory by 1 (this will add $1m / year to depreciation)
# 1) Delta_Number_of_factories += 1
# 2) Delta_SG_A increase  2%
def action1():
    global Delta_Number_of_factories
    global Delta_SG_A
    Delta_Number_of_factories += 1
    Delta_SG_A += 0.02

# Introduce additional sources of  critical suppliers such as batteries
# 1) COGS[i] add by 2%
def action2():
    global Delta_COGS
    Delta_COGS += 0.02

# Create another distribution center to be closer to customers
# Number_of_units_sold increase by 15%
# FG_Inventory_holding[i] increase 7%
# Logistics_cost increase by 5%
def action3():
    global Delta_Number_of_units_sold
    global Delta_FG_Inventory_holding
    global Delta_Logistics_cost
    Delta_Number_of_units_sold += 0.15
    Delta_FG_Inventory_holding += 0.07
    Delta_Logistics_cost += 0.05

# Hold more finished goods to improve product availability for sales
# 0) Cannot be taken with action 16 in the same year
# 1) Delta_Number_of_units_sold  increased 10%
# 2) Delta_FG_Inventory_holding increased 4%
def action4():
    global Delta_Number_of_units_sold
    global Delta_FG_Inventory_holding
    Delta_Number_of_units_sold += 0.1
    Delta_FG_Inventory_holding += 0.04

# Introduce Complete Knockdowm Concept (CKD) to reduce import tax
# 1) COGS increase by 1%
# 2) Logistic cost decrease by 9%
def action5():
    global Delta_COGS
    global Delta_Logistics_cost
    Delta_COGS += 0.01
    Delta_Logistics_cost -= 0.09

# Improve product quality through R&D
# delay effects!
# 1) Unit_price increase by 7% from Year + 1
# 2) R_D increase by 10%
def action6():
    global Delta_R_D
    Delta_R_D += 0.1

# Improve manufacturing processes such as postponement to increase manufacturing productivity
# delay effects in COGS cost Decrease by 3% from Year + 1
# 1) Delta_R_D increase 5%
def action7():
    global Delta_R_D
    Delta_R_D += 0.05

# Relocate backoffice processing (invoicing, data entry, documentation) to low cost country
# 1) SG_A decrease by 2%
def action8():
    global Delta_SG_A
    Delta_SG_A -= 0.02

# Work with its distributors on risk sharing contracts to increase sales
# 1) Number_of_units_sold Increase by 10%
# 2) Raw_Inventory_holding increase by 5%
# 3) FG_Inventory_holding increase by 5%
def action9():
    global Delta_Number_of_units_sold
    global Delta_Raw_Inventory_holding
    global Delta_FG_Inventory_holding
    Delta_Number_of_units_sold += 0.1
    Delta_Raw_Inventory_holding += 0.05
    Delta_FG_Inventory_holding += 0.05

# Invest into new machinery to increase manufacturing efficiency
# 1) Number_of_additional_new_machines_introduced increase 1
def action10():
    global Delta_Number_of_additional_new_machines_introduced
    Delta_Number_of_additional_new_machines_introduced += 1

# Share demand information with suppliers
# 1)  Raw_Inventory_holding decrease  20%
def action11():
    global Delta_Raw_Inventory_holding
    Delta_Raw_Inventory_holding -= 0.2

# Decrease unit sales price   0.95*1.08 = 1.026
# 0) can't take with action13
# 1) Unit_price decrease by 5%
# 2) Number_of_units_sold increase by 8%
def action12():
    global Delta_Number_of_units_sold
    global Delta_Unit_price
    Delta_Unit_price -= 0.05
    Delta_Number_of_units_sold += 0.08

#  increase unit sales price   1.1*0.93 = 1.023
# 0) Cannot be taken together with action 12 in the same year
# 1) Unit_price increase 10%
# 2)  Number_of_units_sold decrease 7%
def action13():
    global Delta_Unit_price
    global Delta_Number_of_units_sold
    Delta_Unit_price  += 0.1
    Delta_Number_of_units_sold -= 0.07

# Invest in worker training through training in new technologies and process improvement
# 1) Delay effects COGS cost Reduce by 6% from Year + 1
# 2) SG_A increase by 3%
def action14():
    global Delta_SG_A
    Delta_SG_A += 0.03

# Invest in online sales capabilities such as the use of virtual showrooms and augmented reality
# 1) Number_of_units_sold increase by 9% from    Year + 1
# 2) Logistics_cost increase by 5%
# 3) R_D increase by  2%
def action15():
    global Delta_Logistics_cost
    global Delta_R_D
    Delta_Logistics_cost += 0.05
    Delta_R_D += 0.05

# conflict with action4
# Introduce  a pull model for production  - Take pre-orders first before production
# 1) Number_of_units_sold Reduce by 3%
# 2) Raw_Inventory_holding Reduce by 5%
# 3) FG_Inventory_holding Reduce by 5%
def action16():
    global Delta_Number_of_units_sold
    global Delta_Raw_Inventory_holding
    global Delta_FG_Inventory_holding
    Delta_Number_of_units_sold -= 0.03
    Delta_Raw_Inventory_holding -= 0.05
    Delta_FG_Inventory_holding -= 0.05


# -------------------Events------------------
AllEvents = [EVENT0, EVENT1, EVENT2, EVENT3, EVENT4, EVENT5, EVENT6]


# select actions
AllActions = [action0, action1, action2, action3, action4, action5, action6, action7, action8,
              action9, action10, action11, action12, action13, action14, action15, action16]


# Set the start value of year i  to the end value of year i-1 if i>1
def GetPreviousYearValue(i):
    # Market
    Number_of_units_sold[i] = Number_of_units_sold[i-1]
    Unit_price[i] = Unit_price[i-1]
    # Production
    Number_of_factories[i] = Number_of_factories[i-1]
    Number_of_additional_new_machines_introduced[i] = Number_of_additional_new_machines_introduced[i-1]
    Each_new_machinery_had_depreciation_of[i] = Each_new_machinery_had_depreciation_of[i - 1]
    COGS[i] = COGS[i-1]

    # Finished goods inventory
    FG_Inventory_holding[i] = FG_Inventory_holding[i-1]

    # Raw materials inventory
    Raw_Inventory_holding[i] = Raw_Inventory_holding[i-1]

    # Logistics
    Logistics_cost[i] = Logistics_cost[i-1]

    # R_D
    R_D[i]  =  R_D[i-1]

    #S_A
    SG_A[i] =  SG_A[i-1]

# at the begin of every round set the delta value to 0
def SetDeltaValuetoZero():
    global Delta_Number_of_units_sold
    global Delta_Unit_price
    global Delta_Number_of_factories
    global Delta_Number_of_additional_new_machines_introduced
    global Delta_Each_new_machinery_had_depreciation_of
    global Delta_COGS
    global Delta_FG_Inventory_holding
    global Delta_Raw_Inventory_holding
    global Delta_Logistics_cost
    global Delta_R_D
    global Delta_SG_A
    Delta_Number_of_units_sold = 0  # %x
    Delta_Unit_price = 0
    Delta_Number_of_factories = 0
    Delta_Number_of_additional_new_machines_introduced = 0
    Delta_Each_new_machinery_had_depreciation_of = 0
    Delta_COGS = 0
    Delta_FG_Inventory_holding = 0
    Delta_Raw_Inventory_holding = 0
    Delta_Logistics_cost = 0
    Delta_R_D = 0
    Delta_SG_A = 0

# add changes to data in year i
def AddChangesToData(i):

    Number_of_units_sold[i] *= 1+Delta_Number_of_units_sold

    Unit_price[i] *= 1+Delta_Unit_price

    Number_of_factories[i] += Delta_Number_of_factories

    Number_of_additional_new_machines_introduced[i] += Delta_Number_of_additional_new_machines_introduced

    # No changes for this row
    Each_new_machinery_had_depreciation_of[i] += Delta_Each_new_machinery_had_depreciation_of

    COGS[i] *= 1+Delta_COGS

    FG_Inventory_holding[i] *= 1+Delta_FG_Inventory_holding

    Raw_Inventory_holding[i] *= 1+Delta_Raw_Inventory_holding

    Logistics_cost[i] *= 1+Delta_Logistics_cost
    R_D[i]  *= 1+Delta_R_D
    SG_A[i] *= 1+Delta_SG_A

# take actions for year year  AsInNumber and AllEvents are in form of number matrix
def ActionsforYear(year,AsInNumber,EsInNumber):
    
    EVENTS  = [0]* 7
    EVENTS = setEventValues(EsInNumber, EVENTS, AllEvents)
    Actions = [[0] * 3] * 7
    Actions =  setActionValues(AsInNumber,Actions,AllActions)
    
    # set original values of year 1 to year 0
    if year>=1:
        GetPreviousYearValue(year)
    # at the start set all Delta value to zero
    SetDeltaValuetoZero()
    # Delay effets
    global Delta_Number_of_units_sold
    global Delta_Unit_price
    global Delta_COGS
    #  EVENT effects
    if year >= 1:
        EVENTS[year-1](year-1,Actions[0:year])
    # delay effects

    if year>=1 :
        if action1 in Actions[year-1]:
            Delta_Number_of_units_sold += 0.22
        if action6 in Actions[year-1]:
            Delta_Unit_price += 0.07
        if action7 in Actions[year-1]:
            Delta_COGS -= 0.03
        if action14 in Actions[year-1]:
            Delta_COGS -= 0.06
        if action15 in Actions[year-1]:
            Delta_Number_of_units_sold += 0.09
    # Take actions for year i
    for j in range(len(Actions[year])):
        Actions[year][j]()
    # set changes to data
    AddChangesToData(year)
    # calculate all data
    RenewData(year)

# get the current situation for year Year AsInNumber is the actions matrix for all Year
def CurrentSituationforYear( EndYear,AsInNumber,EsInNumber):
    # take actions from year 0 to year year
    for i in range(1, EndYear+1):
        ActionsforYear(i,AsInNumber,EsInNumber)

# Events take effects for next round
def ChooseEventsforTear(i,Actions):
    global Event1Cards
    global Event2Cards
    global Event3Cards
    global Event4Cards
    global Event5Cards
    global Event6Cards
    # take one EVENT for the year
    p = random.random()
    P1 = 1.0 * Event1Cards / TotalCards
    P2 = 1.0 * (Event1Cards + Event2Cards) / TotalCards
    P3 = 1.0 * (Event1Cards + Event2Cards + Event3Cards) / TotalCards
    P4 = 1.0 * (Event1Cards + Event2Cards + Event3Cards + Event4Cards) / TotalCards
    P5 = 1.0 * (Event1Cards + Event2Cards + Event3Cards + Event4Cards + Event5Cards) / TotalCards
    if 0 <= p < P1:
        EVENT1(i, Actions)  # EVENT1 happen
        Event1Cards -= 1  # delete one Event1Card
    elif P1 <= p < P2:
        EVENT2(i, Actions)
        Event2Cards -= 1
    elif P2 <= p < P3:
        EVENT3(i, Actions)
        Event3Cards -= 1
    elif P3 <= p < P4:
        EVENT4(i, Actions)
        Event4Cards -= 1
    elif P4 <= p < P5:
        EVENT5(i, Actions)
        Event5Cards -= 1
    else:
        EVENT6(i, Actions)
        Event6Cards -= 1


# As stores number
# ActionList is what we want
# A is all actions
def setActionValues(As,Actions,A):
     for i in range( len(As) ):
        Actions[i] = [ A[As[i][0]], A[As[i][1]], A[As[i][2]] ]
     return Actions

# Es stores number
# Events is events happend
def setEventValues(Es,Events,EventsList):
    for i in range(len(Es)):
        Events[i] = EventsList[Es[i]]
    return Events


# create Random Events
def generateRandomEvents():
    events = [0]*7
    events[0] = 0
    events[1] = 2
    for i in range(2,7):
        events[i] = random.randint(1,6)
    return events

def main():

    # store action values
    AsInNumber = [
                      [0, 0, 0],
                      [4, 11, 13],
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]    ]


    EventsInnumber = [0,2,0,0,0,0,0]
    EVENTS = [EVENT0]*7
    EVENTS = setEventValues(EventsInnumber, EVENTS, AllEvents)
    year = 6
    CurrentSituationforYear(year, AsInNumber, EventsInnumber)


#main()













