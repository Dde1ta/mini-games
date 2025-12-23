import tkinter as tk
from random import randint
from random import choice
import keyboard as key


class Block:

    def __init__(self, number: int):
        self.number = number

    def increase(self):
        self.number = self.number*2

    def get_number(self) -> int:
        return self.number

    def set_number(self,number: int):
        self.number = number


class Main:
    def __init__(self, x, y):

        self.score = 0
        self.age = 0
        self.running = True
        self.last = None
        self.xn = x
        self.yn = y
        self.blocks = [[Block(1) for i in range(self.xn)] for i in range(self.yn)]

    def get_matrix(self):
        return [[block.get_number() if block.get_number() != 1 else 0 for block in row] for row in self.blocks]

    def avg_block_size(self):
        sum_ = 0
        n = 0
        for row in self.blocks:
            for block in row:
                if block.get_number() == 1:
                    pass
                else:
                    sum_ += block.get_number()
                    n += 1

        return sum_//n

    def get_score(self):
        return self.score

    def increase_score(self):
        self.score = 0
        for row in self.blocks:
            for block in row:
                if block.get_number() == 1:
                    pass
                else:
                    self.score += block.get_number()
        self.score += (self.age//20)*2

    def spawn(self):
        self.check_over()
        self.age += 1
        if not self.running:
            print('Game Over :(')
        else:
            i, j = [randint(0, 3), randint(0, 3)]

            while self.blocks[i][j].get_number() != 1:
                i,j = [randint(0, 3), randint(0, 3)]

            ticks = choice([
                1,1,1,1,1,1,1,1,
                2,2,2,2,
                3
            ])

            for k in range(ticks):
                self.blocks[i][j].increase()

            print(self.get_matrix())

    def check_over(self):
        flag = False
        for row in range(self.xn):
            for col in range(self.yn):
                if self.blocks[row][col].get_number() == 1:

                    flag = True
                    return False
                    break
                if row == 0:
                    if col == 0:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col + 1].get_number())

                    elif col == self.yn - 1:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col - 1].get_number())

                    else:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col - 1].get_number())
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col + 1].get_number())

                    flag |= (self.blocks[row][col].get_number() == self.blocks[row + 1][col].get_number())

                elif row == self.xn - 1:
                    if col == 0:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col + 1].get_number())

                    elif col == self.yn - 1:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col - 1].get_number())

                    else:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col - 1].get_number())
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col + 1].get_number())

                    flag |= (self.blocks[row][col].get_number() == self.blocks[row - 1][col].get_number())

                else:
                    if col == 0:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col + 1].get_number())

                    elif col == self.yn - 1:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col - 1].get_number())

                    else:
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col - 1].get_number())
                        flag |= (self.blocks[row][col].get_number() == self.blocks[row][col + 1].get_number())

                    flag |= (self.blocks[row][col].get_number() == self.blocks[row + 1][col].get_number())
                    flag |= (self.blocks[row][col].get_number() == self.blocks[row - 1][col].get_number())

        self.playing = flag
        if not flag:
            print("game Over")

        return not flag

    def down(self):
        if self.check_over():
            print("No Possible")
            return None

        self.last = 'd'
        for row in range(len(self.blocks)-2,-1,-1):
            for column in range(len(self.blocks[0])):
                current_row = row
                current_column = column
                while self.blocks[current_row+1][current_column].get_number() == 1:
                    self.blocks[current_row + 1][current_column].set_number(self.blocks[current_row][current_column].get_number())
                    self.blocks[current_row][current_column].set_number(1)
                    current_row += 1
                    if current_row+1 >= len(self.blocks):
                        break
                    # self.__display__()
                    # input(f"{row} {column} {current_row} {current_column}")
                if current_row+1 >= len(self.blocks):
                    pass
                else:
                    if self.blocks[current_row+1][current_column].get_number() == self.blocks[current_row][current_column].get_number():
                        self.blocks[current_row + 1][current_column].increase()
                        self.blocks[current_row][current_column].set_number(1)
                        self.score += self.avg_block_size()

        if(self.check_over()):
            self.running = False

        self.spawn()

    def right(self):
        if self.check_over():
            print("No Possible")
            return None
        self.last = 'r'
        for row in range(len(self.blocks)):
            for column in range(len(self.blocks[0])-2,-1,-1):
                current_row = row
                current_column = column
                while self.blocks[current_row ][current_column+1].get_number() == 1:
                    self.blocks[current_row][current_column+1].set_number(
                    self.blocks[current_row][current_column].get_number())
                    self.blocks[current_row][current_column].set_number(1)
                    current_column += 1
                    if current_column + 1 >= len(self.blocks[0]):
                        break
                    # self.__display__()
                    # input(f"{row} {column} {current_row} {current_column}")
                if current_column + 1 >= len(self.blocks):

                    pass
                else:
                    if self.blocks[current_row][current_column+1].get_number() == self.blocks[current_row][current_column].get_number():
                        self.blocks[current_row][current_column+1].increase()
                        self.blocks[current_row][current_column].set_number(1)
                        self.score += self.avg_block_size()

        if (self.check_over()):
            self.running = False

        self.spawn()

    def left(self):
        if self.check_over():
            print("No Possible")
            return None
        self.last = 'l'
        for row in range(len(self.blocks)):
            for column in range(1,len(self.blocks[0])):
                current_row = row
                current_column = column
                while self.blocks[current_row][current_column - 1].get_number() == 1:
                    self.blocks[current_row][current_column - 1].set_number(
                    self.blocks[current_row][current_column].get_number())
                    self.blocks[current_row][current_column].set_number(1)
                    current_column -= 1
                    if current_column - 1 < 0:
                        break
                    # self.__display__()
                    # input(f"{row} {column} {current_row} {current_column}")
                if current_column - 1 < 0:
                    pass
                else:
                    if self.blocks[current_row][current_column- 1].get_number() == self.blocks[current_row][
                        current_column].get_number():
                        self.blocks[current_row][current_column - 1].increase()
                        self.blocks[current_row][current_column].set_number(1)
                        self.score += self.avg_block_size()

        if (self.check_over()):
            self.running = False

        self.spawn()

    def up(self):
        if self.check_over():
            print("No Possible")
            return None
        self.last = 'u'
        for row in range(1,len(self.blocks)):
            for column in range(len(self.blocks[0])):
                current_row = row
                current_column = column
                while self.blocks[current_row - 1][current_column].get_number() == 1:
                    self.blocks[current_row - 1][current_column].set_number(
                    self.blocks[current_row][current_column].get_number())
                    self.blocks[current_row][current_column].set_number(1)
                    current_row -= 1
                    if current_row - 1 < 0:
                        break
                    # self.__display__()
                    # input(f"{row} {column} {current_row} {current_column}")
                if current_row - 1 < 0:
                    pass
                else:
                    if self.blocks[current_row - 1][current_column].get_number() == self.blocks[current_row][
                        current_column].get_number():
                        self.blocks[current_row - 1][current_column].increase()
                        self.blocks[current_row][current_column].set_number(1)
                        self.score += self.avg_block_size()

        if (self.check_over()):
            self.running = False

        self.spawn()

    def __display__(self):
        for i in self.blocks:
            for j in i:
                print(j.get_number(),end = "\t")
            print("\n")
        print("\n")


