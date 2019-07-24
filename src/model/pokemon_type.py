from enum import Enum, auto


class PokemonType(Enum):
    """Enum that represents all the possible types of a pokemon and of a pokemon's move"""
    Normal = auto()
    Fire = auto()
    Water = auto()
    Electric = auto()
    Grass = auto()
    Ice = auto()
    Fighting = auto()
    Poison = auto()
    Ground = auto()
    Flying = auto()
    Psychic = auto()
    Bug = auto()
    Rock = auto()
    Ghost = auto()
    Dragon = auto()
    Dark = auto()
    Steel = auto()
    Fairy = auto()


class TypeMultiplier:
    """
    Dictionaries that contains type relations
    PokemonType: MoveType

    """

    weakTo = {
        PokemonType.Normal: [PokemonType.Fighting],
        PokemonType.Fire: [PokemonType.Water, PokemonType.Ground, PokemonType.Rock],
        PokemonType.Water: [PokemonType.Electric, PokemonType.Grass],
        PokemonType.Electric: [PokemonType.Ground],
        PokemonType.Grass: [PokemonType.Fire, PokemonType.Ice, PokemonType.Poison, PokemonType.Flying, PokemonType.Bug],
        PokemonType.Ice: [PokemonType.Fire, PokemonType.Fighting, PokemonType.Rock],
        PokemonType.Fighting: [PokemonType.Flying, PokemonType.Psychic, PokemonType.Fairy],
        PokemonType.Poison: [PokemonType.Ground, PokemonType.Psychic],
        PokemonType.Ground: [PokemonType.Water, PokemonType.Grass, PokemonType.Ice],
        PokemonType.Flying: [PokemonType.Electric, PokemonType.Ice, PokemonType.Rock],
        PokemonType.Psychic: [PokemonType.Bug, PokemonType.Dark, PokemonType.Ghost],
        PokemonType.Bug: [PokemonType.Fire, PokemonType.Flying, PokemonType.Rock],
        PokemonType.Rock: [PokemonType.Water, PokemonType.Grass, PokemonType.Fighting, PokemonType.Steel],
        PokemonType.Ghost: [PokemonType.Ghost, PokemonType.Dark],
        PokemonType.Dragon: [PokemonType.Dragon, PokemonType.Ice, PokemonType.Fairy],
        PokemonType.Dark: [PokemonType.Bug, PokemonType.Fighting, PokemonType.Fairy],
        PokemonType.Steel: [PokemonType.Fire, PokemonType.Fighting, PokemonType.Ground],
        PokemonType.Fairy: [PokemonType.Poison, PokemonType.Steel]
    }

    resistsTo = {
        PokemonType.Normal: [],
        PokemonType.Fire: [PokemonType.Fire, PokemonType.Grass, PokemonType.Ice, PokemonType.Bug, PokemonType.Steel,
                           PokemonType.Fairy],
        PokemonType.Water: [PokemonType.Fire, PokemonType.Water, PokemonType.Ice, PokemonType.Steel],
        PokemonType.Electric: [PokemonType.Electric, PokemonType.Flying, PokemonType.Steel],
        PokemonType.Grass: [PokemonType.Water, PokemonType.Electric, PokemonType.Grass, PokemonType.Ground],
        PokemonType.Ice: [PokemonType.Ice],
        PokemonType.Fighting: [PokemonType.Bug, PokemonType.Rock, PokemonType.Dark],
        PokemonType.Poison: [PokemonType.Grass, PokemonType.Fighting, PokemonType.Poison, PokemonType.Bug,
                             PokemonType.Rock, PokemonType.Dark],
        PokemonType.Ground: [PokemonType.Poison, PokemonType.Rock],
        PokemonType.Flying: [PokemonType.Ground, PokemonType.Grass, PokemonType.Bug],
        PokemonType.Psychic: [PokemonType.Fighting, PokemonType.Psychic],
        PokemonType.Bug: [PokemonType.Grass, PokemonType.Fighting, PokemonType.Ground],
        PokemonType.Rock: [PokemonType.Normal, PokemonType.Fire, PokemonType.Poison, PokemonType.Flying],
        PokemonType.Ghost: [PokemonType.Poison, PokemonType.Bug],
        PokemonType.Dragon: [PokemonType.Fire, PokemonType.Grass, PokemonType.Water],
        PokemonType.Dark: [PokemonType.Ghost, PokemonType.Dark],
        PokemonType.Steel: [PokemonType.Normal, PokemonType.Grass, PokemonType.Ice, PokemonType.Flying,
                            PokemonType.Psychic, PokemonType.Bug, PokemonType.Rock, PokemonType.Dragon,
                            PokemonType.Steel, PokemonType.Fairy],
        PokemonType.Fairy: [PokemonType.Fighting, PokemonType.Bug, PokemonType.Dark]
    }
    immuneTo = {
        PokemonType.Normal: [PokemonType.Ghost],
        PokemonType.Fire: [],
        PokemonType.Water: [],
        PokemonType.Electric: [],
        PokemonType.Grass: [],
        PokemonType.Ice: [],
        PokemonType.Fighting: [],
        PokemonType.Poison: [],
        PokemonType.Ground: [PokemonType.Electric],
        PokemonType.Flying: [PokemonType.Ground],
        PokemonType.Psychic: [],
        PokemonType.Bug: [],
        PokemonType.Rock: [],
        PokemonType.Ghost: [PokemonType.Normal, PokemonType.Fighting],
        PokemonType.Dragon: [],
        PokemonType.Dark: [PokemonType.Psychic],
        PokemonType.Steel: [PokemonType.Poison],
        PokemonType.Fairy: [PokemonType.Dragon]
    }
