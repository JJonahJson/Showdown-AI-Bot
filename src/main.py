import asyncio
from websocket import create_connection
import po_io


async def main():
    """
    Loading function. Connect websocket then launch bot.
    """
    websocket = create_connection(
        'ws://sim.smogon.com:8000/showdown/websocket')
    while True:
        message = websocket.recv()
        print("<< {}".format(message))
        await po_io.stringing(websocket, message)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
