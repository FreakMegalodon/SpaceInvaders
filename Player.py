from PPlay.gameimage import *

# Classe base do jogador
class Player:
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, game):
        self.game           = game
        self.janela         = self.game.janela
        #self.teclado        = self.janela.get_keyboard()
        self.game_image     = GameImage("Assets/images/tank.png")
        self.game_image.set_position(self.janela.width * 0.5 - self.game_image.width * 0.5,  self.janela.height - self.game_image.height - 10)
        #self.game..game_images.append(self.game_image)
        #self.velocity       = 200.0
        self.current_state  = Player_State_Playing(self.game, self)
        return
    #End Region
    #Region Methods
    def update(self):
        self.current_state.do()
        return

    
    def death(self):
        self.game.current_game_state.decrease_lives()
        self.current_state = Player_State_Raising(self.game, self)
        return
    #End Region

class Player_State_Playing:
    def __init__(self, game, player):
        self.game           = game
        self.player         = player
        self.janela         = self.game.janela
        self.teclado        = self.janela.get_keyboard()
        self.velocity       = 200.0
        return

    def do(self):
        self.move()
        return

    def move(self):
        if self.teclado.key_pressed("LEFT") or self.teclado.key_pressed("A"):
            self.player.game_image.x = max(0, min(self.player.game_image.x - (self.velocity * self.janela.delta_time()), self.janela.width - self.player.game_image.width))
        if self.teclado.key_pressed("RIGHT") or self.teclado.key_pressed("D"):
            self.player.game_image.x = max(0, min(self.player.game_image.x + (self.velocity * self.janela.delta_time()), self.janela.width - self.player.game_image.width))
        return

class Player_State_Raising():
    def __init__(self, game, player):
        self.game           = game
        self.player         = player
        self.janela         = self.game.janela
        self.velocity       = 100.0
        
        self.player.game_image.set_position((self.janela.width - self.player.game_image.width) / 2, self.janela.height)
        return

    def do(self):
        self.move()
        return
    
    def move(self):
        self.player.game_image.y -= 0.5 * self.velocity * self.janela.delta_time()
        if self.player.game_image.y <= self.janela.height - self.player.game_image.height - 10:
            self.player.game_image.y = self.janela.height - self.player.game_image.height - 10
            self.player.current_state = Player_State_Playing(self.game, self.player)
        return