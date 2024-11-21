import pygame
from constantes import *
from ruleta import Ruleta
from boton import *
from textos import *
from apuesta import Apuesta
from personaje import Personaje

#? INICIALIZAMOS LAS CLASES QUE USAREMOS
jugador = Personaje(1000)
ruleta = Ruleta()
apuestas = [
    Apuesta(jugador,"pleno", 300, 5),
    Apuesta(jugador,"pleno", 300, 6),
    Apuesta(jugador,"color", 100,  "rojo")
]

#? CONFIGURAMOS LA INTERFAZ PYGAME
pygame.init()
pantalla = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
juego = True
pygame.display.set_caption("RULETA (AMERICANA) - CASINO")

#? CARGAMOS LA FUENTE A USAR & LA IMAGEN DE LA RULETA
fuente = pygame.font.Font("fonts/GeneralSans-SemiBold.ttf", 15)
flecha = pygame.image.load("assets/flecha.png").convert_alpha()
imagen = pygame.image.load("assets/ruleta.png").convert_alpha()

#? BOTON DE GIRO
btn_giro = Boton(799, 433, 175, 36, "GIRAR / PARAR", type="bool")

#? BOTONES DE LAS CASILLAS
casillas = [
    (1, "rojo"), (2, "negro"), (3, "rojo"), (4, "negro"),
    (5, "rojo"), (6, "negro"), (7, "rojo"), (8, "negro"),
    (9, "rojo"), (10, "negro"), (11, "negro"), (12, "rojo"),
    (13, "negro"), (14, "rojo"), (15, "negro"), (16, "rojo"),
    (17, "negro"), (18, "rojo"), (19, "rojo"), (20, "negro"),
    (21, "rojo"), (22, "negro"), (23, "rojo"), (24, "negro"),
    (25, "rojo"), (26, "negro"), (27, "rojo"), (28, "negro"),
    (29, "negro"), (30, "rojo"), (31, "negro"), (32, "rojo"),
    (33, "negro"), (34, "rojo"), (35, "negro"), (36, "rojo")
]

btn_casilla = ListaBotonesSelect()
x,y=0,0
w,h,gap=40,36,5
for btn in casillas:
    color = VERDE if btn[1]=="verde" else NEGRO if btn[1]=="negro" else ROJO
    btn_casilla.add(Boton(529+(w+gap)*x, 310+(h+gap)*y, w, h, btn[0], color, 18, "white", hover=False))
    x+=1
    if x==10:
        y+=1
        x=0

#? BOTONES DE ACCION (TIPOS DE APUESTA)
btn_apuesta = ListaBotonesOpcion()
t_apuesta = ["PLENO", "DIVIDIDA", "CALLE", "SEISENA", "DOCENA", "PAR", "IMPAR", "ALTO", "BAJO", "APOSTAR"]
x,y=0,0
w,h,gap=85,36,5
for btn in t_apuesta:
    btn_apuesta.add(Boton(529+(w+gap)*x, 220+(h+gap)*y, w, h, btn))
    x+=1
    if x==5:
        y+=1
        x=0

#? BOTONES DE SUMA DE CANTIDAD DE DINERO
btn_cant = ListaBotones()
x,y=0,0
w,h,gap=40,36,5
t_cantidad = [10, 100, 1000, 50, 500, "DEL"]
for btn in t_cantidad:
    btn_cant.add(Boton(844+(w+gap)*x, 130+(h+gap)*y, w, h, btn))
    x+=1
    if x==3:
        y+=1
        x=0
btn_cant.botones[5].color_normal = NEGRO
btn_cant.botones[5].color_texto = "white"

#? CUADRO DE TEXTO
cuadrotxt = CuadroTxt(844, 89, 130, 36, 0, VERDE, 20, "white")

rondas = 0
log = []
opcion = None
selected = []

