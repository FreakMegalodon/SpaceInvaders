from PPlay.gameimage import *
from random import random
# Classe base do jogador
class Player:
    #Region Fields
    player          = None
    player_position = 0
    janela          = None
    teclado         = None
    velocity        = 300
    up, down        = "", ""
    #End Region
    #Region Constructors
    def __init__(self, janela, player_position):
        self.player_position            = player_position
        self.janela                     = janela
        self.player                     = GameImage(self.get_img())
        self.player.x, self.player.y    = self.set_start_pos()
        self.teclado                    = self.janela.get_keyboard()
        self.up, self.down = self.set_player_keys()
        return
    #End Region
    #Region Methods
    def get_img(self): return "Assets/player1.png" if self.player_position == 1 else "Assets/player2.png"

    def set_start_pos(self): return (10, (self.janela.height * 0.5) - (self.player.height * 0.5)) if self.player_position == 1 else (self.janela.width - 10 - self.player.width, (self.janela.height * 0.5) - (self.player.height * 0.5))

    def set_player_keys(self): return ("W", "S") if self.player_position == 1 else ("UP", "DOWN")

    def move(self):
        #player1.y = max(0, min(mouse.Mouse.get_position(self=Mouse)[1], janela.height - player1.height))
        if self.teclado.key_pressed(self.up):   self.player.y = max(0, min(self.player.y - (self.velocity * self.janela.delta_time()), self.janela.height - self.player.height))
        if self.teclado.key_pressed(self.down): self.player.y = max(0, min(self.player.y + (self.velocity * self.janela.delta_time()), self.janela.height - self.player.height))
        return
    
    def move_ia(self, direcao):
        fator_velocidade = 0
        while fator_velocidade < 0.6:
            fator_velocidade = random()
        if not direcao:
            self.player.y = max(0, min(self.player.y - (self.velocity * self.janela.delta_time()), self.janela.height - self.player.height))
        else:
            self.player.y = max(0, min(self.player.y + (self.velocity * self.janela.delta_time()), self.janela.height - self.player.height))

    #End Region
