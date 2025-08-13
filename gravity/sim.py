import tkinter as tk
from simulants import *


class Sim:
    def __init__(self, master: tk.Frame, sim_field: Field, cycle: int = 100):
        self.prev = {}
        self.master = master
        self.canvas_main = tk.Canvas(self.master, height=800, width=1500, bg='black')

        self.sim_field = sim_field

        self.SUN_RADIUS = 25
        self.SUN_COLOR = 'yellow'

        self.offset = [750, 400]  # the shift in orign when arrow keys are pressed

        self.cycle = cycle

        self.scale = 1

        self.lines = [
            [
                {
                    'x1': None,
                    'y1': None,
                    'x2': None,
                    'y2': None,
                    'color': None
                }
                for i in range(self.sim_field.number_of_objects())
            ]
            for j in range(self.cycle)
        ]

        self.tick = 0

        self.SCREEN_HEIGHT = 800

        self.PLANET_RADIUS = 10
        self.PLANET_COLOR = "cyan"
        self.canvas_main.pack()

        self.state = True

    def state_change(self, e: tk.Event):
        self.state = not self.state
        print(self.state)

    def get_tick(self):
        return self.tick % self.cycle

    def draw(self):
        self.remove()
        obj = self.sim_field.get_field()

        for i in obj:
            c = i.get_coords()
            c = self.__get_draw_coords(c[0], c[1])

            r = i.radius / (1 + self.scale * .1)

            if "sun" == i.tag:
                self.canvas_main.create_oval(
                    c[0] - r,
                    c[1] - r,
                    c[0] + r,
                    c[1] + r,
                    fill=i.color,
                    tags='p'
                )
            else:
                self.canvas_main.create_oval(
                    c[0] - r,
                    c[1] - r,
                    c[0] + r,
                    c[1] + r,
                    fill=i.color,
                    tags='p'
                )

        self.master.after(self.sim_field.time, self.update)

    def draw_lines(self):
        current_tick = self.get_tick()
        obj = self.sim_field.get_field()
        for i in range(len(obj)):
            c_new = obj[i].get_coords()
            c_prev = self.prev[obj[i].get_tag()]

            self.lines[current_tick][i] = {
                'x1': c_new[0],
                'y1': c_new[1],
                'x2': c_prev[0],
                'y2': c_prev[1],
                'color': obj[i].color
            }

            c_new = self.__get_draw_coords(c_new[0], c_new[1])
            c_prev = self.__get_draw_coords(c_prev[0], c_prev[1])

            self.canvas_main.create_line(
                c_prev[0], c_prev[1],
                c_new[0], c_new[1],
                fill=obj[i].color, tags=str("line_") + str(current_tick)
            )

    def remove_previous_line(self):
        current_tick = self.get_tick()
        self.canvas_main.delete(str("line_") + str(current_tick))

    def remove(self):
        self.canvas_main.delete('p')

    def paused(self):
        self.master.after(16, self.update)

    def re_draw(self):
        dummy = {
            'x1': None,
            'y1': None,
            'x2': None,
            'y2': None,
            'color': None
        }

        for tick in range(self.cycle):
            for line in self.lines[tick]:
                if line == dummy:
                    continue

                else:
                    c1 = self.__get_draw_coords(line["x1"], line["y1"])
                    c2 = self.__get_draw_coords(line["x2"], line["y2"])
                    self.canvas_main.create_line(
                        c1[0], c1[1],
                        c2[0], c2[1],
                        fill=line["color"], tags=str("line_") + str(tick)
                    )

        obj = self.sim_field.get_field()

        for i in obj:
            c = i.get_coords()
            c = self.__get_draw_coords(c[0], c[1])
            r = i.radius / (1 + self.scale * .1)

            if "sun" == i.tag:
                self.canvas_main.create_oval(
                    c[0] - r,
                    c[1] - r,
                    c[0] + r,
                    c[1] + r,
                    fill=i.color,
                    tags='p'
                )
            else:
                self.canvas_main.create_oval(
                    c[0] - r,
                    c[1] - r,
                    c[0] + r,
                    c[1] + r,
                    fill=i.color,
                    tags='p'
                )

    def shift_objects(self, x_off: int, y_off: int):
        self.offset[0] += x_off
        self.offset[1] += y_off

        self.remove()

        for i in range(self.cycle):
            self.canvas_main.delete(str("line_") + str(i))

        self.master.after(16, self.re_draw)

    def update(self):
        if self.state:

            self.tick += 1

            for obj in self.sim_field.get_field():
                self.prev[obj.get_tag()] = obj.get_coords()

            self.sim_field.update()

            self.remove_previous_line()

            self.draw_lines()

            self.master.after(16, self.draw)
        else:
            self.master.after(16, self.paused)

    def set_scale(self, delta: int = 0):
        if delta <= 0:
            while self.scale + delta <= 0:
                delta *= .1

        self.scale += delta
        for i in range(self.cycle):
            self.canvas_main.delete(str("line_") + str(i))
        self.remove()
        self.re_draw()

    def __get_draw_coords(self, x: int, y: int) -> [int,int]:
        return [
            (x // self.scale) + self.offset[0],
            self.offset[1] - (y // self.scale)
        ]
