from jugador import Jugador

class Apuesta:
    def __init__(self, jugador : Jugador , tipo, cantidad, opciones=None):
        self.jugador = jugador
        self.tipo = tipo
        self.opciones = [opciones]
        self.cantidad = cantidad
        self.pagada = False
        jugador.dinero -= cantidad

    def verificar_g(self, result):
        if result[0] != 0:
            if self.tipo == "color":
                return result[1] in self.opciones
            elif self.tipo == "par":
                return result[0]%2==0
            elif self.tipo == "impar":
                return not result[0]%2==0
            elif self.tipo == "bajo":
                return 1 <= result[0] <= 18
            elif self.tipo == "alto":
                return 19 <= result[0] <= 38
            else:
                return result[0] in self.opciones
        
    def pagar(self):
        pago = 0
        if self.tipo == 'pleno':
            pago = 35 * self.cantidad
        elif self.tipo == 'dividida':
            pago = 17 * self.cantidad
        elif self.tipo == 'calle':
            pago = 11 * self.cantidad
        elif self.tipo == 'esquina':
            pago = 8 * self.cantidad
        elif self.tipo == 'seisena':
            pago = 5 * self.cantidad
        elif self.tipo in ["color", 'par', 'impar', 'alto', 'bajo']:
            pago = 2 * self.cantidad
        elif self.tipo == 'docena':
            pago = 2 * self.cantidad
        elif self.tipo == 'columna':
            pago = 2 * self.cantidad
        self.jugador.dinero += pago
        self.pagada = True
        return pago
    
class ListaApuestas:
    def __init__(self, apuestas=[]):
        self.apuestas:list[Apuesta] = apuestas
    
    def add(self, newBets: list[Apuesta] | Apuesta):
        if type(newBets) == list[Apuesta]:
            for bet in newBets:
                self.add(bet)
        elif type(newBets) == Apuesta:
            self.apuestas.append(newBets)

