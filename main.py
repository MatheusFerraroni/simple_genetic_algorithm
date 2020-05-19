import GA
import numpy as np
import matplotlib.pyplot as plt


def evaluateScore(genome):

    if len(genome)!=16:
        raise Exception("Tamanho invalido para o genoma", len(genome))

    board = np.zeros([8,8], dtype=int)
    size = len(board)

    for p in range(0,len(genome)-1,2):
        board[genome[p]][genome[p+1]] = 1

    damas_casas_diferentes = 0
    for i in range(size):
        for j in range(size):
            if board[i][j]==1:
                damas_casas_diferentes += 1

    total_hits = 0
    for i in range(size):
        for j in range(size):
            if board[i][j]==1: # se tiver uma rainha aqui checa se ela colide com alguma outra

                hit = False
                k = i-1
                while k>0 and not hit: # checagem horizontal e vertical
                    if board[k][j]==1:
                        hit = True
                    k = k-1

                k = i+1
                while k<size and not hit:
                    if board[k][j]==1:
                        hit = True
                    k = k+1

                k = j-1
                while k>0 and not hit:
                    if board[i][k]==1:
                        hit = True
                    k = k-1

                k = j+1
                while k<size and not hit:
                    if board[i][k]==1:
                        hit = True
                    k = k+1

                k = i+1
                kk = j+1
                while k>0 and k<size and kk>0 and kk<size and not hit: # checagem na diagonal
                    if board[k][kk]==1:
                        hit = True
                    k = k+1
                    kk = kk+1

                k = i+1
                kk = j-1
                while k>0 and k<size and kk>0 and kk<size and not hit:
                    if board[k][kk]==1:
                        hit = True
                    k = k+1
                    kk = kk-1

                k = i-1
                kk = j-1
                while k>0 and k<size and kk>0 and kk<size and not hit:
                    if board[k][kk]==1:
                        hit = True
                    k = k-1
                    kk = kk-1

                k = i-1
                kk = j+1
                while k>0 and k<size and kk>0 and kk<size and not hit:
                    if board[k][kk]==1:
                        hit = True
                    k = k-1
                    kk = kk+1

                if hit:
                    total_hits += 1


    return 8-total_hits



def printMapa(genome):

    if len(genome)!=16:
        raise Exception("Tamanho invalido para o genoma", len(genome))

    board = np.zeros([8,8], dtype=int)
    size = len(board)

    for p in range(0,len(genome)-1,2):
        board[genome[p]][genome[p+1]] = 1

    print(board)


def main():


    g = GA.GeneticAlgorithm()
    g.set_evaluate(evaluateScore)
    g.set_mutation_rate(0.1)
    g.set_iteration_limit(1000)
    g.set_population_size(30)
    g.set_max_score(8)

    g.run()




    geracoes = []
    maxs = []
    mins = []
    meds = []
    bests = []
    for i in range(len(g.historic)):
        geracoes.append(g.historic[i]["geracao"])
        maxs.append(g.historic[i]["max"])
        mins.append(g.historic[i]["min"])
        meds.append(g.historic[i]["avg"])
        bests.append(g.historic[i]["best"])



    fig, ax = plt.subplots()
    line1, = ax.plot(geracoes, maxs, label='Max Score')
    line2, = ax.plot(geracoes, meds, label='Average Score')
    line2, = ax.plot(geracoes, mins, label='Min Score')
    line2, = ax.plot(geracoes, bests, label='Best Score')



    ax.legend()
    plt.show()

if __name__ == '__main__':
    main()