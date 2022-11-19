from random import randrange
from turtle import Turtle
from item import Laser


class PlayerShip(Turtle):
    def __init__(self, name=""):
        super().__init__()
        self.__name = name
        self.__score = 0
        self.__life = 3
        self.__shoot_status = False
        self.pensize(5)
        self.speed(0)
        self.shapesize(3)
        self.color("white")
        self.penup()
        self.goto(x=-600, y=0)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, new_score):
        self.__score = new_score

    @property
    def life(self):
        return self.__life

    @life.setter
    def life(self, new_life):
        self.__life = new_life

    @property
    def shoot_status(self):
        return self.__shoot_status

    @shoot_status.setter
    def shoot_status(self, new_status):
        self.__shoot_status = new_status

    def move_up(self):
        if self.ycor() + 10 < 360:
            self.goto(self.xcor(), self.ycor() + 10)

    def move_down(self):
        if self.ycor() - 10 > -360:
            self.goto(self.xcor(), self.ycor() - 10)

    def move_left(self):
        if self.xcor() - 20 > -640:
            self.backward(20)

    def move_right(self):
        if self.xcor() + 20 < 640:
            self.forward(20)

    def add_score(self, enemy):
        enemy.hideturtle()
        self.score += enemy.point

    def shoot(self, enemies):
        if self.shoot_status:
            self.shoot_status = False
            laser = Laser(self)
            while laser.xcor() < 650:
                for index, enemy_ship in enemies.items():
                    if isinstance(enemy_ship, EnemyShip) \
                            and laser.is_collide(enemy_ship):
                        self.add_score(enemy_ship)
                        enemies[index] = None
                        laser.clear_laser()
                        break
                    elif isinstance(enemy_ship, BossShip) \
                            and laser.is_boss_collide(enemy_ship):
                        laser.clear_laser()
                        enemy_ship.health -= 1
                        if enemy_ship.health <= 0:
                            self.add_score(enemy_ship)
                            enemies[index] = None
                            break
                        break
                laser.forward(100)
                laser.clear()
            self.shoot_status = True


class EnemyShip(Turtle):
    def __init__(self, point=0):
        super().__init__()
        self.__point = point
        self.hideturtle()
        self.shapesize(3)
        self.color("orange")
        self.penup()
        self.goto(700, 0)
        self.setheading(180)
        self.showturtle()
        self.speed(5)
        self.goto(randrange(300, 601, 50), randrange(-300, 301, 50))

    @property
    def point(self):
        return self.__point

    def move(self):
        self.goto(randrange(-300, 600), randrange(-300, 300))

    def shoot(self, player):
        enemy_laser = Laser(self)
        enemy_laser.color("green")
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
        super().__init__()
        self.__health = health
        self.__point = 5000
        self.hideturtle()
        self.penup()
        self.shapesize(25)
        self.color("red")
        self.speed(0)
        self.goto(700, 0)
        self.setheading(180)
        self.showturtle()
        self.speed(5)
        self.goto(randrange(300, 551, 50), randrange(-100, 101, 50))

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, new_health):
        self.__health = new_health

    @property
    def point(self):
        return self.__point

    def move(self):
        self.goto(randrange(0, 500), randrange(-100, 100))

    def shoot(self, player):
        enemy_laser = Laser(self)
        enemy_laser.color("blue")
        enemy_laser.pensize(150)
        while enemy_laser.xcor() > -650:
            if isinstance(player, PlayerShip) \
                    and enemy_laser.is_boss_laser_collide(player):
                player.life = 0
                enemy_laser.penup()
                enemy_laser.goto(-1000, 0)
            enemy_laser.backward(100)
        enemy_laser.clear()
