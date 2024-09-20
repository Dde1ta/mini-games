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
            self.win = self.is_connect_4(self.set_red)
        else:
            self.canvas.itemconfig(self.oval_dict[str(zonex)][last], fill=self.set_yellow)
            self.active_color = self.active_red
            self.win = self.is_connect_4(self.set_yellow)

        print(self.win)

    def is_connect_4(self,color):
        for x in self.oval_dict:
            for oval in range(len(self.oval_dict[x])):
                if(self.check_4(int(x),oval,color,0,'all')):
                    return True


    def check_4(self,zonex,current,color,n,direction):
        if n == 4:
            return True

        if zonex < 0:
            return False

        if zonex > 1600:
            return False

        if current < 0:
            return False

        if current >= len(self.oval_dict['0']):
            return False

        if self.canvas.itemcget(self.oval_dict[str(zonex)][current],"fill") != color:
            return False

        match(direction):
            case 'l':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex-100,current,color,n+1,'l')

            case 'd':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex, current - 1, color, n + 1,'d')

            case 'r':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex + 100, current, color, n + 1,'r')

            case 'u':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex, current + 1, color, n + 1,'u')

            case 'lu':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex - 100, current+1, color, n + 1, 'lu')

            case 'ld':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex - 100, current - 1, color, n + 1, 'ld')

            case 'ru':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex + 100, current+1, color, n + 1, 'ru')

            case 'rd':
                if self.canvas.itemcget(self.oval_dict[str(zonex)][current], "fill") != color:
                    return False
                return self.check_4(zonex - 100, current, color, n + 1, 'rd')

            case _:
                directions = ['l','r','d','u','lu','ld','ru','rd']
                is_win = False

                for d in directions:
                    is_win = is_win or self.check_4(zonex,current,color,n,d)

                return is_win


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
