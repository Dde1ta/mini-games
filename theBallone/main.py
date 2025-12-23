import tkinter as tk
import numpy as np
import random

class Ball:

    def __init__(self, game_canvas: tk.Canvas, clan: str, n: int, x: float, y: float, seed: int, step: int):
        self.clan = clan
        self.x = x
        self.y = y
        self.canvas = game_canvas
        self.RADIUS = 8
        self.n = n
        self.color = "green" if clan == "s" else "blue" if clan == "p" else "black"
        self.normal_func = np.random.normal
        self.time_step = step

    def move(self):
        self.x = self.x + np.sqrt(self.time_step) * self.normal_func(0, 1)
        self.y = self.y + np.sqrt(self.time_step) * self.normal_func(0, 1)

    def change_clan_to(self, clan):
        self.clan = clan
        self.color = "green" if clan == "s" else "blue" if clan == "p" else "black"

    def draw(self):
        self.canvas.delete("ball" + str(self.n))
        self.canvas.create_oval(
            self.x - self.RADIUS,
            self.y - self.RADIUS,
            self.x + self.RADIUS,
            self.y + self.RADIUS,
            fill=self.color,
            tags="ball" + str(self.n)
        )



class Game:
    def __init__(self, root: tk.Tk, **kwargs):
        """


        :param root:
        :param height:
        :param width:
        :return:
        """
        self.canvas = tk.Canvas(root, height=kwargs["height"], width=kwargs["width"])
        self.canvas.pack()
        self.ball_list = []

        self.make_balls()
        self.start()



    def make_balls(self):
        self.ball_list = [
            Ball(self.canvas, random.choice(['s', 'p', 'r']), i,
                 random.randint(100, 1400), random.randint(100, 700),
                 seed=i, step=10) for i in range(100)
        ]

    def start(self):
        self.canvas.after(16, self.draw)

    def draw(self):
        for ball in self.ball_list:
            ball.move()
            ball.draw()

        self.canvas.after(16, self.start)


if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("1500x800")
    root.title("Nope!!")

    game = Game(root, height=800, width=1500)

    root.mainloop()

