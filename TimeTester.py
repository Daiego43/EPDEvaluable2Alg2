"""
La función de este script es la de probar a cambiar varios parámetros de cada
problema para consultar la variación en el tiempo de ejecución
"""
from AlgoritmoGenetico import GA as g
from AntColonyOptimization import ACO as a
import numpy as np
import matplotlib.pyplot as plt


def influencia_num_objetos_GA():
    x = []
    y = []
    for i in range(100, 1001, 100):
        ga = g.GeneticAlgorithm(i, 10)
        print(i)
        x.append(ga.NUM_OBJETOS)
        t = ga.tiempo_medio_ejecucion()
        y.append(t)

    file = open("GA_Tiempo_NUMOBJETOS.txt", "x")
    file.write("NUM_OBJETOS\tTIEMPO_MEDIO_EJECUCION\n")
    for i in range(len(x)):
        file.write(str(x[i]) + "\t" + str(y[i]) + "\n")
    file.close()


def influencia_tam_pob_GA():
    x = []
    y = []
    for i in range(100, 1001, 100):
        ga = g.GeneticAlgorithm(10, i)
        print(i)
        x.append(ga.TAM_POBLACION)
        t = ga.tiempo_medio_ejecucion()
        y.append(t)

    file = open("GA_Tiempo_TAMPOBLACION.txt", "x")
    file.write("TAM_POBLACION\tTIEMPO_MEDIO_EJECUCION\n")
    for i in range(len(x)):
        file.write(str(x[i]) + "\t" + str(y[i]) + "\n")
    file.close()


def influencia_num_hormigas_ACO():
    x = []
    y = []
    for i in range(10, 151, 10):
        print(i)
        aco = a.AntColonyOptimization(i, 10, 300)
        tiempo, mejor = aco.tiempo_medio_ejecucion()
        x.append(i)
        y.append(tiempo)

    file = open("ACO_tiempo_hormigas.txt", "x")
    file.write("NUM_HORMIGAS\tTIEMPO_MEDIO_EJECUCION\n")
    for i in range(len(x)):
        file.write(str(x[i]) + "\t" + str(y[i]) + "\n")
    file.close()


def influencia_num_objetos_ACO():
    x = []
    y = []
    for i in range(100, 600, 100):
        print(i)
        aco = a.AntColonyOptimization(5, i, 3000)
        tiempo, mejor = aco.tiempo_medio_ejecucion()
        x.append(i)
        y.append(tiempo)

    file = open("ACO_tiempo_objetos.txt", "x")
    file.write("NUM_OBJETOS\tTIEMPO_MEDIO_EJECUCION\n")
    for i in range(len(x)):
        file.write(str(x[i]) + "\t" + str(y[i]) + "\n")
    file.close()


def plotGADataObjetos():
    xnum = []
    ytiempoobjetos = []

    data_objetos = open("GA_Tiempo_NUMOBJETOS.txt", "r")
    line = data_objetos.readline()
    while len(line) != 0:
        line = data_objetos.readline()
        datos = line.split()
        if len(datos) != 0:
            xnum.append(int(datos[0]))
            ytiempoobjetos.append(float(datos[1]))
    data_objetos.close()

    xpoints = np.array(xnum)
    ypoints = np.array(ytiempoobjetos)

    plt.xlabel("Numero de objetos")
    plt.ylabel("Segundos")
    plt.plot(xpoints, ypoints)
    plt.show()


def plotGADataPoblacion():
    xnum = []
    ytiempopoblacion = []

    data_poblacion = open("GA_Tiempo_TAMPOBLACION.txt", "r")
    line = data_poblacion.readline()
    while len(line) != 0:
        line = data_poblacion.readline()
        datos = line.split()
        if len(datos) != 0:
            xnum.append(int(datos[0]))
            ytiempopoblacion.append(float(datos[1]))
    data_poblacion.close()

    xpoints = np.array(xnum)
    ypoints = np.array(ytiempopoblacion)

    plt.xlabel("Numero de individuos de la población")
    plt.ylabel("Segundos")
    plt.plot(xpoints, ypoints)
    plt.show()


def plotACODataHormigas():
    xnum = []
    ytiempoobjetos = []

    data_objetos = open("ACO_tiempo_hormigas.txt", "r")
    line = data_objetos.readline()
    while len(line) != 0:
        line = data_objetos.readline()
        datos = line.split()
        if len(datos) != 0:
            xnum.append(int(datos[0]))
            ytiempoobjetos.append(float(datos[1]))
    data_objetos.close()

    xpoints = np.array(xnum)
    ypoints = np.array(ytiempoobjetos)

    plt.xlabel("Numero de hormigas")
    plt.ylabel("Segundos")
    plt.plot(xpoints, ypoints)
    plt.show()


def plotACODataObjetos():
    xnum = []
    ytiempoobjetos = []

    data_objetos = open("ACO_tiempo_objetos.txt", "r")
    line = data_objetos.readline()
    while len(line) != 0:
        line = data_objetos.readline()
        datos = line.split()
        if len(datos) != 0:
            xnum.append(int(datos[0]))
            ytiempoobjetos.append(float(datos[1]))
    data_objetos.close()

    xpoints = np.array(xnum)
    ypoints = np.array(ytiempoobjetos)

    plt.xlabel("Numero de objetos")
    plt.ylabel("Segundos")
    plt.plot(xpoints, ypoints)
    plt.show()
