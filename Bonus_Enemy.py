import  random
from    PPlay.gameimage import  *
from    enum            import  Enum
from    GameStates      import  *

class Bonus_Enemy:
    #Region Constructors
    def __init__(self, game, x, y, type, path, stamina, score, kill):
        self.game           = game
        self.stamina        = stamina
        self.score          = score
        self.type           = type
        self.kill_score     = kill
        self.game_image     = GameImage(path)
        self.top_bounds     = 1200
        self.bottom_bounds  = 500
        self.velocity       = 100
        self.reset_position()
        return
    #End Region
    #Region Methods
    def update(self):
        self.move()
        self.check_position()
        return

    def move(self):
        self.game_image.set_position(self.game_image.x + (self.velocity * self.game.janela.delta_time() * self.bonus_dir), 0)
        return

    def hit(self):
        self.stamina -= 10
        self.add_score(self.score)
        if self.stamina <= 0: self.death()
        return

    def death(self):
        self.reset_position()
        self.add_score(self.kill_score)
        return

    def add_score(self, val):
        self.game.current_game_state.score += val
        return

    def reset_position(self):
        dir = random.randint(0, 100)
        start_bound = random.randint(self.bottom_bounds, self.top_bounds)
        if dir < 50:
            self.bonus_dir  = 1
            start_pos       = -start_bound
        else:
            self.bonus_dir  = -1
            start_pos       = self.game.janela.width + start_bound
        self.game_image.set_position(start_pos, 0)
        return

    def check_position(self):
        if self.game_image.x > self.game.janela.width + self.top_bounds + 10 or self.game_image.x < -self.top_bounds - 10: self.reset_position()
        return
    #End Region