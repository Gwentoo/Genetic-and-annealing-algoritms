import numpy as np
from PIL import Image
import random

# Считывание изображения и перевод в матрицу из 0 и 1
def Image2Matrix(img_name):
    img = Image.open(f"{img_name}").convert("L")
    img = img.point(lambda x: 0 if x > 128 else 1, '1')
    array = np.asarray(img, dtype='uint8')
    return array

#Размеры матрицы
def size(array):
    M = len(array)
    N = len(array[0])
    return (M, N)

#Фитнесс-функция
def FitnessMax(arrayTest, arrayTrue):
    sum = 0
    M, N = size(arrayTest)
    for i in range(M):
        for j in range(N):
            if arrayTest[i][j] == arrayTrue[i][j]:
                sum += 1
    return sum/(M*N)

#Создание одной особи
def Individual(M, N):
    array = []
    for i in range(M):
        array.append([])
        for j in range(N):
            x = random.choice([0, 1])
            array[i].append(x)
    array = np.array(array)
    return array

#Скрещивание
def Crossing(image, arr1, arr2):
    descendant = []
    for i in range(size(arr1)[0]):
        descendant.append([])
        for j in range(size(arr1)[1]):
            choice = [arr1[i][j], arr2[i][j]]
            x = random.choice(choice)
            descendant[i].append(x)
    descendant = np.array(descendant)
    return (descendant, FitnessMax(descendant, image))

#Создание популяции из count особей
def createPopulation(image, count, M, N):
    Population = []
    for i in range(count):
        Ind = Individual(M, N)
        Population.append((Ind, FitnessMax(Ind, image)))
    Population = sorted(Population, key=lambda x: x[1], reverse=True)
    return Population

#Мутация
def Mutant(image, array):
    M, N = size(array)
    for i in range(round(M*N/3)):
        x = random.randint(0, M-1)
        y = random.randint(0, N - 1)
        if array[x][y] == 0:
            array[x][y] = 1
        else:
            array[x][y] = 0
    array = np.array(array)
    return (array, FitnessMax(array, image))

# Алгоритм
def genetic(image):
    count = 100 #количество особей в популяции
    chance = 0.2 #шанс мутации
    M, N = size(image)
    Population = createPopulation(image, count, M, N)
    history = [] #история точности
    for i in range(1000):

        #Составляем список родителей
        parents = []
        for k in range(count):
            parents.append(Population[k])

        #Производим скрещивание и мутации
        posterity = []
        for p in range(count - 1):
            for j in range(p+1, count - 1):
                new_gen = Crossing(image, parents[p][0], parents[j][0])
                x = random.random()

                #Создаем большую мутацию
                if x <= chance:
                    new_gen = Mutant(image, new_gen[0])

                posterity.append(new_gen)
        Population = sorted(posterity, key=lambda x: x[1], reverse=True)
        Population = Population[:count]

        #Сохраняем изображение и точность лучшей особи
        history.append(Population[0][1])

        #Критерий остановки
        if len(history) >= 3:
            if (Population[0][1] == 1) or (history[-1] == history[-2] == history[-3]):
                break

    return [M*N,  max(history)]

#Запуск
image1 = Image2Matrix('Gear.png')
print(genetic(image1))












