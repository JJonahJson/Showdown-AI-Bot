from typing import Tuple
from enum import Enum, auto

class  StatsType(Enum):
	HP = auto()
	Attack= auto()
	Defense = auto()
	SpecialAttack = auto()
	SpecialDefense = auto()
	Speed = auto()
	Accuracy = auto()
	Evasion = auto()


class Stats:

	"""
	This class contains pokemon's statistics and methods to  change them.

	"""

	"""
	Multipliers for statistics changes

	"""
	multipliers = {
		-6: 0.25,
		-5: 0.29,
		-4:  0.33,
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
	"""
	Multipliers for accuracy and evasion changes

	"""
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
	
	def __init__(self, hp:int, attack:int, defense:int, specialAttack:int, specialDefense:int, speed:int):
		self.baseStats = {
			StatsType.HP: hp,
			StatsType.Attack: attack,
			StatsType.Defense: defense,
			StatsType.SpecialAttack: specialAttack,
			StatsType.SpecialDefense: specialDefense,
			StatsType.Speed: speed,
			StatsType.Accuracy: 1,
			StatsType.Evasion: 1
		}
		self.mulStats = {
			StatsType.Attack: 0,
			StatsType.Defense: 0,
			StatsType.SpecialAttack: 0,
			StatsType.SpecialDefense: 0,
			StatsType.Speed: 0,
			StatsType.Accuracy: 0,
			StatsType.Evasion: 0
		}

	"""
	Changes the multipliers from -6 to 6, these are all set to 0 at the start
	"""
	def modify(self, type: StatsType, quantity:int):
		if (self.mulStats[type] + quantity) > 6:
			self.mulStats[type] = 6
		elif (self.mulStats[type] + quantity) < -6:
			self.mulStats[type] = -6
		else:
			self.mulStats[type] += quantity
	
	"""
	Returns all the changed statistics
	"""
	def getActual(self, type: StatsType) :
		if type is StatsType.Accuracy or type is StatsType.Evasion:
			return  self.baseStats[type] * self.multipliersAE[self.mulStats[type]]
		else:
			return self.baseStats[type] * self.multipliers[self.mulStats[type]]



	
