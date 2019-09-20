#Region Preprocessor
import  DisplayUtils as dsman
from enum import Enum
from PPlay.gameimage import *
from PPlay.keyboard import *
from PPlay.mouse import *
from GameStates import *

#End Region
class Button():
    #Region Fields
    sprite          = None
    #End Region
    #Region Constructors
    def __init__(self, sprite):
        self.sprite = sprite
        return
    #End Region
    #Region Methods
    #End Region