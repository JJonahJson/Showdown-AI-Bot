from pokemon import Pokemon
from moves.move import Move
from pokemontype import PokemonType as t


class DamageCalculator:

    @staticmethod
    def calculate(user:Pokemon, move:Move, target:Pokemon) -> int:
        baseDamage = (((10 + user.level*2) * user.attack + move.basePower) / 250 * target.defense) + 2
        # TODO Need efficacia STAB modificatori and N [0.85-1.00]
        return baseDamage


class TypeMultiplier:
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

    strongTo = {

    }
    ineffectiveTo = {}
    
