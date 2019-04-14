from math import log

class RecurrenciaMaestra: 
    """
    Clase que representa una recurrencia de las que se consideran en el 
    teorema maestro, de la forma T(n)=aT(n/b)+n^k. Se interpreta que en n/b
    la división es entera.
    Además de los métodos que aparecen a continuación, tienen que funcionar 
    los siguientes operadores: 
        ==, !=,
        str(): la representación como cadena debe ser 'aT(n/b)+n^k'
        []: el parámetro entre corchetes es el valor de n para calcular T(n).
    """
    cont=0
    def __eq__(self,oper):
        result=False
        if(self.a==oper.a and self.b==oper.b and self.k==oper.k ):
            result=True
        return result
        
        
    def __ne__(self,oper):
        return not self==oper
    
    
    def __str__(self):
        return str(self.a)+'T(n/'+str(self.b)+')+n^'+str(self.k)
        
        
    def __getitem__(self,indice):
        
        if not 0==indice:
            
            return int(self.a*self[int(indice/self.b)]+pow(indice,self.k))
        else:
                
                return self.inicial
    
    def __init__(self, a, b, k, inicial = 0):
        """
        Constructor de la clase, los parámetros a, b, y k son los que
        aparecen en la fórmula aT(n/b)+n^k. El parámetro inicial es el valor
        para T(0).
        """
        self.a=a
        self.b=b
        self.k=k
        self.inicial=inicial

        
    def metodo_maestro(self):
        """
        Devuelve una cadena con el tiempo de la recurrencia de acuerdo al 
        método maestro. La salida está en el formato "O(n^x)" o "O(n^x*log(n))",
        siendo x un número.
        """
        result=''
        if self.a < pow(self.b,self.k):
            result='O(n^'+str(self.k)+')'
        
        if self.a == pow(self.b,self.k):
            result='O(n^'+str(self.k)+'*log(n))'
        
        if self.a > pow(self.b,self.k):
             result='O(n^'+str(log(self.a,self.b))+')'
                
        return result
        
       
    def __iter__(self):
        """
        Generador de valores de la recurrencia: T(0), T(1), T(2), T(3)..., 
        indefinidamente.
        Aunque sea una recurrencia, los valores *no* deben calcularse 
        recursivamente.
        """
        self.cont=0
        return self
        
    
    def __next__(self):
        result=0
        while True:
            if self.cont==0 and self.k==0:
                result=int(self.a*self[int(self.cont/self.b)]+0)            
            else:
                result=int(self.a*self[int(self.cont/self.b)]+pow(self.cont,self.k))

            self.cont+=1
            return result

def test_recurrencia_maestra_operadores(): 
    """Casos de prueba para los operadores de RecurrenciaMaestra."""
    r1 = RecurrenciaMaestra(2, 2, 2)
    
    # Tests para los operadores == y !=
    assert r1 == RecurrenciaMaestra(2, 2, 2)
    assert not r1 != RecurrenciaMaestra(2, 2, 2)
    for a, b, k in ((1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1) ):
        assert r1 != RecurrenciaMaestra(a, b, k)
        assert not r1 == RecurrenciaMaestra(a, b, k)

    # Tests para str()
    assert str(r1) == "2T(n/2)+n^2"
    assert str(RecurrenciaMaestra(7, 4, 3)) == "7T(n/4)+n^3"
    
    # Tests para []
    for n, valor in enumerate((0, 1, 6, 11, 28, 37, 58, 71, 120, 137, 174, 195, 
                               260, 285, 338, 367, 496, 529, 598, 635)):
        assert r1[n] == valor
        
    r2 = RecurrenciaMaestra(1, 2, 0, 1) 
    for n, valor in enumerate((1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 
                               6, 6, 6, 6)):
        assert r2[n] == valor 
               
    r3 = RecurrenciaMaestra(4, 3, 1)
    for n, valor in enumerate((0, 1, 2, 7, 8, 9, 14, 15, 16, 37, 38, 39, 44, 45,
                               46, 51, 52, 53, 74, 75)):
        assert r3[n] == valor  
    hola=pow(x,2)


if __name__ == "__main__":
    x=2
    test_recurrencia_maestra_operadores()
    print("OK")  