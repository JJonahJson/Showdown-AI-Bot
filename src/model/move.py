from abc import ABC


class Move(ABC):
    """This class represents a move of a pokemon
    Args:
        moveName (str): The name of the move
        moveEffect Function: the effect of the move
        accuracy (int) or (bool): The accuracy of the move, if true the move is secured to hit.
        basePower (int): The base power of the move
        category (str): Physical if the move is a physical move or special if is a special one
        pp (int): Power points of a move
        priority (int): The level of a priority of the move
        isZ (bool): If the move is Z
        critRatio (int): Critical ratio of the move
        target (str): Which targets are possble in the move
        moveType (str): Type of the move
    """
    
    def __init__(self, moveName:str, moveEffect, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType):

        self.moveName = moveName
        self.moveEffect = moveEffect
        self.accuracy = accuracy
        self.basePower = basePower
        self.category = category
        self.pp = pp
        self.priority = priority
        self.isZ = isZ
        self.critRatio = critRatio
        self.moveType = moveType
    
    """
    Args:
        pokemon(Pokemon): the target of the move
    """
    def invokeMove(self, pokemon):
        pass

