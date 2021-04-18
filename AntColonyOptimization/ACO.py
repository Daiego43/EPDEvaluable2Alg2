"""
Problema 2
Se pide implementar un algoritmo de ACO para el problema de la mochila, siguiendo las directrices
generales descritas en las clases de EB. Suponga que se dispone de N objetos y que cada uno de ellos tiene asociado
un peso (p) y un beneficio (b). El problema consiste en encontrar el subconjunto de objetos de valor máximo que
cumpla la restricción de que la suma de sus pesos sea menor o igual que una cota C prefijada (la capacidad de la
mochila). Parametrice el problema con 100 objetos con pesos y beneficios comprendidos entre 1 y 100,
y con una capacidad máxima de 3000.
"""
import random as r
from functools import reduce
import time as t
import numpy as np


class Hormiga:
    def __init__(self, ident):
        self.id = ident
        self.value = 0
        self.mochila = []
        self.pesomochila = 0

    def resetHormiga(self):
        self.mochila = []
        self.value = 0
        self.pesomochila = 0

    def take_object(self, id_Objeto: int, peso_Objeto: int):
        self.mochila.append(id_Objeto)
        self.pesomochila += peso_Objeto

    def setValue(self, value):
        self.value = value

    def str(self):
        return "Hormiga " + str(self.id) + ": " + str(self.mochila) + "--> valor: " + str(self.value) + "  peso: " + str(self.pesomochila)


def chooseObject(probabilidades, objetos):
    probsyobj = list(zip(probabilidades, objetos))
    # Ordeno los objetos y sus probabilidades segun la probabilidad
    probsyobj.sort()
    # Y ahora puedo separar esos dos vectores
    i = 0
    for unit in probsyobj:
        probabilidades[i] = unit[0]
        objetos[i] = unit[1]
        i += 1
    # Tengo los mismos vectores de probabilidad y objetos pero ambos ordenados por la probabilidad de transicion
    # Puedo calcular la suma acumulativa de las probabilidades
    probabilidades_acumulativas = []
    sumador = lambda x, y: x + y
    for i in range(len(probabilidades)):
        probabilidades_acumulativas.append(reduce(sumador, probabilidades[i:]))
    # FINALMENTE PUEDO GENERAR UN NUMERO ALEATORIO Y VER SI ESTA EN UN INTERVALO
    floataleatorio = r.uniform(0, 1)
    i = 0
    found = False
    while i in range(len(probabilidades_acumulativas) - 1) and not found:
        if probabilidades_acumulativas[i] >= floataleatorio > probabilidades_acumulativas[i + 1]:
            eleccion = objetos[i]
            found = True
        i += 1
    if probabilidades_acumulativas[-1] >= floataleatorio > 0:
        eleccion = objetos[-1]

    return eleccion


