import math
from abc import ABC, abstractmethod
from math import *


class Calculator:

    def __init__(self):
        pass

    def get_angle(self, x1: int, y1: int, x2: int, y2: int) -> float:
        d = x2 - x1
        y = y2 - y1
        mod = self.get_distance(x1, y1, x2, y2)
        theta = pi - acos(d / mod) if y < 0 else pi + acos(d / mod)

        # print(theta,theta*(180/pi) ,end=" ")

        return theta

    def get_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return pow(
            (x2 - x1) ** 2 + (y2 - y1) ** 2,
            0.5
        )

    def get_components(self, force: float, angle: float):
        horizontal = force * cos(angle)
        vertical = force * sin(angle)
        # print(horizontal, vertical)
        return [horizontal, vertical]


class Field:
    def __init__(self, G: float, time: float, objects_list):
        self.objects_list = objects_list
        self.time = time
        self.G = G

    def update(self):
        pervious_state = self.objects_list.copy()

        for planets in self.objects_list:
            planets.acceration(pervious_state, G=self.G)

        for planets in self.objects_list:
            planets.move(time=self.time)

        return self.objects_list

    def get_field(self):
        return self.objects_list

    def print_field(self):
        for i in self.objects_list:
            print(i)
        print("_" * 50)

    def number_of_objects(self) -> int:
        return len(self.objects_list)

class Things:

    def __init__(self, mass: int, x: int, y: int, vel_x: int, vel_y: int, tag: str = "", color: str = None,
                 density: int = 1000):
        self.moveable = False
        self.mass = mass
        self.pos_x = x
        self.pos_y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.tag = tag
        self.a = [0, 0]
        self.color = color
        self.radius = (mass // density)

    def get_coords(self) -> list[int]:
        return [self.pos_x, self.pos_y]

    def get_coords_draw(self) -> list[int]:
        return [self.pos_x + 750, 400 - self.pos_y]

    @abstractmethod
    def get_force_applied(self, field, G: float) -> list[float]:
        ...

    def acceration(self, field, G: float) -> None:
        f = self.get_force_applied(field, G)
        self.a = [f[0] / self.mass, f[1] / self.mass]

    def move(self, time: int):
        self.vel_x -= self.a[0] * time
        self.vel_y -= self.a[1] * time

        self.pos_x += self.vel_x * time
        self.pos_y += self.vel_y * time

    def get_tag(self):
        return self.tag

    def __str__(self):
        return (f"{self.color} "
                f""
                f"{self.tag} at {self.pos_x},{self.pos_y} going with speed {self.vel_x, self.vel_y} has mass {self.mass}")


class Sun(Things):

    def __init__(self, mass: int, x: int, y: int, vel_x: int, vel_y: int, tag: str = "", color: str = "yellow",
                 density: int = 1000):
        super().__init__(mass, x, y, vel_x, vel_y, tag="sun", color=color, density=density)

    def get_force_applied(self, field: Field, G) -> list[int]:
        return [0, 0]


class Planet(Things):
    def __init__(self, mass: int, x: int, y: int, density: int, vel_x: int, vel_y: int, tag: str = "", color: str = "cyan"):
        super().__init__(mass, x, y, vel_x, vel_y, tag, color, density=density)
        self.cal = Calculator()

    def single_force(self, other, G: float):
        nu = self.mass * other.mass
        de = self.cal.get_distance(self.pos_x, self.pos_y, other.pos_x, other.pos_y) ** 2
        if de == 0:
            f = G * (nu / 1)
        else:
            f = G * (nu / de)

        return self.cal.get_components(f, self.cal.get_angle(self.pos_x, self.pos_y, other.pos_x, other.pos_y))

    def get_force_applied(self, field, G: float) -> list[float]:
        f = [0, 0]
        for obj in field:
            if obj.tag != self.tag:
                f_new = self.single_force(obj, G)
                f[0] += f_new[0]
                f[1] += f_new[1]

        return f

#
# if __name__ == "__main__":
#     suns = [
#         Sun(
#             mass=10000,
#             x=0,
#             y=0,
#             vel_y=0,
#             vel_x=0,
#             tag="sun"
#         ),
#         Planet(
#             mass=100,
#             x=100,
#             y=0,
#             vel_x=0,
#             vel_y=0,
#             tag='Plante'
#         )
#     ]
#
#     G = 100
#     time = 5
#     field = Field(G, time / 1000, suns)
#
#     field.update()
