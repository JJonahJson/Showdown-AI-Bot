from protocol import senders, login

battles = []
nb_fights_max = 20
nb_fights_simu_max = 6
nb_fights = 0

formats = [
    "gen7randombattle",
    "gen7monotyperandombattle",
    "gen7hackmonscup",
    "gen7challengecup1v1",
    "gen6battlefactory",
    "gen7bssfactory"
]


async def stringing(websocket, message, usage=0):
    """
    First filtering function on received messages.
    Handle challenge and research actions.
    :param websocket: Websocket stream.
    :param message: Message received from server. Format : room|message1|message2.
    :param usage: 0: Only recieving. 1 Challenging Synedh. 2 searching random battles.
    """
    global nb_fights_max
    global nb_fights
    global nb_fights_simu_max
    global battles
    global formats

    string_tab = message.split('|')
    if string_tab[1] == "challstr":
        # If we got the challstr, we now can log in.
        await login.log_in(websocket, string_tab[2], string_tab[3])
    elif string_tab[1] == "updateuser" and string_tab[2] == "tapulabu":
        # Once we are connected.
        if usage == 1:
            await senders.challenge(websocket, "alfamax", formats[0])
        if usage == 2:
            await senders.searching(websocket, formats[0])
            nb_fights += 1
    elif string_tab[1] == "deinit" and usage == 2:
        # If previous fight is over and we're in 2nd usage
        if nb_fights < nb_fights_max:  # If it remains fights
            await senders.searching(websocket, formats[0])
            nb_fights += 1
        # If it don't remains fights
        elif nb_fights >= nb_fights_max and len(battles) == 0:
            exit(0)
    elif "|inactive|Battle timer is ON:" in message and usage == 2:
        # If previous fight has started and we can do more simultaneous fights and we're in 2nd usage.
        if len(battles) < nb_fights_simu_max and nb_fights < nb_fights_max:
            await senders.searching(websocket, formats[0])
            nb_fights += 1
    elif "updatechallenges" in string_tab[1]:
        # If somebody challenges the bot
        try:
            if string_tab[2].split('\"')[3] != "challengeTo":
                if string_tab[2].split('\"')[5] in formats:
                    await senders.sender(websocket, "", "/accept " + string_tab[2].split('\"')[3])
                else:
                    await senders.sender(websocket, "", "/reject " + string_tab[2].split('\"')[3])
                    await senders.sender(websocket, "", "/pm " + string_tab[2].split('\"')[3]
                                         + ", Sorry, I accept only solo randomized metas.")
        except KeyError:
            pass
    elif string_tab[1] == "pm" and "SuchTestBot" not in string_tab[2]:
        if string_tab[4] == ".info":
            await senders.sender(websocket, "", "/pm " + string_tab[2] + ", Showdown Battle Bot. Active for "
                                 + ", ".join(formats[:-1]) + " and "
                                 + formats[-1] + ".")
            await senders.sender(websocket, "", "/pm " + string_tab[2] + ", Please challenge me to test your skills.")
        else:
            await senders.sender(websocket, "", "/pm " + string_tab[2] + ", Unknown command, type \".info\" for help.")
