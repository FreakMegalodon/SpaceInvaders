from PPlay.gameimage import *

# Classe base do jogador
class Bullet:
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, game, x, y, bullet_type):
        """
        Bullet Type: 0 for player | 1 for enemy
        """
        self.game           = game
        self.janela         = game.janela
        if bullet_type == 0:
            self.game_image     = GameImage("Assets/images/bullet.png")
            self.velocity       = -500.0
            self.current_state  = Bullet_State_Start(self.game.current_game_state, self)
        else:
            self.game_image     = GameImage("Assets/images/bullet.png")
            self.velocity       = 300.0
            self.current_state  = Bullet_State_Enemy(self.game.current_game_state, self)

        self.start_position = [x, y]        
        self.game_image.set_position(x - self.game_image.width * 0.5, y - self.game_image.height)
        
        return
    #End Region
    #Region Methods
    def update(self):
        self.game_image.set_position(self.game_image.x, self.game_image.y + self.velocity * self.janela.delta_time() )
        self.current_state.do()
        return
        
    def change_state(self):
        self.current_state = Bullet_State_Check_Collision(self.game.current_game_state, self)
        return
    #End Region

class Bullet_State_Start:
    def __init__(self, game_state, bullet):
        self.game_state = game_state
        self.bullet = bullet
        return
    
    def do(self):
        if self.game_state.max_y <= self.bullet.game_image.y:
            self.bullet.change_state()
        return
    
class Bullet_State_Check_Collision:
    def __init__(self, game_state, bullet):
        self.game_state = game_state
        self.bullet     = bullet
        return

    def do(self):
        self.collision()
        return

    def collision(self):
        for line in self.game_state.enemy_parent:
            for enemy in line:
                if self.bullet.game_image.collided(enemy.game_image):
                    enemy.hit()
                    self.bullet.game_image.set_position(0, -50)
                    return
        if self.bullet.game_image.collided(self.game_state.bonus_enemy.game_image):
            self.game_state.bonus_enemy.hit()
            self.bullet.game_image.set_position(0, -50)

        return

class Bullet_State_Enemy:
    def __init__(self, game_state, bullet):
        self.game_state = game_state
        self.bullet = bullet
        return
    def do(self):
        if self.bullet.game_image.collided(self.game_state.player.game_image):
            self.bullet.game_image.set_position(self.bullet.game_image.x, 10000)
            self.game_state.player.death()
        return