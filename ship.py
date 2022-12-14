from random import randrange
from turtle import Turtle
from item import Laser
from sys import platform


class PlayerShip(Turtle):
    def __init__(self, name=""):
        """ Create Player's Ship Sprite with name, score, life, shoot_status,
        shot_count, and hit_count attributes
        """
        super().__init__(visible=False)
        self.__name = name
        self.__score = 0
        self.__life = 3
        self.__shoot_status = False
        self.__shot_count = 0
        self.__hit_count = 0
        self.shape("images/player_ship.gif")
        self.pensize(15)
        # Check user's OS to set speed
        if platform == "win32":
            self.speed(5)
        elif platform == "darwin":
            self.speed(0)
        self.color("#BA0000")
        self.penup()
        self.goto(-700, randrange(-100, 100))
        self.showturtle()

    @property
    def name(self):
        """ Name property represents Player's Name """
        return self.__name

    @name.setter
    def name(self, new_name):
        """Sets the name of Player"""
        self.__name = new_name

    @property
    def score(self):
        """ Score property represents Player's Score """
        return self.__score

    @score.setter
    def score(self, new_score):
        """Sets the score of Player"""
        self.__score = new_score

    @property
    def life(self):
        """ Life property represents Player's Life """
        return self.__life

    @life.setter
    def life(self, new_life):
        """Sets the life of Player"""
        self.__life = new_life

    @property
    def shoot_status(self):
        """ Shoot Status property represents Player's Shoot Status """
        return self.__shoot_status

    @shoot_status.setter
    def shoot_status(self, new_status):
        """Sets the shoot status of Player"""
        self.__shoot_status = new_status

    @property
    def shot_count(self):
        """ Shot Count property represents Player's Total Shot Count """
        return self.__shot_count

    @shot_count.setter
    def shot_count(self, new_shot_count):
        """Sets the shot count of Player"""
        self.__shot_count = new_shot_count

    @property
    def hit_count(self):
        """ Hit Count property represents Player's Total Hit Count """
        return self.__hit_count

    @hit_count.setter
    def hit_count(self, new_hit_count):
        """Sets the hit count of Player"""
        self.__hit_count = new_hit_count

    @property
    def accuracy(self):
        """ Accuracy property represents Player's Shot Accuracy """
        if self.shot_count == 0:
            return 0
        return (self.hit_count / self.shot_count) * 100

    def move_up(self, enemies):
        """ Move Player's Ship Sprite Up """
        if self.ycor() + 10 < 360:
            self.goto(self.xcor(), self.ycor() + 10)
            self.enemy_collide(enemies)

    def move_down(self, enemies):
        """ Move Player's Ship Sprite Down """
        if self.ycor() - 10 > -360:
            self.goto(self.xcor(), self.ycor() - 10)
            self.enemy_collide(enemies)

    def move_left(self, enemies):
        """ Move Player's Ship Sprite Left """
        if self.xcor() - 20 > -640:
            self.backward(20)
            self.enemy_collide(enemies)

    def move_right(self, enemies):
        """ Move Player's Ship Sprite Right """
        if self.xcor() + 20 < 640:
            self.forward(20)
            self.enemy_collide(enemies)

    def add_score(self, enemy):
        """ Add Enemy's Point to Player """
        enemy.hideturtle()
        self.score += enemy.point

    def shoot(self, enemies):
        """ Shoot out Laser and check collision with enemies """
        if self.shoot_status:
            self.shoot_status = False
            self.shot_count += 1
            laser = Laser(self)
            while laser.xcor() < 650:
                for index, enemy_ship in enemies.items():
                    # Check Collision with EnemyShip
                    if isinstance(enemy_ship, EnemyShip) \
                            and laser.is_collide(enemy_ship):
                        self.add_score(enemy_ship)
                        self.hit_count += 1
                        enemies[index] = None
                        laser.clear_laser()
                        break
                    # Check Collision with BossShip
                    elif isinstance(enemy_ship, BossShip) \
                            and laser.is_boss_collide(enemy_ship):
                        laser.clear_laser()
                        enemy_ship.health -= 1
                        self.hit_count += 1
                        if enemy_ship.health <= 0:
                            self.add_score(enemy_ship)
                            enemies[index] = None
                            break
                        break
                laser.forward(100)
                laser.clear()
            self.shoot_status = True

    def is_enemy_collide(self, enemy):
        """ Check PlayerShip and EnemyShip Collision """
        return abs(self.xcor() - enemy.xcor()) < 20 \
               and abs(self.ycor() - enemy.ycor()) < 30

    def enemy_collide(self, enemies):
        """ Apply Collision Effect to PlayerShip and EnemyShip """
        for index, enemy in enemies.items():
            if isinstance(enemy, EnemyShip) and self.is_enemy_collide(enemy):
                enemies[index] = None
                enemy.hideturtle()
                self.life -= 1
                return None


