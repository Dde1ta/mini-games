import Main

class Game:
    def __init__(self,game = None):
        self.game = game

    def step(self,action):
        match action:
            case 0:
                '''
                up
                '''
                self.game.up()
            case 1:
                '''
                down
                '''
                self.game.down()
            case 2:
                '''
                left
                '''
                self.game.left()
            case 3:
                '''
                right
                '''
                self.game.right()

        return None