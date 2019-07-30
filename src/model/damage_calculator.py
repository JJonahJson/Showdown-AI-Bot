from random import uniform

from model.move_type import MoveCategory
from model.pokemon_type import TypeMultiplier
from model.status_type import StatusType
from model.weather_type import WeatherModifiers, FieldModifiers


class DamageCalculator:
    """This class contains a static method for damage calculation"""

    # Pokemon1 assumiamo sia bot
    # Pokemon2 assumiamo sia oppo
    @staticmethod
    def weak_to(pokemon1_type, pokemon2_type):
        return pokemon2_type in TypeMultiplier.weakTo[pokemon1_type]

    @staticmethod
    def resists_to(pokemon1_type, pokemon2_type):
        return pokemon2_type in TypeMultiplier.resistsTo[pokemon1_type]

    @staticmethod
    def immune_to(pokemon1_type, pokemon2_type):
        return pokemon2_type in TypeMultiplier.immuneTo[pokemon1_type]

    @staticmethod
    def calculate(weather, terrain, user, move, target) -> int:
        """Method to predict the damage
        :param weather: The current weather
        :param terrain: The current terrain
        :param user: The pokemon who casts the move
        :param move: The move object
        :param target: The target pokemon
        :return: An int that represents the predicted damage dealt
        """

        if move.category is MoveCategory.Status:
            return 0
        if DamageCalculator.immune_to(target.types[0], move.move_type) or \
                (len(target.types) > 1 and DamageCalculator.immune_to(target.types[1], move.move_type)):
            return 0

        else:
            base_damage = (((2*user.level +10)*user.stats.get_actual(move.scale_with)*move.calculate_base_power(
                user.types))/(
                    250*target.stats.get_actual(move.defends_on))+2)

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
        if user.non_volatile_status == StatusType.Brn and move.scale_with.name == "Atk":
            burn_multiplier = 0.5

        return int(base_damage * mult * terrain_mult * user.damage_output_multiplier * target.damage_input_multiplier *
                   roll * burn_multiplier)
