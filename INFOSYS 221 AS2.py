import random
import json
                            #REQUIRES SnakeLadderJSON.json file to exist in the same DIRECTORY
class Game:
    def __init__(self, player1):
        self.playerOne = player1
        self.playerTwo = player("computer")
        self.endPosition = 25
        self.startSnakePositions = [] #int
        self.startLadderPositions = []  #int
        self.snakeArray = []    #snakes
        self.ladderArray = []   #ladders
        self.gameIsRunning = True

    def rollDice(self):
        diceRoll = random.randint(1, 6)
        print("you rolled a", diceRoll)
        return diceRoll

    def startGame(self):
        self.readJSON()                     #read JSON and populate arrays

        while self.gameIsRunning:                   #main game loop
            self.playTurn(self.playerOne)
            if self.checkWin():
                break

            self.playTurn(self.playerTwo)
            if self.checkWin():
                break

        return

    def EndGame(self, player):
        print(player.name, " has won!")
        return

    def checkWin(self):
        print("-------------------------")
        print(self.playerOne)
        print(self.playerTwo)
        print("-------------------------")

        #check player1
        if self.playerOne.boardPosition == self.endPosition:
            self.EndGame(self.playerOne)
            return True

        #check player2
        if self.playerTwo.boardPosition == self.endPosition:
            self.EndGame(self.playerTwo)
            return True
        return False

    def playTurn(self, player):
        while True:
            print()
            print(player)
            userInput = input("press enter to roll the dice! >>")
            if userInput == "":
                break

        rollDiceNumber = self.rollDice()
        player.move(rollDiceNumber)

        #if player lands on ladder
        if player.boardPosition in self.startLadderPositions:                           # use according ladder
            ladderPosIndex = self.startLadderPositions.index(player.boardPosition)      #get the index of that ladder in the startLadderPostions
            self.ladderArray[ladderPosIndex].useLadder(player)                          # use corrosponding ladder in ladderArray

        #if player lands on snake
        elif player.boardPosition in self.startSnakePositions:                          # use according snake
            snakePosIndex = self.startSnakePositions.index(player.boardPosition)        # get the index of that snake in the startSnakePositions
            self.snakeArray[snakePosIndex].useSnake(player)                             # use corrosponding ladder in SnakeArray

        #if player lands over 100
        if player.boardPosition > self.endPosition:                                     #if player is over 100, already moved over 100 at this point
            print("you have gone over the target!")
            player.boardPosition -= rollDiceNumber
            #player has already moved over target, moving player back to original position
            print("you have to land exactly at", self.endPosition)
            print("staying where your are!")

        print("player", player.name, "is at", player.boardPosition)

        return

    def readJSON(self):
        with open('SnakeLadderJSON.json') as json_file:
            data = json.load(json_file)
            self.populateArrays(data)
        return

    def populateArrays(self, data):
        for i in data['boardPosition']:
            startPos = i['position']
            endPos = i['moveTo']
            if startPos > endPos:                           #its a snake
                tempSnake = snake(startPos, endPos)         #create snake
                self.startSnakePositions.append(startPos)   #add startPost to startSnakePositions
                self.snakeArray.append(tempSnake)           #add snake object to snakeArray

            if endPos > startPos:                           #its a ladder
                tempLadder = ladder(startPos, endPos)       #create ladder
                self.startLadderPositions.append(startPos)  #add startPost to startLadderPositions
                self.ladderArray.append(tempLadder)         #add ladder object to ladderArray

        return

    def __str__(self):
        print()
        print("----- Game Settings ----")
        print("player:", self.playerOne.name, ", boardPosition:",self.playerOne.boardPosition)
        print("player:", self.playerTwo.name, ", boardPosition:",self.playerTwo.boardPosition)
        print("first to:", self.endPosition)
        print("-------------------------")
        print()
        return ""
#---------------------------------------------------------
class player:
    def __init__(self, name):
        self.name = name
        self.boardPosition = 0

    def move(self, steps):
        print("moving player", self.name, "steps...")
        self.boardPosition += steps
        return self.boardPosition

    def __str__(self):
        return "{} is at: {}".format(self.name,self.boardPosition)
#---------------------------------------------------------
class snake:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = start - end

    def useSnake(self, player):
        print("oh no,", player.name, "has landed on a Snake!")
        player.boardPosition -= self.length                             #this moves the player
        self.printSnake(player, self.start, self.end)
        return

    def printSnake(self, player, start, end):
        print(player.name,"has used snake from", start, "to", end)
        return
#---------------------------------------------------------
class ladder:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = end - start

    def useLadder(self, player):
        print("congrats!", player.name, "has landed on a Ladder!")
        player.boardPosition += self.length                             #this moves the player
        self.printLadder(player, self.start, self.end)
        return

    def printLadder(self, player, start, end):
        print(player.name, "has used ladder from", start, "to", end)
        return



#---------------------------------------------------------


print("welcome to snakes and ladders")
playerName = input("what is your name? \n >>")
print("starting game with a computer")

Game = Game(player(playerName))

print(Game)

Game.startGame()
print("Game has ended")
