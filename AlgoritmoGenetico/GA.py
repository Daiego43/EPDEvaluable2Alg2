"""
Problema 1
Se dispone de una balanza con dos platillos y de n objetos, cada uno de los cuales tiene un peso positivo. El
objetivo es encontrar un reparto de los objetos entre los dos platillos de la balanza de forma que la diferencia
entre los pesos de los objetos situados en cada platillo sea mínima.
"""
import random as r
import time as t
import numpy as np


class GeneticAlgorithm:
    TAM_POBLACION = 20  # Tamaño elegido para la población
    ELITE_PCT = 50      # Porcentaje de elitismo escogido
    NUM_OBJETOS = 10  # Numero de objetos a situar en los platillos de la balanza
    RANGO_PESOS = 100   # Rango maximo de peso de los objetos a colocar
    MUTATION_PCT = 10   # Probabilidad de aparicion de una mutacion tras realizar un cruce
    NUM_ITER = 30       # Numero de iteraciones como condicion de parada

    def generateObjectDict(self):
        """
        Inicializa un diccionario con keys de 0 a NUM_OBJETOS
        para cada key existe un value aleatorio dentro del rango [1, RANGO_PESOS]
        :return: objetos: dict
        """
        objetos = {}
        for i in range(self.NUM_OBJETOS):
            objetos.update({i: r.randint(1, self.RANGO_PESOS)})
        return objetos

    def generateRandomIndividual(self):
        """
        Genera una solucion aleatoria del problema, todas las pesas deben estar colocadas en un lado
        u otro de la balanza.
        Las soluciones son de la forma [0,1,0,0,...1] -> un array de NUM_OBJETOS
        Si es 0 quiere decir que el objeto está en el platillo izquierdo
        Si es 1 quiere decir que el objeto está en el platillo derecho
        Los valores de cada objeto se pueden consultar gracias al diccionario que se crea con la funcion
        'generateObjectDict()'
        :return: individuo: list
        """
        individuo = []
        for i in range(self.NUM_OBJETOS):
            individuo.append(r.randint(0, 1))
        return individuo

    def fitness(self, solucion):
        """
        Devuelve la diferencia en valor absoluto de los objetos en los platillos de
        la balanza
        :param solucion: list
        :return: fitness: int
        """
        platilloleft = 0
        platilloright = 0
        for i in range(len(solucion)):
            if solucion[i] == 0:
                platilloleft += self.dictObjetos[i]
            else:
                platilloright += self.dictObjetos[i]
        return abs(platilloleft - platilloright)

    def generarPoblacionInicial(self):
        """
        Genera una lista poblacion inicial
        La poblacion esta compuesta por TAM_POBLACION individuos distintos
        :return: poblacion: list
        """
        poblacion = []
        while len(poblacion) != self.TAM_POBLACION:
            solucion = self.generateRandomIndividual()
            if solucion not in poblacion:
                poblacion.append(solucion)
        return poblacion

    def seleccionarElite(self, poblacion):
        """
        Selecciona de la poblacion actual los individuos que forman
        parte de la élite.
        En este caso la élite es evaluada en cuanto al fitness que proporcionan.
        Se tomaran tantos individuos como indicados por el ELITE_PCT
        La funcion devuelve una lista con los individuos de elite
        :return: elite: list
        """
        num_elite = int((self.ELITE_PCT * self.TAM_POBLACION) / 100)
        fitness_poblacion = list(map(self.fitness, poblacion))  # Mapeamos la poblacion con la funcion de fitness
        fitness_e_individuos = list(zip(fitness_poblacion, poblacion))  # Agrupamos cada individuo con su fitness
        fitness_e_individuos.sort()  # Ordenamos segun el fitness, el orden viene dado gracias al criterio de ordenacion
                                     # de tuplas en python
        # "UnZipeamos la lista fitness e individuos"
        for i in range(len(fitness_e_individuos)):
            fitness_e_individuos[i] = fitness_e_individuos[i][1]

        elite = fitness_e_individuos[:num_elite]    # De la poblacion tomamos el num_elite
        return elite

    def mutar(self, individuo):
        """
        Recibe un individuo y devuelve el mismo
        individuo, que puede estar o no mutado.
        La mutacion consiste en coger un gen al azar y permutarlo
        :param individuo: list
        :return individuo: list
        """
        prob_mutacion = r.randint(0, 100)
        if prob_mutacion in range(self.MUTATION_PCT):   # Para determinar si el individuo muta o no
            mutagen = r.randint(0, len(individuo)-1)
            if individuo[mutagen] == 0:
                individuo[mutagen] = 1
            else:
                individuo[mutagen] = 0

        return individuo

    def cruzarIndividuos(self, padre, madre):
        """
        Genera un hijo a partir de dos individuos
        aplica la funcion de mutacion tras crearlo
        :param padre: list
        :param madre: list
        :return: hijo: list
        """
        z = tuple(zip(padre, madre))
        hijo = []
        for i in range(len(z)):
            # Elijo con un 50/50 si el hijo va a heredar el gen de su padre o de su madre
            hijo.append(z[i][r.randint(0, 1)])
        hijo = self.mutar(hijo)
        return hijo

    def newGen(self, poblacion):
        """
        Genera una nueva poblacion de individuos en base a una poblacion inicial
        :param poblacion:
        :return:
        """
        nuevaGeneracion = self.seleccionarElite(poblacion)
        # Los primeros sujetos de la nueva generación son la élite de la anterior generación
        # Ahora vamos a seleccionar individuos al azar entre la poblacion para generar hijos
        while len(nuevaGeneracion) != self.TAM_POBLACION:
            padre = poblacion[r.randint(0, self.TAM_POBLACION - 1)]
            madre = poblacion[r.randint(0, self.TAM_POBLACION - 1)]
            hijo = self.cruzarIndividuos(padre, madre)
            if hijo not in nuevaGeneracion:
                nuevaGeneracion.append(hijo)
        return nuevaGeneracion

    def selectBest(self, poblacion):
        """
        Devuelve el individuo con mejor de la poblacion
        :param poblacion:
        :return:
        """
        lista_elite = self.seleccionarElite(poblacion)
        return lista_elite[0]

    def traducirSolucion(self, solucion):
        """
        Traduce la solución en forma de vector binario en forma de solución
        del problema en el formato [[pesos platillo izquierdo][ pesos platillo derecho]]
        :param solucion: list
        :return: list
        """
        platilloLeft = []
        platilloRight = []
        for i in range(len(solucion)):
            if solucion[i] == 0:
                platilloLeft.append(i)
            else:
                platilloRight.append(i)
        return [platilloLeft, platilloRight]

    def GASolve(self):
        """
        Metodo principal del algoritmo
        Lleva a cabo el procedimiento para la optimización
        :return: None
        """
        pobActual = self.generarPoblacionInicial()
        iteraciones = 0

        while iteraciones < self.NUM_ITER and self.fitness(self.selectBest(pobActual)) != 0:
            pobActual = self.newGen(pobActual)
            iteraciones += 1

        return self.selectBest(pobActual)

    def tiempo_medio_ejecucion(self):
        listaTiempos = []

        for i in range(30):
            tinicial = t.time()
            self.GASolve()
            tfinal = t.time() - tinicial
            listaTiempos.append(tfinal)

        media = np.mean(listaTiempos)
        return media

    def GASolveVisual(self):
        """
        Metodo principal del algoritmo
        Lleva a cabo el procedimiento para la optimización de forma visual
        :return: None
        """
        pobActual = self.generarPoblacionInicial()
        iteraciones = 0
        print("Diccionario de objetos y pesos: ", self.dictObjetos)
        print("Poblacion inicial:")
        for i in pobActual:
            print("- ", self.traducirSolucion(i), "Fitness:", self.fitness(i))
        while iteraciones < self.NUM_ITER and self.fitness(self.selectBest(pobActual)) != 0:
            pobActual = self.newGen(pobActual)
            iteraciones += 1

        if iteraciones < self.NUM_ITER:
            print("Se ha encontrado el optimo! Tras", iteraciones, "generaciones")
        else:
            print("Individuos resultantes tras", self.NUM_ITER, "generaciones")
        for i in pobActual:
            print("- ", self.traducirSolucion(i), "Fitness:", self.fitness(i))
        best = self.selectBest(pobActual)
        print("Individuo con mejor fitness:", best)
        print("Fitness:", self.fitness(best))
        print("Balanza: ", self.traducirSolucion(best))

    def __init__(self, numObjetos=10, tamPob=10):
        self.NUM_OBJETOS = numObjetos
        self.TAM_POBLACION = tamPob
        self.dictObjetos = self.generateObjectDict()

    def printProblemDetails(self):
        print("\t\t\t\tProblema de la balanza. Algoritmo Genético. Parámetros")
        print("Numero de objetos:", self.NUM_OBJETOS)
        print("Rango de pesos", self.RANGO_PESOS)
        print("Tamaño de poblacion:", self.TAM_POBLACION, "individuos")
        print("Porcentaje de elitismo:", self.ELITE_PCT, "%")
        print("Probabilidad de mutaciones:", self.MUTATION_PCT, "%")
        print("Numero de iteraciones, Generaciones de individuos:", self.NUM_ITER)
        print("Objetos:", self.dictObjetos)