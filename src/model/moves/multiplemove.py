from move import Move

class MultipleMove(Move):

    def __init__(self, moveName:str, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType, onUser, onTarget):
        Move.__init__(self, moveName, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType, onUser, onTarget)

    
    def invokeMove(self, pokemons):
        for pokemon in pokemons:
            self.moveEffect(pokemon)
