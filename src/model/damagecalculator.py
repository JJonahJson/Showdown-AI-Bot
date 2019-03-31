from pokemon import Pokemon
from moves.move import Move
from pokemontype import PokemonType as t
from random import uniform
from field import Weather as w

class TypeMultiplier:

    """ Dictionaries that contains type relations
        Pokemon type: Move Type
    """
    weakTo = {
        t.Normal: [t.Fighting],
        t.Fire: [t.Water, t.Ground, t.Rock],
        t.Water: [t.Electric, t.Grass],
        t.Electric: [t.Ground],
        t.Grass: [t.Fire, t.Ice, t.Poison, t.Flying, t.Bug],
        t.Ice: [t.Fire, t.Fighting, t.Rock],
        t.Fighting: [t.Flying, t.Psychic, t.Fairy],
        t.Poison: [t.Ground, t.Psychic],
        t.Ground: [t.Water, t.Grass, t.Ice],
        t.Flying: [t.Electric, t.Ice, t.Rock],
        t.Psychic: [t.Bug, t.Dark, t.Ghost],
        t.Bug: [t.Fire, t.Flying, t.Rock],
        t.Rock: [t.Water, t.Grass, t.Fighting, t.Steel],
        t.Ghost: [t.Ghost, t.Dark],
        t.Dragon: [t.Dragon, t.Ice, t.Fairy],
        t.Dark: [t.Bug, t.Fighting, t.Fairy],
        t.Steel: [t.Fire, t.Fighting, t.Ground],
        t.Fairy: [t.Poison, t.Steel]
    }

    resistsTo = {
        t.Normal : [],
        t.Fire : [t.Fire, t.Grass, t.Ice, t.Bug, t.Steel, t.Fairy],
        t.Water : [t.Fire, t.Water, t.Ice, t.Steel],
        t.Electric : [t.Electric, t.Flying, t.Steel],
        t.Grass : [t.Water, t.Electric, t.Grass, t.Ground],
        t.Ice : [t.Ice],
        t.Fighting : [t.Bug, t.Rock, t.Dark],
        t.Poison : [t.Grass, t.Fighting, t.Poison, t.Bug, t.Rock, t.Dark],
        t.Ground : [t.Poison, t.Rock],
        t.Flying : [t.Ground, t.Grass, t.Bug],
        t.Psychic : [t.Fighting, t.Psychic],
        t.Bug : [t.Grass, t.Fighting, t.Ground],
        t.Rock : [t.Normal, t.Fire, t.Poison, t.Flying],
        t.Ghost : [t.Poison, t.Bug],
        t.Dragon : [t.Fire, t.Grass, t.Water],
        t.Dark : [t.Ghost, t.Dark],
        t.Steel : [t.Normal, t.Grass, t.Ice, t.Flying, t.Psychic, t.Bug, t.Rock, t.Dragon, t.Steel, t.Fairy],
        t.Fairy : [t.Fighting, t.Bug, t.Dark]
    }
    ineffectiveTo = {
        t.Normal : [t.Ghost],
        t.Fire : [],
        t.Water : [],
        t.Electric : [],
        t.Grass : [],
        t.Ice : [],
        t.Fighting : [],
        t.Poison : [],
        t.Ground : [t.Electric],
        t.Flying : [t.Ground],
        t.Psychic : [],
        t.Bug : [],
        t.Rock : [],
        t.Ghost : [t.Normal, t.Fighting],
        t.Dragon : [],
        t.Dark : [t.Psychic],
        t.Steel : [t.Poison],
        t.Fairy : [t.Dragon]
    }

"""This class contains a static dict for the weather multipliers
"""
class WeatherModifiers:
    modifiers = {
        (t.Water, w.Rain): 1.5,
        (t.Water, w.Sun): 0.5,
        (t.Fire, w.Rain): 0.5,
        (t.Fire, w.Sun): 2,
        (t.Electric, w.Wind):0.5,
        (t.Ice, w.Wind): 0.5,
        (t.Rock, w.Wind):0.5
    }

"""This class contains a static method for damage calculation
"""
class DamageCalculator:

    @staticmethod
    def calculate(weather:w, user:Pokemon, move:Move, target:Pokemon) -> int:

        if target.types in TypeMultiplier.ineffectiveTo[move.moveType]:
            return 0
        else:
            baseDamage = (((10 + user.level*2) * user.stats[move.scaleWith] + move.calculateBasePower()) / 250 * target.stats[move.defendsOn]) + 2

            mult = WeatherModifiers.modifiers[(move.moveType, weather)]
            roll = uniform(0.85, 1)

            # Multiple calculation
            for pkmnType in target.types:
                if move.moveType in TypeMultiplier.weakTo[pkmnType]:
                    mult *= 2
                elif move.MoveType in TypeMultiplier.resistsTo[pkmnType]:
                    mult *= 0.5

            return int(baseDamage * mult *  user.damageOutputMultiplier *  target.damageInputMultiplier * roll)

