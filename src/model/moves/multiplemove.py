from move import Move

class MultipleMove(Move):

    def __init__(self, moveName:str, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType,
        onUser, onTarget):
        Move.__init__(self, moveName, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType,
        onUser, onTarget)

    
    def invokeMove(self, pokemons):
        pass