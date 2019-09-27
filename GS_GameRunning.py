#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils    as      dsman
from    enum            import  Enum
from    PPlay.gameimage import  *
from    PPlay.keyboard  import  *
from    PPlay.mouse     import  *
from    GameStates      import  *

#End Region

class GS_GameRunning():
    game_images             = []
    menu_buttons            = dict()
    ship                    = None
    velocity                = 300
    fps                     = 0
    contador                = 0
    tempo_transcorrido      = 0
    bullets                 = []
    contador_bullet_time    = 0

    def __init__(self, game_mngr):
        self.game_mngr  = game_mngr
        self.janela     = self.game_mngr.janela
        self.mouse      = self.janela.get_mouse()
        self.teclado    = self.janela.get_keyboard()
        self.set_images()
        #self.set_menu_buttons()
        return
    
    def on_state_enter(self):
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC"): self.game_mngr.change_state(GameStates.Menu)
        self.move()
        if (self.teclado.key_pressed("S") or self.teclado.key_pressed("SPACE")) and self.contador_bullet_time > 0.1:
            self.new_bullet(self.ship.x + self.ship. width * 0.5, self.ship.y)
            self.contador_bullet_time = 0
        return

    def update(self):
        self.contador_bullet_time += self.janela.delta_time()
        self.move_bullets()
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
        self.ship     = GameImage("Assets/images/ship.png")
        self.ship.set_position(self.janela. width * 0.5, self.janela.height - 80)
        self.game_images.append(self.ship)
        return 
    
    def new_bullet(self, x, y):
        bullet = GameImage("Assets/images/bullet.png")
        bullet.set_position(x  - bullet.width * 0.5, y)
        self.bullets.append(bullet)
        return

    def move(self):
        #player1.y = max(0, min(mouse.Mouse.get_position(self=Mouse)[1], janela.height - player1.height))
        if self.teclado.key_pressed("LEFT"):   self.ship.x = max(0, min(self.ship.x - (self.velocity * self.janela.delta_time()), self.janela.width - self.ship.width))
        if self.teclado.key_pressed("RIGHT"): self.ship.x = max(0, min(self.ship.x + (self.velocity * self.janela.delta_time()), self.janela.width - self.ship.width))
        return
    
    def move_bullet(self, b):
        b.set_position(b.x, b.y - 500 * self.janela.delta_time())
        return

    def move_bullets(self):
        for bullet in self.bullets:
            self.move_bullet(bullet)
        return
    
    def destroy_bullet(self, b):
        if b.y < -b.height - 10:
            self.bullets.remove(b)
            print("bullet removida")
        return

    def destroy_bullets(self):
        for b in self.bullets:
            self.destroy_bullet(b)
        return
    #End Region