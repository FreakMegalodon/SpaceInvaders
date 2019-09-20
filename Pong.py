#Todo: mover draw_text para dsman

from    PPlay.window    import *
from    PPlay.gameimage import *
from    PPlay.sprite    import *
from    PPlay.mouse     import *
import  InputMan        as inman
import  UpdateMan       as upman
import  DisplayMan      as dsman
from    GameManager     import *
#from    Player          import *
#from    Ball            import *

def testar_mouse(xi, yi, xf, yf):
    ms = janela.get_mouse()
    if ms.is_over_area([xi, yi], [xf, yf]) and  ms.is_button_pressed(1):
        print("!")
    return


janela        = dsman.iniciarJanela(0, 0, "")
isPlaying     = True
#game_manager  = GameManager(1)
bg            = GameImage("Assets/bg.png")
menu_jogar = GameImage("Assets/jogar.png")
menu_dif = GameImage("Assets/dif.png")
menu_rank = GameImage("Assets/rank.png")
menu_sair = GameImage("Assets/sair.png")
#player1_      = Player(janela, 1)
#player2_      = Player(janela, 2)
#ball_         = Ball(janela)
#gameImages    = [bg, ball_.ball, player1_.player, player2_.player]
gameImages    = [bg, menu_jogar, menu_dif, menu_rank, menu_sair]
#mouse.Mouse.hide(self=Mouse)  
#janela.draw_text("Sample", 10, 10, size=12, color=(0,0,0), font_name="Arial", bold=False, italic=False)
h = janela.width / 10
while isPlaying:
    menu_jogar.x = janela.width / 2 - menu_jogar.width / 2
    menu_jogar.y = h
    menu_dif.x = janela.width / 2 - menu_dif.width / 2
    menu_dif.y = 20 + h * 2
    menu_rank.x = janela.width / 2 - menu_rank.width / 2
    menu_rank.y = 20 + h * 3
    menu_sair.x = janela.width / 2 - menu_sair.width / 2
    menu_sair.y = 20 + h * 4
    testar_mouse(menu_jogar.x, menu_jogar.y, menu_jogar.x + menu_jogar.width, menu_jogar.y + menu_jogar.height)
    #gm = False
    #if not game_manager.game_over():
    #    player1_.move()
    #    player2_.move_ia(ball_.direcao_bola())
    #    ball_.processar(player1_.player, player2_.player)
    #else:
    #    gm = True
    #game_manager.controlar_placar(ball_.emitir_pontuacao())
    #inman.process()
    #upman.process()
    dsman.drawStack(gameImages)
    #janela.draw_text(str(game_manager.pontos_1), 10, 10, size=40, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
    #janela.draw_text(str(game_manager.pontos_2), janela.width - 40, janela.height - 50, size=40, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
    #if gm:
    #    janela.draw_text("Game Over", (janela.width / 2), (janela.height / 2), size=50, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
    dsman.render(janela)
    isPlaying = not inman.TeclaDeSairPressionada()