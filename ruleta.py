import pygame

class Ruleta:
    def __init__(self):
        pygame.init()
        # CONSTANTES
        self.ACC = 0.8
        self.click = pygame.mixer.Sound("assets/click.wav")

        # VARIABLES
        self.vel = 0
        self.acc = self.ACC
        self.ang = 0
        self.posCas = 0

        # ESTADOS
        self.turn = False
        self.isStop = False
        self.isGetCasilla = False
        self.rondas = 0
        self.size = 360/38

        self.casillas = [
            (0,  "verde"),
            (28, "negro"), (9,  "rojo"), (26, "negro"), (30, "rojo"),
            (11, "negro"), (7,  "rojo"), (20, "negro"), (32, "rojo"),
            (17, "negro"), (5,  "rojo"), (22, "negro"), (34, "rojo"),
            (15, "negro"), (3,  "rojo"), (24, "negro"), (36, "rojo"),
            (13, "negro"), (1,  "rojo"), ( 0, "verde"), (27, "rojo"),
            (10, "negro"), (25, "rojo"), (29, "negro"), (12, "rojo"),
            (8,  "negro"), (19, "rojo"), (31, "negro"), (18, "rojo"),
            (6,  "negro"), (21, "rojo"), (33, "negro"), (16, "rojo"),
            (4,  "negro"), (23, "rojo"), (35, "negro"), (14, "rojo"),
            (2,  "negro")
        ]

    def show(self, imagen, flecha, display):
        posRuleta = (320, 290)
        ruletaRotada = pygame.transform.rotate(imagen, self.ang)
        cuadroRuleta = ruletaRotada.get_rect(center=posRuleta)
        display.blit(ruletaRotada, cuadroRuleta.topleft)
        posFlecha = (305, 40)
        display.blit(flecha, posFlecha)

    def move(self):
        if self.turn:
            if self.vel < 8:
                self.vel += self.acc
        else:
            pos = self.get_pos()
            #! DETERMINAMOS EL CAMBIO DE UNA CASILLA A OTRA
            if pos != self.posCas:
                self.posCas = pos
                if self.vel < 1.1:
                    self.click.play()

            if self.vel > 0.1:
                self.vel *= .98
            else:
                self.vel = 0
        
        self.isStop = (self.vel == 0)

        self.ang+=self.vel
        if self.ang >= 360:
            self.ang = 0

    def get_pos(self):
        pos = round(self.ang/self.size)
        pos = 0 if pos==38 else pos
        return pos

    def get_casilla(self):
        pos = self.get_pos()
        self.posCas = pos
        self.isGetCasilla = True
        return self.casillas[pos]