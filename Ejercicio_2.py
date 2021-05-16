import threading
import random
import logging
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)


class ListaFinita(list):

    def __init__(self, max_elementos):
        self.max_elementos = max_elementos
        super().__init__()

    def pop(self, index):
        assert len(self) != 0, "lista vacía"
        return super().pop(index)

    def append(self, item):
        assert len(self) < self.max_elementos, "lista llena"
        super().append(item)

    def insert(self, index, item):
        assert index < self.max_elementos, "índice inválido"
        super().insert(index, item)

    def full(self):
        return len(self) == self.max_elementos

    def isEmpty(self):
        return len(self) == 0


class Productor(threading.Thread):
    listaPaises = [("España", "Madrid"), ("Francia", "París"), ("Italia", "Roma"), ("Inglaterra", "Londres"),
                   ("Alemania", "Berlín"), ("Rusia", "Moscú"), ("Turquía", "Istambul"), ("China", "Pekín"),
                   ("Japón", "Tokio"), ("Emiratos Árabes", "Dubai"), ("Argentina", "Buenos Aires"),
                   ("Brasil", "Brasilia"), ("Colombia", "Bogotá"),
                   ("Uruguay", "Montevideo"), ]

    def __init__(self, lista):
        super().__init__()
        self.lista = lista
        self.lockProductor = threading.Lock()

    def run(self):
        while True:
            self.lockProductor.acquire()
            try:
                while self.lista.full():
                    pass
                paisAlAzar = random.randint(0, len(self.listaPaises) - 1)
                self.lista.append(self.listaPaises[paisAlAzar])
                logging.info(f'produjo el item: {self.lista[-1]}')
                time.sleep(random.randint(1, 5))
            finally:
                self.lockProductor.release()


class Consumidor(threading.Thread):
    def __init__(self, lista):
        super().__init__()
        self.lista = lista
        self.lockConsumidor = threading.Lock()

    def run(self):
        while True:
            self.lockConsumidor.acquire()
            try:
                while self.lista.isEmpty():
                    pass
                elemento = self.lista.pop(0)
                logging.info(f'La capital de {elemento[0]} es {elemento[1]}')
                time.sleep(random.randint(1, 5))
            finally:
                self.lockConsumidor.release()


def main():
    hilos = []
    lista = ListaFinita(4)

    for i in range(4):
        productor = Productor(lista)
        consumidor = Consumidor(lista)
        hilos.append(productor)
        hilos.append(consumidor)

        logging.info(f'Arrancando productor {productor.name}')
        productor.start()

        logging.info(f'Arrancando productor {consumidor.name}')
        consumidor.start()

    for h in hilos:
        h.join()


if __name__ == '__main__':
    main()
