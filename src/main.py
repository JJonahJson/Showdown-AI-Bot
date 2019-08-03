import asyncio
import argparse
import getpass
from websocket._core import create_connection
from protocol.game_control import GameLoop
import model.setup_logger
import logging

logger = logging.getLogger("Main")


async def main(password):
    """
    Loading function. Connect websocket then launch bot.
    """
    parser = argparse.ArgumentParser(description="Pokemon Showdown Bot")
    parser.add_argument("-o", "--opponent_name", type=str,
                        help="The username of the opponent you want the bot to challenge", default=None)
    parser.add_argument("-u", "--username", type=str, help="The username of your Pokemon Showdown account",
                        required=True)
    parser.add_argument("-d", "--difficulty", type=str, help="The difficulty", default="easy",
                        choices={"easy", "normal", "hard"})
    parser.add_argument("-m", "--mode", type=str, help="The way to use the bot, 'searching' or 'challenging'",
                        required=True, choices={"searching", "challenging"})
    parser.add_argument("-g", "--gen", type=int, help="The pokemon generation chosen for the random battle", default=7,
                        choices={1, 2, 3, 4, 5, 6, 7})
    parser.add_argument("-s", "--sex", type=str, help="The sex choosen for your account", default="m",
                        choices={"m", "f"})
    args = parser.parse_args()
    websocket = create_connection('ws://sim.smogon.com:8000/showdown/websocket')

    gl = GameLoop(websocket, args.username, password, args.sex, args.gen, args.difficulty, args.mode,
                               args.opponent_name)

    print("Starting bot with username {} vs {}".format(args.username, args.opponent_name))
    print("-----------------------------------------------------------------------")
    while True:
        message = websocket.recv()
        logger.debug(message)
        await gl.handle_message(message)


if __name__ == "__main__":
    password = getpass.getpass(prompt="Insert your Pokemon Showdown password\n")
    asyncio.get_event_loop().run_until_complete(main(password))
