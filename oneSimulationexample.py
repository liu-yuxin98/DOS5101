# Author liu yuxin
# 2021/02/06
import BasicVariableandFucforsimulation as SG
import optimizationf as T

if __name__ == "__main__":
    # actions for the game
    Actions = [[0, 0, 0],
               [0, 0, 0],
               [0,0,0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]

    # events for the game
    Events = [0, 0, 0, 0, 0, 0, 0]
    OP = T.Trycases(6, Actions, Events)
    print('Overall Operating Profit is ' + str(OP))
    print(SG.ValueOperatingprofit)








