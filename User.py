"""
1) Login or register (register should create relevant files for new user)
2) Enter some sort of main loop where the user can say what they want to happen
3) Do what the user says 
"""

import hashlib
import CSVReader
import AlcoholConsumption
import GoalManager
import RewardSystem
import graphManager
import sleep

# TODO:
#   1) Put sleep data in class instance
#   2) Get sleep input and write to CSV file
#   3) Test

# Date,Alcohol Consumption (count),Sleep Analysis [Asleep] (hr),Sleep Analysis [In Bed] (hr),Sleep Analysis [Core] (hr),Sleep Analysis [Deep] (hr),Sleep Analysis [REM] (hr),Sleep Analysis [Awake] (hr) 

class User:
    def __init__(self):
        self.CSVReader = CSVReader.CSVReader()
        self.AlcoholConsumption = AlcoholConsumption.AlcoholConsumption()
        self.sleep = sleep.sleep()
        self.userFile = None
        self.GoalManager = None
        self.RewardSystem = None
        self.GraphManager = None

        self.loginOrRegister()
        self.mainLoop()

    def mainLoop(self):
        self.CSVReader.read(self.userFile)

        for key, value in self.getRawAlcoholData().items():
            self.AlcoholConsumption.record(key[:10], value)

        #for column in self.getRawSleepData():
         #   for key, value in column:
          #      self.sleep

        while True:
            action = input("Enter 'a' to add alcohol data, 's' to add sleep data, 'g' to access your goals, 'r' to access your rewards, 'p' to plot graphs, or 'e' to exit: ")
            while action not in ['a', 'g', 'r', 'p', 'e']:
                action = input("Enter 'a' to add alcohol data, 'g' to access your goals, 'r' to access your rewards, or 'e' to exit: ")

            if action == 'a':
                self.enterNewAlcoholData()
            elif action == 's':
                self.enterNewSleepData()
            elif action == 'g':
                inp = input("Enter 's' to set new goals, or 'p' to see your progress: ")
                while inp not in ['s', 'p']:
                    inp = input("Enter 's' to set new goals, or 'p' to see your progress: ")
                if inp == 's':
                    self.GoalManager.setGoals()
                else:
                    self.GoalManager.trackProgress()
            elif action == 'r':
                self.RewardSystem.redeemRewards()
                with open(self.username+"Points.txt", 'w') as f:
                    f.write(str(self.RewardSystem.points))
            elif action == 'p':
                self.GraphManager.plot_graphs()
            else:
                exit()
    
    def enterNewSleepData(self):
        pass

    def enterNewAlcoholData(self):
        date = input("Enter the date in format YYYY-MM-DD: ")
        quantity = int(input("Enter the number of units you had: "))

        if date in self.AlcoholConsumption.consumption_record.keys():
            self.AlcoholConsumption.record(date, quantity)
            
            with open(self.userFile, 'r') as f:
                raw = f.readlines()
            
            for row in raw:
                if row[:19] == date + " 00:00:00":
                    currentRow = row.split(',')
                    break
            
            currentRow[1] = str(quantity)
            currentRow = ",".join(currentRow)
            
            newRaw = []
            for row in raw:
                if row[:19] == date + " 00:00:00":
                    currentRow = row.split(',')
                    currentRow[1] = str(quantity)
                    currentRow = ",".join(currentRow)
                    newRaw.append(currentRow)
                else:
                    newRaw.append(row)

            with open(self.userFile, 'w') as f:
                f.write("".join(newRaw))

        else:
            self.AlcoholConsumption.record(date, quantity)
            with open(self.userFile, 'a') as f:
                f.write("\n"+date+" 00:00:00,"+str(quantity)+",0,0,0,0,0,0,")

    def loginOrRegister(self):
        self.credentialsFile = "credentials.txt"
        self.username = None
        x = ''
        while x not in ['l', 'r']:
            x = input("Enter 'l' to login or 'r' to register a new account: ")
        if x == 'l':
            self.login()
        else:
            self.register()

    def getRawSleepData(self):
        #data = self.CSVReader.dicts[1:] # self.asleep, self.in_bed, self.core, self.deep, self.rem, self.awake
        #dataDict = {}
        #for key, value in data[0]:
            #dataDict[key] = [value]
        
        #for i in range(1, 6):
        pass


    def getRawAlcoholData(self):
        return self.CSVReader.alcohol

    def login(self):
        username = input("Enter your username: ")
        password = hashString(input("Enter your password: "))

        while not self.check(username, password):
            print("Invalid credentials.\n")
            username = input("Enter your username: ")
            password = hashString(input("Enter your password: "))

        self.username = username
        self.userFile = username + "Data.csv"
        self.GoalManager = GoalManager.GoalManager(username + "Goals.txt", self.userFile)
        with open(username+"Points.txt", 'r') as f:
            points = int(f.read())
        self.RewardSystem = RewardSystem.RewardSystem(points, self.userFile)
        self.GraphManager = graphManager.GraphManager(self.userFile)

    def check(self, username, password):
        with open(self.credentialsFile, 'r') as f:
            raw = [x.strip('\n').split(',') for x in f.readlines()]
        for line in raw:
            if username == line[0]:
                if password == line[1]:
                    return True
                return False
        return False

    def register(self):
        username = input("Enter your username: ")
        password = hashString(input("Enter your password: "))

        with open(self.credentialsFile, 'r+') as f: # move while outside open
            raw = f.read()
            while username in [x.split(',')[0] for x in raw.split("\n")]:
                print("Username already taken.\n")
                username = input("Enter your username: ")
                password = hashString(input("Enter your password: "))
            f.write(username+','+password+'\n')

        self.username = username
        self.userFile = username + "Data.csv"
        with open(username + "Goals.txt", 'w') as f:
            f.write("")
        self.GoalManager = GoalManager.GoalManager(username + "Goals.txt", self.userFile)
        with open(username + "Points.txt", 'w') as f:
            f.write("0")
        self.RewardSystem = RewardSystem.RewardSystem(0, self.userFile)
        self.GraphManager = graphManager.GraphManager(self.userFile)

def hashString(string):
    return hashlib.md5(string.encode()).hexdigest()

user = User()
