from ast import literal_eval

class Game:
    def __init__(self, id):
        self.ready1 = False
        self.ready2 = False
        self.connect = False
        self.id = id
        self.turn = 0
        self.all_ships1 = []
        self.all_ships2 = []
        self.azs1 = []
        self.azs2 = []
        self.shots1 = []
        self.shots2 = []
        self.winnerP = -1
        self.restart1 = False
        self.restart2 = False

    def connected(self):
        return self.connect

    def both_ready(self):
        return self.ready1 and self.ready2

    def player_ready(self, player):
        if player == 0:
            self.restart1 = False
            self.ready1 = True
        elif player == 1:
            self.restart2 = False
            self.ready2 = True

    def turn_passed(self, player):
        if player == 0:
            self.turn = 1
        else:
            self.turn = 0

    def append_ships(self, player, ship):
        if player == 0:
            s = literal_eval(ship)
            self.all_ships1.append(s)
        elif player == 1:
            s = literal_eval(ship)
            self.all_ships2.append(s)

    def append_az(self, player, az):
        if player == 0:
            a = literal_eval(az)
            self.azs1.append(a)
        elif player == 1:
            a = literal_eval(az)
            self.azs2.append(a)

    def append_shots(self, player, shot):
        if player == 0:
            s = literal_eval(shot)
            self.shots1.append(s)
            self.turn = 1
        elif player == 1:
            s = literal_eval(shot)
            self.shots2.append(s)
            self.turn = 0

    def player_reset(self, player):
        if player == 0:
            self.restart1 = True
        elif player == 1:
            self.restart2 = True

    def both_reset(self):
        return self.restart1 and self.restart2

    def reset(self, p):
        self.ready1 = False
        self.ready2 = False
        self.turn = 0
        self.all_ships1 = []
        self.all_ships2 = []
        self.azs1 = []
        self.azs2 = []
        self.shots1 = []
        self.shots2 = []
        self.winnerP = -1

