"""
Implementación de un algoritmo genetico
"""
import GA as ga


if __name__ == "__main__":
    g = ga.GeneticAlgorithm(10, 50)

    g.printProblemDetails()
    # print(g.tiempo_medio_ejecucion())


