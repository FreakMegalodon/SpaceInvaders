from PPlay.gameimage import *

# Classe base do jogador
class Bullet:
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, janela, x, y):
        self.game_image     = GameImage("Assets/images/bullet.png")
        self.janela         = janela
        self.start_position = [x, y]
        self.velocity       = 500.0
        self.game_image.set_position(x - self.game_image.width * 0.5, y - self.game_image.height)
        #print("Debug: new bullet!")
        return
    #End Region
    #Region Methods
    def update(self):
        self.game_image.set_position(self.game_image.x, self.game_image.y - self.velocity * self.janela.delta_time() )
        return
    #End Region