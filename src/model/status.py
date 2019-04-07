from enum import Enum, auto

class StatusType(Enum):
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
	StatusType.Paralyzed: [PokemonType.Electric],
	StatusType.Frozen: [PokemonType.Ice],
	StatusType.Burned: [PokemonType.Fire]
}



class Status():
	def __init__(self, type:StatusType):
		self.type = type

	"""Method which applies a non volatile status, used also to specify when fainted, returns True if succeed, False instead
	"""
	def applyNonVolatileStatus(self, type:StatusType, pokemon) -> bool:
		for pkmnType in pokemon.types:
			if pkmnType in immune[type]:
				return	False
		pokemon.nonVolatileStatus = type
		return True
	
	"""Method which adds a volatile status to pokemon's volatile status list
	"""
	def addVolatileStatus(self, type:StatusType, pokemon):
		pokemon.volatileStatus.append(type)

	"""Method which removes a volatile status to pokemon's volatile status list
	"""
	def removeVolatileStatus(self, type:StatusType, pokemon):
		pokemon.volatileStatus.remove(type)
	
	"""Method which applies changes to the damage output multiplier
	"""
	def addOutputEffect(self, pokemon, stat:Stats, value:float):
		pokemon.damageOutputMultiplier *= value

	"""Method which removes changes to the damage output multiplier
	"""	
	def removeOutputEffect(self, pokemon, value:float):
		pokemon.damageOutputMultiplier /= value

	"""Method which adds changes to the specified volatile stat
	"""
	def addVolatileStatMod(self, pokemon, type:StatsType, value:float):
		pokemon.volatileStatus[type] *= value
	
	"""Method which removes changes to the specified volatile stat
	"""
	def removeVolatileStatMod(self, pokemon, type:StatsType, value:float):
		pokemon.volatileStatus[type] /= value

	"""Method which decreases pokemon's hp based on a specified percentage
	"""
	def decreaseHP(self, pokemon, percentage: float):
		pokemon.stats.damage = pokemon.stats.baseStats[StatsType.HP] * percentage
