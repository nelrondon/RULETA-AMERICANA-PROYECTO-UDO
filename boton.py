import pygame
from constantes import *

# Clase Boton
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color=GRIS, fs=16, color_txt="black", hover=True, value=None, type=None):
        # ATRIBUTOS ESCENCIALES
        self.texto = str(texto)
        if type=="bool":
            self.value = False if value==None else True
        else:
            self.value = texto if value==None else value

        # RENDERIZADO
        self.pos = (x,y)
        bd = 2
        self.rect = pygame.Rect(x+bd, y+bd, ancho-bd*2, alto-bd*2)
        self.borde = pygame.Rect(x, y, ancho, alto)
        self.fuente = pygame.font.Font("fonts/GeneralSans-SemiBold.ttf", fs)

        # COLORES
        self.color_texto = color_txt
        self.color_normal = GRIS if color==None else color
        ajustar_brillo = lambda clr, factor: tuple(min(255, int(c * factor)) for c in clr)
        self.color_hover = ajustar_brillo(self.color_normal, 0.7)

        # ESTADOS
        self.type = type
        self.canHover = hover
        self.select = False
        


    def dibujar(self, pantalla:pygame.Surface):
        # Cambiar color si el mouse está sobre el botón
        mouse_pos = pygame.mouse.get_pos()
        color_actual = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_normal

        color_borde = color_actual if self.canHover else self.color_normal

        if not self.canHover:
            color_actual = self.color_normal
        
        if self.select:
            color_actual = self.color_hover
            color_borde = (79, 128, 255)
    
        pygame.draw.rect(pantalla, color_borde, self.borde)
        pygame.draw.rect(pantalla, color_actual, self.rect)
        
        # Renderizar el texto
        texto_renderizado = self.fuente.render(self.texto, True, self.color_texto)
        pantalla.blit(texto_renderizado, 
                      (self.rect.x + (self.rect.width - texto_renderizado.get_width()) // 2,
                       self.rect.y + (self.rect.height - texto_renderizado.get_height()) // 2))
    
    def isClick(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class ListaBotones: 
    def __init__(self, type=None):
        self.type = type
        self.botones:list[Boton] = []

    def __len__(self):
        return len(self.botones)

    def __getitem__(self, indice):
        return self.botones[indice]

    def get(self):
        return self.botones
    
    def add(self, btn:Boton):
        if type(btn) == list:
            for b in btn:
                self.add(b)
        else:
            if not self.type==None:
                if btn.type != "btn":
                    btn.type = self.type
            self.botones.append(btn)
    
    def dibujar(self, pantalla):
        for b in self.botones:
            b.dibujar(pantalla)

    def default(self):
        pass

class ListaBotonesSelect(ListaBotones):
    def __init__(self, maxSelected=0):
        super().__init__("selection")
        self.maxSelect = maxSelected
        self.selectes = 0

    def get_selects(self):
        sel = []
        for b in self.botones:
            if b.select:
                sel.append(b.value)
        return sel
    
    def countSelected(self):
        self.selectes = len(list(filter(lambda btn: btn.select, self.botones)))
        return self.selectes

    def isClick(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for btn in self.botones:
                if btn.borde.collidepoint(event.pos):
                    self.countSelected()
                    if not self.maxSelect or self.selectes < self.maxSelect:
                        btn.select = not btn.select
                    else:
                        btn.select = False
                    self.countSelected()
                    return True
    
    def default(self):
        for btn in self.botones:
            btn.select = False


    
class ListaBotonesOpcion(ListaBotones):
    def __init__(self):
        super().__init__("opcion")
        self.__opcion = ""
        self.canSelect = True

    def get_opcion(self):
        return self.__opcion

    def isClick(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.canSelect:
            for btn in self.botones:
                if btn.borde.collidepoint(event.pos):
                    if btn.select:
                        btn.select = False
                        self.__opcion = ""

                    else:
                        self.default()
                        btn.select = True
                        self.__opcion = str(btn.value)
                    return True

    def default(self):
        self.__opcion = ""
        for btn in self.botones:
            btn.select = False