from constantes import *
from boton import Boton
from apuesta import Apuesta

def PanelCasillas(casillas:list[list[int, str]]):
    botonesCasillas = []
    x,y=0,0
    posCasillas = (650, 232)
    w,h,gap=40,36,5
    for btn in casillas:
        if btn != None:
            color = VERDE if btn[1]=="verde" else NEGRO if btn[1]=="negro" else ROJO
            botonesCasillas.append(
                Boton(
                    posCasillas[0]+(w+gap)*x,
                    posCasillas[1]-(h+gap)*y, 
                    w, h, btn[0], color, 17, "white", hover=False
                )
            )
        y+=1
        if y==3:
            x+=1
            y=0
    return botonesCasillas

def PanelApuestas():
    botonesApuesta = []
    posBotones = (650, 273)
    textBotones = ["1ERA DOCENA", "2DA DOCENA", "3ERA DOCENA", "1-18", "PAR", "ROJO", "NEGRO", "IMPAR", "19-36"]
    valueBotones = ["D1", "D2", "D3", "low", "even", "rojo", "negro", "odd", "high"]
    x,y=0,0
    w,h,gap=175,36,5
    for i in range(len(textBotones)):
        btn = textBotones[i]
        value = valueBotones[i]
        if y==0:
            botonesApuesta.append(Boton(
                posBotones[0]+(w+gap)*x,
                posBotones[1]+(h+gap)*y,
                w,h,btn, value=value))
        else:
            w = 85;
            color = ROJO if btn=="ROJO" else NEGRO if btn == "NEGRO" else GRIS
            color_txt = "black" if color == GRIS else "white"
            botonesApuesta.append(Boton(
                posBotones[0]+(w+gap)*x,
                posBotones[1]+(h+gap)*y,
                w,h,btn,color,color_txt=color_txt, value=value))
        x+=1
        if y==0:
            if x==3:
                y+=1
                x=0
        else:
            if x==6:
                y+=1
                x=0
    return botonesApuesta

def PanelMonto():
    botonesCantidad = []
    botones = [10, 100, 1000, 50, 500, 5000, "C", "DEL"]
    posBtn = (605, 531)
    x,y=0,0
    w,h,gapx, gapy=85,36,5, 5
    for btn in botones:
        color = GRIS
        if x==2:
            w = 40
            gapx = 50
            color = BLANCO
            if y==1:
                h = 77
                gapy = -36

        botonesCantidad.append(
            Boton(
                posBtn[0]+(w+gapx)*x,
                posBtn[1]+(h+gapy)*y,
                w, h, btn, color=color, fs=17
            )
        )

        y+=1
        if y==3:
            x+=1
            y=0
    return botonesCantidad

def crearApuesta(jugador, cant, type, opc):
    if not type:
        type = list(RELACIONES.keys())[len(opc)-1]
    elif type in ["D1", "D2", "D3", "C1", "C2", "C3"]:
        opc = type
        type = "dozen" if type[0]=="D" else "column"
    elif type in ["rojo", "negro"]:
        opc = type
        type = "color"
    return Apuesta(jugador, type, cant, opc)
