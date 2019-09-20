#
#Processa todos os inputs da aplicação
#

from PPlay.keyboard import *

kb = Keyboard()

def process():
    if kb.key_pressed("esc"):
        print("Esc")
    return

def TeclaDeSairPressionada():
    return kb.key_pressed("esc")