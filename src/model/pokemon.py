from stats import Stats
from typing import List
from moves.move import Move

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
	def __init__(self, name:str, types:list, gender, stats:Stats, moves: List[Move],abilities:list, weight:float, status, item, level:int):
		self. name = name
		self.types = types
		self.gender = gender
		self.stats = stats
		self.abilities = abilities
		self.weight = weight
		self.status = status
		self.item = item
		self.level = level
		self.moves = moves
		self.damageOutputMultiplier = 1
		self.damageInputMultiplier = 1


	def getUsableMoves(self) ->List[Move]:
		return list(filter(lambda move: move.isUsable, self.moves))


	
	
