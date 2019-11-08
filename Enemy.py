from    PPlay.gameimage import  *
from    enum            import  Enum
from    GameStates      import  *

class EnemyType(Enum):
    No_enemy    = 0
    Enemy_one   = 1
    Enemy_two   = 2
    Enemy_tree  = 4
    Enemy_Boss  = 8
    Enemy_bonus = 16

# Classe base do jogador
class Enemy:
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, game, x, y, type, path, stamina, score, kill):
        self.game           = game
        self.janela         = self.game.janela
        self.stamina        = stamina
        self.score          = score
        self.type           = type
        self.kill = kill
        self.game_image     = GameImage(path)
        self.game_image.set_position(x, y)
        self.alive          = True
        return
    #End Region
    #Region Methods
    def update(self):
        return

    def hit(self):
        self.stamina -= 10
        self.add_score(self.score)
        if self.stamina <= 0:
             self.death()
        return

    def death(self):
        self.game_image.set_position(self.game_image.x, 1000)
        self.alive = False
        self.add_score(self.kill)
        if self.type == EnemyType.Enemy_bonus:
            self.game.current_game_state.current_state.spawn_bonus()
            return
        if not self.game.current_game_state.current_state.enemies_are_alive():
            self.game.current_game_state.create_enemy_matrix()
        return
    
    def add_score(self, val):
        self.game.current_game_state.score += val
        return
    #End Region