from random import randrange
from turtle import Turtle
from item import Laser


class PlayerShip(Turtle):
    def __init__(self, name=""):
        super().__init__(visible=False)
        self.__name = name
        self.__score = 0
        self.__life = 3
        self.__shoot_status = False
        self.__shot_count = 0
        self.__hit_count = 0
        self.pensize(15)
        self.speed(0)
        self.shapesize(3)
        self.color("white")
        self.penup()
        self.goto(-700, randrange(-100, 100))
        self.showturtle()

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

    @property
    def shot_count(self):
        return self.__shot_count

    @shot_count.setter
    def shot_count(self, new_shot_count):
        self.__shot_count = new_shot_count

    @property
    def hit_count(self):
        return self.__hit_count

    @hit_count.setter
    def hit_count(self, new_hit_count):
        self.__hit_count = new_hit_count

    @property
    def accuracy(self):
        if self.shot_count == 0:
            return 0
        return (self.hit_count / self.shot_count) * 100

    def move_up(self, enemies):
        if self.ycor() + 10 < 360:
            self.goto(self.xcor(), self.ycor() + 10)
            self.enemy_collide(enemies)

    def move_down(self, enemies):
        if self.ycor() - 10 > -360:
            self.goto(self.xcor(), self.ycor() - 10)
            self.enemy_collide(enemies)

    def move_left(self, enemies):
        if self.xcor() - 20 > -640:
            self.backward(20)
            self.enemy_collide(enemies)

    def move_right(self, enemies):
        if self.xcor() + 20 < 640:
            self.forward(20)
            self.enemy_collide(enemies)

    def add_score(self, enemy):
        enemy.hideturtle()
        self.score += enemy.point

    def shoot(self, enemies):
        if self.shoot_status:
            self.shoot_status = False
            self.shot_count += 1
            laser = Laser(self)
            while laser.xcor() < 650:
                for index, enemy_ship in enemies.items():
                    if isinstance(enemy_ship, EnemyShip) \
                            and laser.is_collide(enemy_ship):
                        self.add_score(enemy_ship)
                        self.hit_count += 1
                        enemies[index] = None
                        laser.clear_laser()
                        break
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
        return abs(self.xcor() - enemy.xcor()) < 20 \
               and abs(self.ycor() - enemy.ycor()) < 30

    def enemy_collide(self, enemies):
        for index, enemy in enemies.items():
            if isinstance(enemy, EnemyShip) and self.is_enemy_collide(enemy):
                enemies[index] = None
                enemy.hideturtle()
                self.life -= 1
                return None


class EnemyShip(Turtle):
    def __init__(self):
        super().__init__(visible=False)
        self.__point = 100
        self.shapesize(3)
        self.color("orange")
        self.pencolor("white")
        self.penup()
        self.speed(0)
        self.goto(700, 0)
        self.setheading(180)
        self.pendown()
        self.pensize(15)
        self.showturtle()
        self.goto(randrange(300, 551, 20), randrange(-300, 301, 20))
        self.penup()
        self.clear()
        self.speed(5)

    @property
    def point(self):
        return self.__point

    def move(self):
        self.goto(randrange(-300, 600), randrange(-300, 300))

    def shoot(self, player):
        player.shoot_status = False
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
        player.shoot_status = True


class BossShip(Turtle):
    def __init__(self, health=0):
        super().__init__(visible=False)
        self.__health = health
        self.__point = 5000
        self.penup()
        self.shapesize(25)
        self.color("red")
        self.pencolor("white")
        self.pensize(50)
        self.speed(0)
        self.goto(700, 0)
        self.setheading(180)
        self.showturtle()
        self.pendown()
        self.goto(randrange(250, 401, 50), randrange(-100, 101, 50))
        self.clear()
        self.penup()
        self.speed(5)

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
