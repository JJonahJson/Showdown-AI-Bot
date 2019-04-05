from src.model.status import StatusType
from src.model.item import Item
from src.model.stats import StatsType

from typing import Dict, List

class Pokemon:
	"""
	This class represents a Pokémon.
	name (str) = pokemon's name
	types (list) = pokemon's types (or type)
	gender( str) = pokemon's gender (male, female or neutral)
	stats (Stats) = actual pokemon's statistics
	abilities (list) = list of possible pokemon's abilities
	weight (int) = pokemon's weight which may influence some moves power
	status(StatusType) = pokemon's status (poisoned, fainted, ecc.)
	item(str) = pokemon's held item
	level(int) = pokemon's level (from 1 to 100)

	"""
	def __init__(self, name:str, types:list, gender, stats, moves: Dict,abilities:list, weight:float, status:StatusType, item:Item, level:int):
		self. name = name
		self.types = types
		self.gender = gender
		self.stats = stats
		self.abilities = abilities
		self.weight = weight
		self.item = item
		self.level = level
		self.moves = moves
		self.damageOutputMultiplier = 1
		self.damageInputMultiplier = 1
		self.status = StatusType.Normal

	"""Methods that returns all usable moves
	"""
	def getUsableMoves(self) ->List:
		return {k:v for k,v in self.moves if v.isUsable()}

	"""Methods that apply a move
	"""
	def useMove(self, moveIndex:int, targets: Dict, targetIndex:int, weather, field):
		self.moves[moveIndex].invokeMove(self, targets, targetIndex, weather, field)

	def applyStatus(self, status):
		if status is not StatusType.Normal:
			self.status = status

	"""More speed 
	"""
	def __lt__(self, otherPokemon):
		return self.stats[StatsType.Speed] > otherPokemon.stats[StatsType.Speed]
	
