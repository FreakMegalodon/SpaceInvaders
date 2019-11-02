#Region Preprocessor
import  DisplayUtils    as      dsman
import  InputMan        as      inman
from    enum            import  Enum
from    GS_Menu         import  *
from    GameStates      import  *
from    GS_GameRunning  import  *
from    GS_Dificuldades import  *
from    Dificuldades    import  *
#End Region
class Game():
    #Region Fields
    is_playing      = True
    janela          = dsman.iniciarJanela()
    game_states     = dict()
    current_state   = None
    difficulty      = Dificuldades.Normal
    #End Region
    #Region Constructors
    def __init__(self):
#
#        self.game_states[GameStates.Menu]           = GS_Menu(self)
#
        self.change_state(GameStates.Menu)
        return
    #End Region
    #Region Methods
    def run(self):
        print("Entrando no jogo")
        while self.is_playing:
            self.current_game_state.process_inputs()
            self.current_game_state.update()
            self.current_game_state.render()
        return
    
    def change_state(self, new_state):
        print("Debug: Mudar state para %s"%str(new_state))
        if self.current_state is not None                   : self.current_game_state.on_state_exit()
        self.current_state = new_state
        if self.current_state == GameStates.Dificuldades    : self.current_game_state = GS_Dificuldades(self)
        if self.current_state == GameStates.Exit            : pass
        if self.current_state == GameStates.Intro           : pass
        if self.current_state == GameStates.Menu            : self.current_game_state = GS_Menu(self)
        if self.current_state == GameStates.Paused          : pass
        if self.current_state == GameStates.Ranking         : pass
        if self.current_state == GameStates.Running         : self.current_game_state = GS_GameRunning(self)
        self.current_game_state.on_state_enter()
        return
    
    def change_difficulty(self, difficulty):
        self.difficulty = difficulty
        return
    #End Region