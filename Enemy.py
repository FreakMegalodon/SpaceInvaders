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
    def __init__(self, game, x, y, type, path):
        self.game           = game
        self.janela         = self.game.janela
        self.game_image     = GameImage(path)
        self.game_image.set_position(x, y)
        game.game_images.append(self.game_image)
        
        return
    #End Region
    #Region Methods
    def update(self):
        return
    
    #End Region