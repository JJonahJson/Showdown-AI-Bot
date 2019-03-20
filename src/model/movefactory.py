from singlemove import SingleMove
from multiplemove import MultipleMove

class MoveFactory:
    subclasses = {
        'normal': SingleMove,
        'multiple': MultipleMove
    }

    def CreateMove(target, moveName:str, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType):

        return MoveFactory.subclasses[target](moveName, 
        moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType)

