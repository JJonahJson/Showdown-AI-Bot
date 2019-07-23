import asyncio

from websocket import create_connection

from src.protocol import game_control


async def main():
    """
    Loading function. Connect websocket then launch bot.
    """
    websocket = create_connection(
        'ws://sim.smogon.com:8000/showdown/websocket')

    gl = game_control.GameLoop(websocket)
    while True:
        message = websocket.recv()
        print("<< {}".format(message))
        await gl.challenge_loop(message)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
