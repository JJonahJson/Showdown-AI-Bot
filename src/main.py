import asyncio
from websocket import create_connection
from src.protocol import game_control
from src.model.field import BattleFieldSingle
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk
from src.model.stats import Stats


async def main():
    """
    Loading function. Connect websocket then launch bot.
    """
    websocket = create_connection(
        'ws://sim.smogon.com:8000/showdown/websocket')
    stats = Stats(100, 100, 100, 100, 100, 100)
    pokemon1 = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", stats, None, None, None, None, None, None, 50)
    pokemon2 = Pokemon("Kyogre", [pk.Water], "", stats, None, None, None, None, None, None, 50)
    pokemon3 = Pokemon("Qwilfish", [pk.Water, pk.Poison], "Male", stats, None, None, None, None, None, None, 50)
    pokemon4 = Pokemon("Gyarados", [pk.Water, pk.Flying], "Male", stats, None, None, None, None, None, None, 50)
    battleField = BattleFieldSingle(pokemon1, pokemon2, {1: pokemon4},
                                    {1: pokemon3})
    gl = game_control.GameLoop(websocket, battleField)
    while True:
        message = websocket.recv()
        print("<< {}".format(message))
        await gl.challenge_loop(message)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
