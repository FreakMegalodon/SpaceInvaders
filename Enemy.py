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
        self.stamina        = 50
        return
    #End Region
    #Region Methods
    def update(self):
        return
    def hit(self):
        self.stamina -= 10
        self.add_score(100)
        if self.stamina <= 0:
             self.death()
        return

    def death(self):
        self.game_image.set_position(self.game_image.x, 1000)
        self.add_score(400)
        return
    
    def add_score(self, val):
        self.game.game_states[self.game.current_state].score += val
        return
    #End Region