class Apuesta:
    def __init__(self, jugador, tipo, cantidad, opciones=None):
        jugador.dinero -= cantidad
        self.tipo = tipo
        self.opciones = [opciones]
        self.cantidad = cantidad
        self.pagada = False

    def verificar_g(self, result):
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
        
    def pagar(self, jugador, pago):
        jugador.dinero += pago
    
    def calcular_pago(self):
        if self.tipo == 'pleno':
            return 35 * self.cantidad
        elif self.tipo == 'dividida':
            return 17 * self.cantidad
        elif self.tipo == 'calle':
            return 11 * self.cantidad
        elif self.tipo == 'esquina':
            return 8 * self.cantidad
        elif self.tipo == 'seisena':
            return 5 * self.cantidad
        elif self.tipo in ["color", 'par', 'impar', 'alto', 'bajo']:
            return 2 * self.cantidad
        elif self.tipo == 'docena':
            return 2 * self.cantidad
        elif self.tipo == 'columna':
            return 2 * self.cantidad
        return 0