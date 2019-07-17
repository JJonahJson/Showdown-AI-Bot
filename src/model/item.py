from src.model.stats import StatsType

from abc import ABC, abstractmethod


class Item(ABC):
    """
    Abstract class that represents a generic item in game.
    Args:
    name (str): Name of the item

    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def add_effect(self, pokemon):
        """Abstract method used to implement the effect of the item"""
        pass

    @abstractmethod
    def remove_effect(self, pokemon):
        """Abstract method used to remove the effect of the item"""
        pass

    @abstractmethod
    def add_lock(self, pokemon, move):
        """Abstract method for locking a pokemon on a move"""
        pass

    @abstractmethod
    def remove_lock(self, pokemon, move):
        """Abstract method for removing a lock from pokemon's moves"""
        pass

    @abstractmethod
    def activate(self, pokemon):
        """Abstract method for the berry item"""
        pass


class StatsItem(Item):
    """
    Class used to represent an item that affect the stats of a pokemon
    Args:
    name (str): name of the item
    statsType (StatsType): the stat that it affects
    value (float): Multiplier of the stat

    """

    def __init__(self, name, stats_type, value: float):
        super().__init__(name)
        self.stats_type = stats_type
        self.value = value

    def add_effect(self, pokemon):
        pokemon.stats.increase_volatile_mul(self.stats_type, self.value)

    def remove_effect(self, pokemon):
        pokemon.stats.decrease_volatile_mul(self.stats_type, self.value)


class MoveItem(Item):
    """
    Class used to represent items that affect a particular move type of a pokemon
    Args:
    name (str): name of the item
    moveType (PokemonType): Type of the move.
    value (float): Multiplier of the move

    """

    def __init__(self, name, move_type, value: float):
        super().__init__(name)
        self.move_type = move_type
        self.value = value

    def add_effect(self, pokemon):
        for move in pokemon.moves:
            if move.move_type is self.move_type:
                move.add_power_multiply(self.value)

    def remove_effect(self, pokemon):
        for move in pokemon.moves:
            if move.move_type is self.move_type:
                move.remove_power_multiply(self.value)


class DamageItem(Item):
    """
    Class that represents an item that modifies the total output damage of a pokemon
    Args:
    name (str): name of the item
    value (float): multiplier of the damage (str): name of the item

    """

    def __init__(self, name, value: float):
        super().__init__(name)
        self.value = value

    def add_effect(self, pokemon):
        pokemon.damage_output_multiplier = pokemon.damage_output_multiplier * self.value

    def remove_effect(self, pokemon):
        pokemon.damage_output_multiplier = pokemon.damage_output_multiplier / self.value


class ChoiceItem(StatsItem):
    """
    Class that represents a choice item
    Args:
    name (str): name of the item
    statsType (StatsType): the stat that it affects
    value (float): Multiplier of the stat
    
    """

    def __init__(self, name, stats, value: float):
        super().__init__(name, stats, value)

    def add_lock(self, pokemon, move):
        for to_lock in pokemon.moves:
            if to_lock != move:
                to_lock.isUsable = False

    def remove_lock(self, pokemon, move):
        for to_lock in pokemon.moves:
            to_lock.isUsable = True


class HealingBerry(Item):
    """
    Class that represents a berry that heals when the hp go beyond a threshold
    Args:
    name (str): name of the berry
    threshold(int): % of the hp that activate the berry
    value(int): % of the base health to restore

    """

    def __init__(self, name: str, threshold: int, value: int):
        super().__init__(name)
        self.threshold = threshold
        self.value = value

    def activate(self, pokemon):
        # If under the threshold then activate
        if pokemon.stats.get_actual_hp() <= (pokemon.stats.base_stats[StatsType.HP] * (self.threshold / 100)):
            pokemon.stats.increase_hp(pokemon.stats.base_stats[StatsType.HP] * (self.value / 100))
