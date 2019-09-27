#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils    as      dsman
from    enum            import  Enum
from    PPlay.gameimage import  *
from    PPlay.keyboard  import  *
from    PPlay.mouse     import  *
from    GameStates      import  *
from    Bullet          import  *
from    Enemy           import  *
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
        self.x_space    = 60
        self.y_space    = 70    
        self.max_enemy_timer = 3
        self.move_x     = True
        self.move_y     = False
        self.create_enemy_matrix()
        return
    
    def on_state_enter(self):
        self.enemy_timer    = 0.0
        self.dir            = 1        
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
        self.enemy_timer += self.janela.delta_time()
        if self.enemy_timer >= self.max_enemy_timer:
            self.move_enemies()
            self.enemy_timer = 0

        for b in self.bullets_parent: b.update()
        for line in self.enemy_parent:
            for e in line:
                e.update()
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
        self.player.set_position(self.janela. width * 0.5, self.janela.height - 10 - self.player.height)
        self.game_images.append(self.bg)
        self.game_images.append(self.player)
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

    def create_enemy_matrix(self):
        x, y = 0, 0
        self.enemy_parent = []
        for i in range(4):
            line    = []
            for j in range(3):
                en  = Enemy(self.janela, x, y, "")
                line.append(en)
                self.game_images.append(en.game_image)
                x   += self.x_space
                print("x: %d,y: %d"%(x, y))
            self.enemy_parent.append(line)
            x       = 0
            y       += self.y_space
        return
    
    def move_enemies(self):
        #if not (greater_x == 360 or least_x == 0):
        least_x, greater_x  = self.max_enemies_pos()
        if (greater_x >= 360 and self.dir == 1) or (least_x == 0 and self.dir == -1):
            self.move_down()
            self.max_enemy_timer *= 0.5
            self.dir *= -1
            return
        self.move_side(self.dir)
        return

    def max_enemies_pos(self):
        min_x = self.janela.width + 200
        max_x = 0
        for i in range(len(self.enemy_parent)):
            for j in range(len(self.enemy_parent[i])):
                if self.enemy_parent[i][j] is not None:
                    if self.enemy_parent[i][j].game_image.x < min_x     : min_x = self.enemy_parent[i][j].game_image.x
                    elif self.enemy_parent[i][j].game_image.x > max_x   : max_x = self.enemy_parent[i][j].game_image.x
        print("%d, %d"%(min_x, max_x))
        return min_x, max_x
    
    def move_side(self, direction):
        for line in self.enemy_parent:
            for e in line:
                e.game_image.x += self.x_space * direction

    def move_down(self):
        for line in self.enemy_parent:
            for e in line:
                e.game_image.y += self.y_space
     
    #End Region