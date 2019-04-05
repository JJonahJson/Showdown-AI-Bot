class Action():

    POKEMON = 0
    MOVE = 1
    TARGET = 2
    PLAYER = 3

    def __init__(self, pokemon, move, target, player):
        self.action = (pokemon, move, target, player)

    def __lt__(self, otherAction):
        if self.action[Action.MOVE] < otherAction.action[Action.MOVE]:
            return True
        else:
            return self.action[Action.POKEMON] < otherAction[Action.POKEMON]

class Game():

    triggerAtTurnStarts = []
    triggerAtTurnEnds = []

    def __init__(self, battlefield):
        self.battlefield = battlefield
        self.turnCounter = 1

    def executeTurn(self, action1:list, action2:list):
        Game.triggerStart()
        moveTurn = sorted(action1 + action2)
        for pokemon, move, target, player in moveTurn:
            # TODO Modeling as index or using the objects?!
            self.battlefield.doMove(player, pokemon, move, target)
        self.turnCounter += 1
        Game.triggerEnd()
    
    # TODO Determinare i parametri dei trigger per queste funzioni "ad eventi" 
    @staticmethod
    def triggerStart():
        for function in Game.triggerAtTurnStarts:
            function()

    @staticmethod
    def triggerEnd():
        for function in Game.triggerAtTurnEnds:
            function()
        