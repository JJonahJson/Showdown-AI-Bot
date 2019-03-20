class Pokemon:
	"""
	This class represents a Pokémon.
	name (str) = pokemon's name
	types (list) = pokemon's types (or type)
	gender( str) = pokemon's gender (male, female or neutral)
	stats (Stats) = actual pokemon's statistics
	abilities (list) = list of possible pokemon's abilities
	weight (int) = pokemon's weight which may influence some moves power
	status(str) = pokemon's status (poisoned, fainted, ecc.)
	item(str) = pokemon's held item
	level(int) = pokemon's level (from 1 to 100)

	"""
	def __init__(self, name, types, gender, stats, abilities, weight, status, item, level):
		self. name = name
		self.types = types
		self.gender = gender
		self.stats = stats
		self.abilities = abilities
		self.weight = weight
		self.status = status
		self.item = item
		self.level = level

	
	
