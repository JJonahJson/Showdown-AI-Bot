class Action:
    """
    Model class for an action
    """

    POKEMON = 0
    MOVE = 1
    TARGET = 2
    PLAYER = 3

    def __init__(self, pokemon, move, target, player):
        self.action = (pokemon, move, target, player)

    def __lt__(self, other_action):
        """
        Ordering method, order actions based on pokemon speed and priority
        :param otherAction:
        :return:
        """
        if self.action[Action.MOVE] < other_action.action[Action.MOVE]:
            return True
        elif self.action[Action.MOVE] > other_action.action[Action.MOVE]:
            return False
        else:
            return self.action[Action.POKEMON] < other_action[Action.POKEMON]


# TODO Implement switch

class Game:
    """
    Model class for a game
    """

    turn_start = []
    turn_end = []

    def __init__(self, battlefield):
        self.battlefield = battlefield
        self.turn_counter = 1

    def execute_turn(self, action1: list, action2: list):
        """
        Simulates a turn based on the actions passed as params
        :param action1: Chosen actions for team1
        :param action2: Chosen actions for team2
        :return:
        """
        Game.trigger_start()
        move_turn = sorted(action1 + action2)
        for pokemon, move, target, player in move_turn:
            # TODO Modeling as index or using the objects?!
            self.battlefield.do_move(player, pokemon, move, target)
        self.turn_counter += 1
        Game.trigger_end()

    # TODO Determinare i parametri dei trigger per queste funzioni "ad eventi" ù
    @staticmethod
    def trigger_start():
        """
        Method that triggers the functions in turn_start
        :return:
        """
        for function in Game.turn_start:
            function()

    @staticmethod
    def trigger_end():
        """
        Method that triggers the functions in turn_end
        :return:
        """
        for function in Game.turn_end:
            function()
