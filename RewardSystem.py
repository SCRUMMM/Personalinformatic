"""
RewardSystem for CM12005 coursework by Liam O'Connor

Awards points for sleeping well, drinking little and for unlocking acheivements
Pop-up window displays points earned and how they were earned

A bronze/silver/gold trophy jpg may be displayed depending on how many points have been earned

Example Usage:
rs = RewardSystem()
rs.redeemRewards()
"""

from CSVReader import CSVReader
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, date, timedelta

class RewardSystem:
    def __init__(self, recordsFilePath) -> None:
        self.points = 0
        self.fPath = recordsFilePath
    def redeemRewards(self):

        self.awardPoints()
        generalPoints = self.points
        messages = "Points earned: \n\n"
        messages += str(self.points) + " points awarded for sleeping well and drinking less over the past 30 days\n\n"
        messages += self.acheivements()
        messages += str(self.points - generalPoints) + " points awarded for acheivements in total\n\n"
        messages += "Point total: " + str(self.points) + "\n"
        window = tk.Tk()
        label = tk.Label(window, text = messages)
        label.pack()

        def collapseWindow():
            window.destroy()

        trophyFile = ""
        cap = "Earn more points to earn trophies!"
        if self.points > 900:
            trophyFile = "gold.jpg"
            cap = "You earned a gold trophy! Congratulations!"
        elif self.points > 650:
            trophyFile = "silver.jpg"
            cap = "You earned a silver trophy! Well done!"
        elif self.points > 400:
            trophyFile = "bronze.jpg"
            cap = "You earned a bronze trophy! Keep it up!"
        if trophyFile != "":
            trophy = Image.open(trophyFile)
            trophy = trophy.resize((100,150))
            photo = ImageTk.PhotoImage(trophy)
            trophyLab = tk.Label(window, image=photo)
            trophyLab.pack()
        caption = tk.Label(window, text = "\n" + cap + "\n")
        caption.pack()

        closeButton = tk.Button(window, text = "Exit", command = collapseWindow)
        closeButton.pack()

        blank = tk.Label(window, text = "\n")
        blank.pack()

        window.mainloop()

        
    def awardPoints(self):
        # points only awarded for last 30 days
        # 1 point for every hour of sleep, up to 9 per day, then take away one for every extra hour slept
        # 5 extra points for a night of quality of sleep (>= 2 hours of rem sleep)
        # 5 extra points for 7-9 hours of sleep
        # 5 points awarded for less than 15 units of alcohol drunk in a day
        # 5 extra points for 0 units of alcohol drunk in a day

        hours = self.getHours()
        alcoholConsumption = self.getDrinks()
        rem = self.getQualities()
        #today = date.today().strftime("%Y-%m-%d")

        for i in range(30, 0, -1):
            day = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")
            try:
                thisHours = int(hours[day])
                if thisHours <= 9:
                    self.points += thisHours
                else:
                    self.points += 9
                    self.points -= (thisHours - 9)
                if 7 <= thisHours and thisHours <= 9:
                    self.points += 5
            except:
                pass
            try:
                thisQuality = rem[day]
                if thisQuality >= 2: #!!!!!!!!!!!!!!
                    self.points += 5
            except:
                pass
            try:
                thisDrink = int(alcoholConsumption[day])
                if thisDrink < 15:
                    self.points += 5
                if thisDrink == 0:
                    self.points += 5
            except:
                pass

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

    def acheivements(self):
        #Acheivement: Sleep between 7 and 9 hours a night for 10/100/365 consecutive days
        hours = self.getHours()
        alcoholConsumption = self.getDrinks()
        rem = self.getQualities()

        earliest = self.dateToDaysAgo(self.earliestDateInKeys(hours))
        earliestDrink = self.dateToDaysAgo(self.earliestDateInKeys(alcoholConsumption))
        if earliestDrink < earliest:
            earliest = earliestDrink
        
        message = ""
        currentConsecutiveGoodSleeps = 0
        mostConsecutiveGoodSleeps = 0
        for i in range (earliest, 0, -1):
            day = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")
            try:
                if 7 <= hours[day]  and hours[day] <= 9:
                    currentConsecutiveGoodSleeps += 1
                else:
                    raise Exception("")
            except:
                if mostConsecutiveGoodSleeps < currentConsecutiveGoodSleeps:
                    mostConsecutiveGoodSleeps = currentConsecutiveGoodSleeps
                currentConsecutiveGoodSleeps = 0
        if mostConsecutiveGoodSleeps < currentConsecutiveGoodSleeps:
            mostConsecutiveGoodSleeps = currentConsecutiveGoodSleeps
        if mostConsecutiveGoodSleeps >= 10:
            message += "Acheivement Unlocked: Sleep between 7 and 9 hours a night for 10 days in a row\nReward: 30 points\n"
            self.points += 30
            if mostConsecutiveGoodSleeps >= 100:
                message += "Acheivement Unlocked: Sleep between 7 and 9 hours a night for 100 days in a row\nReward: 50 points\n"
                self.points += 50
                if mostConsecutiveGoodSleeps >= 365:
                    message += "Acheivement Unlocked: Sleep between 7 and 9 hours a night every day for a year\nReward: 100 points\n"
                    self.points += 100
        #Acheivement: Drink less than 40/20 units of alcohol in a week
        leastUnitsInAWeek  = earliest * 1000
        for i in range (1, earliest - 5, 1):
            units = 0
            for drink in range (i, i+7, 1):
                day = (date.today() - timedelta(days=drink)).strftime("%Y-%m-%d")
                try:
                    units += alcoholConsumption[day]
                except:
                    units += leastUnitsInAWeek
            if units < leastUnitsInAWeek:
                leastUnitsInAWeek = units
        if leastUnitsInAWeek < 40:
            message += "Acheivement Unlocked: Drink less than 40 units of alcohol over the span of a week\nReward: 40 points\n"
            self.points += 40
            if leastUnitsInAWeek < 20:
                message += "Acheivement Unlocked: Drink less than 20 units of alcohol over the span of a week\nReward: 60 points\n"
                self.points += 60
        #Acheivement: Get quality sleep for 10/20/30 days in a month (30-day period)
        mostQualitySleeps = 0
        for i in range (earliest, 30, -1):
            goodSleeps = 0
            for sleep in range (i, i-30, -1):
                day = (date.today() - timedelta(days=sleep)).strftime("%Y-%m-%d")
                try:
                    if rem[day] >= 2: # "Quality" is placeholder !!!!!!!!!!!!!!!!!!
                        goodSleeps += 1
                except:
                    pass
            if goodSleeps > mostQualitySleeps:
                mostQualitySleeps = goodSleeps
        if mostQualitySleeps >= 10:
            message += "Acheivement Unlocked: Get 10 days of quality sleep (at least 2 hours of REM per day) in a month\nReward: 30 points\n"
            self.points += 30
            if mostQualitySleeps >= 20:
                message += "Acheivement Unlocked: Get 20 days of quality sleep (at least 2 hours of REM per day) in a month\nReward: 50 points\n"
                self.points += 50
                if mostQualitySleeps >= 30:
                    message += "Acheivement Unlocked: Get 30 days of quality sleep (at least 2 hours of REM per day) in a month\nReward: 100 points\n"
                    self.points += 100
        return message

    def cleanseDict(self, dict): #ensure dictionary is formatted correctly
        keysToDel = []
        for key in dict.keys():
            if len(key) != 10:
                keysToDel.append(key)
                continue
            word = ""
            try:
                for char in dict[key]:
                    if not (char == ' ' or char == '\"'):
                        word += char
                dict[key] = word
            except:
                pass
        for key in keysToDel:
            del dict[key]
        return dict
    def getHours(self): 
        csvGet = CSVReader()
        csvGet.read(self.fPath)
        hours = getattr(csvGet, "asleep")
        return self.cleanseDict(hours)
    def getQualities(self):
        csvGet = CSVReader()
        csvGet.read(self.fPath)
        qualities = getattr(csvGet, "rem")
        return self.cleanseDict(qualities)
    def getDrinks(self):
        csvGet = CSVReader()
        csvGet.read(self.fPath)
        drinks = getattr(csvGet, "alcohol")
        return self.cleanseDict(drinks)


