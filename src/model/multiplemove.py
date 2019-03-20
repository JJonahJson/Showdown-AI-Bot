from move import Move

class MultipleMove(Move):

    def __init__(self, moveName:str, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType):
        Move.__init__(self, moveName, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType)

    
    def invokeMove(self, pokemons):
        for pokemon in pokemons:
            self.moveEffect(pokemon)
