import tkinter as tk
from simulants import *


class Sim:
    def __init__(self, master: tk.Frame, sim_field: Field, cycle: int):
        self.master = master
        self.canvas_main = tk.Canvas(self.master, height=800, width=1500, bg='black')

        self.sim_field = sim_field

        self.SUN_RADIUS = 25
        self.SUN_COLOR = 'yellow'

        self.prev = {}

        self.cycle = cycle

        self.lines = [{'x1': None,
                       'y1': None,
                       'x2': None,
                       'y2': None,
                       'color': None}
                      for i in range(self.cycle)]

        self.tick = 0

        self.SCREEN_HEIGHT = 800

        self.PLANET_RADIUS = 10
        self.PLANET_COLOR = "cyan"
        self.canvas_main.pack()

        self.state = True

    def state_change(self, e :tk.Event):
        self.state = not self.state
        print(self.state)

    def get_tick(self):
        return self.tick % self.cycle

    def draw(self):
        self.remove()
        obj = self.sim_field.get_field()

        self.tick += 1

        for i in obj:
            c = i.get_coords_draw()

            if "sun" == i.tag:
                self.canvas_main.create_oval(
                    c[0] - self.SUN_RADIUS,
                    c[1] - self.SUN_RADIUS,
                    c[0] + self.SUN_RADIUS,
                    c[1] + self.SUN_RADIUS,
                    fill=i.color,
                    tags='p'
                )
            else:
                self.canvas_main.create_oval(
                    c[0] - self.PLANET_RADIUS,
                    c[1] - self.PLANET_RADIUS,
                    c[0] + self.PLANET_RADIUS,
                    c[1] + self.PLANET_RADIUS,
                    fill=i.color,
                    tags='p'
                )


        self.master.after(self.sim_field.time, self.update)

    def draw_lines(self):
        current_tick = self.get_tick()
        obj = self.sim_field.get_field()
        for i in obj:
            c_new = i.get_coords_draw()
            c_prev = self.prev[i.get_tag()]

            self.canvas_main.create_line(
                c_prev[0], c_prev[1],
                c_new[0], c_new[1],
                fill=i.color, tags=str("line_") + str(current_tick)
            )

    def remove_previous_line(self):
        current_tick = self.get_tick()
        self.canvas_main.delete(str("line_") + str(current_tick))

    def remove(self):
        self.canvas_main.delete('p')

    def paused(self):
        self.master.after(16, self.update)

    def update(self):
        if self.state:
            for obj in self.sim_field.get_field():
                self.prev[obj.get_tag()] = obj.get_coords_draw()

            self.sim_field.update()

            self.remove_previous_line()

            self.draw_lines()

            self.master.after(16, self.draw)
        else:
            self.master.after(16, self.paused)


