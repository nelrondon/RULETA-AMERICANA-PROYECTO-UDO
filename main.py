import pygame
from constantes import *
from ruleta import Ruleta
from boton import *
from textos import *
from apuesta import ListaApuestas
from jugador import Jugador
from utils import *

#? INICIALIZAMOS LAS CLASES QUE USAREMOS
jugador = Jugador(1000)
ruleta = Ruleta()
apuestas = ListaApuestas()

#? CONFIGURAMOS LA INTERFAZ PYGAME
pygame.init()

pantalla = pygame.display.set_mode((1280, 720))
reloj = pygame.time.Clock()
juego = True
pygame.display.set_caption("RULETA (AMERICANA) - CASINO")

#? ESTADOS DE PANTALLA 
# juego, portada, instrucciones
displayState = "portada"

#? CARGAMOS LA FUENTE A USAR & LA IMAGEN Y SONIDO DE LA RULETA
fuente = pygame.font.Font("fonts/GeneralSans-SemiBold.ttf", 15)
flecha = pygame.image.load("assets/flecha.png").convert_alpha()
imagen = pygame.image.load("assets/ruleta.png").convert_alpha()
spin_up = pygame.mixer.Sound("assets/spin_up.wav")
spin_down = pygame.mixer.Sound("assets/spin_down.wav")

fondo = pygame.image.load("assets/fondo.png").convert()
instr = pygame.image.load("assets/instrucciones.png").convert()
portada = pygame.image.load("assets/portada.png").convert()

