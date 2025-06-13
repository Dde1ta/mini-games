from abc import abstractmethod


class Piece:
    def __init__(self, pos: list[int], name: str = None):
        self.pos = pos
        self.name = name
        self.color = name[0]
        self.mapping_x = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        }

    def get_position(self):
        return self.pos

    def position_in_grid(self) -> list[int]:
        """
        Return the x,y coordinates of the piece
        """
        return [self.pos[0], int(self.pos[1])]

    def get_piece(self) -> str:
        return self.name

    def get_color(self) -> str:
        return self.name[0]

    @abstractmethod
    def move(self, **kwargs): ...

    @abstractmethod
    def possible_movement(self) -> list[list[int]]: ...


class Pawn(Piece):

    def __init__(self, pos=None, name: str = None):
        super().__init__(pos, name)

    def move(self, **kwargs):
        #self.pos = self.pos[0] + str(int(self.pos[1]) + 1)
        pass

    def attack(self, direction: int):
        """
        Direction -1 = left
        Direction +1 = right
        :param direction:
        :return: None
        """
        self.pos = [self.pos[0] - direction, self.pos[1]]

    def possible_movement(self) -> list[list[int]]:
        movement = []

        if self.color == 'w':
            if self.pos[0] <= 0:
                movement.extend([[self.pos[0], self.pos[1] - 1], [self.pos[0] + 1, self.pos[1] - 1]])

            elif self.pos[0] >= 7:
                movement.extend([[self.pos[0], self.pos[1] - 1], [self.pos[0] - 1, self.pos[1] - 1]])

            else:
                movement.extend([[self.pos[0], self.pos[1] - 1], [self.pos[0] - 1, self.pos[1] - 1], [self.pos[0] + 1, self.pos[1] - 1]])

            return movement
        else:
            if self.pos[0] <= 0:
                movement.extend([[self.pos[0], self.pos[1] + 1], [self.pos[0] + 1, self.pos[1] + 1]])

            elif self.pos[0] >= 7:
                movement.extend([[self.pos[0], self.pos[1] + 1], [self.pos[0] - 1, self.pos[1] + 1]])

            else:
                movement.extend([[self.pos[0], self.pos[1] + 1], [self.pos[0] - 1, self.pos[1] + 1],
                                 [self.pos[0] + 1, self.pos[1] + 1]])
            return movement


