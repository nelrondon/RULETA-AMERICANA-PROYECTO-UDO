from jugador import Jugador
from constantes import COMBOS, RELACIONES

class Apuesta:
    def __init__(self, jugador : Jugador , tipo, cantidad, opciones=None):
        self.jugador = jugador
        self.tipo = tipo
        self.opciones = opciones
        self.cantidad = cantidad
        self.pagada = False

        self.pago = 0
        self.isWin = False
        jugador.dinero -= cantidad

    def pagarApuesta(self, result:list[int, str]):
        gano = False
        if result[0] != 0:
            if self.tipo == "column" or self.tipo == "dozen":
                self.opciones = COMBOS[self.opciones]

            if self.tipo == "color":
                gano = result[1] in self.opciones
            elif self.tipo == "even":
                gano = result[0]%2==0
            elif self.tipo == "odd":
                gano = not result[0]%2==0
            elif self.tipo == "low":
                gano = 1 <= result[0] <= 18
            elif self.tipo == "high":
                gano = 19 <= result[0] <= 38
            else:
                if type(self.opciones) == int:
                    gano = result[0] == self.opciones
                else:
                    gano = result[0] in self.opciones

        pago = 0
        if gano:
            for tipo, mult in RELACIONES.items():
                if self.tipo == tipo:
                    pago = mult*self.cantidad
        self.jugador.dinero += pago
        self.pagada = True
        self.isWin = gano
        self.pago = pago
    
    def __str__(self):
        terminos = {
            "C1": "1era Columna",
            "C2": "2da Columna",
            "C3": "3era Columna",
            "D1": "1era Docena",
            "D2": "2da Docena",
            "D3": "3ra Docena",
            "odd": "impares",
            "even": "pares",
            "high": "19 al 36",
            "low": "1 al 18",
        }
        if self.tipo == "dozen" or self.tipo == "column":
            return f"Apostaste {self.cantidad}, a la {terminos[self.opciones]}."
        if self.tipo == "color":
            return f"Apostaste {self.cantidad}, al {self.opciones}."
        if self.tipo == "even" or self.tipo == "odd":
            return f"Apostaste {self.cantidad}, a los {terminos[self.tipo]}."
        if self.tipo == "high" or self.tipo == "low":
            return f"Apostaste {self.cantidad}, por los numeros del {terminos[self.tipo]}."
        else:
            n = list(RELACIONES.keys()).index(self.tipo)+1
            if n == 1:
                return f"Apostaste {self.cantidad}, al {self.opciones}"
            else:
                return f"Apostaste {self.cantidad}, a {n} numeros {self.opciones}"

    
class ListaApuestas:
    def __init__(self, apuestas=[]):
        self.apuestas:list[Apuesta] = apuestas
    
    def add(self, newBets: list[Apuesta] | Apuesta):
        if type(newBets) == list[Apuesta]:
            for bet in newBets:
                self.add(bet)
        elif type(newBets) == Apuesta:
            self.apuestas.append(newBets)

    def __getitem__(self, i):
        return self.apuestas[i]

    def clear(self):
        self.apuestas.clear()

    def __len__(self):
        return len(self.apuestas)

# player = Jugador(3000)
# apuesta = Apuesta(player, "street", 2000, [2,3,5,6])

# print(apuesta)
# print(apuesta.pagarApuesta((6, "rojo")))
