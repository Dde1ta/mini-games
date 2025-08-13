import random
from math import *
import tkinter as tk
from math import *
import random as ran
from ds.queues import Heap

class MazeNode:

    def __init__(self, x1:int, y1:int, x2: int, y2: int, recived_from: list[str] ,pointing_to: str,type: str,pos : list[int] ,canvas: tk.Canvas = None):
        """

        :param x1: x1 coordinate
        :param y1: y1 coordinate
        :param x2: x2 coordinate
        :param y2: y2 coordinate
        :param recived_from: the direction from which it is pointed to
        :param pointing_to: the direction it points to
        :param type: "Orgin": green, "Correct": green, "Traveling": red, "Destination": orange
        :param canvas: the main Canvas of the root
        """

        self.x1, self.y1, self.x2, self.y2 = x1,y1,x2,y2
        self.tag = str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2)
        self.isOrign = pointing_to == ''
        self.type = type

        self.canvas = canvas

        self.pointing = pointing_to
        self.recived = recived_from
        self.pos = pos

        self.__draw_main_box__()
        self.__draw_boaders__()

    def __draw_main_box__(self):
        if self.type == "O":
            self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                  fill = "yellow", width=0, tags = self.tag)
        elif self.type == "D":
            self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                         fill="orange", width=0, tags=self.tag)
        elif self.type == "T":
            self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                         fill="red", width=0, tags=self.tag)
        elif self.type == "C":
            self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                         fill="green", width=0, tags=self.tag)
        elif self.type == "M":
            self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                         fill="black", width=0, tags=self.tag)


        self.canvas.update()

    def __draw_boaders__(self):

        def up_boader():
            width = self.x2 - self.x1
            height = (self.y2 - self.y1)//10

            self.canvas.create_rectangle(self.x1, self.y1,
                                  self.x1+width, self.y1+height,
                                  fill = "black", tags = self.tag)

        def down_boader():
            width = self.x2 - self.x1
            height = (self.y2 - self.y1) // 10

            self.canvas.create_rectangle(self.x1, self.y2 - height,
                                         self.x1 + width, self.y2,
                                         fill="black", tags=self.tag)
        def left_boader():
            width = (self.x2 - self.x1) // 10
            height = (self.y2 - self.y1)

            self.canvas.create_rectangle(self.x1, self.y1,
                                         self.x1 + width, self.y1 + height,
                                         fill="black", tags=self.tag)

        def right_boader():
            width = (self.x2 - self.x1) // 10
            height = (self.y2 - self.y1)

            self.canvas.create_rectangle(self.x2, self.y1,
                                         self.x2 - width, self.y1 + height,
                                         fill="black", tags=self.tag)

        if self.pointing != "u" and "u" not in self.recived:
            up_boader()

        if self.pointing != "d" and "d" not in self.recived:
            down_boader()

        if self.pointing != "l" and "l" not in self.recived:
            left_boader()

        if self.pointing != "r" and "r" not in self.recived:
            right_boader()

        self.canvas.update()

    def update_block(self,recived_from: str = None ,pointing_to: str = None):
        self.canvas.delete(self.tag)
        self.recived = recived_from if recived_from != None else self.recived
        self.pointing = pointing_to if pointing_to != None else self.pointing
        self.isOrign = self.pointing == ''
        self.__draw_main_box__()
        self.__draw_boaders__()
        self.canvas.update()

    def set_type(self,type = None):
        self.type = type
        self.update_block()

    def set_distance(self, destination):
        self.distance = abs(destination.pos[0] - self.pos[0]) + abs(destination.pos[1] - self.pos[1])

    def __le__(self, other):
        assert type(other) == type(MazeNode)

        return self.distance < other.distance

    def __gt__(self, other):

        return (self.distance > other.distance)


    def __str__(self):
        return str(self.distance)

