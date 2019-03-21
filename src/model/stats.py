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
	
	def __init__(self, hp, attack, defense, specialAttack, specialDefense, speed):
		self.hp = hp
		self.attack = attack
		self.defense = defense
		self.specialAttack = specialAttack
		self.specialDefense = specialDefense
		self.speed = speed
		self.atkMul = 0
		self.defMul = 0
		self. spaMul = 0
		self. spdMul = 0
		self.speMul = 0
		self.changes = {
			"atk": self.atkMul,
			"def": self.defMul,
			"spa": self.spaMul,
			"spd": self.spdMul,
			"spe": self.speMul
		}

	def increase(self, type, quantity):
		if (self.changes[type] + quantity) > 6:
			self.changes[type] = 6
		elif (self.changes[type] + quantity) < -6:
			self.changes[type] = -6
		else:
			self.changes[type] += quantity

	def getActual(self):
		return (self.hp,
		Stats.multipliers[self.atkMul]*self.attack, 
		Stats.multipliers[self.defMul]*self.defense,
		Stats.multipliers[self.spaMul]*self.specialAttack,
		Stats.multipliers[self.spdMul]*self.specialDefense,
		Stats.multipliers[self.speMul]*self.speed
		)

stat = Stats(0,0,0,0,0,0)
print(stat.getActual())

	
