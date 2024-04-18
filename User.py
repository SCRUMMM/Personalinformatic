import hashlib
import CSVReader
import AlcoholConsumption
import json

class User:
    def __init__(self):
        self.CSVReader = CSVReader.CSVReader()
        self.AlcoholConsumption = AlcoholConsumption.AlcoholConsumption()
        self.userAlcoholFile = None

        self.loginOrRegister()
        self.mainLoop()

    def mainLoop(self):
        # Or maybe AlcoholConsumption class could be serialised and stored in a normal text file?
        self.AlcoholConsumption
        with open(self.userAlcoholFile, "r") as f:
            self.AlcoholConsumption.consumption_record = json.loads(f.read())
        
        while True:
            action = input() # what should i do?
            # do stuff

    def enterNewAlcoholData(self):
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
        self.userAlcoholFile = self.username + "Alcohol.json"
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

        newAlcoholConsumption = AlcoholConsumption.AlcoholConsumption()
        serialised = json.dumps(newAlcoholConsumption.__dict__)
        self.userAlcoholFile = self.username+"Alcohol.json"
        with open(self.userAlcoholFile, 'w') as f:
            f.write(serialised)


def hashString(string):
    return hashlib.md5(string.encode()).hexdigest()

user = User()
