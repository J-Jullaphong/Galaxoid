from random import choice, randrange
from turtle import Screen, Turtle, onkey, bye, register_shape
from ship import PlayerShip, EnemyShip, BossShip
from item import Buff
from time import sleep

story_lines = ["Galaxoid, A Space Terrorist has spread",
               "its power around the galaxy.",
               "It is a dark time for the Empire.",
               "An Endless War has begun.",
               "Your job is to end this war."]


class Game:
    def __init__(self, player_name=""):
        register_shape("images/enemy_ship.gif")
        register_shape("images/player_ship.gif")
        register_shape("images/boss_ship.gif")
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

    def player_move_up(self):
        self.player.move_up(self.enemy)

    def player_move_down(self):
        self.player.move_down(self.enemy)

    def player_move_left(self):
        self.player.move_left(self.enemy)

    def player_move_right(self):
        self.player.move_right(self.enemy)

    def close_window(self):
        self.player.life = 0

    def key_press(self):
        onkey(self.player_move_up, "Up")
        onkey(self.player_move_down, "Down")
        onkey(self.player_move_right, "Right")
        onkey(self.player_move_left, "Left")
        onkey(self.player_shoot, "space")
        onkey(self.close_window, "Escape")

    def play_game(self):
        self.screen = Screen()
        self.screen.setup(1280, 720)
        self.screen.bgpic("images/space_bg.gif")
        self.screen.title("Galaxoid")
        self.title()
        self.story(story_lines)
        life_title = self.show_life()
        life_title.write(f"Life: {self.player.life}",
                         font=("Arial", 42, "normal"))
        score_title = self.show_score()
        score_title.write(f"Score: {self.player.score}",
                          font=("Arial", 42, "normal"))
        self.key_press()
        self.screen.listen()
        self.player.pendown()
        self.player.goto(-500, 0)
        self.player.clear()
        self.player.penup()
        player_score = 0
        player_life = 3
        while True:
            if not self.player.life:
                self.game_over()
                sleep(3)
                break
            if player_life != self.player.life:
                player_life = self.player.life
                life_title.undo()
                if self.player.life == 1:
                    life_title.color("red")
                    life_title.write("!!DANGER!!",
                                     font=("Arial", 42, "normal"))
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
                self.boss_spawn()
                self.wave += 1
                self.player.shoot_status = True
            elif all(enemy_ship is None for enemy_ship in self.enemy.values()):
                self.player.shoot_status = False
                self.spawn()
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
            self.screen.update()
        bye()

    def spawn(self):
        self.enemy.clear()
        self.enemy.update({index: EnemyShip()
                           for index in range(self.wave + 3)})

    def boss_spawn(self):
        self.enemy.clear()
        self.enemy[0] = BossShip(self.wave)

    def buff_spawn(self):
        self.buff.clear()
        self.buff[0] = Buff()

    def title(self):
        title_turtle = Turtle(visible=False)
        title_turtle.color("#FFE81F")
        title_turtle.penup()
        title_turtle.sety(-100)
        title_turtle.write("GALAXOID", font=("Arial", 200, "bold"),
                           align="center")
        sleep(5)
        title_turtle.clear()

    def story(self, story):
        story_turtle = Turtle(visible=False)
        story_turtle.color("#43A5CF")
        story_turtle.penup()
        story_turtle.write("A long time yet to come in a galaxy "
                           "very very close...", font=("Arial", 42, "normal"),
                           align="center")
        sleep(3)
        story_turtle.color("#FFE81F")
        story_turtle.sety(50)
        for line in range(len(story)):
            story_turtle.clear()
            try:
                story_turtle.write(story[line], font=("Arial", 42, "normal"),
                                   align="center")
                story_turtle.sety(0)
                story_turtle.write(story[line+1], font=("Arial", 42, "normal"),
                                   align="center")
                story_turtle.sety(-50)
                story_turtle.write(story[line+2], font=("Arial", 42, "normal"),
                                   align="center")
                story_turtle.sety(50)
                sleep(4)
            except IndexError:
                sleep(2)
                story_turtle.clear()
                break

    def show_life(self):
        life_title = Turtle(visible=False)
        life_title.penup()
        life_title.color("white")
        life_title.setpos(-550, 300)
        return life_title

    def show_score(self):
        score_title = Turtle(visible=False)
        score_title.penup()
        score_title.color("white")
        score_title.setpos(350, 300)
        return score_title

    def game_over(self):
        game_over = Turtle(visible=False)
        game_over.penup()
        game_over.color("red")
        game_over_shadow = Turtle(visible=False)
        game_over_shadow.penup()
        game_over_shadow.color("white")
        game_over_shadow.sety(-8)
        game_over_shadow.forward(8)
        game_over_shadow.write(f"GAME OVER", font=("Arial", 100, "bold"), align="center")
        game_over.write(f"GAME OVER", font=("Arial", 100, "bold"), align="center")
