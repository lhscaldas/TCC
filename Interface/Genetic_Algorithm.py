# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 10:27:33 2021

@author: lhsca
"""

import numpy as np
from numpy.random import randint
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import cm
from math import atan2, pi, sqrt, cos, sin
from time import time

def plot_cells(cells_m):
        fig, ax = plt.subplots()
        fig.canvas.set_window_title('Domínio')
        ax.matshow(cells_m, cmap=cm.binary, extent=[0,30*116,-30*73,0])
        ax.hlines(y=np.arange(-73, 0)*30, xmin=np.full(73, 0)*30,
               xmax=np.full(73, 116)*30, color="black", zorder=1, linewidths=0.25)
        ax.vlines(x=np.arange(0, 116)*30, ymin=np.full(116, -73)*30,
               ymax=np.full(116, 0)*30, color="black", zorder=1, linewidths=0.25)
        plt.title('Domínio')
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        ax.xaxis.set_ticks_position('bottom')
        plt.show()

def xy2matrix(xy_rest):
    matrix=np.zeros((73,116))
    for rectangle in xy_rest:
            y=int(rectangle[0])
            x=int(rectangle[1])
            matrix[y][x]=1
    return matrix

def xy2n(cells_xy):
    cells_n=list()
    for cell in cells_xy:
        cells_n.append(int(cell[0]*116+cell[1]))
    return cells_n

def plot(path_n, restrictions_n):
    # domain
    domain_m = np.zeros((73, 116))
    domain_s = domain_m.reshape((73*116,))
    restrictions_s = domain_s.copy()
    restrictions_s[restrictions_n] += 1
    restrictions_m = restrictions_s.reshape((73, 116))
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.matshow(restrictions_m, cmap=cm.binary, extent=[0,30*116,-30*73,0], zorder=0)
    ax.hlines(y=np.arange(-73, 0)*30, xmin=np.full(73, 0)*30,
               xmax=np.full(73, 116)*30, color="black", zorder=1, linewidths=0.25)
    ax.vlines(x=np.arange(0, 116)*30, ymin=np.full(116, -73)*30,
               ymax=np.full(116, 0)*30, color="black", zorder=1, linewidths=0.25)
    path_x = [(n % 116)*30+15 for n in path_n]
    path_y = [-(n//116)*30-15 for n in path_n]
    ax.plot(path_x, path_y, "o-", zorder=1)
    ax.scatter(path_x[0], path_y[0], marker="^",
               zorder=2, s=100, c="k", label="início")
    ax.scatter(path_x[-1], path_y[-1], marker="X",
               zorder=2, s=100, c="k", label="fim")
    plt.title('Domínio')
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    ax.xaxis.set_ticks_position('bottom')
    plt.legend()
    plt.show()

def plot_result(path_n, restrictions_n, eval, gen, dt):
    # domain
    domain_m = np.zeros((73, 116))
    domain_s = domain_m.reshape((73*116,))
    restrictions_s = domain_s.copy()
    restrictions_s[restrictions_n] += 1
    restrictions_m = restrictions_s.reshape((73, 116))
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.matshow(restrictions_m, cmap=cm.binary, extent=[0,30*116,-30*73,0], zorder=0)
    ax.hlines(y=np.arange(-73, 0)*30, xmin=np.full(73, 0)*30,
               xmax=np.full(73, 116)*30, color="black", zorder=1, linewidths=0.25)
    ax.vlines(x=np.arange(0, 116)*30, ymin=np.full(116, -73)*30,
               ymax=np.full(116, 0)*30, color="black", zorder=1, linewidths=0.25)
    path_x = [(n % 116)*30+15 for n in path_n]
    path_y = [-(n//116)*30-15 for n in path_n]
    ax.scatter(path_x[0], path_y[0], marker="o", zorder=2, s=100, c="g", label="início")
    ax.plot(path_x, path_y, "o-", zorder=1, label=f"{eval:4.6} metros")
    ax.scatter(path_x[-1], path_y[-1], marker="o", zorder=2, s=100, c="r", label="fim")
    plt.title(f"Resultado obtido após {gen} gerações ({dt:4.4} segundos)")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    ax.xaxis.set_ticks_position('bottom')
    current_handles, current_labels = plt.gca().get_legend_handles_labels()
    handle_list = [current_handles[1],current_handles[0], current_handles[2]]
    label_list = [current_labels[1],current_labels[0], current_labels[2]]
    plt.legend(handle_list,label_list)
    plt.show()


def multiplot(paths_n, restrictions_n):
    # domain
    domain_m = np.zeros((73, 116))
    domain_s = domain_m.reshape((73*116,))
    restrictions_s = domain_s.copy()
    restrictions_s[restrictions_n] += 1
    restrictions_m = restrictions_s.reshape((73, 116))
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.matshow(restrictions_m, cmap=cm.binary, extent=[0,30*116,-30*73,0], zorder=0)
    ax.hlines(y=np.arange(-73, 0)*30, xmin=np.full(73, 0)*30,
               xmax=np.full(73, 116)*30, color="black", zorder=1, linewidths=0.25)
    ax.vlines(x=np.arange(0, 116)*30, ymin=np.full(116, -73)*30,
               ymax=np.full(116, 0)*30, color="black", zorder=1, linewidths=0.25)
    for path_n in paths_n:
        path_x = [(n % 116)*30+15 for n in path_n]
        path_y = [-(n//116)*30-15 for n in path_n]
        ax.plot(path_x, path_y, "o-", zorder=1)
    ax.scatter(path_x[0], path_y[0], marker="^",
               zorder=2, s=100, c="k", label="início")
    ax.scatter(path_x[-1], path_y[-1], marker="X",
               zorder=2, s=100, c="k", label="fim")
    plt.title('Domínio')
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    ax.xaxis.set_ticks_position('bottom')
    
    plt.show()
    

def fullPath(path_n):
    path_x = [n % 116*30+15 for n in path_n]
    path_y = [-(n//116*30)-15 for n in path_n]
    full_path = list()
    for i in range(len(path_n)):
        if path_n[i] not in full_path:
            full_path.append(path_n[i])
        if i < len(path_n)-1:
            x0 = path_x[i]
            x1 = path_x[i+1]
            y0 = path_y[i]
            y1 = path_y[i+1]
            x = x1-x0
            y = y1-y0
            alfa = atan2(y, x)
            l = sqrt(x**2+y**2)
            n = round(l/10)
            if n > 0:
                dl = l/n
                for j in range(1, n):
                    dx = x0+j*dl*cos(alfa)
                    dy = y0+j*dl*sin(alfa)
                    new_cell = (round((-dy-15)/30))*116+round((dx-15)/30)
                    if new_cell not in full_path:
                        full_path.append(new_cell)
    return full_path

def checkCollision(path_n, restrictions_n):
    n_col = 0
    full_path = fullPath(path_n)
    for node in full_path:
        if node in restrictions_n:
            n_col += 1
    return n_col

def genPoint(p1,p2):
    path_n = [p1,p2]
    path_x = [n%116*30+15 for n in path_n]
    path_y = [(n//116*30)-15 for n in path_n]
    d = 300
    if path_x[1]>path_x[0]:
        new_x=randint(path_x[0], path_x[0]+d)
    else:
        new_x=randint(path_x[0]-d, path_x[0])
    if path_y[1]>path_y[0]:
        new_y=randint(path_y[0], path_y[0]+d)
    else:
        new_y=randint(path_y[0]-d, path_y[0])
    new_point=((new_y+30)//30)*116+((new_x+30)//30)
    return new_point

def genPaths(begin, end, n_points, n_paths, restrictions_n):
    paths = list()
    while len(paths) < n_paths:
        i=0
        path = list()
        path.append(begin)
        while len(path)<n_points-1:
            new_point = genPoint(path[-1],end)
            safe_pass = checkCollision([path[-1],new_point],restrictions_n) == 0
            closer_to_end = length([new_point,end]) < 1*length([path[-1],end])
            i+=1
            if (safe_pass and closer_to_end) or i>10:
                path.append(new_point)
        path.append(end)
        safe_pass = checkCollision(path,restrictions_n) == 0
        if safe_pass:
            paths.append(path)
            # print(f"{len(paths)} caminhos gerados")
    return paths

def encode(path):
    length=len(path)
    path_matrix = list()
    for node in path:
        gene = np.binary_repr(node, width=13)
        path_matrix.append([int(x) for x in gene])
    path_matrix = np.array(path_matrix)
    chromossome = path_matrix.reshape((13*length,))
    return chromossome.tolist()


def decode(path_s):
    length=int(len(path_s)/13)
    path_v = np.array(path_s)
    path_m = path_v.reshape((length, 13))
    path = list()
    for node in path_m:
        num = int("".join(str(x) for x in node), 2)
        path.append(num)
    return(path)


def multi_encode(paths):
    pop = list()
    for path in paths:
        pop.append(encode(path))
    return pop


def multi_decode(pop):
    paths = list()
    for chromo in pop:
        paths.append(decode(chromo))
    return paths

def length(path_n):
    d = 0
    path_x = [n % 116*30+15 for n in path_n]
    path_y = [-(n//116*30)-15 for n in path_n]
    for i in range(0, len(path_n)-1):
        x0 = path_x[i]
        y0 = path_y[i]
        x1 = path_x[i+1]
        y1 = path_y[i+1]
        d += sqrt((x1-x0)**2+(y1-y0)**2)
    return d

def objective(path_s, restrictions_n):
    path_n = decode(path_s)
    F = length(path_n)
    ncol = checkCollision(path_n, restrictions_n)
    if ncol > 0:
        F += ncol * np.sqrt(3500**2+2200**2)
    return F

# tournament selection
def selection(pop, scores, k=3):
    # first random selection
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

# crossover two parents to create two children
def crossover(p1, p2, r_cross):
    length=int(len(p1)/13)
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross:
        # select crossover point that is not on the end of the string
        pt = 13*randint(1, length-1)  # randint(1, len(p1)-2)
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]

# mutation operator
def mutation(bitstring, r_mut, beginend):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]
    begin=[int(x) for x in np.binary_repr(beginend[0], width=13)]
    end=[int(x) for x in np.binary_repr(beginend[1], width=13)]
    bitstring[0:13]=begin
    bitstring[-13:]=end

def genetic_algorithm(objective, restrictions_n, beginend, n_nodes, n_iter, n_pop, r_cross, r_mut):
    # initial population of random bitstring
    paths = genPaths(beginend[0], beginend[1], n_nodes, n_pop, restrictions_n)
    # multiplot(paths, restrictions_n)
    print("População inicial criada")
    pop = multi_encode(paths)
    # keep track of best solution
    best, best_eval, best_gen = pop[0], objective(pop[0],restrictions_n), 0
    # enumerate generations
    for gen in range(n_iter):
        # evaluate all candidates in the population
        scores = [objective(c,restrictions_n) for c in pop]
        # check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval, best_gen = pop[i], scores[i], gen
            # print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))
            # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                mutation(c, r_mut, beginend)
                # store for next generation
                children.append(c)
        # replace population
        pop = children
    return [best, best_eval, best_gen]

# if __name__ == '__main__':
#     pressed_cells = [(25.0, 26.0), (25.0, 27.0), (25.0, 28.0), (24.0, 28.0), (23.0, 28.0), (22.0, 28.0), (21.0, 29.0), (21.0, 28.0), (20.0, 29.0), (19.0, 29.0), (18.0, 29.0), (17.0, 29.0), (17.0, 30.0), (16.0, 30.0), (15.0, 30.0), (14.0, 30.0), (13.0, 30.0), (12.0, 30.0), (12.0, 31.0), (11.0, 31.0), (10.0, 31.0), (9.0, 31.0), (8.0, 31.0), (7.0, 31.0), (7.0, 32.0), (6.0, 32.0), (4.0, 32.0), (5.0, 32.0), (3.0, 32.0), (2.0, 32.0), (2.0, 33.0), (0.0, 33.0), (1.0, 33.0), (1.0, 32.0), (0.0, 32.0), (2.0, 31.0), (3.0, 31.0), (4.0, 31.0), (5.0, 31.0), (6.0, 31.0), (7.0, 30.0), (8.0, 30.0), (9.0, 30.0), (10.0, 30.0), (11.0, 30.0), (12.0, 29.0), (11.0, 29.0), (13.0, 29.0), (14.0, 29.0), (15.0, 29.0), (15.0, 28.0), (16.0, 28.0), (16.0, 29.0), (17.0, 28.0), (19.0, 28.0), (18.0, 28.0), (20.0, 28.0), (20.0, 27.0), (19.0, 27.0), (21.0, 27.0), (23.0, 27.0), (24.0, 27.0), (22.0, 27.0), (24.0, 26.0), (23.0, 26.0), (19.0, 41.0), (20.0, 42.0), (19.0, 42.0), (20.0, 41.0), (18.0, 41.0), (18.0, 42.0), (17.0, 42.0), (17.0, 41.0), (17.0, 40.0), (18.0, 40.0), (17.0, 39.0), (16.0, 40.0), (16.0, 39.0), (15.0, 39.0), (15.0, 38.0), (16.0, 38.0), (14.0, 38.0), (14.0, 39.0), (13.0, 39.0), (13.0, 38.0), (12.0, 39.0), (12.0, 38.0), (11.0, 39.0), (11.0, 38.0), (10.0, 38.0), (10.0, 39.0), (11.0, 40.0), (10.0, 40.0), (8.0, 40.0), (9.0, 40.0), (9.0, 39.0), (9.0, 38.0), (8.0, 39.0), (8.0, 38.0), (7.0, 39.0), (7.0, 40.0), (6.0, 40.0), (6.0, 39.0), (5.0, 39.0), (5.0, 40.0), (4.0, 40.0), (3.0, 40.0), (4.0, 39.0), (2.0, 39.0), (3.0, 39.0), (2.0, 40.0), (1.0, 40.0), (0.0, 40.0), (3.0, 41.0), (4.0, 41.0), (4.0, 42.0), (4.0, 43.0), (4.0, 44.0), (4.0, 46.0), (4.0, 45.0), (4.0, 47.0), (5.0, 47.0), (5.0, 48.0), (5.0, 49.0), (5.0, 50.0), (4.0, 50.0), (4.0, 51.0), (4.0, 52.0), (3.0, 52.0), (3.0, 53.0), (2.0, 53.0), (2.0, 54.0), (2.0, 55.0), (1.0, 55.0), (1.0, 56.0), (0.0, 56.0), (0.0, 57.0), (0.0, 58.0), (0.0, 59.0), (0.0, 60.0), (1.0, 61.0), (0.0, 61.0), (2.0, 61.0), (2.0, 62.0), (3.0, 62.0), (4.0, 63.0), (4.0, 62.0), (5.0, 63.0), (6.0, 63.0), (7.0, 63.0), (7.0, 62.0), (7.0, 61.0), (6.0, 62.0), (7.0, 60.0), (8.0, 60.0), (8.0, 59.0), (9.0, 59.0), (9.0, 58.0), (9.0, 57.0), (10.0, 56.0), (10.0, 57.0), (11.0, 56.0), (11.0, 57.0), (12.0, 57.0), (12.0, 58.0), (13.0, 58.0), (14.0, 58.0), (14.0, 57.0), (14.0, 56.0), (15.0, 56.0), (15.0, 55.0), (17.0, 55.0), (16.0, 56.0), (16.0, 55.0), (17.0, 56.0), (15.0, 57.0), (15.0, 58.0), (15.0, 59.0), (16.0, 57.0), (16.0, 59.0), (16.0, 58.0), (16.0, 60.0), (17.0, 60.0), (18.0, 59.0), (17.0, 59.0), (18.0, 58.0), (18.0, 57.0), (19.0, 57.0), (19.0, 56.0), (18.0, 56.0), (17.0, 57.0), (17.0, 58.0), (19.0, 55.0), (19.0, 54.0), (20.0, 54.0), (21.0, 55.0), (20.0, 56.0), (20.0, 57.0), (20.0, 55.0), (21.0, 53.0), (21.0, 54.0), (21.0, 52.0), (22.0, 51.0), (21.0, 51.0), (22.0, 53.0), (22.0, 52.0), (22.0, 50.0), (23.0, 51.0), (23.0, 50.0), (23.0, 48.0), (23.0, 49.0), (24.0, 50.0), (24.0, 49.0), (24.0, 48.0), (23.0, 47.0), (24.0, 47.0), (24.0, 46.0), (24.0, 45.0), (25.0, 46.0), (25.0, 45.0), (24.0, 44.0), (25.0, 44.0), (26.0, 43.0), (24.0, 43.0), (25.0, 43.0), (25.0, 42.0), (25.0, 41.0), (25.0, 40.0), (25.0, 39.0), (26.0, 39.0), (26.0, 40.0), (26.0, 41.0), (26.0, 42.0), (27.0, 40.0), (27.0, 39.0), (27.0, 41.0)]
#     restrictions = xy2n(pressed_cells)
#     beginend = [3496, 1212]
#     # beginend = [1212, 3496+30]
#     # beginend = [3496, 3496+50]
#     n_nodes = int(length(beginend)/500)+3

    # n_paths = 40
    # t1=time()
    # paths = genPaths(beginend[0], beginend[1], n_nodes, n_paths, restrictions)
    # print(f"nova demorou {time()-t1} segundos")
    # multiplot(paths, restrictions)

    # n_pop=40
    # n_iter=200
    # r_cross=0.9
    # r_mut=1/(n_pop*sqrt(13*n_nodes)) # Tu e Yang 2003

    # ti = time()
    # best, best_eval, best_gen = genetic_algorithm(objective, restrictions, beginend, n_nodes, n_iter, n_pop, r_cross, r_mut)
    # dt = time()-ti
    # best_path = decode(best)
    # best_length = length(best_path)
    # plot_result(best_path, restrictions, best_length, best_gen+1, dt) # para debug