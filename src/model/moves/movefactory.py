from singlemove import SingleMove
from multiplemove import MultipleMove

class MoveFactory:
    subclasses = {
        'single': SingleMove,
        'multiple': MultipleMove
    }

    def CreateMove(target, moveName:str, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType,
        onUser, onTarget):

        return MoveFactory.subclasses[target](moveName, 
        accuracy, basePower, category,
        pp, priority,
        isZ, critRatio, moveType,
        onUser, onTarget)