class King(Piece):

    def __init__(self, pos=None, name: str = None):
        super().__init__(pos, name)

    def move(self, **kwargs):
        self.pos = kwargs["pos"]

    def possible_movement(self) -> list[list[int]]:
        pos_current = self.pos
        movement = []

        if (pos_current[0] > 0 and pos_current[1] > 0) and (
                pos_current[0] < 7 and pos_current[1] < 7):
            movement.extend([
                [self.pos[0] - 1, int(self.pos[1])],
                [self.pos[0] - 1, int(self.pos[1] + 1)],
                [self.pos[0] - 1, int(self.pos[1] - 1)],
                [self.pos[0], int(self.pos[1] + 1)],
                [self.pos[0], int(self.pos[1] - 1)],
                [self.pos[0] + 1, int(self.pos[1])],
                [self.pos[0] + 1, int(self.pos[1] + 1)],
                [self.pos[0] + 1, int(self.pos[1] - 1)]
            ])
            return movement

        if pos_current[0] == 0 and pos_current[1] == 0:
            movement.extend([
                [self.pos[0], int(self.pos[1] + 1)],
                [self.pos[0] + 1, int(self.pos[1])],
                [self.pos[0] + 1, int(self.pos[1] + 1)],
            ])
            return movement

        if pos_current[0] == 0 and pos_current[1] == 7:
            movement.extend([
                [self.pos[0], int(self.pos[1] - 1)],
                [self.pos[0] + 1, int(self.pos[1])],
                [self.pos[0] + 1, int(self.pos[1] - 1)],
            ])
            return movement

        if pos_current[0] == 7 and pos_current[1] == 1:
            movement.extend([
                [self.pos[0], int(self.pos[1] + 1)],
                [self.pos[0] - 1, int(self.pos[1])],
                [self.pos[0] - 1, int(self.pos[1] + 1)],
            ])
            return movement

        if pos_current[0] == 7 and pos_current[1] == 7:
            movement.extend([
                [self.pos[0], int(self.pos[1] - 1)],
                [self.pos[0] - 1, int(self.pos[1])],
                [self.pos[0] - 1, int(self.pos[1] - 1)],
            ])
            return movement

        if pos_current[0] == 0:
            movement.extend([
                [self.pos[0], int(self.pos[1] + 1)],
                [self.pos[0], int(self.pos[1] - 1)],
                [self.pos[0] + 1, int(self.pos[1])],
                [self.pos[0] + 1, int(self.pos[1] + 1)],
                [self.pos[0] + 1, int(self.pos[1] - 1)],
            ])
            return movement

        if pos_current[1] == 0:
            movement.extend([
                [self.pos[0] - 1, int(self.pos[1])],
                [self.pos[0] - 1, int(self.pos[1] + 1)],
                [self.pos[0], int(self.pos[1] + 1)],
                [self.pos[0] + 1, int(self.pos[1])],
                [self.pos[0] + 1, int(self.pos[1] + 1)]
            ])
            return movement

        if pos_current[0] == 7:
            movement.extend([
                [self.pos[0] - 1, int(self.pos[1])],
                [self.pos[0] - 1, int(self.pos[1] + 1)],
                [self.pos[0] - 1, int(self.pos[1] - 1)],
                [self.pos[0], int(self.pos[1] + 1)],
                [self.pos[0], int(self.pos[1] - 1)],
            ])
            return movement

        if pos_current[1] == 7:
            movement.extend([
                [self.pos[0] - 1, int(self.pos[1])],
                [self.pos[0] - 1, int(self.pos[1] - 1)],
                [self.pos[0], int(self.pos[1] - 1)],
                [self.pos[0] + 1, int(self.pos[1])],
                [self.pos[0] + 1, int(self.pos[1] - 1)],
            ])
            return movement


class Knight(Piece):

    def __init__(self, pos=None, name: str = None):
        super().__init__(pos, name)

    def move(self, **kwargs):
        self.pos = kwargs["pos"]

    def possible_movement(self) -> list[list[int]]:
        """
        movement of a Knight is x±2, y±1 and x±1 ,y±2


        :return: List of all coordinates of movement
        """

        pos_current = self.pos
        movement = []

        # x and y are in range 3 - 6 and c - f

        if (pos_current[0] - 2) >= 0 and int(pos_current[1]) - 1 >= 0:
            movement.append([(pos_current[0] - 2), int(pos_current[1]) - 1])

        if (pos_current[0] - 2) >= 0 and int(pos_current[1]) + 1 < 8:
            movement.append([(pos_current[0] - 2), int(pos_current[1]) + 1])

        if (pos_current[0] + 2) < 8 and int(pos_current[1]) - 1 >= 0:
            movement.append([(pos_current[0] + 2), int(pos_current[1]) - 1])

        if (pos_current[0] + 2) < 8 and int(pos_current[1]) + 1 < 8:
            movement.append([(pos_current[0] + 2), int(pos_current[1]) + 1])

        if (pos_current[0] - 1) >= 0 and int(pos_current[1]) - 2 >= 0:
            movement.append([(pos_current[0] - 1), int(pos_current[1]) - 2])

        if (pos_current[0] - 1) >= 0 and int(pos_current[1]) + 2 < 8:
            movement.append([(pos_current[0] - 1), int(pos_current[1]) + 2])

        if (pos_current[0] + 1) < 8 and int(pos_current[1]) - 2 >= 0:
            movement.append([(pos_current[0] + 1), int(pos_current[1]) - 2])

        if (pos_current[0] + 1) < 8 and int(pos_current[1]) + 2 < 8:
            movement.append([(pos_current[0] + 1), int(pos_current[1]) + 2])

        return movement


