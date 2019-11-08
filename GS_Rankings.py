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

class GS_Rankings():
    game_images = []

    def __init__(self, game):
        self.game               = game
        self.janela             = self.game.janela
        self.teclado            = self.janela.get_keyboard()
        self.current_state      = Rankings_State(self.game, self)
        return
    
    def on_state_enter(self):
        self.set_images()
        self.get_rankings()
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC")  : self.game.change_state(GameStates.Menu)
        return

    def update(self):
        self.current_state.do_update()
        return

    def render(self):
        self.janela.set_background_color([0, 0, 0])
        self.current_state.do_render()
        self.janela.update()
        return
    
    def set_images(self):
        self.game_images.append(GameImage("Assets/images/rankings_bg.png"))
        return 
    def get_rankings(self):
        #TODO Generalize, then isolate to other class
        file = "ranking.rkf"
        data = open(file, "r", encoding="utf-8")
        self.ranking_elements = []
        for line in data:
            score, name = line.split("|")
            name = name[:3]
            self.ranking_elements.append([score, name])
        data.close()
        return


class Rankings_State():
    def __init__(self, game, rankings):
        self.game       = game
        self.rankings   = rankings
        self.pulse_val  = 0
        self.grow       = True

    def do_update(self):
        #self.pulse()
        return

    def do_render(self):
        dsman.drawStack(self.rankings.game_images)
        self.game.janela.draw_text("HI SCORE", 50, 200, size= 50 + self.pulse_val, color=(120, 120, 255), font_name="Lucida Console", bold=False, italic=False)
        for i in range(len(self.rankings.ranking_elements)):
            record = "%s    %s"%(self.rankings.ranking_elements[i][1], self.rankings.ranking_elements[i][0].rjust(9, "0"))
            self.game.janela.draw_text(record, 50 + 10 * i, 250 + 50 * i, size=30, color=(140 + i * 20, 140 + i * 10, 255), font_name="Lucida Console", bold=False, italic=False)
        return

    def pulse(self):
        if self.pulse_val > 20: self.grow = False
        elif self.pulse_val < 0: self.grow = True
        self.pulse_val += int(120 * self.game.janela.delta_time() * (1 if self.grow else -1))
