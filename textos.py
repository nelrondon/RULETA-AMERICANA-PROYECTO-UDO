import pygame

class Texto:
    def __init__(self, msg, display, color="black", fs=15, bld=False, pos=None):
        self.msg = msg
        self.pos = pos
        if bld:
            self.fuente = pygame.font.Font("fonts/GeneralSans-Semibold.ttf", fs)
        else:
            self.fuente = pygame.font.Font("fonts/GeneralSans-Regular.ttf", fs)
        self.color = color
        self.display = display
    
    def mostrar(self, pos:tuple):
        txt = self.fuente.render(self.msg, True, self.color)
        self.display.blit(txt, self.pos if self.pos != None else pos)

class CuadroTxt:
    def __init__(self, x, y, ancho, alto, texto, color=(200, 200, 200), fs=16, color_txt="black", label=""):
        self.pos = (x, y)
        self.txt = str(texto)
        self.memoria = []
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.fuente = pygame.font.Font("fonts/GeneralSans-SemiBold.ttf", fs)
        self.label = label

        self.color = color
        self.color_txt = color_txt

    def get(self):
        return int(self.txt)
    
    def mostrar(self, pantalla, text=None):
        pygame.draw.rect(pantalla, self.color, self.rect)
        if not text:
            self.txt = str(sum(self.memoria))
        else:
            self.txt = str(text)

        if self.label != "":
            mrglabel = 8
            label = Texto(self.label, pantalla, self.color_txt, 13, True)
            label.mostrar([x+mrglabel for x in self.pos])

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