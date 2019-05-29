
from math import log

def exponenciacion_divide_y_venceras(n):
    """
    Utiliza el método divide y vencerás para indicar cómo elevar a la n, siendo 
    n un número natural.
    Devuelve una lista, donde cada elemento se corresponde con una 
    multiplicación.
    Las multiplicaciones se representan como tuplas de 3 elementos: el
    exponente del resultado y los exponentes de los dos elementos multiplicados,
    en orden decreciente.
    Las multiplicaciones tienen que estar en la lista en el orden en el que
    se realizarían.
    """
    lista=[]
    while n>1:
        lista1=()
        if(n%2==0):
            result=(n/2)
            lista1=(int(n),int(result),int(result))
            n=result
            lista.append(lista1)
        else:
            result=(n-1)
            lista1=(int(n),int(result),1)
            n=result
            lista.append(lista1)
    return list(reversed(lista))

def exponenciacion_iterativa(n):
    """
    Utiliza el método iterativo basado en la representación binaria del 
    exponente para indicar cómo elevar a la n, siendo n un número natural.
    Devuelve una lista, donde cada elemento se corresponde con una
    multiplicación.
    Las multiplicaciones se representan como tuplas de 3 elementos: el
    exponente del resultado y los exponentes de los dos elementos multiplicados,
    en orden decreciente.
    Las multiplicaciones tienen que estar en la lista en el orden en el que
    se realizarían.
    """
    r=0
    a=1
    lista=[]
    while n>=1:
        tupli=()
        if(n%2!=0):
            if(r+a==a):
                r=r+a
            else: 
                tupli=(a+r,a,r)
                lista.append(tupli)  
                r=r+a
            if n!=1:
                tupli=(a+a,a,a)
                lista.append(tupli)  
                a=a+a
        else:
            tupli=(a+a,a,a)
            lista.append(tupli)
            a=a+a
        n=int(n/2)    
    return lista      

def comprueba_multiplicaciones(n, multiplicaciones):
    """
    Comprueba si una lista de multiplicaciones calcula la pontencia a la n.
    Las multiplicaciones se expresan como tuplas de 3 elementos, con los
    exponentes del resultado y de los multiplicandos.
    """
    
    calculados = set([1])
    for m in multiplicaciones:
        if (m[1] not in calculados or m[2] not in calculados
            or m[0] != m[1] + m[2]):
            return False
        calculados.add(m[0])
    return m[0] == n

def cadena_multiplicaciones(multiplicaciones, base = "a"):
    """Devuelve una cadena con la representación de las multiplicaciones."""
    
    return '\n'.join(
        "{0}^{1} = {0}^{2} * {0}^{3}".format(base, *m)
        for m in multiplicaciones)

if __name__ == "__main__": 
    print(cadena_multiplicaciones([(2, 1, 1), (3, 2, 1), (6, 3, 3), (12, 6, 6), 
        (24, 12, 12), (25, 24, 1), (50, 25, 25), (100, 50, 50)])) 


def test_exponenciacion():
    """
    Tests para funciones que indican cómo elevar a un número natural
    utilizando multiplicaciones.
    """
    
    multiplicaciones = exponenciacion_divide_y_venceras(100)
                        
    assert multiplicaciones == [(2, 1, 1), (3, 2, 1), (6, 3, 3), (12, 6, 6), 
        (24, 12, 12), (25, 24, 1), (50, 25, 25), (100, 50, 50)]
    
    assert cadena_multiplicaciones(multiplicaciones) == ("""a^2 = a^1 * a^1
a^3 = a^2 * a^1
a^6 = a^3 * a^3
a^12 = a^6 * a^6
a^24 = a^12 * a^12
a^25 = a^24 * a^1
a^50 = a^25 * a^25
a^100 = a^50 * a^50""")
    
    multiplicaciones = exponenciacion_iterativa(100)
    
#    assert multiplicaciones == [(2, 1, 1), (4, 2, 2), (8, 4, 4), (16, 8, 8), 
#       (32, 16, 16), (36, 32, 4), (64, 32, 32), (100, 64, 36)]
    
    assert cadena_multiplicaciones(multiplicaciones) == ("""a^2 = a^1 * a^1
a^4 = a^2 * a^2
a^8 = a^4 * a^4
a^16 = a^8 * a^8
a^32 = a^16 * a^16
a^36 = a^32 * a^4
a^64 = a^32 * a^32
a^100 = a^64 * a^36""")
    
    for metodo_exponenciacion in (exponenciacion_divide_y_venceras, 
                                  exponenciacion_iterativa):

        for n in range(2,10000):
            multiplicaciones = metodo_exponenciacion(n)
            assert comprueba_multiplicaciones(n, multiplicaciones)
            assert len(multiplicaciones) <= 2 * log(n, 2)

if __name__ == "__main__": 
    test_exponenciacion()
    print("OK")