#? BUCLE DEL JUEGO
while juego:
    #? COLOR DE FONDO DE PANTALLA
    pantalla.fill(FONDO)

    #? CUADRADO DE LOG
    rect = pygame.rect.Rect(529, 45, 305, 162)
    pygame.draw.rect(pantalla, NEGRO, rect)

    #? MOSTRAR RULETA
    ruleta.show(imagen, pantalla)

    #? MOVIMIENTO DE LA RULETA
    ruleta.move()

    print(ruleta.isStop())

    #? CONTROLADOR PARA CUANDO LA RULETA SE DETIENE
    if ruleta.isStop() and rondas > 0 and len(apuestas)>0:
        result = ruleta.get_casilla()
        for apuesta in apuestas:
            if not apuesta.pagada:
                fs = 15
                if apuesta.verificar_g(result) and not result[0] == 0:
                    pago = apuesta.calcular_pago()
                    log.append(Texto(f"+ {pago} fichas, por apuesta tipo {apuesta.tipo}", pantalla, VERDE, fs))
                    apuesta.pagar(jugador, pago)
                else:
                    log.append(Texto(f"\tPerdiste la apuesta tipo {apuesta.tipo}", pantalla, ROJO, fs))
                apuesta.pagada = True

    #! RENDERIZAMOS LA FLECHA QUE DETERMINA LA CASILLA GANADORA
    pantalla.blit(flecha, (235, 0))

    #? INICIALIZAMOS LOS TEXTOS
    textos = [
        fuente.render(f"Angulo: {ruleta.ang:.2f}", True, "white"),
        fuente.render(f"Velocidad: {ruleta.vel:.2f}", True, "white"),
        fuente.render(f"Aceleración: {ruleta.acc}", True, "white"),
        fuente.render(f"Dinero: {jugador.dinero}", True, "white")
    ]

    #! RENDERIZADO DE TEXTOS DEL REGISTRO
    y = 50
    for t in range(len(log)):
        log[t].mostrar((529, y+(t*15)))

    #! RENDERIZADO DE TEXTOS DE PRUEBA (ANGULO,VELOCIDAD,ACELERACION)
    x = 10 ; y = 10
    for t in range(len(textos)):
        pantalla.blit(textos[t], (x,y+(t*16)))

    #! RENDERIZADO DEL CUADRO DE TEXTO
    cuadrotxt.mostrar(pantalla)
    
    #! RENDERIZADO DE BOTON DE GIRO
    btn_giro.dibujar(pantalla)

    #! RENDERIZADO DE BOTONES (CANTIDAD)
    btn_cant.dibujar(pantalla)
    #! RENDERIZADO DE BOTONES (APUESTAS)
    btn_apuesta.dibujar(pantalla)
    #! RENDERIZADO DE BOTONES (CASILLA)
    btn_casilla.dibujar(pantalla)

    #? ACTUALIZACION DE LA PANTALLA
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False

        #? EVENTO DE BOTONES (DINERO)
        for btn in btn_cant.get():
            if btn.isclick(event):
                if btn.value == "DEL":
                    cuadrotxt.pop_mem()
                else:
                    cuadrotxt.add_mem(btn.value)
        
        #? EVENTO DE LOS BOTONES DE CASILLA
        for btn in btn_casilla.get():
            if btn.isclick(event):
                pass

        #? EVENTO DE CLICK EN LOS BOTONES DE APUESTA
        for btn in btn_apuesta.get():
            if btn.isclick(event):
                if btn.value == "APOSTAR":
                    selected = btn_casilla.get_selects()
                    #? CONVIERTO LOS VALORES DE SELECT A ENTEROS
                    selected = [int(x) for x in selected]
                    if (not opcion == None) and len(selected)>0 and int(cuadrotxt.txt)>0:
                        #? AGREGAR APUESTA
                        print(f"{opcion} -> {selected} -> {cuadrotxt.txt}")
                        #? DESPUES DE AGREGAR APUESTA - VALORES POR DEFECTO
                        opcion = None
                        btn_casilla.default()
                        btn_apuesta.default()
                        cuadrotxt.default()
                else:
                    id_btn = btn_apuesta.get().index(btn)
                    opcion = btn_apuesta.opcion(id_btn)

        #? EVENTO DE CLICK EN EL BOTON DE GIRAR/PARAR
        if btn_giro.isclick(event):
            btn_giro.value = ruleta.isStop()
            ruleta.turn = ruleta.isStop()

            if ruleta.isStop():
                rondas+=1
            else:
                pass

            print(btn_giro.value)


pygame.quit()
