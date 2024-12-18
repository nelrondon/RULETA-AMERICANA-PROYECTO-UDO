import pygame
from constantes import *
from ruleta import Ruleta
from boton import *
from textos import *
from apuesta import Apuesta, ListaApuestas
from jugador import Jugador

#? INICIALIZAMOS LAS CLASES QUE USAREMOS
jugador = Jugador(1000)
ruleta = Ruleta()
apuestas = ListaApuestas([
    Apuesta(jugador,"pleno", 300, 5),
    Apuesta(jugador,"pleno", 300, 6),
    Apuesta(jugador,"color", 100,  "rojo")
])

#? CONFIGURAMOS LA INTERFAZ PYGAME
pygame.init()

pantalla = pygame.display.set_mode((1280, 720))
reloj = pygame.time.Clock()
juego = True
pygame.display.set_caption("RULETA (AMERICANA) - CASINO")

#? CARGAMOS LA FUENTE A USAR & LA IMAGEN DE LA RULETA
fuente = pygame.font.Font("fonts/GeneralSans-SemiBold.ttf", 15)
flecha = pygame.image.load("assets/flecha.png").convert_alpha()
imagen = pygame.image.load("assets/ruleta.png").convert_alpha()

#? BOTON DE GIRO
btn_giro = Boton(799, 433, 175, 36, "GIRAR / PARAR", type="bool")

#? BOTONES DE LAS CASILLAS

botonesCasillas = ListaBotonesSelect()

x,y=0,0
posCasillas = (98, 530)
w,h,gap=40,36,5
for btn in CASILLAS:
    if btn != None:
        color = VERDE if btn[1]=="verde" else NEGRO if btn[1]=="negro" else ROJO
        botonesCasillas.add(
            Boton(
                posCasillas[0]+(w+gap)*x,
                posCasillas[1]+(h+gap)*y, 
                w, h, btn[0], color, 18, "white", hover=False
            )
        )
    x+=1
    if x==10:
        y+=1
        x=0

#? BOTONES DE ACCION (TIPOS DE APUESTA)
botonesApuesta = ListaBotonesOpcion()
textBotones = ["PLENO", "DIVIDIDA", "CALLE", "SEISENA", "DOCENA", "PAR", "IMPAR", "ALTO", "BAJO", "APOSTAR"]
x,y=0,0
w,h,gap=85,36,5
for btn in textBotones:
    botonesApuesta.add(Boton(529+(w+gap)*x, 220+(h+gap)*y, w, h, btn))
    x+=1
    if x==5:
        y+=1
        x=0

#? BOTONES DE SUMA DE CANTIDAD DE DINERO
botonesCantidad = ListaBotones()
x,y=0,0
w,h,gap=40,36,5
t_cantidad = [10, 100, 1000, 50, 500, "DEL"]
for btn in t_cantidad:
    botonesCantidad.add(Boton(844+(w+gap)*x, 130+(h+gap)*y, w, h, btn))
    x+=1
    if x==3:
        y+=1
        x=0
botonesCantidad.botones[5].color_normal = NEGRO
botonesCantidad.botones[5].color_texto = "white"

#? CUADRO DE TEXTO
cuadroMonto = CuadroTxt(844, 89, 130, 36, 0, VERDE, 20, "white")
log = []
opcion = None
selected = []

def handleBtnGiro():
    ruleta.turn = ruleta.isStop
    ruleta.isGetCasilla = False
    log.clear()
    btn_giro.value = ruleta.isStop
    if ruleta.isStop:
        ruleta.rondas += 1


#? BUCLE DEL JUEGO
while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False

        #? EVENTO DE BOTONES (DINERO)
        for btn in botonesCantidad.get():
            if btn.isClick(event):
                if btn.value == "DEL":
                    cuadroMonto.pop_mem()
                else:
                    cuadroMonto.add_mem(btn.value)
        
        #? EVENTO DE LOS BOTONES DE CASILLA
        for btn in botonesCasillas.get():
            if btn.isClick(event):
                pass

        #? EVENTO DE CLICK EN LOS BOTONES DE APUESTA
        for btn in botonesApuesta.get():
            if btn.isClick(event):
                if btn.value == "APOSTAR":
                    selected = botonesCasillas.get_selects()

                    #? CONVIERTO LOS VALORES DE SELECT A ENTEROS
                    selected = [int(x) for x in selected]
                    if (not opcion == None) and len(selected)>0 and int(cuadroMonto.txt)>0:
                        
                        #? AGREGAR APUESTA
                        print(f"{opcion} -> {selected} -> {cuadroMonto.txt}")
                        
                        #? DESPUES DE AGREGAR APUESTA - VALORES POR DEFECTO
                        opcion = None
                        botonesCasillas.default()
                        botonesApuesta.default()
                        cuadroMonto.default()
                else:
                    id_btn = botonesApuesta.get().index(btn)
                    opcion = botonesApuesta.get_opcion(id_btn)

        #? EVENTO DE CLICK EN EL BOTON DE GIRAR/PARAR
        if btn_giro.isClick(event):
            handleBtnGiro()
            

    #? COLOR DE FONDO DE PANTALLA
    pantalla.fill(FONDO)
    pygame.draw.rect(pantalla, NEGRO, (640, 0, 640, 720))

    #? CUADRADO DE LOG
    rect = pygame.rect.Rect(529, 45, 305, 162)
    pygame.draw.rect(pantalla, "white", rect)

    #? MOSTRAR RULETA
    ruleta.show(imagen, flecha, pantalla)

    #? MOVIMIENTO DE LA RULETA
    ruleta.move()

    #todo CONTROLADOR PARA CUANDO LA RULETA SE DETIENE
    if ruleta.isStop and ruleta.rondas != 0 and len(apuestas) > 0 and not ruleta.isGetCasilla:
        result = ruleta.get_casilla()
        print(result)
        for apuesta in apuestas:
            if not apuesta.pagada:
                if apuesta.verificar_g(result):
                    pago = apuesta.pagar()
                    log.append(Texto(f"+ {pago} fichas, por apuesta tipo {apuesta.tipo}", pantalla, VERDE))
                else:
                    log.append(Texto(f"\tPerdiste la apuesta tipo {apuesta.tipo}", pantalla, ROJO))

    #? INICIALIZAMOS LOS TEXTOS
    txtPruebas = [
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
    for t in range(len(txtPruebas)):
        pantalla.blit(txtPruebas[t], (x,y+(t*16)))

    #! RENDERIZADO DEL CUADRO DE TEXTO
    cuadroMonto.mostrar(pantalla)
    
    #! RENDERIZADO DE BOTON DE GIRO
    btn_giro.dibujar(pantalla)

    #! RENDERIZADO DE BOTONES (CANTIDAD)
    botonesCantidad.dibujar(pantalla)
    #! RENDERIZADO DE BOTONES (APUESTAS)
    botonesApuesta.dibujar(pantalla)
    #! RENDERIZADO DE BOTONES (CASILLA)
    botonesCasillas.dibujar(pantalla)

    #? ACTUALIZACION DE LA PANTALLA
    pygame.display.flip()
    reloj.tick(60)

    

pygame.quit()
