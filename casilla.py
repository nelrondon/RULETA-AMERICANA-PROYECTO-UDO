casilla = [0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, "00", 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2]

def determinar_casilla(a):

    casilla = list(map(lambda x: (x, "rojo" if casilla.index(x)%2==0 else "negro"), casilla))

    casilla[0] = (0, "verde")
    casilla[19] = (0, "verde")

    pos = int(round((a%360)/(360/38)))

    return casilla[pos]

print(casilla.index(0))