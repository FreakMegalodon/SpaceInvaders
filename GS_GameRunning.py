#Region Preprocessor
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
    game_images_running     = []
    game_images_game_over   = []
    fps                     = 0
    contador                = 0
    tempo_transcorrido      = 0
    bullets_parent          = []
    contador_bullet_time    = 0

    def __init__(self, game):
        self.game               = game
        self.janela             = self.game.janela
        #self.mouse              = self.janela.get_mouse()
        self.teclado            = self.janela.get_keyboard()
        self.is_running         = True
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
        self.current_state      = Runnuning_State_Playing(self.game, self)
        return
    
    def on_state_enter(self):
        self.enemy_timer                = 0.0
        self.dir                        = 1
        self.contador_enemy_bullet_time = 0.0
        self.max_enemy_bullet_time      = 3
        self.create_enemy_matrix()
        return
    
    def on_state_exit(self):
        self.is_running = False
        self.enemy_parent.clear()
        self.bullets_parent.clear()
        self.game_images_running.clear()
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC")  : self.game.change_state(GameStates.Menu)
        if self.teclado.key_pressed("Y")    : self.current_state = Running_State_GameOver(self.game, self)
        #self.fire()
        return

    def update(self):
        if self.is_running:
            self.delta_time = self.janela.delta_time()
            self.enemy_timer            += self.delta_time 
            self.contador_bullet_time   += self.delta_time 

            self.current_state.do_update()
        return

    def render(self):
        self.janela.set_background_color([0, 0, 0])
        #self.count_fps()
        self.current_state.do_render()

        self.janela.draw_text(str(self.fps), 30, 30, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
        self.janela.draw_text(str(self.score) + " | " + str(self.lives), 30, 60, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
        self.janela.update()
        return
    
    def set_images(self):
        self.bg         = ScrollableBackground(self, "Assets/images/game_background_night_01.png", 25)
        self.stars_f    = ScrollableBackground(self, "Assets/images/game_background_night_02.png", 40)
        self.stars_b    = ScrollableBackground(self, "Assets/images/game_background_night_03.png", 50)
        self.player     = Player(self.game)
        self.game_images_running.append(self.bg.game_image)
        self.game_images_running.append(self.stars_f.game_image)
        self.game_images_running.append(self.stars_b.game_image)

        self.game_images_running.append(self.bg.copy)
        self.game_images_running.append(self.stars_f.copy)
        self.game_images_running.append(self.stars_b.copy)

        self.game_images_running.append(self.player.game_image)
        
        self.game_over = [GameImage("Assets/images/game_over_main.png"), GameImage("Assets/images/game_over_console.png")]
        self.game_over[0].set_position((self.game.janela.width - self.game_over[0].width) * 0.5, 100)
        self.game_over[1].set_position((self.game.janela.width - self.game_over[1].width) * 0.5, 300)
        return 
    
    def new_bullet_object(self, x, y):
        bullet = Bullet(self.game, x, y, 0)
        self.bullets_parent.append(bullet)
        self.game_images_running.append(bullet.game_image)
        return

    def destroy_bullets(self):
        """
        Destroi os tiros fora dos limites da tela
        """
        for b in self.bullets_parent:
            if (b.game_image.y < -b.game_image.height - 10) or (b.game_image. y > self.janela.height + 30):
                self.game_images_running.remove(b.game_image)
                self.bullets_parent.remove(b)
        return

    def enemy_fire(self):
        """
        Tiro dos inimigos, de posicoes aleatorias, pelo menos, a cada self.contador_enemy_bullet_time
        """
        self.contador_enemy_bullet_time += self.delta_time
        if self.contador_enemy_bullet_time >= self.max_enemy_bullet_time:
            random.seed()
            line                            = random.choice(self.enemy_parent)
            en                              = random.choice(line)
            while en is None: en = random.choice()
            bullet                          = Bullet(self.game, en.game_image.x + self.x_space / 2, en.game_image.y + self.y_space, 1)
            self.bullets_parent.append(bullet)
            self.game_images_running.append(bullet.game_image)
            self.contador_enemy_bullet_time = 0
        
        return

    def count_fps(self):
        """
        Conta FPS baseado na contagem incremental de janela.delta_time()
        """
        self.tempo_transcorrido += self.delta_time
        self.contador += 1
        if self.tempo_transcorrido >= 1:
            self.fps = self.contador
            self.contador = 0
            self.tempo_transcorrido = 0
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
                self.game_images_running.append(en.game_image)
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
            self.current_state = Running_State_GameOver(self.game, self)
         return
    #End Region

class Runnuning_State_Playing():
    def __init__(self, game, running):
        self.game       = game
        self.running    = running

    def do_update(self):
        self.running.bg.update()
        self.running.stars_f.update()
        self.running.stars_b.update()
        self.running.player.update()
        self.running.count_fps()

        for b in self.running.bullets_parent: b.update()

        for line in self.running.enemy_parent:
            for e in line: e.update()

        if self.running.enemy_timer >= self.running.max_enemy_timer:
            self.running.move_enemies()
            self.running.enemy_timer = 0

        self.running.destroy_bullets()
        self.running.enemy_fire()
        return

    def do_render(self):
        dsman.drawStack(self.running.game_images_running)
        return

class Running_State_GameOver():
    def __init__(self, game, running):
        self.game       = game
        self.running    = running
        self.timer      = 0.0
        self.transition = 2.0
        self.go_index   = 0
        return

    def do_update(self):
        self.timer += self.game.janela.delta_time()
        if self.go_index == len(self.running.game_over): self.running.current_state = Running_State_Input(self.game, self.running)
        if self.timer >= self.transition:
            self.running.game_images_game_over.append(self.running.game_over[self.go_index])
            self.go_index   += 1
            self.timer      = 0.0
        return
    
    def do_render(self):
        dsman.drawStack(self.running.game_images_running)
        dsman.drawStack(self.running.game_images_game_over)
        return

class Running_State_Input():
    def __init__(self, game, running):
        self.game       = game
        self.running    = running
        self.rank_player()
        return


    def do_update(self):
        return

    def do_render(self):
        dsman.drawStack(self.running.game_images_running)
        dsman.drawStack(self.running.game_images_game_over)
        return
    
    def rank_player(self):
        if self.running.score > self.game.least_ranking_position:
            val = input("Entre suas iniciais: ")
            if len(val) > 3: val = val[:3]
            val = val.upper()
            file        = "ranking.rkf"
            data        = open(file, "r", encoding="utf-8")
            lines     = data.readlines()[:4]
            ranking = []
            for line in lines:
                a, b    = line.split("|")
                a       = int(a)
                ranking.append([a, b])
            data.close()
            ranking.append([self.running.score, val + "\n"])
            ranking.sort()
            ranking.reverse()
            data    = open(file, "w", encoding="utf-8")
            for line in ranking: data.write(str(line[0]) + "|" + line[1])
            data.close()
            self.game.change_state(GameStates.Menu)
        return