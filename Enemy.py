from PPlay.gameimage import *
from enum import Enum

class EnemyType(Enum):
    No_enemy    = 0
    Enemy_one   = 1
    Enemy_two   = 2
    Enemy_tree  = 4
    Enemy_Boss  = 8

# Classe base do jogador
class Enemy:
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, janela, x, y, type):
        self.game_image     = GameImage("Assets/images/enemy-03.png")
        self.janela         = janela
        self.start_position = [x, y]
        #self.velocity       = 500.0
        #self.game_image.set_position(x - self.game_image.width * 0.5, y - self.game_image.height)
        self.game_image.set_position(x, y)
        #print("Debug: new bullet!")
        return
    #End Region
    #Region Methods
    def update(self):
        #self.game_image.set_position(self.game_image.x, self.game_image.y - self.velocity * self.janela.delta_time() )
        return
    #End Region