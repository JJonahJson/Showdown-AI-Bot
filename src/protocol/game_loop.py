import src.protocol.senders as s


class GameLoop:

    def __init__(self, websocket):
        self.ws = websocket

    def game_loop(self, message):
        lines = message.splitlines()
        for line in lines[1:]:
            current = line.split('|')
            if current[1] == "init":
                #TODO: find battletag -> 1234
                await s.sendmessage(self.ws, 1234, "Welcome")
                await s.sendmessage("/timer on")
            #TODO: Set battle_id
            elif current[1] == "request":
                if current[2] == '':
                    continue;
                # Maj team bot
                if len(current[2]) == 1:
                    try:
                        # TODO: Changhe and send to request loader
                        await battle.req_loader(current[3].split('\n')[1], websocket)
                    except KeyError as e:
                        print(e)
                        print(current[3])
                else:
                    # TODO: Changhe and send to request loader
                    await battle.req_loader(current[2], websocket)
            elif current[1] == "teampreview":
                # TODO: IA Knapsack which pokemon do we carry
                await battle.make_team_order(websocket)
            elif current[1] == "turn":
                # TODO: Call IA to decide which move
                await battle.make_action(websocket)
            elif current[1] == "callback" and current[2] == "trapped":
                await battle.make_move(websocket)
            elif current[1] == "win":
                #TODO: WE win
                await s.sendmessage(self.ws, 1234, "wp")
                await s.leaving(self.ws, 1234)
            elif current[1] == "c":
                # This is a message
                pass
            else:
                # Send to battlelog
                pass
