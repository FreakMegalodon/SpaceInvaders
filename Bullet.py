from PPlay.gameimage import *

# Classe base do jogador
class Bullet:
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, game, x, y):
        self.game           = game
        self.janela         = game.janela
        self.game_image     = GameImage("Assets/images/bullet.png")
        self.start_position = [x, y]
        self.velocity       = 500.0
        self.game_image.set_position(x - self.game_image.width * 0.5, y - self.game_image.height)
        #self.enemy_list     = game.game_states[game.current_state].enemy_parent
        #print("Debug: new bullet!")
        return
    #End Region
    #Region Methods
    def update(self):
        self.game_image.set_position(self.game_image.x, self.game_image.y - self.velocity * self.janela.delta_time() )
        self.collision()
        return
    
    def collision(self):
        for line in self.game.game_states[self.game.current_state].enemy_parent:
            for enemy in line:
                if self.game_image.collided(enemy.game_image):
                    #self.game.game_states[self.game.current_state].enemy_parent.remove(enemy)
                    #line.remove(enemy)
                    enemy.hit()
                    self.game_image.set_position(0, -50)
                    return
        return
        #if x -first_x or x > last_x:return
        #binary_search(x): int index da coluna
        #loop coluna da linha
        #return
        
        self.game_image.collided()
        return
    def search_enemy_column(self):
        return
    #End Region