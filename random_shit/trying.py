import tkinter as tk
import pynput

root = tk.Tk()
root.geometry("500x500")
root.config(bg='black')
root.title("Trying tree thing :D")

canvas = tk.Canvas(root, bg='black', width=500, height=500)
canvas.pack()

centers = [
    [100, 100],
    [400, 400]
]

radius = 5
active = 7
offest = 5

taged = -1

mouse_x = 0
mouse_y = 0

def on_mouse_click(x: int, y: int, button, pressed):
    global taged
    global mouse_x
    global mouse_y

    mouse_x = x
    mouse_y = y

    if check_near(centers[0]):
        taged = 0 if taged != -1 else -1

    elif check_near(centers[1]):
        taged = 1 if taged != -1 else -1

    else:
        taged = -1
    print([x, y])


def on_mouse_move(x: int, y: int):
    global mouse_x
    global mouse_y

    mouse_x = x
    mouse_y = y

    if taged != -1:
        centers[taged] = [x, y]

    print(x, y)


def redraw():
    left_radius = active if check_near(centers[0]) else radius
    right_radius = active if check_near(centers[1]) else radius

    canvas.create_line(centers[0][0], centers[0][1],
                       centers[1][0], centers[1][1],
                       fill='white')

    canvas.create_oval(centers[0][0] - left_radius, centers[0][1] - left_radius,
                       centers[0][0] + left_radius, centers[0][1] + left_radius,
                       fill='white')

    canvas.create_oval(centers[1][0] - right_radius, centers[1][1] - right_radius,
                       centers[1][0] + right_radius, centers[1][1] + right_radius,
                       fill='white')


def check_near(center):
    return (center[0] + radius + offest > mouse_x > center[0] - radius - offest) and (
            center[1] + radius + offest > mouse_y > center[1] - radius - offest)

def main():
    if taged != -1:
        on_mouse_move()


mouse_controller = pynput.mouse.Controller()

mouse_listener = pynput.mouse.Listener(
    on_move=None,
    on_click=on_mouse_click,
    on_scroll=None
)

mouse_listener.start()

redraw()

root.mainloop()
