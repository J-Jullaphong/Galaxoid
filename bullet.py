from turtle import Turtle


class Laser(Turtle):
    def __init__(self, ship):
        super().__init__()
        self.hideturtle()
        self.color("red")
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
