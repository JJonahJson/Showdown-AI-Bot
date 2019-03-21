class Stats:
	"""
	This class contains pokemon's statistics and methods to  change them.

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
	Multipliers for accuracy and evasion

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
	
	def __init__(self, hp, attack, defense, specialAttack, specialDefense, speed):
		self.hp = hp
		self.attack = attack
		self.defense = defense
		self.specialAttack = specialAttack
		self.specialDefense = specialDefense
		self.speed = speed
		self.accuracy = 1
		self.evasion = 1
		self.atkMul = 0
		self.defMul = 0
		self. spaMul = 0
		self. spdMul = 0
		self.speMul = 0
		self.accMul = 0
		self.evaMul = 0
		self.changes = {
			"atk": self.atkMul,
			"def": self.defMul,
			"spa": self.spaMul,
			"spd": self.spdMul,
			"spe": self.speMul,
			"accuracy": self.accMul,
			"evasion": self.evaMul
		}

	def modify(self, type: str, quantity:int):
		if (self.changes[type] + quantity) > 6:
			self.changes[type] = 6
		elif (self.changes[type] + quantity) < -6:
			self.changes[type] = -6
		else:
			self.changes[type] += quantity

	def getActual(self):
		return (
		Stats.multipliers[self.atkMul]*self.attack, 
		Stats.multipliers[self.defMul]*self.defense,
		Stats.multipliers[self.spaMul]*self.specialAttack,
		Stats.multipliers[self.spdMul]*self.specialDefense,
		Stats.multipliers[self.speMul]*self.speed,
		Stats.multipliersAE[self.accMul]*self.accuracy,
		Stats.multipliersAE[self.evaMul]*self.evasion
		)



	