class EnemyShip(Turtle):
    def __init__(self):
        """ Create Enemy's Ship Sprite with point attribute """
        super().__init__(visible=False)
        self.__point = 100
        self.shape("images/enemy_ship.gif")
        self.color("#4800C9")
        self.penup()
        # Check user's OS to set speed
        if platform == "win32":
            self.speed(5)
        elif platform == "darwin":
            self.speed(0)
        self.goto(700, 0)
        self.setheading(180)
        self.pendown()
        self.pensize(15)
        self.showturtle()
        self.goto(randrange(300, 551, 20), randrange(-300, 301, 20))
        self.penup()
        self.clear()
        if platform == "win32":
            self.speed(1)
        elif platform == "darwin":
            self.speed(5)

    @property
    def point(self):
        """ Point property represents Enemy's Point """
        return self.__point

    def move(self):
        """ Randomly move EnemyShip across the screen """
        self.goto(randrange(-300, 600), randrange(-300, 300))

    def shoot(self, player):
        """ Shoot out Laser and check collision with PlayerShip """
        enemy_laser = Laser(self)
        enemy_laser.color("#29FF11")
        while enemy_laser.xcor() > -650:
            if isinstance(player, PlayerShip) \
                    and enemy_laser.is_collide(player):
                player.life -= 1
                enemy_laser.penup()
                enemy_laser.goto(-1000, 0)
            enemy_laser.backward(100)
            enemy_laser.clear()


class BossShip(Turtle):
    def __init__(self, health=0):
        """ Create Boss's Ship Sprite with health, and point attributes """
        super().__init__(visible=False)
        self.__health = health
        self.__point = 5000
        self.penup()
        self.shape("images/boss_ship.gif")
        self.color("#4800C9")
        self.pensize(50)
        # Check user's OS to set speed
        if platform == "win32":
            self.speed(5)
        elif platform == "darwin":
            self.speed(0)
        self.goto(700, 0)
        self.setheading(180)
        self.showturtle()
        self.pendown()
        self.goto(randrange(250, 401, 50), randrange(-100, 101, 50))
        self.clear()
        self.penup()
        # Check user's OS to set speed
        if platform == "win32":
            self.speed(1)
        elif platform == "darwin":
            self.speed(5)

    @property
    def health(self):
        """ Health property represents Boss's Health """
        return self.__health

    @health.setter
    def health(self, new_health):
        """Sets the health of Boss"""
        self.__health = new_health

    @property
    def point(self):
        """ Point property represents Boss's Point """
        return self.__point

    def move(self):
        """ Randomly move BossShip across the screen """
        self.goto(randrange(0, 500), randrange(-100, 100))

    def shoot(self, player):
        """ Shoot out Laser and check collision with PlayerShip """
        enemy_laser = Laser(self)
        enemy_laser.color("#29FF11")
        enemy_laser.pensize(150)
        while enemy_laser.xcor() > -650:
            if isinstance(player, PlayerShip) \
                    and enemy_laser.is_boss_laser_collide(player):
                player.life = 0
                enemy_laser.penup()
                enemy_laser.goto(-1000, 0)
            enemy_laser.backward(100)
        enemy_laser.clear()
