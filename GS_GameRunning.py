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
        self.teclado            = self.game.janela.get_keyboard()
        self.is_running         = True
        self.delta_time         = 0
        self.set_images()

        self.enemy_types                         = dict()
        self.enemy_types[EnemyType.Enemy_one]    = "Assets/images/enemy-01.png"
        self.enemy_types[EnemyType.Enemy_two]    = "Assets/images/enemy-02.png"
        self.enemy_types[EnemyType.Enemy_tree]   = "Assets/images/enemy-03.png"

        self.x_space            = 60
        self.y_space            = 70
        self.en_lines           = 1
        self.max_lines          = 4
        self.en_columns         = 3
        self.max_columns        = 5
        self.enemie_count       = 3
        self.max_enemies_count  = 20

        self.default_en_timer   = 3
        self.max_enemy_timer    = self.default_en_timer
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
   
    def change_substate(self, ind):
        """
        0: Runnuning_State_Playing
        1: Running_State_GameOver
        2: Running_State_Input
        """
        if ind == 0: self.current_state = Runnuning_State_Playing(self.game, self)
        if ind == 1: self.current_state = Running_State_GameOver(self.game, self)
        if ind == 2: self.current_state = Running_State_Input(self.game, self)



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
            while not en.alive:
                line    = random.choice(self.enemy_parent)
                en      = random.choice(line)
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
        x, y                                = 0, self.y_space
        self.enemy_parent = []
        for i in range(self.en_lines):
            line    = []
            e_type  = random.choice(list(self.enemy_types.keys()))
            for j in range(self.en_columns):               
                en  = Enemy(self.game, x, y, e_type, self.enemy_types[e_type],30, 100, 400)
                line.append(en)
                self.game_images_running.append(en.game_image)
                x   += self.x_space
                #print("x: %d,y: %d"%(x, y))
            self.enemy_parent.append(line)
            x       = 0
            y       += self.y_space
            self.max_y = y + self.y_space
        self.en_columns += 1
        if self.en_columns > self.max_columns:
            self.en_columns = 3
            self.en_lines   = min(self.en_lines + 1, self.max_lines)
        self.max_enemy_timer = self.default_en_timer
        self.default_en_timer *= 0.95
        return
    
    def move_enemies(self):
        least_x, greater_x  = self.max_enemies_pos()
        if (greater_x >= 360 and self.dir == 1) or (least_x == 0 and self.dir == -1):
            self.move_down()
            self.max_enemy_timer *= 0.75
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
            self.game_over()
         return

    #End Region

class Runnuning_State_Playing():
    def __init__(self, game, running):
        self.game           = game
        self.running        = running
        self.bonus_time     = 2.0
        self.bonus_dir      = 1
        self.bonus_enemy    = Enemy(self.game, -100, 0, EnemyType.Enemy_bonus, "Assets/images/enemy-01.png", 10, 200, 3000)
        self.bonus_image    = [self.bonus_enemy.game_image]

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
        self.update_bonus()
        return

    def do_render(self):
        dsman.drawStack(self.running.game_images_running)
        dsman.drawStack(self.bonus_image)
        return

    def enemies_are_alive(self):
        for line in self.running.enemy_parent:
            for enem in line: 
                if enem.alive: return True
        return False

    def update_bonus(self):
        self.move_bonus()
        
        #if self.bonus_image[0].x < self.game.janela.width or self.bonus_image[0].x > -300:
            
        #else:
            #self.spawn_bonus()
            #print("Debug: Bonus released: %d"%self.bonus_image[0].x)
        #if len(self.bonus_image) == 0:
        #    self.bonus_time -= self.game.janela.delta_time()
        #    if self.bonus_time <= 0:
        #        self.bonus_time = 2.0
        #        self.spawn_bonus()
        #else:
            #print(self.bonus[0].x)
        return

    def spawn_bonus(self):
        dir = random.randint(0, 100)
        if dir < 50:
            self.bonus_dir = 1
            start_pos = -300
        else:
            self.bonus_dir = -1
            start_pos = self.game.janela.width + 300
        return

    def move_bonus(self):
        self.bonus_image[0].set_position(self.bonus_image[0].x + (100 * self.game.janela.delta_time() * self.bonus_dir), 0)
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
        if self.go_index == len(self.running.game_over):
            print("Debug: wait for input")
            #self.running.current_state = Running_State_Input(self.game, self.running)
            self.running.change_substate(2)
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
            self.game.change_state(GameStates.Ranking)
        else: self.game.change_state(GameStates.Menu)
        return