#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils    as      dsman
from    enum            import  Enum
from    PPlay.gameimage import  *
from    PPlay.keyboard  import  *
from    PPlay.mouse     import  *
from    GameStates      import  *
from    Bullet          import  *
#End Region

class GS_GameRunning():
    game_images             = []
    menu_buttons            = dict()
    player                    = None
    velocity                = 300
    fps                     = 0
    contador                = 0
    tempo_transcorrido      = 0
    bullets                 = []
    bullets_parent          = []
    contador_bullet_time    = 0

    def __init__(self, game_mngr):
        self.game_mngr  = game_mngr
        self.janela     = self.game_mngr.janela
        self.mouse      = self.janela.get_mouse()
        self.teclado    = self.janela.get_keyboard()
        self.set_images()
        return
    
    def on_state_enter(self):
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC"): self.game_mngr.change_state(GameStates.Menu)
        self.move()
        if (self.teclado.key_pressed("S") or self.teclado.key_pressed("SPACE")) and self.contador_bullet_time > 0.1:
            self.new_bullet_object(self.player.x + self.player. width * 0.5, self.player.y)
            self.contador_bullet_time = 0
        return

    def update(self):
        self.contador_bullet_time += self.janela.delta_time()
        for b in self.bullets_parent: b.update()
        self.destroy_bullets()
        return

    def render(self):
        self.janela.set_background_color([0, 0, 0])
        self.tempo_transcorrido += self.janela.delta_time()
        self.contador += 1
        if self.tempo_transcorrido >= 1:
            self.fps = self.contador
            self.contador = 0
            self.tempo_transcorrido = 0
        dsman.drawStack(self.game_images)
        dsman.drawStack(self.bullets)
        self.janela.draw_text(str(self.fps), 30, 30, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
        self.janela.update()
        return
    
    def set_images(self):
        self.bg         = GameImage("Assets/images/game_background_night_01.png")
        self.player     = GameImage("Assets/images/tank.png")
        ####
        self.enemy1      = GameImage("Assets/images/enemy-01.png")
        self.enemy2      = GameImage("Assets/images/enemy-02.png")
        self.enemy2.set_position(150, self.enemy2.y)
        self.enemy3      = GameImage("Assets/images/enemy-03.png")
        self.enemy3.set_position(300, self.enemy3.y)
        ####
        self.player.set_position(self.janela. width * 0.5, self.janela.height - 10 - self.player.height)
        self.game_images.append(self.bg)
        self.game_images.append(self.player)
        ####
        self.game_images.append(self.enemy1)
        self.game_images.append(self.enemy2)
        self.game_images.append(self.enemy3)
        ####
        return 
    
    def new_bullet_object(self, x, y):
        bullet = Bullet(self.janela, x, y)
        self.bullets_parent.append(bullet)
        self.game_images.append(bullet.game_image)
        return
        
    def move(self):
        if self.teclado.key_pressed("LEFT"):   self.player.x = max(0, min(self.player.x - (self.velocity * self.janela.delta_time()), self.janela.width - self.player.width))
        if self.teclado.key_pressed("RIGHT"): self.player.x = max(0, min(self.player.x + (self.velocity * self.janela.delta_time()), self.janela.width - self.player.width))
        return
    
    def destroy_bullets(self):
        for b in self.bullets_parent:
            if b.game_image.y < -b.game_image.height - 10:
                self.game_images.remove(b.game_image)
                self.bullets_parent.remove(b)
        return
    #End Region