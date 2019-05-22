from src.model.pokemontype import PokemonType
from src.model.stats import StatsType
from enum import Enum, auto


class StatusType(Enum):
	"""Class that represents all possible statuses of a pokemon"""
	Normal = auto(),
	Fainted = auto(),
	Poisoned = auto(),
	BPoisoned = auto(),
	Burned = auto(),
	Paralyzed = auto(),
	Frozen = auto(),
	Asleep = auto(),
	Infatuated = auto(),
	Confused = auto(),
	Trapped = auto(),
	LeechSeed = auto(),
	Protected = auto(),
	Endure = auto(),
	Fly = auto(),
	Dig = auto(),
	Flinched = auto()


nonVolatile = {
	StatusType.Normal: False,
	StatusType.Fainted: True,
	StatusType.Poisoned: True,
	StatusType.BPoisoned: True,
	StatusType.Burned: True,
	StatusType.Paralyzed: True,
	StatusType.Frozen: True,
	StatusType.Asleep:True,

	StatusType.Infatuated: False,
	StatusType.Flinched: False,
	StatusType.Confused: False,
	StatusType.Protected: False,
	StatusType.Trapped: False,
	StatusType.Endure: False,
	StatusType.Fly: False,
	StatusType.Dig:False,
	StatusType.LeechSeed:False
}

immune = {
	StatusType.Poisoned: [PokemonType.Poison, PokemonType.Steel],
	StatusType.BPoisoned: [PokemonType.Poison, PokemonType.Steel],
	StatusType.Paralyzed: [PokemonType.Electric],
	StatusType.Frozen: [PokemonType.Ice],
	StatusType.Burned: [PokemonType.Fire],
	StatusType.Normal: [],
	StatusType.Fainted: []
}


class Status():
	"""Class that represents a pokemon's status and the methods applicables"""
	def __init__(self, type: StatusType):
		self.type = type

	def applyNonVolatileStatus(self, status:Status, pokemon) -> bool:
		"""Method which applies a non volatile status, used also to specify when fainted, returns True if succeed, False instead"""
		for pkmnType in pokemon.types:
			if pkmnType in immune[type] or pokemon.nonVolatileStatus.type is not StatusType.Normal:
				return	False
		pokemon.nonVolatileStatus.type = type
		return True
	
	def addVolatileStatus(self, status:Status, pokemon):
		"""Method which adds a volatile status to pokemon's volatile status list"""
		pokemon.volatileStatus.append(status)

	def removeVolatileStatus(self, status:Status, pokemon):
		"""Method which removes a volatile status to pokemon's volatile status list"""
		pokemon.volatileStatus.remove(status)
	
	def addOutputEffect(self, pokemon, value:float):
		"""Method which applies changes to the damage output multiplier"""
		pokemon.damageOutputMultiplier *= value

	def removeOutputEffect(self, pokemon, value:float):
		"""Method which removes changes to the damage output multiplier	"""	
		pokemon.damageOutputMultiplier /= value

	def addVolatileStatMod(self, pokemon, type:StatsType, value:float):
		"""Method which adds changes to the specified volatile stat"""
		pokemon.stats.volatileMul[type] *= value
	
	def removeVolatileStatMod(self, pokemon, type:StatsType, value:float):
		"""Method which removes changes to the specified volatile stat"""
		pokemon.stats.volatileMul[type] /= value

	def decreaseHP(self, pokemon, percentage: float):
		"""Method which decreases pokemon's hp based on a specified percentage"""
		pokemon.stats.damage = pokemon.stats.baseStats[StatsType.HP] * percentage