class Draw:
    def __init__(self,frame = None, x = 4, y = 4):
        self.main = Main(x, y)
        self.frame = frame
        self.x = x
        self.y = y
        self.score = self.main.get_score()
        self.set_lables()
        self.main.spawn()
        self.animate()



    def set_lables(self):
        self.label_list = [[tk.Label(self.frame, text="", bg='white',
                                height=2, width=4, borderwidth=1, relief="solid",
                                font=("Calibri", 50)) for i in range(self.x)] for j in range(self.y)]
        self.score_label = tk.Label(text = f"Score = {self.score}",bg = "white",font=("Calibri", 50))
        self.first_draw()

    def first_draw(self):

        for row in range(1,len(self.label_list)+1):
            for column in range(1,len(self.label_list[row-1])+1):
                self.label_list[row-1][column-1].grid(row=row, column=column)
        self.score_label.place(x = 1000,y = 0)
        self.add_hotkeys()

    def add_hotkeys(self):
        key.add_hotkey('a', self.main.left)
        key.add_hotkey('d', self.main.right)
        key.add_hotkey('s', self.main.down)
        key.add_hotkey('w', self.main.up)

    def draw(self):
        for i in range(len(self.label_list)):
            for j in range(len(self.label_list[0])):
                if self.main.blocks[i][j].get_number() == 1:
                    self.label_list[i][j].config(text = "")
                else:
                    self.label_list[i][j].config(text=self.main.blocks[i][j].get_number())
        self.score_label.config(text = f"Score = {self.main.get_score()}")
        self.animate()

    def animate(self):
        self.frame.after(60, self.draw)



def game_consol():
    main = Main()

    running = True

    main.spawn()
    main.__display__()

    while(running):
        command = input("Enter move")
        match command:
            case 'd':
                main.right()
                main.check_over()
                main.spawn()
                main.__display__()

            case 'a':
                main.left()
                main.check_over()
                main.spawn()
                main.__display__()

            case 'w':
                main.up()
                main.check_over()
                main.spawn()
                main.__display__()

            case 's':
                main.down()
                main.check_over()
                main.spawn()
                main.__display__()

            case _:
                running = False

    pass
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry("560x755")
#     root.config(bg = "black")
#
#     label_frame = tk.Frame(root, width=700, height=600, bg="white")
#     label_frame.pack_propagate(False)
#     label_frame.place(x=0 , y= 0)
#
#     game = Draw(frame = label_frame)
#
#     root.mainloop()
#     #
#
#     # game_consol()
#
# # game_consol()
