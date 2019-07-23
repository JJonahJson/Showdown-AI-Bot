from src.model.move import SingleMove
from src.model.pokemon import Pokemon


class DamageTracker:

    def __init__(self):
        self.tracker = {}

    def add_damage(self, caster_pokemon: Pokemon, damage_perc, move: SingleMove, target_pokemon: Pokemon):
        """Method that add an entry in the tracker
        :param caster_pokemon: Pokemon that use the move
        :param damage_perc: Damage in %
        :param move: The move
        :param target_pokemon: Target pokemon
        :return:
        """
        self.tracker[(caster_pokemon.name, move.move_name, target_pokemon.name)] = damage_perc

    def get_damage(self, caster_pokemon: Pokemon, move: SingleMove, target_pokemon: Pokemon):
        """Method that retrieve the % damage
        :param caster_pokemon: pokemon that use the move
        :param target_pokemon: pokemon that receive the move
        :param move: move obj
        :return:
        """
        return self.tracker.get((caster_pokemon.name, move.move_name, target_pokemon.name), -1)

    def remove_caster(self, caster_pokemon: Pokemon):
        """Remove an entry for the caster pokemon use this in case of buff of pokemon_bot or debuff of enemy
        :param caster_pokemon: caster pokemon
        :return:
        """
        keys = [key for key in self.tracker.keys() if key[0] == caster_pokemon.name]
        for key in keys:
            self.tracker.pop(key)

    def remove_target(self, target_pokemon: Pokemon):
        """Remove an entry for the target pokemon use this in case of buff of pokemon_oppo or debuff of bot
        :param target_pokemon:
        :return:
        """
        keys = [key for key in self.tracker.keys() if key[2] == target_pokemon.name]
        for key in keys:
            self.tracker.pop(key)

    def clear_tracks(self):
        """Clears the dict
        :return:
        """
        self.tracker.clear()