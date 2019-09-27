from PPlay.gameimage import *

# Classe base do jogador
class Player:
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, game):
        self.game           = game
        self.janela         = self.game.janela
        self.teclado        = self.janela.get_keyboard()
        self.game_image     = GameImage("Assets/images/tank.png")
        self.game_image.set_position(self.janela.width * 0.5 - self.game_image.width * 0.5,  self.janela.height - self.game_image.height - 10)
        self.game.game_images.append(self.game_image)
        self.velocity       = 200.0
        return
    #End Region
    #Region Methods
    def update(self):
        self.move()
        return

    def move(self):
        if self.teclado.key_pressed("LEFT") or self.teclado.key_pressed("A"):
            self.game_image.x = max(0, min(self.game_image.x - (self.velocity * self.janela.delta_time()), self.janela.width - self.game_image.width))
        if self.teclado.key_pressed("RIGHT") or self.teclado.key_pressed("D"):
            self.game_image.x = max(0, min(self.game_image.x + (self.velocity * self.janela.delta_time()), self.janela.width - self.game_image.width))
        return    
    #End Region