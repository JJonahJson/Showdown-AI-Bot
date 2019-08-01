from model.pokemon_type import PokemonType as t
from model.field_type import Weather as w, Field as f


class WeatherModifiers:
    """This class contains a static dict for the weather multipliers"""
    modifiers = {
        (t.Water, w.Raindance): 1.5,
        (t.Water, w.Primordialsea): 1.5,
        (t.Fire, w.Primordialsea): 0,
        (t.Fire, w.Desolateland): 1.5,
        (t.Water, w.Desolateland):0,
        (t.Water, w.Sunnyday): 0.5,
        (t.Fire, w.Raindance): 0.5,
        (t.Fire, w.Sunnyday): 2,
        (t.Electric, w.Deltastream): 0.5,
        (t.Ice, w.Deltastream): 0.5,
        (t.Rock, w.Deltastream): 0.5
    }


class FieldModifiers:
    """This class contains a static dict for the terrain modifiers"""
    modifiers = {
        (t.Psychic, f.Psychic): 1.5,
        (t.Electric, f.Electric): 1.5,
        (t.Grass, f.Grassy): 1.5
    }
