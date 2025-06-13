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
    def __init__(self):
        self.blocks = [[Block(1) for i in range(4)] for i in range(4)]
        self.score = 0
        self.age = 0
        self.playing = True
        self.last = None

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
        self.score += self.age*2

    def spawn(self):
        #self.check_over()
        if self.playing and not self.playing:
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
        print(self.playing)
        for i in self.blocks:
            for j in i:
                if j.get_number() == 1:
                    break
        else:
            self.playing = False

        print(self.playing)

    def down(self):

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

        self.spawn()

    def right(self):

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
        self.spawn()

    def left(self):

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
        self.spawn()

    def up(self):

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
        self.spawn()

    def __display__(self):
        for i in self.blocks:
            for j in i:
                print(j.get_number(),end = "\t")
            print("\n")
        print("\n")


class Draw:
    def __init__(self,frame = None):
        self.main = Main()
        self.frame = frame
        self.score = self.main.get_score()
        self.set_lables()
        self.main.spawn()
        self.animate()


    def set_lables(self):
        self.label_list = [[tk.Label(self.frame, text="", bg='white',
                                height=2, width=4, borderwidth=1, relief="solid",
                                font=("Calibri", 50)) for i in range(4)] for j in range(4)]
        self.score_label = tk.Label(text = f"Score = {self.score}",bg = "white",font=("Calibri", 50))
        self.first_draw()

    def first_draw(self):

        for row in range(1,len(self.label_list)+1):
            for column in range(1,len(self.label_list[row-1])+1):
                self.label_list[row-1][column-1].grid(row=row, column=column)
        self.score_label.place(x = 0,y = 675)
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
