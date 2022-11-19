from random import choice, randrange
from turtle import Screen, Turtle, onkey, bye
from ship import PlayerShip, EnemyShip, BossShip


class Game:
    def __init__(self, player_name=""):
        self.__player = PlayerShip(player_name)
        self.__enemy = {}
        self.__screen = None

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, new_player):
        self.__player = new_player

    @property
    def enemy(self):
        return self.__enemy

    @enemy.setter
    def enemy(self, new_enemy):
        self.__enemy = new_enemy

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, new_screen):
        self.__screen = new_screen

    def player_shoot(self):
        self.player.shoot(self.enemy)

    def close_window(self):
        self.player.life = 0

    def key_press(self, ship):
        onkey(ship.move_up, "Up")
        onkey(ship.move_down, "Down")
        onkey(ship.move_left, "Left")
        onkey(ship.move_right, "Right")
        onkey(self.player_shoot, "space")
        onkey(self.close_window, "Escape")

    def play_game(self):
        self.screen = Screen()
        self.screen.setup(1280, 720)
        self.screen.bgpic("space_bg.gif")
        self.screen.title("Galaxoid")
        life_title = self.show_life()
        life_title.write(f"Life: {self.player.life}",
                         font=("Arial", 42, "normal"))
        score_title = self.show_score()
        score_title.write(f"Score: {self.player.score}",
                          font=("Arial", 42, "normal"))
        self.key_press(self.player)
        self.screen.listen()
        player_score = 0
        player_life = 3
        enemy_turn = 1
        wave = 1
        while True:
            if not self.player.life:
                break
            if player_life > self.player.life:
                life_title.undo()
                if self.player.life == 1:
                    life_title.color("red")
                life_title.write(f"Life: {self.player.life}",
                                 font=("Arial", 42, "normal"))
            if player_score < self.player.score:
                score_title.undo()
                score_title.write(f"Score: {self.player.score}",
                                  font=("Arial", 42, "normal"))
            if all(enemy_ship is None for enemy_ship in
                   self.enemy.values()) and wave % 10 == 0:
                self.player.shoot_status = False
                self.boss_spawn(wave)
                wave += 1
                self.player.shoot_status = True
            elif all(enemy_ship is None for enemy_ship in self.enemy.values()):
                self.player.shoot_status = False
                self.spawn(wave)
                wave += 1
                self.player.shoot_status = True
            if enemy_turn % 20 == 0:
                choice([enemy_ship for enemy_ship in self.enemy.values()
                        if isinstance(enemy_ship, EnemyShip) or
                        isinstance(enemy_ship, BossShip)]).move()
            elif enemy_turn % 30 == 0:
                choice([enemy_ship for enemy_ship in self.enemy.values()
                        if isinstance(enemy_ship, EnemyShip) or
                        isinstance(enemy_ship, BossShip)]).shoot(self.player)
            enemy_turn += 1
            self.screen.update()
        bye()

    def spawn(self, wave):
        self.enemy.clear()
        self.enemy.update({index: EnemyShip(randrange(100, 201, 50))
                           for index in range(wave)})

    def boss_spawn(self, wave):
        self.enemy.clear()
        self.enemy.update({0: BossShip(wave)})

    def show_life(self):
        life_title = Turtle()
        life_title.hideturtle()
        life_title.penup()
        life_title.color("white")
        life_title.setpos(-550, 300)
        return life_title

    def show_score(self):
        score_title = Turtle()
        score_title.hideturtle()
        score_title.penup()
        score_title.color("white")
        score_title.setpos(350, 300)
        return score_title
