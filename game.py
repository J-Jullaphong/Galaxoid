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
        """ Setting up game with player, enemy, buff, wave, and screen
        attributes
        """
        # Register shapes into the game
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
        """ Player property represent PlayerShip"""
        return self.__player

    @player.setter
    def player(self, new_player):
        self.__player = new_player

    @property
    def enemy(self):
        """ Enemy property represents Dictionary of EnemyShip(s) """
        return self.__enemy

    @enemy.setter
    def enemy(self, new_enemy):
        """Sets the Dictionary of Enemy """
        self.__enemy = new_enemy

    @property
    def buff(self):
        """ Buff property represents Dictionary of Buff """
        return self.__buff

    @buff.setter
    def buff(self, new_buff):
        """Sets the Dictionary of Buff """
        self.__buff = new_buff

    @property
    def wave(self):
        """ Wave property represents Wave of the game """
        return self.__wave

    @wave.setter
    def wave(self, new_wave):
        """Sets the wave of the game"""
        self.__wave = new_wave

    @property
    def screen(self):
        """ Screen property represents Screen of the game """
        return self.__screen

    @screen.setter
    def screen(self, new_screen):
        """Sets the screen of the game"""
        self.__screen = new_screen

    def player_shoot(self):
        """ Add Enemy Argument to PlayerShip.shoot() """
        self.player.shoot(self.enemy)

    def player_move_up(self):
        """ Add Enemy Argument to PlayerShip.move_up() """
        self.player.move_up(self.enemy)

    def player_move_down(self):
        """ Add Enemy Argument to PlayerShip.move_down() """
        self.player.move_down(self.enemy)

    def player_move_left(self):
        """ Add Enemy Argument to PlayerShip.move_left() """
        self.player.move_left(self.enemy)

    def player_move_right(self):
        """ Add Enemy Argument to PlayerShip.move_right() """
        self.player.move_right(self.enemy)

    def close_window(self):
        """ Set Player's life to 0 to close the game """
        self.player.life = 0

    def key_press(self):
        """ Receive Player's Key Pressing """
        onkey(self.player_move_up, "Up")
        onkey(self.player_move_down, "Down")
        onkey(self.player_move_right, "Right")
        onkey(self.player_move_left, "Left")
        onkey(self.player_shoot, "space")
        onkey(self.close_window, "Escape")

    def play_game(self):
        """ Start, run, and manage the game """
        # Sets the screen up
        self.screen = Screen()
        self.screen.setup(1280, 720)
        self.screen.bgpic("images/space_bg.gif")
        self.screen.title("Galaxoid")
        # Display game's title and story
        self.title()
        self.story(story_lines)
        # Create life-board and scoreboard
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
            # Check if player life run out
            if self.player.life <= 0:
                self.game_over()
                break
            # Check current player's life to update the life-board
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
            # Check current player's score to update the scoreboard
            if player_score < self.player.score:
                score_title.undo()
                score_title.write(f"Score: {self.player.score}",
                                  font=("Arial", 42, "normal"))
            # Check if there are no more Hostile ships in the screen
            # and spawn EnemyShip or BossShip according to game's wave
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
            # Check if buff is existed in the screen
            if not self.buff:
                self.buff_spawn()
            # Check if the player get buff and apply buff effect to the player
            elif self.buff[0].is_buff_collide(self.player):
                self.buff[0].clear_buff()
                self.buff[0].heal(self.player)
                self.buff_spawn()
            # Random number to determine what Hostile ships do in each turn
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
        # Close the game screen
        bye()

    def spawn(self):
        """ Spawn EnemyShip(s) into the game """
        self.enemy.clear()
        self.enemy.update({index: EnemyShip()
                           for index in range(self.wave + 3)})

    def boss_spawn(self):
        """ Spawn BossShip into the game """
        self.enemy.clear()
        self.enemy[0] = BossShip(self.wave)

    def buff_spawn(self):
        """ Spawn Buff into the game """
        self.buff.clear()
        self.buff[0] = Buff()

    def title(self):
        """ Display Game's Title """
        title_turtle = Turtle(visible=False)
        title_turtle.color("#FFE81F")
        title_turtle.penup()
        title_turtle.sety(-100)
        title_turtle.write("GALAXOID", font=("Arial", 200, "bold"),
                           align="center")
        sleep(5)
        title_turtle.clear()

    def story(self, story):
        """ Display Game's Story """
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
                sleep(3)
            except IndexError:
                sleep(2)
                story_turtle.clear()
                break

    def show_life(self):
        """ Display Player's Life """
        life_title = Turtle(visible=False)
        life_title.penup()
        life_title.color("white")
        life_title.setpos(-550, 300)
        return life_title

    def show_score(self):
        """ Display Player's Score """
        score_title = Turtle(visible=False)
        score_title.penup()
        score_title.color("white")
        score_title.setpos(350, 300)
        return score_title

    def game_over(self):
        """ Display Game Over """
        game_over = Turtle(visible=False)
        game_over.penup()
        game_over.color("red")
        game_over_shadow = Turtle(visible=False)
        game_over_shadow.penup()
        game_over_shadow.color("white")
        game_over_shadow.sety(-8)
        game_over_shadow.forward(8)
        game_over_shadow.write(f"GAME OVER", font=("Arial", 100, "bold"),
                               align="center")
        game_over.write(f"GAME OVER", font=("Arial", 100, "bold"),
                        align="center")
        sleep(3)
