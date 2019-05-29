
# Para dibujar las torres:

%matplotlib inline

import matplotlib.pyplot as plt


class Hanoi:
    """Clase para representar las torres de Hanoi."""
    movi=[]
    def __init__(self, discos):
        """
        El parámetro discos es un entero o una secuencia.
        Si es un entero se refiere al número de discos en el primer poste.
        Si es una secuencia, cada elemento indica en qué poste está el disco.
        Los postes se identifican como 1, 2 y 3.
        El primer elemento de la secuencia se refiere al disco más pequeño,
        el último al más grande.
        """
        self.movi=[]
        if isinstance(discos, int):
            discos = [1] * discos # todos los discos en el poste 1
        else:
            # comprobamos que los valores de la secuencia sean correctos
            assert all(1 <= d <= 3 for d in discos)

        self._discos = list(discos)

        # Almacenamos los postes como una lista de 3 listas
        self._postes = [[], [], []]
        i = len(discos)
        for d in discos[::-1]:
            self._postes[d - 1].append(i)
            i -= 1

    def __len__(self):
        """Devuelve el número de discos"""
        
        return len(self._discos)

    def mueve(self, origen, destino):
        """Mueve el disco superior del poste origen al poste destino."""
        
        assert 1 <= origen <= 3
        assert 1 <= destino <= 3

        poste_origen = self._postes[origen - 1]
        poste_destino = self._postes[destino - 1]
               
        assert len(poste_origen) > 0 # hay discos en el poste origen
        disco = poste_origen[-1]

        # comprobamos si podemos mover el disco:
        assert (len(poste_destino) == 0 # el destino está vacío
                or disco < poste_destino[-1]) # contiene un disco mayor

        # movemos:
        self._discos[disco - 1] = destino
        poste_origen.pop()
        poste_destino.append(disco)

    def __str__(self):
        return str(self._discos)

    def __repr__(self):
        return str(self)
    
    def realiza_movimientos(self, movimientos, imprime = False, dibuja = False):
        """
        Realiza varios movimientos, cada movimiento se indica como un par
        (origen, destino).
        """
        
        if imprime:
            self.imprime()
        if dibuja:
            self.dibuja()
        for origen, destino in movimientos:
            self.mueve(origen, destino)
            if imprime:
                print("\n", origen, "->", destino, sep="")
                self.imprime()
            if dibuja:
                self.dibuja()

    def imprime(self):        
        """Imprime una representación gráfica de las torres"""

        n = len(self)
        for nivel in range(len(self) - 1, -1, -1):
            for poste in self._postes:
                if nivel >= len(poste):
                    print("|", " " * (n - 1), sep="", end=" ")
                else:
                    disco = poste[nivel]
                    print("X" * disco, " " * (n - disco), sep="", end=" ")
            print()
        for poste in self._postes:
            print("=" * n, sep=" ", end=" ")
        print()
        
    def dibuja(self):
        axs = []
        f, axs = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(3,1))
        n = len(self)
        for a, p in zip(axs, self._postes):
            a.set_aspect(1)
            a.axis('off')
            p = p + [0] * (n - len(p))
            left = [(n - x) / 2 for x in p]
            a.barh(range(n), p, height=1, left=left)
        plt.tight_layout()
        plt.show()
        
            
    def hanoipuro(self,n,origen,destino,aux):
        #print(self._postes)
        if n>=0:
            #print("origen, destino, aux", origen, destino, aux)
            yield from self.hanoipuro(n - 1, origen, aux, destino)
            try:
            #print(origen,destino)
                self.mueve(origen,destino)
                yield origen, destino
            except AssertionError:
                pass
            yield from self.hanoipuro(n - 1, aux, destino, origen)
            
    def dameorigen(self,destino):
        mini=0
        pos=0
        cont=1
        aux=0
        for i in self._postes:
            if cont!=destino:
                for j in i:
                    if mini<j:
                        mini=j
                        pos=cont
            cont+=1
            
        for i in range(1,len(self._postes)+1):
            #print("hola",i)
            if i is not pos and i is not destino:
                aux=i
        return pos,aux
    
    def resuelve(self, destino=3):
        """
        Resuelve el problema, moviendo todos los discos al poste destino,
        partiendo de cualquier configuración inicial.

        Devuelve una secuencia con los movimientos, cada movimiento es un par
        (origen, destino).
        """
        aux=0
        pos=0
        
        n=len(self)
        pos,aux=self.dameorigen(destino)
        self.movi=list(self.hanoipuro(n,pos,destino,aux))
        #self.easy()
        
        return self.movi
               
    # 3 discos en el poste 1, mover al poste 3
    h = Hanoi(3)
    movimientos = h.resuelve()
    print(str(h))
    assert str(h) == "[3, 3, 3]"
    h = Hanoi(3)
    h.realiza_movimientos(movimientos, imprime=True)
    h = Hanoi(3)
    h.realiza_movimientos(movimientos, dibuja=True)
    assert str(h) == "[3, 3, 3]"

    # 7 discos en el poste 1, mover al poste 2
    h = Hanoi(7)
    movimientos = h.resuelve(2)
    assert str(h) == str([2] * 7)
    h = Hanoi(7)
    h.realiza_movimientos(movimientos)
    assert str(h) == str([2] * 7)

    # 3 discos repartidos en los 3 postes
    h = Hanoi([1, 3, 2])
    movimientos = h.resuelve()
    assert str(h) == str([3] * 3)
    h = Hanoi([1, 3, 2])
    h.realiza_movimientos(movimientos)
    assert str(h) == str([3] * 3)  
    
    # 6 discos repartidos en los 3 postes
    h = Hanoi([2, 3, 3, 1, 1, 2])
    movimientos = h.resuelve()
    assert str(h) == str([3] * 6)
    h = Hanoi([2, 3, 3, 1, 1, 2])
    h.realiza_movimientos(movimientos)
    assert str(h) == str([3] * 6)        

    # 9 discos repartidos en los 3 postes
    h = Hanoi([2, 3, 3, 1, 1, 2, 3, 1, 2])
    movimientos = h.resuelve()
    assert str(h) == str([3] * 9)
    h = Hanoi([2, 3, 3, 1, 1, 2, 3, 1, 2])
    h.realiza_movimientos(movimientos)
    assert str(h) == str([3] * 9) 

    
if __name__ == "__main__": 
    test_hanoi()
    print("OK")