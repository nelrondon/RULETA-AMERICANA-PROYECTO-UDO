import pygame

class Ruleta:
    def __init__(self):
        # CONSTANTES
        self.ACC = 0.08

        # VARIABLES
        self.vel = 0
        self.acc = self.ACC
        self.ang = 0

        # ESTADOS
        self.turn = False
        self.stop = False

        self.casillas = [
            (0, "verde"),
            (28, "negro"), (9, "rojo"), (26, "negro"), (30, "rojo"),
            (11, "negro"), (7, "rojo"), (20, "negro"), (32, "rojo"),
            (17, "negro"), (5, "rojo"), (22, "negro"), (34, "rojo"),
            (15, "negro"), (3, "rojo"), (24, "negro"), (36, "rojo"),
            (13, "negro"), (1, "rojo"), (0, "verde"), (27, "rojo"),
            (10, "negro"), (25, "rojo"), (29, "negro"), (12, "rojo"),
            (8, "negro"), (19, "rojo"), (31, "negro"), (18, "rojo"),
            (6, "negro"), (21, "rojo"), (33, "negro"), (16, "rojo"),
            (4, "negro"), (23, "rojo"), (35, "negro"), (14, "rojo"),
            (2, "negro")
        ]

    def show(self, imagen, display):
        imagen_rota = pygame.transform.rotate(imagen, self.ang)
        rect_rota = imagen_rota.get_rect(center=(250,250))
        display.blit(imagen_rota, rect_rota.topleft)

    def isStop(self):
        return self.stop

    def move(self):
        keys = pygame.key.get_pressed()

        if self.vel<10:
            self.vel+=self.acc        
        self.ang+=self.vel

        if self.ang >= 360:
            self.ang = 0

        if not self.turn:
            self.vel *= .98
            if self.vel<.1:
                self.vel = 0

        self.acc = self.ACC if self.turn else 0
        self.stop = True if self.vel == 0 else False

        if keys[pygame.K_DOWN] and self.turn:
            self.turn = False
        if keys[pygame.K_UP] and not self.turn:
            self.turn = True

    def get_casilla(self):
        ang_c = (360 / 38)
        pos = int(((self.ang+(ang_c/2)) % 360) / ang_c)
        return self.casillas[pos]