#? MUSICA DE FONDO
pygame.mixer.music.load("assets/casino.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

#? TEXTOS (TITULOS)
titulo1 = Texto("PANEL APUESTA", pantalla, "white", 40, True)

#? BOTON DE GIRO Y APUESTA
btn_giro = Boton(210, 602, 220, 45, "GIRAR / PARAR", type="bool")
btn_apuesta = Boton(920, 378, 220, 45, "APOSTAR")

#? BOTONES DE LAS CASILLAS
botonesCasillas = ListaBotonesSelect(6)
botonesCasillas.add(Boton(605, 150, 40, 57, "00", VERDE, 17, "white", False, type="btn"))
botonesCasillas.add(Boton(605, 212, 40, 57, "0", VERDE, 17, "white", False, type="btn"))
botonesCasillas.add(PanelCasillas(CASILLAS))

#? BOTONES DE ACCION (TIPOS DE APUESTA)
botonesApuesta = ListaBotonesOpcion()
botonesApuesta.add(Boton(1190, 150, 40, 36, "x2", value="C3"))
botonesApuesta.add(Boton(1190, 191, 40, 36, "x2", value="C2"))
botonesApuesta.add(Boton(1190, 232, 40, 36, "x2", value="C1"))
botonesApuesta.add(PanelApuestas())

#? BOTONES DE SUMA DE CANTIDAD DE DINERO
botonesCantidad = ListaBotones()
botonesCantidad.add(PanelMonto())

#? CUADRO DE TEXTO
cuadroDinero = CuadroTxt(605, 367, 220, 77, 0, NEGRO, 20, "white", label="TU DINERO:")
cuadroMonto = CuadroTxt(605, 449, 220, 77, 0, BLANCO, 20, label="MONTO APUESTA:")

log = []
selected = []

#? CUARDRO DE REGISTROD DE APUESTAS 
label = Texto("APUESTAS ACTIVAS: 10", pantalla, bld=True)
rect = pygame.rect.Rect(830, 450, 400, 200)

#? AREAS DE CLICK EN PORTADA E INSTRUCCIONES
areaJugar = pygame.Rect(590, 625, 172, 63)
areaPortada = pygame.Rect(28, 20, 151, 58)
areaSalir = pygame.Rect(795, 633, 133, 51)
areaIntruc = pygame.Rect(310, 634, 252, 50)
areaVolver = pygame.Rect(74, 49, 118, 42)

def handleBtnGiro():
    if len(apuestas) != 0:
        ruleta.turn = ruleta.isStop
        ruleta.isGetCasilla = False
        btn_giro.value = ruleta.isStop
        if ruleta.isStop:
            ruleta.rondas += 1
        
        if ruleta.turn and ruleta.isStop:
            spin_up.play(loops=-1)
        else:
            spin_down.play()
            spin_up.stop()

def handleBtnApostar():
    betAmount = cuadroMonto.get()
    betType = botonesApuesta.get_opcion()
    selected = botonesCasillas.get_selects()
    if betAmount and (betType or selected):
        if len(apuestas) == 0:
            log.clear()
        if len(log) < 8:
            cuadroMonto.default()
            botonesApuesta.default()
            botonesCasillas.default()
            apuesta = crearApuesta(jugador, betAmount, betType, selected)
            apuestas.add(apuesta)
            log.append(Texto(
                str(apuesta),
                pantalla, bld=True
            ))

#? BUCLE DEL JUEGO
while juego:
    for event in pygame.event.get():
        #? EVENTOS GENERALES (MOUSE, TECLADO, ETC...)
        if event.type == pygame.QUIT:
            juego = False

        if displayState == "juego":
            if event.type == pygame.MOUSEBUTTONUP:
                if areaPortada.collidepoint(event.pos):
                    displayState = "portada"
            #? EVENTO DE BOTONES (DINERO)
            for btn in botonesCantidad.get():
                if btn.isClick(event):
                    if btn.value == "DEL":
                        cuadroMonto.pop_mem()
                    elif btn.value == "C":
                        cuadroMonto.default()
                    else:
                        cuadroMonto.add_mem(btn.value)
            
            #? EVENTO DE LOS BOTONES DE CASILLA
            if botonesCasillas.isClick(event):
                botonesApuesta.default()

            #? EVENTO DE CLICK EN LOS BOTONES DE APUESTA
            if botonesApuesta.isClick(event):
                botonesCasillas.default()

            #? EVENTO DE CLICK EN EL BOTON DE GIRAR/PARAR
            if btn_giro.isClick(event):
                handleBtnGiro()

            #? EVENTO DE CLICK EN EL BOTON APOSTAR
            if btn_apuesta.isClick(event):
                handleBtnApostar()

        if displayState == "portada":
            if event.type == pygame.MOUSEBUTTONUP:
                if areaJugar.collidepoint(event.pos):
                    displayState = "juego"
                if areaSalir.collidepoint(event.pos):
                    # AÑADE LA LOGICA PARA SALIR
                    pass
                if areaIntruc.collidepoint(event.pos):
                    displayState = "instrucciones"

        if displayState == "instrucciones":
            if event.type == pygame.MOUSEBUTTONUP:
                if areaVolver.collidepoint(event.pos):
                    displayState = "portada"
        
    if displayState == "portada":
        pantalla.blit(portada, (0, 0))

    if displayState == "instrucciones":
        pantalla.blit(instr, (0, 0))

    if displayState == "juego":
        #? FONDO DE PANTALLA
        pantalla.blit(fondo, (0, 0))

        #? MOSTRAR RULETA
        ruleta.show(imagen, flecha, pantalla)

        #? MOVIMIENTO DE LA RULETA
        ruleta.move()

        #? CONTROLADOR PARA CUANDO LA RULETA SE DETIENE
        if ruleta.isStop and ruleta.rondas != 0 and len(apuestas) > 0 and not ruleta.isGetCasilla:
            result = ruleta.get_casilla()
            for i in range(len(apuestas.apuestas)):
                apuesta = apuestas[i]
                if not apuesta.pagada:
                    apuesta.pagarApuesta(result)
                    color = VERDE if apuesta.isWin else ROJO
                    log[i].color = color
            apuestas.clear()

        #! RENDERIZADO RECTANGULO
        pygame.draw.rect(pantalla, "white", rect)
        label.msg = f"APUESTAS ACTIVAS: {len(apuestas)}"
        label.mostrar((845, 461))

        #! RENDERIZADO DE TITULOS
        titulo1.mostrar((756, 65))

        #! RENDERIZADO DEL CUADRO DE MONTO-APUESTA Y DINERO DE JUGADOR
        cuadroMonto.mostrar(pantalla)
        cuadroDinero.mostrar(pantalla, jugador.dinero)
        
        #! RENDERIZADO DE BOTON DE GIRO/APOSTAR
        btn_giro.dibujar(pantalla)
        btn_apuesta.dibujar(pantalla)

        #! RENDERIZADO DE BOTONES (CANTIDAD)
        botonesCantidad.dibujar(pantalla)
        #! RENDERIZADO DE BOTONES (APUESTAS)
        botonesApuesta.dibujar(pantalla)
        #! RENDERIZADO DE BOTONES (CASILLA)
        botonesCasillas.dibujar(pantalla)

        #! RENDERIZADO DE REGISTRO DE APUESTAS
        gap, x = 18, 0
        for l in log:
            l.mostrar((845, 482+(gap*x)))
            x+=1

    

    #? ACTUALIZACION DE LA PANTALLA
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
