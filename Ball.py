from PPlay.gameimage import *
from random import randint
import math

# Classe base da bola
class Ball:
    #Region Fields
    janela      = None
    ball        = None
    min_vel_x   = 300
    min_vel_y   = 300
    velocity_x  = 0
    velocity_y  = 0
    modifier    = -1.05
    min_delta   = 0
    max_delta   = 0.5
    angulo_15   = math.pi / 12
    #End Region
    #Region Constructors
    def __init__(self, janela):
        self.janela                 = janela
        self.ball                   = GameImage("Assets/bola.png")
        self.set_start_pos()
        return
    #End Region
    #Region Methods
    def set_start_pos(self):
        self.ball.x, self.ball.y = (self.janela.width * 0.5) - (self.ball.width * 0.5), (self.janela.height * 0.5) - (self.ball.height * 0.5)
        f_x, f_y = self.set_angulo_inicial()
        self.velocity_x = self.min_vel_x * f_x
        self.velocity_y = self.min_vel_y * f_y
        #self.velocity_x = self.min_vel_x
        #self.velocity_y = self.min_vel_y
        return 
    def processar(self, other1, other2):

        self.mover()
        self.mudar_rapidez_por_contato_parede()
        self.mudar_rapidez_por_contato_pad(other1, other2)
        return

    def mover(self):
        delta = self.janela.delta_time()
        if delta <= self.min_delta or delta >= self.max_delta: return
        self.ball.x += self.velocity_x * delta
        self.ball.y += self.velocity_y * delta
        return
    
    def mudar_rapidez_por_contato_parede(self):
        if self.ball.y <= 0.0:
            self.ball.y      = 0.0
            self.velocity_y *= self.modifier
        if self.ball.y >= self.janela.height - self.ball.height:
            self.ball.y     = self.janela.height - self.ball.height
            self.velocity_y *= self.modifier
        return
    
    def mudar_rapidez_por_contato_pad(self, other1, other2):
        delta = self.janela.delta_time()
        if delta <= self.min_delta or delta >= self.max_delta: return
        if self.ball.collided_perfect(other1):
            self.ball.x     = other1.x + other1.width
            self.velocity_x *= self.modifier
            return
        if self.ball.collided_perfect(other2):
            self.ball.x     = other2.x - self.ball.width
            self.velocity_x *= self.modifier
            return
        return
    
    def emitir_pontuacao(self):
        if self.ball.x <= 0:
            self.set_start_pos()
            return 2
        elif self.ball.x >= self.janela.width + self.ball.width:
            self.set_start_pos()
            return 1
        return 0
    
    def set_angulo_inicial(self):
        from random import random
        rd_ponto = random()
        rd      = randint(1, 4)
        #print("angulo: %d"%rd)
        x       = math.cos(float(self.angulo_15 * rd * rd_ponto))
        y       = math.sin(float(self.angulo_15 * rd * rd_ponto))
        #print("sen: %f | cos: %f"%(x, y))
        rd      = randint(0, 100)
        x  *= -1 if rd < 50 else 1
        rd      = randint(0,100)
        y  *= -1 if rd < 50 else 1
        
        return x, y
    
    def direcao_bola(self):
        return self.velocity_y > 0
    #End Region