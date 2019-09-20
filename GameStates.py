from enum import Enum

class GameStates(Enum):
    Intro           = 0
    Menu            = 1
    Game_Running    = 2
    Game_Paused     = 3
    Game_Exit       = 4