from random import choice, randrange
from turtle import Screen, Turtle, onkey, bye
from ship import PlayerShip, EnemyShip, BossShip
from item import Buff


class Game:
    def __init__(self, player_name=""):
        self.__player = PlayerShip(player_name)
        self.__enemy = {}
        self.__buff = {}
        self.__wave = 1
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
    def buff(self):
        return self.__buff

    @buff.setter
    def buff(self, new_buff):
        self.__buff = new_buff

    @property
    def wave(self):
        return self.__wave

    @wave.setter
    def wave(self, new_wave):
        self.__wave = new_wave

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
        while True:
            if not self.player.life:
                break
            if player_life != self.player.life:
                player_life = self.player.life
                life_title.undo()
                if self.player.life == 1:
                    life_title.color("red")
                elif self.player.life != 1:
                    life_title.color("white")
                life_title.write(f"Life: {self.player.life}",
                                 font=("Arial", 42, "normal"))
            if player_score < self.player.score:
                score_title.undo()
                score_title.write(f"Score: {self.player.score}",
                                  font=("Arial", 42, "normal"))
            if all(enemy_ship is None for enemy_ship in
                   self.enemy.values()) and self.wave % 10 == 0:
                self.player.shoot_status = False
                self.boss_spawn(self.wave)
                self.wave += 1
                self.player.shoot_status = True
            elif all(enemy_ship is None for enemy_ship in self.enemy.values()):
                self.player.shoot_status = False
                self.spawn(self.wave)
                self.wave += 1
                self.player.shoot_status = True
            if not self.buff:
                self.buff_spawn()
            elif self.buff[0].is_buff_collide(self.player):
                self.buff[0].clear_buff()
                self.buff[0].heal(self.player)
                self.buff_spawn()
            enemy_turn = randrange(1, 100)
            if enemy_turn % 3 == 0:
                choice([enemy_ship for enemy_ship in self.enemy.values()
                        if isinstance(enemy_ship, EnemyShip) or
                        isinstance(enemy_ship, BossShip)]).move()
            elif enemy_turn % 5 == 0:
                choice([enemy_ship for enemy_ship in self.enemy.values()
                        if isinstance(enemy_ship, EnemyShip) or
                        isinstance(enemy_ship, BossShip)]).shoot(self.player)
            self.player.enemy_collide(self.enemy)
            self.screen.update()
        bye()

    def spawn(self, wave):
        self.enemy.clear()
        self.enemy.update({index: EnemyShip()
                           for index in range(wave + 3)})

    def boss_spawn(self, wave):
        self.enemy.clear()
        self.enemy[0] = BossShip(wave)

    def buff_spawn(self):
        self.buff.clear()
        self.buff[0] = Buff()

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
