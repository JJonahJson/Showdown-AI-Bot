import asyncio
import argparse

from websocket import create_connection

from src.protocol import game_control


async def main():
    """
    Loading function. Connect websocket then launch bot.
    """
    parser = argparse.ArgumentParser(description="Pokemon Showdown Bot")
    parser.add_argument("-o", "--opponent_name", type=str, help="username of the opponent you want the bot to challenge")
    args = parser.parse_args()
    websocket = create_connection(
        'ws://sim.smogon.com:8000/showdown/websocket')

    gl = game_control.GameLoop(websocket, args.opponent_name)
    print("Starting bot with opponent {}".format(args.opponent_name))
    while True:
        message = websocket.recv()
        print("<< {}".format(message))
        await gl.challenge_loop(message)



if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
