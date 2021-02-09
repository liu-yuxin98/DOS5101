# Author liu yuxin
# 2021/02/09
import BasicVariableandFucforsimulation as SG
import optimizationf as T
from tkinter import *


class GameSimulationGUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
    # set window
    def set_init_window(self):
        self.init_window_name.title("SimulationGame_v1.0")           # window name
        #self.init_window_name.geometry('320x160+10+10')             # 320 160 is the size of window, +10 +10define the position when window appear
        self.init_window_name.geometry('800x600+10+10')
        #self.init_window_name["bg"] = "black"
        #self.init_window_name.attributes("-alpha",0.9)                          # alpha

        #label
        self.init_data_label = Label(self.init_window_name, text="Rounds")
        self.init_data_label.grid(row=0, column=0)
        self.init_data_label = Label(self.init_window_name, text="Actions for the year")
        self.init_data_label.grid(row=0, column=1)
        self.init_data_label = Label(self.init_window_name, text="Event for the year")
        self.init_data_label.grid(row=0, column=2)
        self.result_data_label = Label(self.init_window_name, text="OperatingProfit")
        self.result_data_label.grid(row=0, column=3)

        self.init_data_label = Label(self.init_window_name, text="R0")
        self.init_data_label.grid(row=1, column=0)
        self.init_data_label = Label(self.init_window_name, text="R1")
        self.init_data_label.grid(row=2, column=0)
        self.init_data_label = Label(self.init_window_name, text="R2")
        self.init_data_label.grid(row=3, column=0)
        self.init_data_label = Label(self.init_window_name, text="R3")
        self.init_data_label.grid(row=4, column=0)
        self.init_data_label = Label(self.init_window_name, text="R4")
        self.init_data_label.grid(row=5, column=0)
        self.init_data_label = Label(self.init_window_name, text="R5")
        self.init_data_label.grid(row=6, column=0)
        self.init_data_label = Label(self.init_window_name, text="R6")
        self.init_data_label.grid(row=7, column=0)

        self.log_label = Label(self.init_window_name, text="Total OperatingProfit ")
        self.log_label.grid(row=8, column=0)
        self.log_label = Label(self.init_window_name, text="IsValid")
        self.log_label.grid(row=9, column=0)

        # data input
        self.actions_Data = Text(self.init_window_name, width=9, height=7)  #data input
        self.actions_Data.grid(row=1, column=1, rowspan=7, columnspan=1)

        self.events_Data = Text(self.init_window_name, width=2, height=7)  # data input
        self.events_Data.grid(row=1, column=2, rowspan=7, columnspan=1)


        # data output
        self.annual_operatingprofit = Text(self.init_window_name, width=12, height=7)  #  annual operating profitdata output
        self.annual_operatingprofit.grid(row=1, column=3, rowspan=7, columnspan=1)

        self.total_operatingprofit = Text(self.init_window_name, width=15, height=1)  # total operating profit output
        self.total_operatingprofit.grid(row=8 ,column=1, rowspan=1, columnspan=1)

        self.is_valid = Text(self.init_window_name, width=30, height=2)  # VALID?
        self.is_valid.grid(row=9, column=1, rowspan=1, columnspan=2)

        #button
        self.CalculateButton = Button(self.init_window_name, text="Start calculating Operaing Profit", bg="lightblue", width=30,
                                              command=self.CalculateOP)  # without ()
        self.CalculateButton.grid(row=10, column=1)

        # func
    # take input data: actions_Data and events_Data. transfer them to the form of Actions number matrix and Events list
    # used in test.Trycases(Endyear,As,Es):

    # get input actions and preprocess it so it can be used in future.
    def preprocessActions(self,str):
        str = str.split('\n')
        str = [str[i] for i in range(len(str)) if str[i] != ' ' and str[i] != '']

        for i in range(len(str)):
            str[i] = str[i].split(' ')

        str = [[str[i][j] for j in range(len(str[i])) if str[i][j] != ''] for i in range(len(str))]
        # if actions are not full, fill in 0 for empty acitons
        if len(str) < 7:
            for i in range(7 - len(str)):
                str.append([0, 0, 0])
        for i in range(len(str)):
            for j in range(len(str[0])):
                str[i][j] = int(str[i][j])
        # only choose actions for 0-6 years
        str = str[0:7]
        # incase one year with 1 or 2 actions
        for i in range(len(str)):
            if len(str[i]) < 3:
                for j in range(3 - len(str[i])):
                    str[i].append(0)
        return str

    # get input Events and preprocess it so it can be used in future.
    def preprocessEvents(self,str):
        str = str.split('\n')
        str =[str[i] for i in range(len(str)) if str[i]!=' ' and str[i]!='']
        # full in blank with 0
        if len(str) < 7:
            for i in range(7 - len(str)):
                str.append(0)
        str = str[0:7]
        str = [int(str[i]) for i in range(len(str))]
        return str

    # verify if actions are valid( no action occur more than 3 times from year2-year6)
    # check if same action appear twice in one year
    def isValid(self,Actions):
        for i in range(len(Actions)):
            for j in range(len(Actions[i])):
                if Actions[i][j]<0 or Actions[i][j]>16:
                    self.is_valid.delete(0.0, END)
                    self.is_valid.insert(0.0, 'INVALID out of boundary')
                    return None

        # from year 2 to year 6
        maxActions = Actions[2:]

        # check each line to see if same action appear twice in one year
        flag = 1
        for i in range(len(maxActions)):
            if maxActions[i][0] == maxActions[i][1] and maxActions[i][0]!=0:

                output = 'NOT VALID! action ' +str(i)+ ' appear more than once'
                self.is_valid.delete(0.0, END)
                self.is_valid.insert(0.0, output)
                flag = 0
                break
            if maxActions[i][0] == maxActions[i][2] and maxActions[i][0]!=0:
                output = 'NOT VALID! action ' +str(i)+ ' appear more than once'
                self.is_valid.delete(0.0, END)
                self.is_valid.insert(0.0, output)
                flag = 0
                break
            if maxActions[i][1] == maxActions[i][2] and maxActions[i][1]!=0:
                self.is_valid.delete(0.0, END)
                output = 'NOT VALID! action ' +str(i)+ ' appear more than once'
                self.is_valid.delete(0.0, END)
                self.is_valid.insert(0.0, output)
                flag = 0
                break

        # no twice action in the actions
        if flag:
            # calculate each actions appear times
            dictmaxactions = dict()
            for i in range(len(maxActions)):
                for j in range(len(maxActions[0])):
                    dictmaxactions[maxActions[i][j]] = dictmaxactions.get(maxActions[i][j], 0) + 1

            actions = 0
            for key in dictmaxactions:
                if dictmaxactions.get(key) > 3:
                    actions = key
                    break
            self.is_valid.insert(0.0, END)
            if actions != 0:
                output = 'Not valid ' + str(actions) + ' occur ' + str(dictmaxactions.get(actions)) + ' times.'
                self.is_valid.delete(0.0, END)
                self.is_valid.insert(0.0, output)
            else:
                self.is_valid.delete(0.0, END)
                self.is_valid.insert(0.0, 'Valid Actions')
            return actions

        else:
            return None


    def CalculateOP(self):
        # pre processing for the input data
        Actions = self.preprocessActions(self.actions_Data.get(1.0, END))

        # decide wether there are some actions taken more than 3 time from year2 to year 6
        maxAct = self.isValid(Actions)

        if maxAct != 0:  # Not valid actions
            return None
        else:
            # events for the game
            Events = self.preprocessEvents(self.events_Data.get(1.0, END))
            OP = T.Trycases(6, Actions, Events)
            self.total_operatingprofit.delete(1.0, END)
            self.total_operatingprofit.insert(1.0, OP)

            AnnualOP = SG.ValueOperatingprofit
            AnnualOP = [int(AnnualOP[i]) for i in range(len(AnnualOP))]

            self.annual_operatingprofit.delete(0.0, END)
            self.annual_operatingprofit.insert(0.0, END)
            AnnualOP = AnnualOP[::-1]
            for i in range(len(AnnualOP)):
                    self.annual_operatingprofit.insert(0.0, '\n')
                    self.annual_operatingprofit.insert(0.0, AnnualOP[i])


def gui_start():
    init_window = Tk()              # create a window
    SimulationGame = GameSimulationGUI(init_window)
    # attributes
    SimulationGame.set_init_window()

    init_window.mainloop()          # keep window show in the screen


gui_start()


