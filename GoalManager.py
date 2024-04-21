"""
GoalManager for CM12005 coursework by Liam O'Connor 2024-04-18

setGoals():
Creates a pop-up window with input boxes where the user can enter to set a goal
The goal is then saved to a CSV file

trackProgress():
Retrieves goals and user statistics from CSV files
Checks to see if goals have been met
Creates a pop-up window which displays all set goals, and specifies if/when they're met
The user has the option to clear all completed goals, i.e. remove them from the database

Example Usage:
goalMan = GoalManager()
goalMan.trackProgress()
goalMan.setGoals()
"""

from Sleep import Sleep
from AlcoholConsumption import AlcoholConsumption
import tkinter as tk
from tkinter import ttk
from CSVReader import CSVReader
from datetime import datetime, date, timedelta

# Make plan / layout in word doc
# add window slider!

class GoalManager:
    def __init__(self, goalsFilename, dataFilename) -> None:
        self.goalsFilename = goalsFilename
        self.dataFilename = dataFilename
    def setGoals(self):
        setNone = True
        while True: #exit with break
            # goal types: max sleep, min sleep, min quality sleep, max alcohol consumption
            menu = tk.Tk()

            def closeMenu():
                global validEntry
                global failOn
                global goalType
                global goalFigure
                global goalSpan
                global goalDuration
                validEntry = True
                failOn = 0
                goalType = ""
                goalFigure = 0
                goalSpan = 0
                goalDuration = 0
                try:
                    goalType     = box1.get().strip()
                except:
                    failOn = 1
                    validEntry = False
                try:
                    goalFigure   = int(box2.get().strip())
                except:
                    failOn = 2
                    validEntry = False
                try:
                    goalSpan     = int(box3.get().strip())
                except:
                    failOn = 3
                    validEntry = False
                try:
                    goalDuration = int(box4.get().strip())
                except:
                    failOn = 4
                    validEntry = False
                menu.destroy()

            
            menu.geometry("400x320")
            label1 = tk.Label(menu, text = "1. Select goal type:")
            choices = ["Minimum Sleep","Minimum Quality Sleep","Maximum Sleep","Maximum Alcohol Consumption"]
            enteredText1 = tk.StringVar()
            box1 = ttk.Combobox(menu, textvariable = enteredText1, values = choices, width = "30")
            label2 = tk.Label(menu, text = "2. Enter how many hours this should be set to for sleep,\nor how many units to be set to for alcohol consumption")
            box2 = tk.Entry(menu, width = 34)
            label3 = tk.Label(menu, text = "3. Enter a number of days you want this to span over \n(e.g. enter 7 to aim for this much sleep/alchohol consumption in a week)")
            box3 = tk.Entry(menu, width = 34)
            label4 = tk.Label(menu, text = "4. Enter the time period (number of days) you want to acheive this for")
            box4 = tk.Entry(menu, width = 34)
            blankLabel1 = tk.Label(menu, text =" ")
            blankLabel2 = tk.Label(menu, text =" ")
            blankLabel3 = tk.Label(menu, text =" ")
            blankLabel4 = tk.Label(menu, text =" ")
            enterButton = tk.Button(menu, text = "Enter details", command = closeMenu)

            label1.pack()
            box1.pack()
            blankLabel1.pack()
            label2.pack()
            box2.pack()
            blankLabel2.pack()
            label3.pack()
            box3.pack()
            blankLabel3.pack()
            label4.pack()
            box4.pack()
            blankLabel4.pack()
            enterButton.pack()

            menu.mainloop()
            try:
                if not validEntry:
                    if (failOn > 1):
                        self.errorMenu("Invalid entry in box " + str(failOn) + "\nValue must be a positive integer")
                    else:
                        self.errorMenu("Invalid entry in box 1")
                    continue

                if goalType == "":
                    self.errorMenu("Box 1 can't be left blank")
                    continue
                if goalType not in choices:
                    self.errorMenu("Box 1 must contain one of the provided option")
                    continue
                if (goalDuration <= 0
                or  goalFigure   <= 0
                or  goalSpan     <= 0):
                    self.errorMenu("Entered numbers must be greater than 0")
                    continue
                if goalSpan > goalDuration:
                    self.errorMenu("The value in the fourth box must be at least the value in the third box")
                    continue
                if (validEntry):
                    setNone = False
                    break
            except:
                setNone = True
                break
        if not setNone:
            self.addEntry(goalType, goalFigure, goalSpan, goalDuration)
            self.addAnother()

    def errorMenu(self, message):
        em = tk.Tk()
        em.geometry("400x75")
        labelE = tk.Label(em, text = "Error: " + message + "\nClose this window to try again")
        labelE.pack()
        def closeWindow():
            em.destroy()
        noButton = tk.Button(em, text = "Close", command = closeWindow)
        noButton.pack()
        em.mainloop()

    def addAnother(self):
        box = tk.Tk()
        labelE = tk.Label(box, text = "Would you like to set another goal?")
        labelE.pack()
        def closeWindow():
            box.destroy()
        def goAgain():
            box.destroy()
            self.setGoals()
        yesButton = tk.Button(box, text = "Yes", command = goAgain)
        noButton = tk.Button(box, text = "No", command = closeWindow)
        yesButton.pack()
        noButton.pack()
        box.mainloop()

    def addEntry(self, goalType, goalFigure, goalSpan, goalDuration):
        import os
        with open(self.goalsFilename, 'a') as goalFile:
            if (os.path.getsize(self.goalsFilename) == 0):
                goalFile.write("\"goalType\", \"goalFigure\", \"goalSpan\", \"goalDuration\"\n")
            goalFile.write("\"" + goalType + "\", \"" + str(goalFigure) + "\", \"" + str(goalSpan) + "\", \"" + str(goalDuration) + "\"\n")

    def trackProgress(self):
        # ASSUMES GIVEN DATES ARE CONSECUTIVE
        goals = [] #String[] array of goals
        with open(self.goalsFilename, 'r') as goalFile:
            for goal in goalFile:
                quoteCount = 0
                thisGT = ""
                thisGF = ""
                thisGS = ""
                thisGD = ""
                for char in goal:
                    if char == '"':
                        quoteCount += 1
                    elif quoteCount == 1:
                        thisGT += char
                    elif quoteCount == 3:
                        thisGF += char
                    elif quoteCount == 5:
                        thisGS += char
                    elif quoteCount == 7:
                        thisGD += char
                if thisGT == "goalType":
                    continue
                goals.append([thisGT, thisGF, thisGS, thisGD])

        message = ""
        areGoalsMet = [False] * len(goals)
        i = 0
        for goal in goals:
            try:
                message += self.checkSleepGoal(goal[0], int(goal[1]), int(goal[2]), int(goal[3])) + "\n"
                if (message[-5:-2] != "met"):
                    areGoalsMet[i] = True
            except:
                pass
            i += 1
        box = tk.Tk()
        label = tk.Label(box, text = "Goal Tracker:\n\n" + message)
        label.pack()
        blank1 = tk.Label(box, text = " ")
        blank2 = tk.Label(box, text = " ")

        def deleteCompleteGoals():
            print(goals)
            with open(self.goalsFilename, 'w') as goalFile:
                goalFile.write("")
            for i in range (0, len(goals), 1):
                if areGoalsMet[i] == False:
                    self.addEntry(goals[i][0], int(goals[i][1]), int(goals[i][2]), int(goals[i][3]))
            closeWindow()
            self.trackProgress()
        def closeWindow():
            box.destroy()

        clearGoalButton = tk.Button(box, text = "Clear complete goals", command = deleteCompleteGoals)
        exitButton = tk.Button(box, text = "Exit", command = closeWindow)
        clearGoalButton.pack()
        blank1.pack()
        exitButton.pack()
        blank2.pack()

        box.mainloop()
    
    def dateOneFirst(self, date1, date2) -> bool:
        year1 = ""
        year2 = ""
        month1 = ""
        month2 = ""
        day1 = ""
        day2 = ""
        dashes = 0
        try:
            for i in range (0, len(date1), 1):
                if date1[i] != '-':
                    if dashes == 0:
                        year1 += date1[i]
                        year2 += date2[i]
                    elif dashes == 1:
                        month1 += date1[i]
                        month2 += date2[i]
                    elif dashes == 2:
                        day1 += date1[i]
                        day2 += date2[i]
                else:
                    dashes += 1
            if year1 < year2:
                return True
            elif year2 > year1:
                return False
            elif month1 < month2:
                return True
            elif month2 > month1:
                return False
            elif day1 < day2:
                return True
            elif day1 > day2:
                return False
            else:
                return True
        except:
            return False

    def earliestDateInKeys(self, dic):
        earliestDate = "9999-12-31"
        for key in dic.keys():
            if self.dateOneFirst(key, earliestDate):
                earliestDate = key
        return earliestDate
    
    def dateToDaysAgo(self, date):
        earlierDate = datetime.strptime(date, "%Y-%m-%d")
        today = datetime.now()
        diff = today - earlierDate
        return diff.days

    def checkSleepGoal(self, goalType, goalFigure, goalSpan, goalDuration):
        
        windowMessage = "Goal: " + goalType + " of " + str(goalFigure) + " per " + str(goalSpan) + " days, for " + str(goalDuration) + " days"

        hours = self.getHours()
        alcoholConsumption = self.getDrinks()
        quality = self.getQualities()
        earliestHour = self.dateToDaysAgo(self.earliestDateInKeys(hours))
        earliestDrink = self.dateToDaysAgo(self.earliestDateInKeys(alcoholConsumption))
        #earliestQuality = self.dateToDaysAgo(self.earliestDateInKeys(quality))

        goalStart = 0
        goalEnd   = 0

        goalMet = False

        max = False
        if (goalType == "Maximum Sleep" or goalType == "Maximum Alcohol Consumption"):
            max = True
        qualityNeeded = False
        if (goalType == "Minimum Quality Sleep"):
            qualityNeeded = True

        if (goalType == "Maximum Alcohol Consumption"):
            hours = alcoholConsumption
            earliestHour = earliestDrink
            
        for i in range (earliestHour, goalDuration, -1):
            goalMet = True
            entered = False
            for j in range(i, i - goalSpan, -1):
                entered = True
                goalStart = i
                goalEnd   = i - goalDuration
                total = 0
                if j - goalSpan <= 0:
                    continue
                for k in range(j, j - goalSpan, -1):
                    day = (date.today() - timedelta(days=k)).strftime("%Y-%m-%d")
                    try:
                        qualityGiven =  qualityNeeded and quality[day] == "Quality"
                    except:
                        #print("error1")
                        pass
                    try:
                        if (not qualityNeeded
                        or      qualityGiven): #!!!!!!!!!!!!!
                            total += int(hours[day])
                    except Exception as e:
                        #print("error2")
                        pass
                if (total > goalFigure and     max
                or  total < goalFigure and not max):
                    goalMet = False
            if (goalMet and entered):
                date1 = (date.today() - timedelta(days=goalStart)).strftime("%Y-%m-%d")
                date2 = (date.today() - timedelta(days=goalEnd  )).strftime("%Y-%m-%d")
                if (date1 == date2):
                    print(goalStart)
                    print(goalEnd)
                    print("woah")
                windowMessage += "\nGoal met from " + str(date1) + " to " + str(date2)
                break
            elif goalMet:
                goalMet = False

        if not goalMet:
            windowMessage += "\nGoal not met"

        return windowMessage + "\n"

        #########################del?
        monitoredDates = {} #LocalDate[]
        monitoredStat  = {} #int[]
        sleepQuality   = {} #String[]
        max = True
        qualityNeeded = False
        if (goalType == "Maximum Sleep" or goalType == "Minimum Sleep" or goalType == "Minimum Quality Sleep"): #!!!!!!
            sleeps = self.getSleeps() #Sleep[]
            monitoredDates = [" "] * len(sleeps)
            monitoredStat  = [0]   * len(sleeps)
            sleepQuality   = [" "] * len(sleeps)
            for i in range (0, len(monitoredDates), 1):
                monitoredDates[i] = sleeps[i].getDate()
                monitoredStat[i]  = sleeps[i].getDuration()
                sleepQuality[i]   = sleeps[i].getQuality()
            if (goalType == "Minimum Sleep" or goalType == "Minimum Quality Sleep"):
                max = False
                if (goalType == "Minimum Quality Sleep"):
                    qualityNeeded = True
        else:
            drinks = self.getDrinks() #AlcoholConsumption[]
            monitoredDates = [" "] * len(drinks)
            monitoredStat  = [0] * len(drinks)
            sleepQuality   = [" "] * len(drinks)
            for i in range (0, len(monitoredDates), 1):
                monitoredDates[i] = drinks[i].getDate()
                monitoredStat[i]  = drinks[i].getQuantity()

        statsLen = len(monitoredStat)

        windowMessage = "Goal: " + goalType + " of " + str(goalFigure) + " per " + str(goalSpan) + " days, for " + str(goalDuration) + " days"
        notMet = True

        lateValid = -2
        earlyValid = -1

        notMet = True

        for i in range (statsLen - 1, goalSpan - 1, -1):
            total = 0
            minIndex = i - goalSpan + 1
            for j in range (i, minIndex - 1, -1):
                if (not qualityNeeded
                or sleepQuality[j] == "Quality"): #!!!!!!
                    total += monitoredStat[j]
            if (total <= goalFigure and     max
            or  total >= goalFigure and not max):
                earlyValid = minIndex
                if lateValid == -2:
                    lateValid = i
            else:
                earlyValid = -1
                lateValid = -2
            if (lateValid - earlyValid) >= goalDuration - 1:
                windowMessage += "\nGoal met from " + str(monitoredDates[earlyValid]) + " to " + str(monitoredDates[lateValid])
                notMet = False
                break
        if notMet:
            windowMessage += "\nGoal not met"   
        return windowMessage + "\n"
        #DELETE GOALS THAT HAVE BEEN MET

    #may be able to delete this
    def intInputPositive(self, output):
        num = input(output)
        validEntry = True
        num = num.strip()
        validNums = "0123456789"
        allZeros = True
        for digit in num:
            if (not validNums.contains(digit)):
                validEntry = False
                break
            if (digit != '0'):
                allZeros = False
        if ((not validEntry) or allZeros):
            print("Input is invalid, please try again")
            if (allZeros):
                print("Number of days can't be 0")
            return -1
        intNum = -1
        try:
            intNum = int(num)
        except:
            return -1
        return intNum

    def cleanseDict(self, dict): #ensure dictionary is formatted correctly
        keysToDel = []
        for key in dict.keys():
            if len(key) != 10:
                keysToDel.append(key)
                continue
            word = ""
            for char in dict[key]:
                if not (char == ' ' or char == '\"'):
                    word += char
            dict[key] = word
        for key in keysToDel:
            del dict[key]
        return dict
    def getHours(self): 
        csvGet = CSVReader()
        csvGet.read(self.dataFilename)
        hours = getattr(csvGet, "hours")
        return self.cleanseDict(hours)
    def getQualities(self):
        csvGet = CSVReader()
        csvGet.read(self.dataFilename)
        qualities = getattr(csvGet, "quality")
        return self.cleanseDict(qualities)
    def getDrinks(self):
        csvGet = CSVReader()
        csvGet.read(self.dataFilename)
        drinks = getattr(csvGet, "alcohol")
        return self.cleanseDict(drinks)


#goalMan = GoalManager()
#goalMan.trackProgress()

# to ask:
# Different things that quality can be stored as


