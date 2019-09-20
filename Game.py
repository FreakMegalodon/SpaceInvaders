#Region Preprocessor
import  DisplayUtils as dsman
import  InputMan     as inman
from GS_Menu import *
from GameStates import *
from GS_GameRunning import *
#End Region
class Game():
    #Region Fields
    is_playing      = True
    janela          = dsman.iniciarJanela()
    game_states     = dict()
    current_state   = GameStates.Game_Running
    mouse = None
    #End Region
    #Region Constructors
    def __init__(self):
        self.game_states[GameStates.Menu] = GS_Menu(self.janela)
        self.game_states[GameStates.Game_Running] = GS_GameRunning(self.janela)
        self.mouse = self.janela.get_mouse()
        return
    #End Region
    #Region Methods
    counter = 10000
    def run(self):
        print("Entrando no jogo")
        while self.is_playing:
            self.game_states[self.current_state].process_inputs()
            self.game_states[self.current_state].update()
            self.game_states[self.current_state].render()
            #new_state = self.game_states[self.current_state].get_mouse_click()
            #if new_state!= self.current_state and new_state is not None: self.change_state(new_state)
        return
    def change_state(self, new_state):
        self.game_states[self.current_state].on_state_exit()
        self.current_state = new_state
        self.game_states[self.current_state].on_state_enter()
        return
    
    def mover():
        return
    #End Region