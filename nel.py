import pygame

from boton import *

# Inicializar pygame
pygame.init()


# Configuración de la ventana
ancho = alto = 400
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Botón con Pygame")

# Colores
blanco = (255, 255, 255)
gris_claro = (200, 200, 200)
gris_oscuro = (100, 100, 100)

# Fuente del texto
fuente = pygame.font.Font(None, 36)

x, y = 10, 4
size = 30
gap = 5
e=20
botones = []
btn = Boton(20, 200, 100, 30, "DEL")
for j in range(y):
    for i in range(x):
        px, py = (size*i)+(gap*i)+e, (size*j)+(gap*j)+e
        num = (i+1)+(x*j)
        botones.append(Boton(px, py, size, size, str(num), type="selection"))

suma = []
texto = 0
run = True
# Loop principal
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        for boton in botones:
            if boton.isclick(event):
                suma.append(int(boton.texto))
                print(boton.value)
        if btn.isclick(event):
            if len(suma)>0:
                suma.pop()  

    texto = sum(suma)
    pantalla.fill(blanco)

    cuadro = fuente.render(str(texto), True, "black")
    pantalla.blit(cuadro, (200, 200))

    for boton in botones:
        boton.dibujar(pantalla)
    btn.dibujar(pantalla)

    pygame.display.flip()

pygame.quit()