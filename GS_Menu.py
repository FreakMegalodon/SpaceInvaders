#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils as dsman
from enum import Enum
from PPlay.gameimage import *
from PPlay.keyboard import *
from PPlay.mouse import *
from GameStates import *

#End Region

class SubMenus(Enum):
    NewGame         = 1
    MainMenu        = 2
    Dificuldades    = 4
    Rankings        = 8
    Exit            = 512

class GS_Menu():
    #Region Fields
    janela          = None
    mouse           = None
    teclado         = None
    game_images     = []
    menu_buttons    = dict()
    #End Region
    #Region Constructors
    def __init__(self, janela):
        self.janela     = janela
        self.mouse      = janela.get_mouse()
        self.teclado    = self.janela.get_keyboard()
        self.mouse      = self.janela.get_mouse()
        self.set_menu_images()
        self.set_menu_buttons()
        return
    #End Region
    #Region Methods
    def on_state_enter(self):
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        self.get_mouse_click()
        return

    def update(self):
        return

    def render(self):
        dsman.drawStack(self.game_images)
        self.janela.update()
        return
    
    def set_menu_images(self):
        bg     = GameImage("Assets/bg.png")
        logo   = GameImage("Assets/logo.png")
        logo.x = (self.janela.width / 2) - (logo. width / 2)
        logo.y = 25.0
        self.game_images.append(bg)
        self.game_images.append(logo)
        return 
    
    def set_menu_buttons(self):
        x_tela = self.janela.width * 0.5
        self.menu_buttons[SubMenus.NewGame]         = GameImage("Assets/images/Btn_01.png")
        self.menu_buttons[SubMenus.Dificuldades]    = GameImage("Assets/images/Btn_03.png")
        self.menu_buttons[SubMenus.Rankings]        = GameImage("Assets/images/Btn_05.png")
        self.menu_buttons[SubMenus.Exit]            = GameImage("Assets/images/Btn_07.png")
        self.menu_buttons[SubMenus.NewGame].set_position(x_tela - self.menu_buttons[SubMenus.NewGame].width * 0.5, 300)
        self.menu_buttons[SubMenus.Dificuldades].set_position(x_tela - self.menu_buttons[SubMenus.Dificuldades].width * 0.5, 400)
        self.menu_buttons[SubMenus.Rankings].set_position(x_tela - self.menu_buttons[SubMenus.Rankings].width * 0.5, 500)
        self.menu_buttons[SubMenus.Exit].set_position(x_tela - self.menu_buttons[SubMenus.Exit].width * 0.5, 600)
        self.game_images.append(self.menu_buttons[SubMenus.NewGame])
        self.game_images.append(self.menu_buttons[SubMenus.Dificuldades])
        self.game_images.append(self.menu_buttons[SubMenus.Rankings])
        self.game_images.append(self.menu_buttons[SubMenus.Exit])
        #self.ship.set_position(x_tela - self.ship.width * 0.5, self.janela.height - 300)
        return

    def get_mouse_click(self):
        x_min, x_max = self.menu_buttons[SubMenus.NewGame].x, self.menu_buttons[SubMenus.NewGame].x + self.menu_buttons[SubMenus.NewGame].width
        y_min, y_max = self.menu_buttons[SubMenus.NewGame].y, self.menu_buttons[SubMenus.NewGame].y + self.menu_buttons[SubMenus.NewGame].height
        if (x_min <= self.mouse.get_position()[0] <= x_max) and (y_min <= self.mouse.get_position()[1] <= y_max):
            if self.mouse.is_button_pressed(1):
                return GameStates.Game_Running


        #self.mouse.get_position()[1]
        return

def move(self):
        #player1.y = max(0, min(mouse.Mouse.get_position(self=Mouse)[1], janela.height - player1.height))
        if self.teclado.key_pressed("LEFT"):   self.player.y = max(0, min(self.ship.x - (self.velocity * self.janela.delta_time()), self.janela.height - self.player.height))
        if self.teclado.key_pressed("RIGHT"): self.player.y = max(0, min(self.player.y + (self.velocity * self.janela.delta_time()), self.janela.height - self.player.height))
        return    #End Region