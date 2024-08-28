import tkinter as tk
import pyautogui as pag
import win32api
class Main:
    def __init__(self,frame = None,height = 0,width = 0):
        self.canvas  = tk.Canvas(frame,height= height, width= width,bg = "Black")
        self.HEIGHT = height
        self.WIDTH = width
        self.oval_dict = {}

        self.active_red = "#950000"
        self.active_yellow = "#DBD400"
        self.set_red = "#FF0000"
        self.set_yellow = "#FFF700"
        self.active_color = self.active_red

        self.per = 0
        self.pressed = False
        self.win = False

        self.draw_grid()
        self.canvas.pack()
        self.animate()

    def draw_grid(self):
        for i in range(20,self.WIDTH-100,100):
            self.oval_dict[str(i-20)] = []
            for j in range(20,self.HEIGHT,100):
                self.canvas.create_rectangle(i,j,i+80,j+80, fill = "grey")

                self.oval_dict[str(i-20)].append(self.canvas.create_oval(i+5,j+5,i+75,j+75,
                                                                                    fill = "black",tags = str(i-20)))

    def get_mouse(self):
        return pag.position()

    def on_press(self,zonex):
        last = len(self.oval_dict[str(zonex)]) - 1
        while self.canvas.itemcget(self.oval_dict[str(zonex)][last],"fill") in [self.set_yellow,self.set_red] and last >= 0:
            last -= 1
        if self.active_color == self.active_red:
            self.canvas.itemconfig(self.oval_dict[str(zonex)][last], fill=self.set_red)
            self.active_color = self.active_yellow
            self.win = self.is_connect_4(zonex,last,self.set_red)
        else:
            self.canvas.itemconfig(self.oval_dict[str(zonex)][last], fill=self.set_yellow)
            self.active_color = self.active_red
            self.win = self.is_connect_4(zonex, last, self.set_yellow)

        print(self.win)

    def is_connect_4(self,zonex,current,color):

        # left i.e zonex -- 100

        left = zonex
        n = 1
        while self.canvas.itemcget(self.oval_dict[str(left)][current],"fill") == color:
            n += 1
            left -= 100
            if(left < 0):
                break
            elif n == 4:
                return True

        # dialgonal left i.e zonex -= 100 current -= 1

        left = zonex
        row = current
        n = 1
        while self.canvas.itemcget(self.oval_dict[str(left)][row], "fill") == color:
            n += 1
            left -= 100
            row += 1
            if (left < 0) or (row >= len(self.oval_dict[str(left)])):
                break
            elif n == 4:
                return True

        # down i.e current -= 1

        row = current
        n = 1
        while self.canvas.itemcget(self.oval_dict[str(zonex)][row], "fill") == color:
            n += 1
            row += 1
            if (row >= len(self.oval_dict[str(left)])):
                break
            elif n == 4:
                return True

        # diagonal right i.e zonex += 100 and current -= 1

        right = zonex
        row = current
        n = 1
        while self.canvas.itemcget(self.oval_dict[str(right)][row], "fill") == color:
            n += 1
            right += 100
            row += 1
            if (left < 0) or (row >= len(self.oval_dict[str(left)])):
                break
            elif n == 4:
                return True

        # right i.e zonex += 100

        right = zonex
        n = 1
        while self.canvas.itemcget(self.oval_dict[str(right)][current], "fill") == color:
            n += 1
            right -= 100
            if (right < 0):
                break
            elif n == 4:
                return True

        return False


    def animate(self):
        if self.win:
            return None
        x,y = self.get_mouse()
        state_left = win32api.GetKeyState(0x01)

        zonex = ((x-150)//100)*100
        zoney = ((y)//100)*100
        last = len(self.oval_dict[str(0)]) - 1

        if zonex <= 1600:

            if zonex != self.per:
                while  last >= 0:

                    if self.canvas.itemcget(self.oval_dict[str(self.per)][last], "fill") not in [self.set_yellow,self.set_red]:
                        self.canvas.itemconfig(self.oval_dict[str(self.per)][last], fill="black")

                    last -= 1
                self.per = zonex
            else:
                pass
            last = len(self.oval_dict[str(0)]) - 1
            while self.canvas.itemcget(self.oval_dict[str(zonex)][last], "fill") in [self.set_yellow, self.set_red] and last >= 0:
                last -= 1
            self.canvas.itemconfig(self.oval_dict[str(zonex)][last], fill=self.active_color)

            #print(state_left)
        else:
            pass

        if not self.pressed:
            if state_left not in [1,0]:
                self.pressed = True
                self.on_press(zonex)
        else:
            if state_left in [1,0]:
                self.pressed = False


        self.cycle()


    def cycle(self):
        self.canvas.after(60,self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1800x1000+150+0")

    frame = tk.Frame(root,height = 1000, width = 1800)
    frame.pack()

    main = Main(frame,1000,1800)

    root.mainloop()
