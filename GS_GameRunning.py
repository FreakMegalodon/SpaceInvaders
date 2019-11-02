#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils            as      dsman
from    enum                    import  Enum
import  random
from    PPlay.gameimage         import  *
from    PPlay.keyboard          import  *
from    PPlay.mouse             import  *
from    GameStates              import  *
from    Bullet                  import  *
from    Enemy                   import  *
from    ScrollableBackground    import  *
from    Player                  import  *
#End Region

class GS_GameRunning():
    game_images             = []
    menu_buttons            = dict()
    fps                     = 0
    contador                = 0
    tempo_transcorrido      = 0
    bullets_parent          = []
    contador_bullet_time    = 0

    def __init__(self, game):
        self.game               = game
        self.janela             = self.game.janela
        self.mouse              = self.janela.get_mouse()
        self.teclado            = self.janela.get_keyboard()
        self.delta_time         = 0
        self.set_images()
        self.x_space            = 60
        self.y_space            = 70    
        self.max_enemy_timer    = 3
        self.move_x             = True
        self.move_y             = False
        self.score              = 0
        self.lives              = 3
        self.max_y              = 0
        self.create_enemy_matrix()
        return
    
    def on_state_enter(self):
        self.enemy_timer                = 0.0
        self.dir                        = 1
        self.contador_enemy_bullet_time = 0.0
        self.max_enemy_bullet_time      = 3
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC"): self.game.change_state(GameStates.Menu)
        self.fire()
        return

    def update(self):
        self.delta_time = self.janela.delta_time()
        self.bg.update()
        self.stars_f.update()
        self.stars_b.update()
        self.player.update()
        self.contador_bullet_time   += self.delta_time 
        self.enemy_timer            += self.delta_time 
        if self.enemy_timer >= self.max_enemy_timer:
            self.move_enemies()
            self.enemy_timer = 0

        for b in self.bullets_parent: b.update()
        for line in self.enemy_parent:
            for e in line:
                e.update()
        self.destroy_bullets()
        self.enemy_fire()
        return

    def render(self):
        self.janela.set_background_color([0, 0, 0])
        self.tempo_transcorrido += self.delta_time
        self.contador += 1
        if self.tempo_transcorrido >= 1:
            self.fps = self.contador
            self.contador = 0
            self.tempo_transcorrido = 0
        dsman.drawStack(self.game_images)
        self.janela.draw_text(str(self.fps), 30, 30, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
        self.janela.draw_text(str(self.score) + " | " + str(self.lives), 30, 60, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
        self.janela.update()
        return
    
    def set_images(self):
        self.bg         = ScrollableBackground(self, "Assets/images/game_background_night_01.png", 25)
        self.stars_f    = ScrollableBackground(self, "Assets/images/game_background_night_02.png", 40)
        self.stars_b    = ScrollableBackground(self, "Assets/images/game_background_night_03.png", 50)
        self.player     = Player(self.game)
        self.game_images.append(self.player.game_image)
        return 
    
    def new_bullet_object(self, x, y):
        bullet = Bullet(self.game, x, y, 0)
        self.bullets_parent.append(bullet)
        self.game_images.append(bullet.game_image)
        return
        
    def fire(self):
        """
        Tiro do jogador, pelo menos, a cada self.contador_bullet_time segundos
        """
        if (self.teclado.key_pressed("S") or self.teclado.key_pressed("SPACE")) and self.contador_bullet_time > 0.1:
            self.new_bullet_object(self.player.game_image.x + self.player.game_image.width * 0.5, self.player.game_image.y)
            self.contador_bullet_time = 0
        return

    def destroy_bullets(self):
        for b in self.bullets_parent:
            if (b.game_image.y < -b.game_image.height - 10) or (b.game_image. y > self.janela.height + 30):
                self.game_images.remove(b.game_image)
                self.bullets_parent.remove(b)
        return

    def enemy_fire(self):
        """
        Tiro dos inimigos, de posicoes aleatorias, pelo menos, a cada self.contador_enemy_bullet_time
        """
        self.contador_enemy_bullet_time += self.delta_time
        if self.contador_enemy_bullet_time >= self.max_enemy_bullet_time:
            # select random enemy
            random.seed()
            #spawn enemy_bullet
            line = random.choice(self.enemy_parent)
            en = random.choice(line)
            while en is None: en = random.choice()
            bullet = Bullet(self.game, en.game_image.x + self.x_space / 2, en.game_image.y + self.y_space, 1)
            self.bullets_parent.append(bullet)
            self.game_images.append(bullet.game_image)
            # zero counter
            self.contador_enemy_bullet_time = 0
        
        return

    def create_enemy_matrix(self):

        random.seed()
        #enemy_types = [EnemyType.Enemy_one, EnemyType.Enemy_two, EnemyType.Enemy_tree]
        enemy_types                         = dict()
        enemy_types[EnemyType.Enemy_one]    = "Assets/images/enemy-01.png"
        enemy_types[EnemyType.Enemy_two]    = "Assets/images/enemy-02.png"
        enemy_types[EnemyType.Enemy_tree]   = "Assets/images/enemy-03.png"
        x, y                                = 0, 0
        self.enemy_parent = []
        for i in range(4):
            line    = []
            e_type  = random.choice(list(enemy_types.keys()))
            for j in range(3):                
                en  = Enemy(self.game, x, y, e_type, enemy_types[e_type])
                line.append(en)
                self.game_images.append(en.game_image)
                x   += self.x_space
                #print("x: %d,y: %d"%(x, y))
            self.enemy_parent.append(line)
            x       = 0
            y       += self.y_space
            self.max_y = y + self.y_space
        return
    
    def move_enemies(self):
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
        #print("%d, %d"%(min_x, max_x))
        return min_x, max_x
    
    def move_side(self, direction):
        for line in self.enemy_parent:
            for e in line:
                e.game_image.x += self.x_space * direction

    def move_down(self):
        for line in self.enemy_parent:
            for e in line:
                e.game_image.y += self.y_space
        self.max_y += self.y_space
        return
     
    def decrease_lives(self):
         self.lives -= 1
         if self.lives <= 0:
            self.game.change_state(GameStates.Menu)
         return
    #End Region