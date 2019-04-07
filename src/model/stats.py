from typing import Tuple
from enum import Enum, auto

"""
Enum class which contains stats' types
"""
class  StatsType(Enum):
	HP = auto()
	Attack= auto()
	Defense = auto()
	SpecialAttack = auto()
	SpecialDefense = auto()
	Speed = auto()
	Accuracy = auto()
	Evasion = auto()

"""
This class contains pokemon's statistics and methods to  change them.
"""
class Stats:

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
		#Initial value of each statistic
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
		#Initial value of each statistics' multiplier
		self.mulStats = {
			StatsType.Attack: 0,
			StatsType.Defense: 0,
			StatsType.SpecialAttack: 0,
			StatsType.SpecialDefense: 0,
			StatsType.Speed: 0,
			StatsType.Accuracy: 0,
			StatsType.Evasion: 0
		}

		self.voltatileMul = {
			StatsType.Attack: 1,
			StatsType.Defense: 1,
			StatsType.SpecialAttack: 1,
			StatsType.SpecialDefense: 1,
			StatsType.Accuracy: 1,
			StatsType.Evasion: 1
		}

		#Initial value of the damage
		self.damage = 0

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
	Increase Pokemon's HP by decreasing the damage
	"""
	def increaseHP(self, quantity:int):
		if(self.damage - quantity) < 0:
			self.damage = 0
		else:
			self.damage -= quantity

	"""
	Decrease Pokemon's HP by increasing the damage
	"""
	def decreaseHP(self, quantity:int):
		if (self.damage + quantity) > self.baseStats[StatsType.HP]:
			self.damage = self.baseStats[StatsType.HP]
		else:
			self.damage += quantity
	
	"""
	Returns the requested statistic eventually modified 
	"""
	def getActual(self, type: StatsType) ->int:
		if type is StatsType.Accuracy or type is StatsType.Evasion:
			return  self.baseStats[type] * self.multipliersAE[self.mulStats[type]] * self.voltatileMul[type]
		else:
			return self.baseStats[type] * self.multipliers[self.mulStats[type]] * self.voltatileMul[type]
	
	"""
	Returns Pokemon's actual HP value by subtracting the damage to the base HP
	"""
	def getActualHP(self)->int:
		return self.baseStats[StatsType.HP] - self.damage

	def addVolatileMul(self, statsType:StatsType, value:float):
		self.voltatileMul[statsType] * value
	
	def removeVolatileMul(self, statsType:StatsType, value:float):
		self.voltatileMul[statsType] / value



	
