from model.stats import StatsType, Stats
from model.status import StatusType
from model.item import Item


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

	def __init__(self, name: str, types: list, gender: str, stats: Stats, moves: Dict, abilities: list, weight: float,
                 non_volatile_status: StatusType, volatile_status: list, item: Item, level: int):
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

	def get_usable_moves(self):
		"""Methods that returns all usable moves"""
		return {k: v for k, v in self.moves if v.isUsable()}

	def use_move(self, move_index: int, target, weather, field):
		"""Methods that apply a move"""
		self.moves[move_index].invokeMove(self, target, weather, field)
		if target.stats.get_actual_hp() <= 0 :
			Status.applyNonVolatileStatus(StatusType.Fainted, target)

	#Duplicato della classe status, vediamo se toglierlo
	def apply_status(self, status):
		from src.model.status import StatusType
		if status is not StatusType.Normal:
			self.status = status

	def __lt__(self, otherPokemon):
		"""More speed"""
		return self.stats[StatsType.Speed] > otherPokemon.stats[StatsType.Speed]