class AntColonyOptimization:
    NUM_OBJETOS = 100
    RANGO_PESOS = 100
    RANGO_BENEFICIOS = 100
    MAX_PESO_MOCHILA = 3000
    NUM_ITER = 10
    NUM_HORMIGAS = 5

    ALPHA = 0.5  # Parametro para denotar la importancia del rastro en la p_transicion
    BETA = 0.8  # Parametro para denotar la importancia de la información heurística en la p_transicion
    Q = 500  # Cantidad de rastro dejado por una hormiga
    p = 0.5  # Porcentaje de eliminación de feromona

    def inicializa_Objetos(self):
        """
        Inicializa un diccionario de objetos para meter en la mochila
        La KEY para acceder a los datos de un objeto es un numero de 0 a NUM_OBJETOS
        El VALUE para cada KEY es una tupla de la forma (PESO, BENEFICIO)
        :return:
        """
        dictObjetos = {}
        for i in range(self.NUM_OBJETOS):
            dictObjetos.update({i: (r.randint(1, self.RANGO_PESOS), r.randint(1, self.RANGO_BENEFICIOS))})
        return dictObjetos

    def inicializar_Rastros(self):
        """
        Inicializa una lista de rastros de tamaño NUM_OBJETOS
        Los rastros iniciales son todos iguales a TAU_o
        :return:
        """
        lista_rastros = []
        for i in range(self.NUM_OBJETOS):
            lista_rastros.append(self.Q)
        return lista_rastros

    def prepararHormigas(self):
        """
        Resetea la lista de hormigas de los anteriores valores tomados
        :return:
        """
        for ant in self.listaHormigas:
            ant.resetHormiga()

    def moverHormigas(self):
        """
        Este método situa las hormigas en un objeto aleatorio para que metan el mismo
        en su mochila y desde ahí comiencen a recorrer y meter objetos en sus respectivas mochilas
        :return:
        """
        for ant in self.listaHormigas:
            objeto_inicial = r.randint(0, self.NUM_OBJETOS - 1)
            ant.take_object(objeto_inicial, self.dictObjetos[objeto_inicial][0])
            puedeCoger = True
            while puedeCoger:
                puedeCoger = self.wander_around(ant)

    def wander_around(self, ant: Hormiga):
        """
        Cuando una hormiga "explora" primero evalua qué objetos puede coger
        en funcion del peso que ya lleva. La lista compuesta por dichos objetos es posibles_visitas.
        Luego aplica la probabilidad de transición a todos los posibles objetos
        Finalmente escoge 1 y lo guarda en su mochila.
        La funcion devuelve un booleano indicando si la hormiga puede o no puede coger objetos
        :return:
        """
        posibles_visitas = []
        # Primero determinamos que objeto puede coger la hormiga
        for objeto in self.dictObjetos:
            if (ant.pesomochila + self.dictObjetos[objeto][0]) < self.MAX_PESO_MOCHILA and objeto not in ant.mochila:
                posibles_visitas.append(objeto)
        # Si puede coger objetos determinaremos cual mediante la probabilidad de transicion
        if len(posibles_visitas) != 0:
            # Este sumatorio es para no hacerlo constantemente al calcular la probabilidad de transicion de todos los
            # objetos posibles
            suma = 0
            for i in posibles_visitas:
                tau = self.rastros[i] ** self.ALPHA
                n = self.dictObjetos[i][1] ** self.BETA
                suma += tau * n

            # Calculamos la probabilidad de transicion para las posibles visitas
            probabilidades = []
            for objeto in posibles_visitas:
                probabilidades.append(self.probabilidad_de_transicion(objeto, suma))

            # Con las probabilidades calculadas y los objetos obtenidos se elige el objeto y se le da a la hormiga
            objeto_elegido = chooseObject(probabilidades, posibles_visitas)
            ant.take_object(objeto_elegido, self.dictObjetos[objeto_elegido][0])
            return True
        else:
            return False

    def probabilidad_de_transicion(self, objeto, suma):
        tau = self.rastros[objeto] ** self.ALPHA
        n = self.dictObjetos[objeto][1] ** self.BETA
        res = tau * n / suma
        return res

    def actualizarRastros(self):
        """
        Para cada objeto se va a actualizar el rastro en función
        del valor total recopilado por la hormiga
        :return:
        """
        for i in range(len(self.rastros)):
            self.rastros[i] = (1 - self.p) * self.rastros[i] + self.hormigasQuePasanPor(i)

    def hormigasQuePasanPor(self, objeto):
        sumaValueHormigas = 0
        for ant in self.listaHormigas:
            if objeto in ant.mochila:
                sumaValueHormigas += self.Q / ant.value
        return sumaValueHormigas

    def ACOSolveVisual(self):
        """
        Metodo principal para resolver el problema de la mochila mediante
        el algoritmo de ACO
        :return:
        """
        self.prepararHormigas()
        self.rastros = self.inicializar_Rastros()
        iter = 0
        mejorValor = 0
        bestKnapsack = []
        while iter < self.NUM_ITER:
            self.moverHormigas()
            self.updValues()
            self.printHormigas()
            self.actualizarRastros()
            bestAnt = self.bestValue()
            if bestAnt.value > mejorValor:
                mejorValor = bestAnt.value
                bestKnapsack = bestAnt.mochila
                print("\nEl mejor valor se ha actualizado")
            self.prepararHormigas()
            iter += 1
            print("\n")
        print("Mejor valor encontrado", mejorValor, "\nMochila:", bestKnapsack)
        return mejorValor

    def ACOSolve(self):
        """
        Metodo principal para resolver el problema de la mochila mediante
        el algoritmo de ACO
        :return:
        """
        self.prepararHormigas()
        self.rastros = self.inicializar_Rastros()
        iter = 0
        mejorValor = 0
        while iter < self.NUM_ITER:
            self.moverHormigas()
            self.updValues()
            self.actualizarRastros()
            bestAnt = self.bestValue()
            if bestAnt.value > mejorValor:
                mejorValor = bestAnt.value
                bestKnapsack = bestAnt.mochila
            self.prepararHormigas()
            iter += 1
        return mejorValor

    def bestValue(self):
        maxv = 0
        for ant in self.listaHormigas:
            if ant.value > maxv:
                maxv = ant.value
                bestAnt = ant
        return bestAnt

    def updValues(self):
        for ant in self.listaHormigas:
            ant.value = sum(list(map(lambda x: self.dictObjetos[x][1], ant.mochila)))

    def inicializarListaHormigas(self):
        listaHormigas = []
        for i in range(self.NUM_HORMIGAS):
            listaHormigas.append(Hormiga(i))
        return listaHormigas

    def printHormigas(self):
        for ant in self.listaHormigas:
            print(str(ant.str()))

    def tiempo_medio_ejecucion(self):
        lista_tiempos = []
        lista_mejores_valores = []
        for i in range(30):
            to = t.time()
            lista_mejores_valores.append(self.ACOSolve())
            tf = t.time() - to
            lista_tiempos.append(tf)
        media = np.mean(lista_tiempos)
        mejor = max(lista_mejores_valores)
        return media, mejor

    def __init__(self, numHormigas=5, numObjetos=10, pesoMax=300):
        self.MAX_PESO_MOCHILA = pesoMax
        self.NUM_HORMIGAS = numHormigas
        self.NUM_OBJETOS = numObjetos
        self.dictObjetos = self.inicializa_Objetos()
        self.listaHormigas = self.inicializarListaHormigas()
        self.rastros = self.inicializar_Rastros()


    def printProblemDetails(self):
        print("\t\t\t\tProblema de la Mochila. Algoritmo ACO. Parámetros")
        print("Numero de objetos:", self.NUM_OBJETOS)
        print("Rango de valores:", self.RANGO_BENEFICIOS)
        print("Rango de pesos:", self.RANGO_BENEFICIOS)
        print("Peso máximo de la mochila:", self.MAX_PESO_MOCHILA)
        print("Numero de hormigas utilizadas:", self.NUM_HORMIGAS)
        print("Alpha:", self.ALPHA)
        print("Beta:", self.BETA)
        print("Cantidad de feromona dejada por una hormiga:", self.Q)
        print("Porcentaje de eliminacion de feromona", str(int(self.p * 100)) + "%")
        print("Objetos:", self.dictObjetos)



