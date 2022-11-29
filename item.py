from turtle import Turtle
from random import randrange
from sys import platform


class Laser(Turtle):
    def __init__(self, ship):
        super().__init__(visible=False)
        self.hideturtle()
        self.color("red")
        if platform == "win32":
            self.speed(5)
        elif platform == "darwin":
            self.speed(0)
        self.penup()
        self.pensize(10)
        self.goto(ship.pos())
        self.pendown()

    def is_collide(self, other):
        return abs(self.xcor() - other.xcor()) < 100 \
               and abs(self.ycor() - other.ycor()) < 20

    def is_boss_collide(self, other):
        return abs(self.xcor() - other.xcor()) < 100 \
               and abs(self.ycor() - other.ycor()) < 125

    def is_boss_laser_collide(self, other):
        return abs(self.xcor() - other.xcor()) < 100 \
               and abs(self.ycor() - other.ycor()) < 100

    def clear_laser(self):
        self.penup()
        self.goto(1000, 0)


class Buff(Turtle):
    def __init__(self):
        super().__init__(visible=False)
        self.color("yellow")
        self.speed(0)
        self.penup()
        self.shape("circle")
        self.goto(randrange(-500, 0, 20), randrange(-300, 300, 20))
        self.showturtle()

    def heal(self, player):
        if player.life < 5:
            player.life += 1
        elif player.life >= 5:
            player.score += 10

    def is_buff_collide(self, player):
        return abs(self.xcor() - player.xcor()) < 30 \
               and abs(self.ycor() - player.ycor()) < 20

    def clear_buff(self):
        self.hideturtle()
        self.penup()
        self.goto(1000, 0)
