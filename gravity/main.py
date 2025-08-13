import tkinter as tk
from sim import Sim
from simulants import *
from typing import Optional
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Main:

    def __init__(self, master: tk.Tk):
        self.master = master

        self.tick = 0
        self.images = []

        self.font = ("Helvetica", 16)
        self.object_list = []
        self.PLANET_RADIUS = 10
        self.SUN_RADIUS = 25

        self.TIME = 1
        self.G = 30

        self.binding()

        self.load_objects_setup()
        self.place_objects_setup()

        self.state = "setup"

    def event_handler(self, e: tk.Event):
        print(e.keysym)
        if e.keysym == 'space':
            if self.state == "siming":
                self.sim.state_change(e)
            else:
                pass

        if e.keysym == "Escape":
            if self.state == "siming":
                self.sim_frame.destroy()
                self.object_list = []

                self.load_objects_setup()
                self.place_objects_setup()

        if e.keysym == "Left":
            if self.state == "siming":
                self.sim.shift_objects(50, 0)

        if e.keysym == "Right":
            if self.state == "siming":
                self.sim.shift_objects(-50, 0)

        if e.keysym == "Up":
            if self.state == "siming":
                self.sim.shift_objects(0, 50)

        if e.keysym == "Down":
            if self.state == "siming":
                self.sim.shift_objects(0, -50)

        if e.keysym == "??":
            if self.state == "siming":
                self.sim.set_scale(delta=e.delta // 120)

    def binding(self):
        self.master.bind("<space>", self.event_handler)
        self.master.bind("<Escape>", self.event_handler)
        self.master.bind("<Left>", self.event_handler)
        self.master.bind("<Right>", self.event_handler)
        self.master.bind("<Up>", self.event_handler)
        self.master.bind("<Down>", self.event_handler)
        self.master.bind("<MouseWheel>", self.event_handler)

    def setup_add_sun(self):
        attribute = self.get_inputs()

        new_sun = Sun(
            mass=attribute['mass'],
            x=attribute['x'],
            y=attribute['y'],
            vel_x=attribute['vx'],
            vel_y=attribute['vy'],
            tag="sun"
        )

        self.object_list.append(new_sun)
        self.draw_object_on_preview(new_sun)

    def setup_add_planet(self):
        attribute = self.get_inputs()

        new_planet = Planet(
            mass=attribute['mass'],
            density=attribute['density'],
            x=attribute['x'],
            y=attribute['y'],
            vel_x=attribute['vx'],
            vel_y=attribute['vy'],
            color=attribute['color'],
            tag="p" + str(len(self.object_list))
        )

        self.object_list.append(new_planet)
        self.draw_object_on_preview(new_planet)

    def draw_object_on_preview(self, object: Sun):
        c = object.get_coords_draw()
        r = object.radius

        self.__preview_canvas.create_line(
            c[0],
            c[1],
            (c[0] + (object.vel_x * self.TIME)),
            (c[1] - (object.vel_y * self.TIME)),
            fill=object.color,
            tags='p'
        )

        self.__preview_canvas.update()

        if "sun" == object.tag:
            self.__preview_canvas.create_oval(
                (c[0] - r),
                (c[1] - r),
                (c[0] + r),
                (c[1] + r),
                fill=object.color,
                tags='p'
            )
        else:
            self.__preview_canvas.create_oval(
                (c[0] - r),
                (c[1] - r),
                (c[0] + r),
                (c[1] + r),
                fill=object.color,
                tags='p'
            )

    def sim_start(self):
        self.destroy_setup()

        self.sim_frame = tk.Frame(self.master, height=800, width=1500, bg='black')

        self.state = "siming"

        self.field = Field(self.G, self.TIME, self.object_list)

        self.sim = Sim(self.sim_frame, self.field)

        self.sim_frame.pack()

        self.tick = self.sim.get_tick()

        self.sim.draw()

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs['fill']
            fill = root.winfo_rgb(fill) + (alpha,)
            fill = (fill[0] // 256, fill[1] // 256, fill[2] // 256, fill[3])

            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.images.append(ImageTk.PhotoImage(image))

            self.__options_canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')

        else:
            self.__options_canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def load_objects_setup(self):

        self.state = "setup"

        self.setup_frame = tk.Frame(self.master, height=800, width=1500, bg='black')

        self.__preview_canvas = tk.Canvas(self.setup_frame, height=750, width=1500, bg="black", highlightthickness=0,
                                          relief='ridge')

        self.__options_canvas = tk.Canvas(self.setup_frame, height=150, width=950, bg="black", highlightthickness=0,
                                          relief='ridge')
        self.create_rectangle(0, 0, 1500, 150, alpha=0.35, fill="white")

        self.__mass_label = tk.Label(self.__options_canvas, text="Mass:", font=self.font, bg='black', fg="white")
        self.__density_label = tk.Label(self.__options_canvas, text="Density:", font=self.font, bg='black', fg="white")
        self.__x_label = tk.Label(self.__options_canvas, text="X:", font=self.font, bg='black', fg="white")
        self.__y_label = tk.Label(self.__options_canvas, text="Y:", font=self.font, bg='black', fg="white")
        self.__vx_label = tk.Label(self.__options_canvas, text="Velocity_x:", font=self.font, bg='black', fg="white")
        self.__vy_label = tk.Label(self.__options_canvas, text="Velocity_y:", font=self.font, bg='black', fg="white")
        self.__color_label = tk.Label(self.__options_canvas, text="Color:", font=self.font, bg='black', fg="white")

        self.__mass_entry = tk.Entry(self.__options_canvas, width=5, font=self.font)
        self.__mass_entry.insert(tk.END, "100")
        self.__density_entry = tk.Entry(self.__options_canvas, width=5, font=self.font)
        self.__density_entry.insert(tk.END, "100")
        self.__x_entry = tk.Entry(self.__options_canvas, width=3, font=self.font)
        self.__x_entry.insert(tk.END, "0")
        self.__y_entry = tk.Entry(self.__options_canvas, width=3, font=self.font)
        self.__y_entry.insert(tk.END, "0")
        self.__vx_entry = tk.Entry(self.__options_canvas, width=3, font=self.font)
        self.__vx_entry.insert(tk.END, "0")
        self.__vy_entry = tk.Entry(self.__options_canvas, width=3, font=self.font)
        self.__vy_entry.insert(tk.END, "0")
        self.__color_entry = tk.Entry(self.__options_canvas, width=5, font=self.font)
        self.__color_entry.insert(tk.END, "red")

        self.__add_sun_button = tk.Button(self.__options_canvas, text="Add the sun", font=self.font,
                                          command=self.setup_add_sun, bg='black', fg="white")
        self.__add_planet_button = tk.Button(self.__options_canvas, text="Add the planet", font=self.font,
                                             command=self.setup_add_planet, bg='black', fg="white")
        self.__start_button = tk.Button(self.__options_canvas, text="Start", font=self.font, command=self.sim_start,
                                        bg='black', fg="white")

    def place_objects_setup(self):
        self.__mass_label.place(x=10, y=10)
        self.__mass_entry.place(x=75, y=10)
        self.__density_label.place(x=10, y=100)
        self.__density_entry.place(x=100, y=100)

        self.__x_label.place(x=170, y=10)
        self.__x_entry.place(x=200, y=10)
        self.__y_label.place(x=170, y=100)
        self.__y_entry.place(x=200, y=100)

        self.__vx_label.place(x=275, y=10)
        self.__vx_entry.place(x=390, y=10)
        self.__vy_label.place(x=275, y=100)
        self.__vy_entry.place(x=390, y=100)

        self.__color_label.place(x=470, y=10)
        self.__color_entry.place(x=550, y=10)

        self.__add_sun_button.place(x=650, y=10)
        self.__add_planet_button.place(x=650, y=100)
        self.__start_button.place(x=850, y=50)

        self.__preview_canvas.place(x=0, y=0)
        self.__options_canvas.place(x=0, y=0)

        self.setup_frame.place(x=0, y=0)

    def get_inputs(self) -> dict[str, int]:
        mass = int(self.__mass_entry.get())
        density = int(self.__density_entry.get())
        x = int(self.__x_entry.get())
        y = int(self.__y_entry.get())
        vx = int(self.__vx_entry.get())
        vy = int(self.__vy_entry.get())
        color = self.__color_entry.get()

        return {
            'mass': mass,
            'density': density,
            'x': x,
            'y': y,
            "vx": vx,
            'vy': vy,
            'color': color
        }

    def destroy_setup(self):
        self.setup_frame.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("1500x800")
    root.config(bg="cyan")

    app = Main(root)

    app.load_objects_setup()
    app.place_objects_setup()

    root.mainloop()
