from pokemon import Pokemon
from moves.move import Move

class DamageCalculator:

    @staticmethod
    def calculate(user:Pokemon, move:Move, target:Pokemon) -> int:
        baseDamage = (((10 + user.level*2) * user.attack + move.basePower) / 250 * target.defense) + 2
        # TODO Need efficacia STAB modificatori and N [0.85-1.00]
        return baseDamage


class TypeMultiplier:

    
