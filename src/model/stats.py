from enum import Enum, auto


class StatsType(Enum):
    """Enum class which contains stats' types"""
    HP = auto()
    Att = auto()
    Def = auto()
    Spa = auto()
    Spd = auto()
    Spe = auto()
    Acc = auto()
    Eva = auto()



class Stats:
    """This class contains pokemon's statistics and methods to  change them."""

    """Multipliers for statistics changes"""
    multipliers = {
        -6: 0.25,
        -5: 0.29,
        -4: 0.33,
        -3: 0.4,
        -2: 0.5,
        -1: 0.67,
        0: 1,
        1: 1.5,
        2: 2,
        3: 2.5,
        4: 3,
        5: 3.5,
        6: 4
    }

    """Multipliers for accuracy and evasion changes	"""
    multipliersAE = {
        -6: 0.33,
        -5: 0.38,
        -4: 0.43,
        -3: 0.5,
        -2: 0.6,
        -1: 0.75,
        0: 1,
        1: 1.33,
        2: 1.67,
        3: 2,
        4: 2.33,
        5: 2.67,
        6: 3
    }

    def __init__(self, hp: int, attack: int, defense: int, special_attack: int, special_defense: int, speed: int):
        # Initial value of each statistic
        self.base_stats = {
            StatsType.HP : hp,
            StatsType.Att: attack,
            StatsType.Def: defense,
            StatsType.Spa: special_attack,
            StatsType.Spd: special_defense,
            StatsType.Spe: speed,
            StatsType.Acc: 1,
            StatsType.Eva: 1
        }
        # Initial value of each statistics' multiplier
        self.mul_stats = {
            StatsType.Att: 0,
            StatsType.Def: 0,
            StatsType.Spa: 0,
            StatsType.Spd: 0,
            StatsType.Spe: 0,
            StatsType.Acc: 0,
            StatsType.Eva: 0
        }
        # Initial value of each statistics' volatile multiplier
        self.voltatile_mul = {
            StatsType.Att: 1,
            StatsType.Def: 1,
            StatsType.Spa: 1,
            StatsType.Spd: 1,
            StatsType.Acc: 1,
            StatsType.Eva: 1
        }
        # Initial value of the damage
        self.damage = 0

    def modify(self, stat_type: StatsType, quantity: int):
        """Changes the multipliers of the specified stat from -6 to 6, these are all set to 0 at the start"""
        if (self.mul_stats[stat_type] + quantity) > 6:
            self.mul_stats[stat_type] = 6
        elif (self.mul_stats[stat_type] + quantity) < -6:
            self.mul_stats[stat_type] = -6
        else:
            self.mul_stats[stat_type] += quantity

    def increase_hp(self, quantity: int):
        """Increase Pokemon's HP by decreasing the damage"""
        if (self.damage - quantity) < 0:
            self.damage = 0
        else:
            self.damage -= quantity

    def decrease_hp(self, quantity: int):
        """Decrease Pokemon's HP by increasing the damage"""
        if (self.damage + quantity) > self.base_stats[StatsType.HP]:
            self.damage = self.base_stats[StatsType.HP]
        else:
            self.damage += quantity

    def get_actual(self, stat_type: StatsType) -> int:
        """Returns the requested statistic eventually modified"""
        if stat_type is StatsType.Acc or type is StatsType.Eva:
            return self.base_stats[stat_type] * self.multipliersAE[self.mul_stats[stat_type]] * self.voltatile_mul[stat_type]
        else:
            return self.base_stats[stat_type] * self.multipliers[self.mul_stats[stat_type]] * self.voltatile_mul[stat_type]

    def get_actual_hp(self) -> int:
        """Returns Pokemon's actual HP value by subtracting the damage to the base HP"""
        return self.base_stats[StatsType.HP] - self.damage

    def increase_volatile_mul(self, stats_type: StatsType, value: float):
        """Increases the volatile multiplier of the specified stat by the given value"""
        self.voltatile_mul[stats_type] *= value

    def decrease_volatile_mul(self, stats_type: StatsType, value: float):
        """Decreases the volatile multiplier of the specified stat by the given value"""
        self.voltatile_mul[stats_type] /= value
