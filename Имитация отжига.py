import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image

#Генерация пунктов
def generate_peaks(N):
    X = [random.uniform(-5, 5) for _ in range(N)]
    Y = [random.uniform(-5, 5) for _ in range(N)]
    return X, Y

#Расстояния между всеми пунктами
def generate_ways(N, X, Y):
    ways = dict()
    for i in range(N):
        for j in range(i+1, N):
            x = ((X[i] - X[j])**2 + (Y[i]-Y[j])**2) ** 0.5
            ways[i, j] = round(x, 3)
    return ways

#Отображения состояния
def plot_graph(X, Y, way, number, en, T):
    plt.scatter(X[1:], Y[1:], c='r', s=20)
    plt.scatter(X[0], Y[0], c='black', s=25)
    for i in range(len(way)-1):
        plt.plot([X[way[i]], X[way[i+1]]], [Y[way[i]], Y[way[i+1]]], color='blue', linewidth=0.5)
    plt.plot([X[way[0]], X[way[len(way)-1]]], [Y[way[0]], Y[way[len(way)-1]]], color='blue', linewidth=0.5)
    plt.xlabel(f"energy = {round(en,1)}  iter = {number*1000}")
    plt.savefig(f"{number}.jpg")
    plt.clf()

#Функция энергии состояния
def energy(way, ways):
    sum = 0
    for i in range(len(way)-1):
        try:
            sum += ways[way[i], way[i+1]]
        except:
            sum += ways[way[i+1], way[i]]
    try:
        sum += ways[way[0], way[len(way)-1]]
    except:
        sum += ways[way[len(way) - 1], way[0]]
    return sum

#Создает начальное состояние
def random_state(N):
    way = [0]
    while len(way) != N:
        x = random.randint(1, N - 1)
        if x not in way:
            way.append(x)

    return way

#Создает новое состояние на основе прошлого
def new_state(way):
    p1 = random.randint(1, len(way)-1)
    p2 = random.randint(1, len(way)-1)

    new_way = []

    if p2 < p1:
        for i in range(p2):
            new_way.append(way[i])
        new_way += way[p2:p1+1][::-1]
        for i in range(p1+1, len(way)):
            new_way.append(way[i])
    else:
        for i in range(p1):
            new_way.append(way[i])
        new_way += way[p1:p2+1][::-1]
        for i in range(p2+1, len(way)):
            new_way.append(way[i])

    return new_way

#Вероятность перехода в новое состояние
def gibbs(T, dE):
    return np.exp(-dE/T)

#Визуализация алгоритма
def gif():
    frames = []

    for frame_number in range(0, 101):
        frame = Image.open(f'{frame_number}.jpg')
        frames.append(frame)

    frames[0].save(
        'result.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=180,
        loop=0
    )


#Алгоритм
def annealing(T, N):
    history = []
    number = 0
    iteration = 1
    X, Y = generate_peaks(N)
    ways = generate_ways(N, X, Y)
    way0 = random_state(N)
    en0 = energy(way0, ways)
    plot_graph(X, Y, way0, number, en0, T)
    number += 1
    while T >= 0.00001:
        way1 = new_state(way0)

        en0 = energy(way0, ways)
        en1 = energy(way1, ways)
        dE = en1 - en0

        if dE <= 0:
            way0 = way1

        else:
            p = gibbs(T, dE)
            r = random.random()
            if r <= p:
                way0 = way1

        history.append(en1)
        iteration += 1
        T = start_T * 0.1 / iteration
        if iteration % 1000 == 0:
            plot_graph(X, Y, way0, number, en1, T)
            number += 1

    return history


start_T = 10
N = 200

history = annealing(start_T, N)
gif()
plt.plot(history)
plt.savefig("history.jpg")
plt.clf()

