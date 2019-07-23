from random import uniform

from src.model.field import Weather as w, Field as f
from src.model.pokemontype import PokemonType as t
from src.model.stats import StatsType
from src.model.status import StatusType
from src.model.move import MoveCategory


class TypeMultiplier:
    """
    Dictionaries that contains type relations
    PokemonType: MoveType

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
        t.Normal: [],
        t.Fire: [t.Fire, t.Grass, t.Ice, t.Bug, t.Steel, t.Fairy],
        t.Water: [t.Fire, t.Water, t.Ice, t.Steel],
        t.Electric: [t.Electric, t.Flying, t.Steel],
        t.Grass: [t.Water, t.Electric, t.Grass, t.Ground],
        t.Ice: [t.Ice],
        t.Fighting: [t.Bug, t.Rock, t.Dark],
        t.Poison: [t.Grass, t.Fighting, t.Poison, t.Bug, t.Rock, t.Dark],
        t.Ground: [t.Poison, t.Rock],
        t.Flying: [t.Ground, t.Grass, t.Bug],
        t.Psychic: [t.Fighting, t.Psychic],
        t.Bug: [t.Grass, t.Fighting, t.Ground],
        t.Rock: [t.Normal, t.Fire, t.Poison, t.Flying],
        t.Ghost: [t.Poison, t.Bug],
        t.Dragon: [t.Fire, t.Grass, t.Water],
        t.Dark: [t.Ghost, t.Dark],
        t.Steel: [t.Normal, t.Grass, t.Ice, t.Flying, t.Psychic, t.Bug, t.Rock, t.Dragon, t.Steel, t.Fairy],
        t.Fairy: [t.Fighting, t.Bug, t.Dark]
    }
    immuneTo = {
        t.Normal: [t.Ghost],
        t.Fire: [],
        t.Water: [],
        t.Electric: [],
        t.Grass: [],
        t.Ice: [],
        t.Fighting: [],
        t.Poison: [],
        t.Ground: [t.Electric],
        t.Flying: [t.Ground],
        t.Psychic: [],
        t.Bug: [],
        t.Rock: [],
        t.Ghost: [t.Normal, t.Fighting],
        t.Dragon: [],
        t.Dark: [t.Psychic],
        t.Steel: [t.Poison],
        t.Fairy: [t.Dragon]
    }


class WeatherModifiers:
    """This class contains a static dict for the weather multipliers"""
    modifiers = {
        (t.Water, w.Raindance): 1.5,
        (t.Water, w.Sunnyday): 0.5,
        (t.Fire, w.Raindance): 0.5,
        (t.Fire, w.Sunnyday): 2,
        (t.Electric, w.Wind): 0.5,
        (t.Ice, w.Wind): 0.5,
        (t.Rock, w.Wind): 0.5
    }


class FieldModifiers:
    modifiers = {
        (t.Psychic, f.Psychic): 1.5,
        (t.Electric, f.Electric): 1.5,
        (t.Grass, f.Grass): 1.5
    }


class DamageCalculator:
    """This class contains a static method for damage calculation"""

    @staticmethod
    def calculate(weather: w, terrain, user, move, target) -> int:

        if move.category is MoveCategory.Status:
            return 0
        if target.types in TypeMultiplier.immuneTo[move.move_type]:
            return 0
        else:
            base_damage = (((10 + user.level * 2) * user.stats.get_actual(move.scale_with) + move.calculate_base_power(
                user.types))
                           / 250 *
                           target.stats.get_actual(move.defends_on)) + 2

        # Try to get the multiplier based on the weather, if is not in the dict get '1'
        mult = WeatherModifiers.modifiers.get((weather, move.move_type), 1)
        terrain_mult = FieldModifiers.modifiers.get((move.move_type, terrain), 1)

        roll = uniform(0.85, 1)

        # Multiple calculation
        for pkmn_type in target.types:
            if move.move_type in TypeMultiplier.weakTo[pkmn_type]:
                mult *= 2
            elif move.move_type in TypeMultiplier.resistsTo[pkmn_type]:
                mult *= 0.5

        burn_multiplier = 1
        if user.non_volatile_status == StatusType.Brn and move.scale_with == StatsType.Atk:
            burn_multiplier = 0.5

        return int(base_damage * mult * terrain_mult * user.damage_output_multiplier * target.damage_input_multiplier *
                   roll * burn_multiplier)
