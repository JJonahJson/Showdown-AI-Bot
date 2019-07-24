import asyncio
import argparse
import getpass
import logging
from websocket._core import create_connection

from src.protocol import game_control


async def main(password):
    """
    Loading function. Connect websocket then launch bot.
    """
    parser = argparse.ArgumentParser(description="Pokemon Showdown Bot")
    parser.add_argument("-o", "--opponent_name", type=str, help="username of the opponent you want the bot to challenge")
    parser.add_argument("-u", "--username", type=str, help="username of your Pokemon Showdown account")
    args = parser.parse_args()
    websocket = create_connection(
        'ws://sim.smogon.com:8000/showdown/websocket')

    gl = game_control.GameLoop(websocket, args.username, password,  args.opponent_name)
    print("Starting bot with opponent {}".format(args.opponent_name))
    while True:
        message = websocket.recv()
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(message)
        await gl.challenge_loop(message)



if __name__ == "__main__":
    password = getpass.getpass(prompt="Insert your Pokemon Showdown password\n")
    asyncio.get_event_loop().run_until_complete(main(password))
