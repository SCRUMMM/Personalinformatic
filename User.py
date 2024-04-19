import hashlib
import CSVReader
import AlcoholConsumption

# TODO:
#   1) Read CSV file for sleep and alcohol data using CSV reader
#   2) Get input and write to CSV file
#   3) Integrate reward system
#   4) Integrate goal manager


class User:
    def __init__(self):
        self.CSVReader = CSVReader.CSVReader()
        self.AlcoholConsumption = AlcoholConsumption.AlcoholConsumption()
        self.alcoholFile = None
        self.sleepFile = None
        self.sleepRecords = None

        self.loginOrRegister()
        self.mainLoop()

    def mainLoop(self):
        with open(self.alcoholFile, "r") as f:
            pass
        
        with open(self.sleepFile, "r") as f:
            pass

        while True:
            action = input() # what should i do?
            # do stuff

    def enterNewAlcoholData(self):
        # write new alcohol data
        pass

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
        pass

    def getRawAlcoholData(self):
        pass

    def login(self):
        username = input("Enter your username: ")
        password = hashString(input("Enter your password: "))

        while not self.check(username, password):
            print("Invalid credentials.\n")
            username = input("Enter your username: ")
            password = hashString(input("Enter your password: "))

        self.username = username
        self.alcoholFile = self.username + "Alcohol.txt"
        self.sleepFile = self.username + "Sleep.txt"
        # should set self.userFile to the CSV file containing this users' data

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

        self.alcoholFile = self.username+"Alcohol.txt"
        self.sleepFile = self.username+"Sleep.txt"


def hashString(string):
    return hashlib.md5(string.encode()).hexdigest()

user = User()
