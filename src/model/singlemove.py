from move import Move

class SingleMove(Move):

    def __init__(self, moveName:str, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType, onUser, onTarget):
        Move.__init__(self, moveName, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType, onUser, onTarget)

    
    def invokeMove(self, pokemon):
        self.moveEffect(pokemon)
