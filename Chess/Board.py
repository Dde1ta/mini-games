import tkinter as tk
from Pieces import *
from PIL import Image
from PIL import ImageTk
import os

class Tile(tk.Canvas):

    def __init__(self, root: tk.Frame = None, piece=None, **kwargs):
        """

        :param label: tk label object
        :param piece: piece object
        :param kwargs: color : color of the tile, images : all the images loaded from the board
        """

        super().__init__(root)

        self.piece = piece

        self.is_empty = piece is None
        self.is_in_path =  False
        self.is_under_attack = False

        self.images = kwargs["images"]
        self.color = kwargs["color"]
        self.create_tile()

    def create_tile(self):
        self.config(bg=self.color)

        if not self.is_empty:
            self.create_image(0,0,image=self.images[self.piece.get_piece()], tags="p")

    def change_state(self):

        self.reset_state()

        if not self.is_empty:
            self.create_image(50, 50, image=self.images[self.piece.get_piece()], tags="p")

        if self.is_in_path:
            self.create_image(50, 50, image=self.images["oa"], tags="i")

        if self.is_under_attack:
            self.create_image(50, 50, image=self.images["on"], tags="u")

    def reset_state(self):
        self.delete("p")
        self.delete("u")
        self.delete("i")
        self.is_empty = self.piece is None

class Board:

    def __init__(self,root : tk.Frame = None,):
        self.frame = root

        self.grid_white = "#FFFFB2"
        self.grid_black = "#BD5B37"

        self.colors = [self.grid_white, self.grid_black]

        self.images = {}
        self.board = []
        self.current_movement = []

        self.load_images()
        self.create_grid()

        self.set_white_pieces()
        self.set_black_pieces()

        self.turn = 'w'

    def load_images(self):
        path = "images/"

        for type_ in os.listdir(path):
            for images in os.listdir(os.path.join(path,type_)):
                print(type_[0], images[1], "".join([type_.lower()[0],images[1]]), images)
                self.images["".join([type_.lower()[0],images[1]])] = ImageTk.PhotoImage(Image.open(os.path.join(path,type_,images)))


    def create_grid(self):
        n = 0
        for i in range(8):
            self.board.append([])
            for j in range(8):

                self.board[i].append(
                    Tile(
                        canvas= self.frame,
                        color=self.colors[(i+j) % 2],
                        images=self.images
                    )
                )
                self.board[i][j].place(x=100*i,y=100*j)
                self.board[i][j].bind("<Enter>", self.hower_over_tile)
                self.board[i][j].bind("<Leave>", self.out_of_hower)

    def hower_over_tile(self,event: tk.Event):
        tile = event.widget
        piece = tile.piece

        if(piece is None):
            return None
        else:
            if(piece.get_color() == self.turn):
                self.current_movement = piece.possible_movement()
            else:
                return None

        print(self.current_movement)

        for move in self.current_movement:
            print(self.board[move[0]][move[1]].is_empty)
            if self.board[move[0]][move[1]].is_empty:
                self.board[move[0]][move[1]].is_in_path = True
                self.board[move[0]][move[1]].change_state()
                print("hellosssssd")
            else:
                self.board[move[0]][move[1]].is_under_attack = True
                self.board[move[0]][move[1]].change_state()
                print("hellosssssd")

    def out_of_hower(self,event):
        for move in self.current_movement:
            print(self.board[move[0]][move[1]].is_empty)
            if self.board[move[0]][move[1]].is_empty:
                self.board[move[0]][move[1]].is_in_path = False
                self.board[move[0]][move[1]].change_state()
                print("hellosd")
            else:
                self.board[move[0]][move[1]].is_under_attack = False
                self.board[move[0]][move[1]].change_state()
                print("hellosd")

    def set_white_pieces(self):
        pawn_row = [self.board[i][-2] for i in range(8)]
        pieces_row = [self.board[i][-1] for i in range(8)]

        for tile in range(len(pawn_row)):
            pawn_row[tile].piece = Pawn([tile,6],'wp')
            pawn_row[tile].change_state()

        pieces_row[0].piece = Rook([0, 7], 'wr')
        pieces_row[7].piece = Rook([7, 7], 'wr')

        pieces_row[1].piece = Knight([1, 7], 'wn')
        pieces_row[6].piece = Knight([6, 7], 'wn')

        pieces_row[2].piece = Bishop([2, 7], 'wb')
        pieces_row[5].piece = Bishop([5, 7], 'wb')

        pieces_row[3].piece = Queen([3, 7], 'wq')
        pieces_row[4].piece = King([4, 7], 'wk')

        for i in pieces_row:
            i.change_state()

        print("Hello")

    def set_black_pieces(self):
        pawn_row = [self.board[i][1] for i in range(8)]
        pieces_row = [self.board[i][0] for i in range(8)]

        for tile in range(len(pawn_row)):
            pawn_row[tile].piece = Pawn([tile, 1],'bp')
            pawn_row[tile].change_state()

        pieces_row[0].piece = Rook([0, 0], 'br')
        pieces_row[7].piece = Rook([7, 0], 'br')

        pieces_row[1].piece = Knight([1, 0], 'bn')
        pieces_row[6].piece = Knight([6, 0], 'bn')

        pieces_row[2].piece = Bishop([2, 0], 'bb')
        pieces_row[5].piece = Bishop([5, 0], 'bb')

        pieces_row[4].piece = Queen([4, 0], 'bq')
        pieces_row[3].piece = King([3, 0], 'bk')

        for i in pieces_row:
            i.change_state()

        print("Hello")

    def switch_turn(self):
        self.turn = "w" if self.turn == "b" else "b"



if __name__ == "__main__":
    root = tk.Tk()

    frame = tk.Frame(root, height= 100*8, width= 100*8)
    board = Board(frame)

    frame.pack()

    root.mainloop()
