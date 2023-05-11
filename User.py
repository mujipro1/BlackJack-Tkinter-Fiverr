'''
Module for User class
'''

class Users:
    def __init__(self) -> None:
        '''Initialize a list of users'''
        self.users = []
        self.readFromFile()

    def addUser(self, user) -> None:
        '''Add a user to the list'''
        self.users.append(user)
    
    def getUsers(self) -> list:
        '''Return the list of users'''
        return self.users

    def writeToFile(self):
        '''Write the users to a file'''
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f'{user.getName()},{user.getScore()},{user.getWins()},{user.getLosses()},{user.getDraws()}\n')
        
    def readFromFile(self):
        '''Read the users from a  file'''
        with open('users.txt', 'r') as file:
            for line in file:
                name, score, wins, losses, draws = line.strip().split(',')
                user = User(name)
                user.score = int(score)
                user.wins = int(wins)
                user.losses = int(losses)
                user.draws = int(draws)
                self.users.append(user)
        
class User:
    def __init__(self, name) -> None:
        '''Initailize a user '''
        self.name = name
        self.score = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
    
    def getName(self) -> str:
        '''Return name'''
        return self.name
    
    def gameWon(self, score) -> None:
        '''Increment wins and score'''
        self.wins += 1
        self.score += score

    def gameLost(self, score) -> None:
        '''Increment losses'''
        self.losses += 1
        self.score += score

    def gameDraw(self, score) -> None:
        '''Increment draws'''
        self.draws += 1
        self.score += score

    def getScore(self) -> int:
        '''Return score'''
        return self.score

    def getWins(self) -> int:
        '''Return wins'''
        return self.wins

    def getLosses(self) -> int:
        '''Return losses'''
        return self.losses
    
    def getDraws(self) -> int:
        '''Return draws'''
        return self.draws
    
        