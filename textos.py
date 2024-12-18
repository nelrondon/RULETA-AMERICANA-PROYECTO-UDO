import pygame

class Texto:
    def __init__(self, msg, display, color="black", fs=15):
        self.msg = msg
        self.fuente = pygame.font.Font("fonts/GeneralSans-Regular.ttf", fs)
        self.color = color
        self.display = display
    
    def mostrar(self, pos):
        txt = self.fuente.render(self.msg, True, self.color)
        self.display.blit(txt, pos)

class CuadroTxt:
    def __init__(self, x, y, ancho, alto, texto, color=(200, 200, 200), fs=16, color_txt="black",):
        self.pos = (x, y)
        self.txt = str(texto)
        self.memoria = []
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.fuente = pygame.font.Font("fonts/GeneralSans-SemiBold.ttf", fs)

        self.color = color
        self.color_txt = color_txt
    
    def mostrar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        self.txt = str(sum(self.memoria))
        
        # Renderizar el texto
        texto_renderizado = self.fuente.render(self.txt, True, self.color_txt)
        pantalla.blit(texto_renderizado, 
                      (self.rect.x + (self.rect.width - texto_renderizado.get_width()) // 2,
                       self.rect.y + (self.rect.height - texto_renderizado.get_height()) // 2))
        
    def default(self):
        self.memoria = []
        self.txt = str(0)

    def pop_mem(self):
        if len(self.memoria)>0:
            self.memoria.pop()
    def add_mem(self, value):
        self.memoria.append(int(value))