class Bishop(Piece):

    def __init__(self, pos=None, name: str = None):
        super().__init__(pos, name)

    def move(self, **kwargs):
        self.pos = kwargs["pos"]

    def possible_movement(self) -> list[list[int]]:
        """
        Bishop moves like x±1,y±1 until we hit the border
        :return: list of all coordinates of possible movement
        """

        current = self.pos
        movement = []
        length_of_dia = 1

        while (current[0] - length_of_dia >= 0) and current[1] - length_of_dia >= 0:
            movement.append([current[0] - length_of_dia, current[1] - length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while (current[0] - length_of_dia >= 0) and current[1] + length_of_dia < 8:
            movement.append([current[0] - length_of_dia, current[1] + length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while (current[0] + length_of_dia < 8) and current[1] - length_of_dia >= 0:
            movement.append([current[0] + length_of_dia, current[1] - length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while (current[0] + length_of_dia < 8) and current[1] + length_of_dia < 8:
            movement.append([current[0] + length_of_dia, current[1] + length_of_dia])
            length_of_dia += 1

        return movement


class Rook(Piece):

    def __init__(self, pos=None, name: str = None):
        super().__init__(pos, name)

    def move(self, **kwargs):
        self.pos = kwargs["pos"]

    def possible_movement(self) -> list[list[int]]:
        """
        Rook moves like x±1 and y±1 until we hit the border
        :return: list of all coordinates of possible movement
        """

        current = self.pos
        movement = []
        length_of_dia = 1

        while current[0] - length_of_dia >= 0:
            movement.append([current[0] - length_of_dia, current[1]])
            length_of_dia += 1

        length_of_dia = 1

        while current[1] + length_of_dia < 8:
            movement.append([current[0], current[1] + length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while current[0] + length_of_dia < 8:
            movement.append([current[0] + length_of_dia, current[1]])
            length_of_dia += 1

        length_of_dia = 1

        while current[1] - length_of_dia >= 0:
            movement.append([current[0], current[1] - length_of_dia])
            length_of_dia += 1

        return movement


class Queen(Piece):
    def __init__(self, pos=None, name: str = None):
        super().__init__(pos, name)

    def move(self, **kwargs):
        self.pos = kwargs["pos"]

    def possible_movement(self) -> list[list[int]]:
        """
        Rook moves like x±1 and y±1 until we hit the border
        :return: list of all coordinates of possible movement
        """

        current = self.pos
        movement = []
        length_of_dia = 1

        while current[0] - length_of_dia >= 0:
            movement.append([current[0] - length_of_dia, current[1]])
            length_of_dia += 1

        length_of_dia = 1

        while current[1] + length_of_dia < 8:
            movement.append([current[0], current[1] + length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while current[0] + length_of_dia < 8:
            movement.append([current[0] + length_of_dia, current[1]])
            length_of_dia += 1

        length_of_dia = 1

        while current[1] - length_of_dia >= 0:
            movement.append([current[0], current[1] - length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while (current[0] - length_of_dia >= 0) and current[1] - length_of_dia >= 0:
            movement.append([current[0] - length_of_dia, current[1] - length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while (current[0] - length_of_dia >= 0) and current[1] + length_of_dia < 8:
            movement.append([current[0] - length_of_dia, current[1] + length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while (current[0] + length_of_dia < 8) and current[1] - length_of_dia >= 0:
            movement.append([current[0] + length_of_dia, current[1] - length_of_dia])
            length_of_dia += 1

        length_of_dia = 1

        while (current[0] + length_of_dia < 8) and current[1] + length_of_dia < 8:
            movement.append([current[0] + length_of_dia, current[1] + length_of_dia])
            length_of_dia += 1

        return movement
