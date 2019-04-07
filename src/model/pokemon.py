from src.model.stats import Stats
from src.model.moves.move import Move
from src.model.pokemontype import PokemonType
from src.model.status import Status, StatusType
from src.model.item import Item

from typing import List

class Pokemon:
	"""
	This class represents a Pokémon.
	name (str) = pokemon's name
	types (list) = pokemon's types (or type)
	gender( str) = pokemon's gender (male, female or neutral)
	stats (Stats) = actual pokemon's statistics
	abilities (list) = list of possible pokemon's abilities
	weight (float) = pokemon's weight which may influence some moves power
	nonVolatileStatus(StatusType) = pokemon's status (poisoned, fainted, ecc.)
	volatileStatus(list) = pokemon's list of volatile Status (confused, attracted, ecc.)
	item(Item) = pokemon's held item
	level(int) = pokemon's level (from 1 to 100)
	moves(list) = pokemon's moves

	"""
	def __init__(self, name:str, types:List[PokemonType], gender:str, stats:Stats, moves: List[Move],abilities:list, weight:float, nonVolatileStatus:StatusType, volatileStatus:List[StatusType], item:Item, level:int):
		self. name = name
		self.types = types
		self.gender = gender
		self.stats = stats
		self.abilities = abilities
		self.weight = weight
		self.nonVolatileStatus = nonVolatileStatus
		self.volatileStatus = volatileStatus
		self.item = item
		self.level = level
		self.moves = moves
		self.damageOutputMultiplier = 1
		self.damageInputMultiplier = 1


	def getUsableMoves(self) ->List[Move]:
		return list(filter(lambda move: move.isUsable, self.moves))


	
	
