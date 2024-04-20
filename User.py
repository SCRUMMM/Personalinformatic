import hashlib
import CSVReader
import AlcoholConsumption
#import Sleep

# TODO:
#   1) Put sleep data in class instance
#   2) Get input and write to CSV file
#   3) Integrate reward system
#   4) Integrate goal manager
#   5) Main loop options

# Date,Alcohol Consumption (count),Sleep Analysis [Asleep] (hr),Sleep Analysis [In Bed] (hr),Sleep Analysis [Core] (hr),Sleep Analysis [Deep] (hr),Sleep Analysis [REM] (hr),Sleep Analysis [Awake] (hr) 

class User:
    def __init__(self):
        self.CSVReader = CSVReader.CSVReader()
        self.AlcoholConsumption = AlcoholConsumption.AlcoholConsumption()
        #self.Sleep = Sleep.sleep()
        self.userFile = None

        self.loginOrRegister()
        self.mainLoop()

    def mainLoop(self):
        self.CSVReader.read(self.userFile)

        for key, value in self.getRawAlcoholData().items():
            self.AlcoholConsumption.record(key[:10], value)

        while True:
            action = input() # what should i do?
            # do stuff

    def enterNewAlcoholData(self):
        date = input("Enter the date in format YYYY-MM-DD: ")
        quantity = int(input("Enter the number of units you had: "))

        if date in self.AlcoholConsumption.consumption_record.keys():
            self.AlcoholConsumption.record(date, quantity)
            # edit existing row
        else:
            self.AlcoholConsumption.record(date, quantity)
            # add new row
            with open(self.userFile, 'a') as f:
                f.write(date+" 00:00:00,"+str(quantity)+",0,0,0,0,0,0,")


        


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
        return self.CSVReader.dicts[1:] # self.asleep, self.in_bed, self.core, self.deep, self.rem, self.awake

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


def hashString(string):
    return hashlib.md5(string.encode()).hexdigest()

user = User()