class Maze:

    def __init__(self, m:int, n:int, width:int, height: int, canvas:tk.Canvas):
        self.m = m
        self.n = n

        self.block_height = height//m
        self.block_width =  width//n

        self.flag = False

        self.maze =[
            [
                MazeNode(
                    x1 = column * self.block_width,
                    x2 = (column + 1) * self.block_width,
                    y1 = row * self.block_height,
                    y2 = (row + 1) * self.block_height,
                    recived_from = [],
                    pointing_to = "u",
                    canvas=canvas,
                    type="",
                    pos=[row, column]

                )

            for column in range(n) ]
        for row in range(m) ]

        self.orign = [m - 1, n - 1]

        self.canvas = canvas

        self.setup()

    def setup(self):

        for row in range(self.m):
            for column in range(self.n):
                if column == 0:
                    self.maze[row][column].update_block(recived_from=[""], pointing_to='r')
                elif column == self.n - 1:
                    if row == 0:
                        self.maze[row][column].update_block(recived_from=["l"], pointing_to='d')
                    elif row == self.m - 1:
                        self.maze[row][column].update_block(recived_from=["l",'u'], pointing_to='')
                        self.maze[row][column].set_type("O")
                    else:
                        self.maze[row][column].update_block(recived_from=["l",'u'],pointing_to='d')
                    #self.maze[row][column].place(x = row * self.block_width, y= column*self.block_height)
                else:
                    self.maze[row][column].update_block(recived_from=["l"], pointing_to='r')
                    #self.maze[row][column].place(x=row * self.block_width, y=column * self.block_height)

    def chose_new_origin(self):
        og_orgin = self.orign

        if og_orgin[0] < self.m - 1 and og_orgin[1] < self.n - 1 and og_orgin[0] > 0 and og_orgin[1] > 0:
            new_orgin = ran.choice(
                [[og_orgin[0] - 1, og_orgin[1]],
                 [og_orgin[0] + 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] + 1],
                 [og_orgin[0], og_orgin[1] - 1]]
            )
        elif og_orgin[0] == self.m - 1 and og_orgin[1] == self.n - 1:
            new_orgin = ran.choice(
                [[og_orgin[0] - 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] - 1]]
            )
        elif og_orgin[0] == 0 and og_orgin[1] == 0:
            new_orgin = ran.choice(
                [[og_orgin[0] + 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] + 1]]
            )
        elif (og_orgin[0] == self.m - 1 and og_orgin[1] == 0):
            new_orgin = ran.choice(
                [[og_orgin[0] - 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] + 1]]
            )
        elif og_orgin[1] == self.n - 1 and og_orgin[0] == 0:
            new_orgin = ran.choice(
                [[og_orgin[0] + 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] - 1]]
            )
        elif og_orgin[0] == self.m - 1:
            new_orgin = ran.choice(
                [[og_orgin[0] - 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] + 1],
                 [og_orgin[0], og_orgin[1] - 1]]
            )
        elif og_orgin[0] == 0:
            new_orgin = ran.choice(
                [[og_orgin[0] + 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] + 1],
                 [og_orgin[0], og_orgin[1] - 1]]
            )
        elif og_orgin[1] == self.n - 1:
            new_orgin = ran.choice(
                [[og_orgin[0] - 1, og_orgin[1]],
                 [og_orgin[0] + 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] - 1]]
            )
        elif og_orgin[1] == 0:
            new_orgin = ran.choice(
                [[og_orgin[0] - 1, og_orgin[1]],
                 [og_orgin[0] + 1, og_orgin[1]],
                 [og_orgin[0], og_orgin[1] + 1]]
            )

        return new_orgin

    def check_recived(self, corrds:list[int]):
        node = self.maze[corrds[0]][corrds[1]]
        rec = node.recived
        new = []
        for di in rec:
            if di == 'u':
                if self.maze[corrds[0] - 1][corrds[1]].pointing == 'd':
                    new.append(di)
            if di == 'd':
                if self.maze[corrds[0] + 1][corrds[1]].pointing == 'u':
                    new.append(di)
            if di == 'l':
                if self.maze[corrds[0]][corrds[1] - 1].pointing == 'r':
                    new.append(di)
            if di == 'r':
                if self.maze[corrds[0]][corrds[1] + 1].pointing == 'l':
                    new.append(di)

        node.recived = new

    def get_corrds(self,di,corrds):
        if di == 'u':
            return [corrds[0] - 1,corrds[1]]

        if di == 'd':
            return [corrds[0] + 1,corrds[1]]

        if di == 'l':
            return [corrds[0], corrds[1] - 1]

        if di == 'r':
            return [corrds[0], corrds[1] + 1]

    def orgin_shift(self,n:int):

        og_orgin = self.orign

        new_orgin = self.chose_new_origin()

        if new_orgin == [og_orgin[0] - 1, og_orgin[1]]:
            self.maze[og_orgin[0]][og_orgin[1]].update_block(pointing_to='u')
            self.maze[og_orgin[0]][og_orgin[1]].set_type("")
            new_orgin_node = self.maze[new_orgin[0]][new_orgin[1]]

            self.check_recived(new_orgin)

            new_orgin_node.recived.extend(['d'])
            po = new_orgin_node.pointing
            new_orgin_node.update_block(pointing_to='')
            new_orgin_node.set_type("O")
            self.check_recived(self.get_corrds(po,new_orgin))
            self.maze[self.get_corrds(po, new_orgin)[0]][self.get_corrds(po, new_orgin)[1]].update_block()

            #print("to u")

        if new_orgin == [og_orgin[0] + 1, og_orgin[1]]:
            self.maze[og_orgin[0]][og_orgin[1]].update_block(pointing_to='d')
            self.maze[og_orgin[0]][og_orgin[1]].set_type("")
            new_orgin_node = self.maze[new_orgin[0]][new_orgin[1]]

            self.check_recived(new_orgin)
            new_orgin_node.recived.extend(['u'])
            po = new_orgin_node.pointing
            new_orgin_node.update_block(pointing_to='')
            new_orgin_node.set_type("O")
            self.check_recived(self.get_corrds(po, new_orgin))
            self.maze[self.get_corrds(po, new_orgin)[0]][self.get_corrds(po, new_orgin)[1]].update_block()


        if new_orgin == [og_orgin[0], og_orgin[1] - 1]:
            self.maze[og_orgin[0]][og_orgin[1]].update_block(pointing_to='l')
            self.maze[og_orgin[0]][og_orgin[1]].set_type("")
            new_orgin_node = self.maze[new_orgin[0]][new_orgin[1]]

            self.check_recived(new_orgin)
            new_orgin_node.recived.extend(['r'])
            po = new_orgin_node.pointing
            new_orgin_node.update_block(pointing_to='')
            new_orgin_node.set_type("O")
            self.check_recived(self.get_corrds(po, new_orgin))
            self.maze[self.get_corrds(po, new_orgin)[0]][self.get_corrds(po, new_orgin)[1]].update_block()
            #print("to l")

        if new_orgin == [og_orgin[0], og_orgin[1] + 1]:
            self.maze[og_orgin[0]][og_orgin[1]].update_block(pointing_to='r')
            self.maze[og_orgin[0]][og_orgin[1]].set_type("")
            new_orgin_node = self.maze[new_orgin[0]][new_orgin[1]]

            self.check_recived(new_orgin)
            new_orgin_node.recived.extend(['l'])
            po = new_orgin_node.pointing
            new_orgin_node.update_block(pointing_to='')
            new_orgin_node.set_type("O")
            self.check_recived(self.get_corrds(po, new_orgin))
            self.maze[self.get_corrds(po, new_orgin)[0]][self.get_corrds(po, new_orgin)[1]].update_block()
            #print("to r")

        self.orign = new_orgin
        self.canvas.after(0, lambda: self.genrate(n-1))

    def genrate(self, n: int = 0):
        self.flag = True
        if n == 0:
            self.select_distination()
            return None

        self.canvas.after(0,lambda :self.orgin_shift(n))
        # for i in range(n):
        #     self.orgin_shift(n)

    def reset(self, n: int = 0):
        for row in range(self.m):
            for column in range(self.n):
                self.maze[row][column].set_type("")


        self.genrate(n)

    def solve_closer(self):
        heap = Heap()

        current = self.orign
        x = current[0]
        y = current[1]
        current_node = self.maze[x][y]

        destination = self.maze[self.dx][self.dy]

        current_node.set_distance(destination)

        heap.insert(current_node)

        while current_node.type != "D":

            self.canvas.after(16, self.__wait__())


            current_node = heap.pop()

            if current_node.type == "T":
                continue

            if current_node.type == "D":
                break

            possible_direction = []

            if current_node.type != "O":
                current_node.set_type("T")
                possible_direction = [current_node.pointing]

            possible_direction.extend(current_node.recived)

            for d in possible_direction:

                next = self.get_corrds(d, current_node.pos)

                if(next == None):
                    continue

                next_node = self.maze[next[0]][next[1]]

                if(next_node.type == "T"):
                    continue

                next_node.set_distance(destination)
                heap.insert(next_node)

        if current_node.type == "D":
            next = self.get_corrds(current_node.pointing, current_node.pos)

            current_node = self.maze[next[0]][next[1]]

            while current_node.type != "O":
                current_node.set_type("C")
                next = self.get_corrds(current_node.pointing, current_node.pos)
                current_node = self.maze[next[0]][next[1]]

    def solve(self, current: list[int] = None):
        if self.flag == False:
            return None

        if current == None:
            current = self.orign

        x = current[0]
        y = current[1]
        current_node = self.maze[x][y]

        if current_node.type == "T":
            return False

        if current_node.type == "D":
            return True
        else:

            current_node.set_type("T")

            pointing_corrds = self.get_corrds(current_node.pointing, current)

            self.canvas.after(16, self.__wait__())

            if (self.solve(pointing_corrds)):
                current_node.set_type("O" if x == self.orign[0] and y == self.orign[1] else "C")
                return True

            for d in current_node.recived:

                reciving_corrds = self.get_corrds(d, current)
                self.canvas.after(0, self.__wait__())
                if (self.solve(reciving_corrds)):
                    current_node.set_type("O" if x == self.orign[0] and y == self.orign[1] else "C")
                    return True

            current_node.set_type("")
            return False

    def select_distination(self):
        self.dx = ran.randint(0,self.m - 1)
        self.dy = ran.randint(0,self.n - 1)

        self.maze[self.dx][self.dx].set_type("D")

    def __wait__(self):
        pass

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x800')

    height = 700
    widht = 700

    canvas = tk.Canvas(root, width=widht, height=height, bd=0, highlightthickness=0,bg = 'cyan')

    canvas.pack()

    maze = Maze(50, 50, widht, height, canvas) # DONOT EXCCED 100 !!!!!!!!!!!!

    genrate_botton = tk.Button(root,text = 'genrate', command = lambda : maze.reset(5000))
    genrate_botton.pack()

    solve_closer_button = tk.Button(root, text = "solver_closer", command=maze.solve_closer)
    solve_closer_button.pack()

    solve_button = tk.Button(root, text="solver", command=maze.solve)
    solve_button.pack()

    root.mainloop()


