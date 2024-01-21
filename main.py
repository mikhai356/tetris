import pygame
import random

from pygame.constants import AUDIO_ALLOW_FORMAT_CHANGE

pygame.init()

# переменные

fps = 15  # количество циклов в секунду
score = 0  # количество очков
x = 0  # мгновенные координаты кубиков для x(в пикселях)
y = 0  # мгновенные координаты кубиков для y(в пикселях)
cube = 25  # сторона квадрат
interface = 100  # ширина интерфейса
wight = 10  # ширина в клеточках
height = 20  # высота в клеточках
screenY = cube * height  # высота в пикселях
screenX = cube * wight  # ширина в пикселях
figure = 0  # переменная, содержащая тип сгенерированной фигуры
level = 1  # уровень
fall = 0  # индикатор падения фигуры
fall1 = 0  # количество кубиков фигуры, под которыми ничего нет, кроме 0ей и своих же кубиков(если меньше четырех,
# то fall = 0)
latency = 0  # переменная для подсчета прошедших кадров после последнего падения
# создание массива и заполнение его нулями
mass = [[0] * wight for i in range(height)]
# создание массива координат в первом массиве для падающей фигуры
massobj = [[0] * 2 for i in range(4)]
"""
massobj[№элемента(от 0 до 3)][0- по игрику;1 - по иксу]
mass[y в клеточках(massobj[№элемента][0])][x в клеточках(massobj[№элемента][1])]
"""
# создание окна и присваивание ему имени
screen = pygame.display.set_mode((screenX + interface, screenY))
pygame.display.set_caption('Tetris')

#функции

#функция заливки фигуры
def figa(massobj,mass,color):
    for i in range(0,4):
        mass[massobj[i][0]][massobj[i][1]] = color

#функция отрисовки
def otris(mass,screen,cube):
    for ymass in range(height):
        for xmass in range(wight):
            if mass[ymass][xmass] == 1 or mass[ymass][xmass] == 8:
                pygame.draw.rect(screen, (0, 0, 200), (xmass * cube, ymass * cube, cube, cube))
            if mass[ymass][xmass] == 2 or mass[ymass][xmass] == 9:
                pygame.draw.rect(screen, (200, 0, 0), (xmass * cube, ymass * cube, cube, cube))
            if mass[ymass][xmass] == 3 or mass[ymass][xmass] == 10:
                pygame.draw.rect(screen, (0, 0, 100), (xmass * cube, ymass * cube, cube, cube))
            if mass[ymass][xmass] == 4 or mass[ymass][xmass] == 11:
                pygame.draw.rect(screen, (0, 200, 0), (xmass * cube, ymass * cube, cube, cube))
            if mass[ymass][xmass] == 5 or mass[ymass][xmass] == 12:
                pygame.draw.rect(screen, (200, 0, 200), (xmass * cube, ymass * cube, cube, cube))
            if mass[ymass][xmass] == 6 or mass[ymass][xmass] == 13:
                pygame.draw.rect(screen, (0, 200, 200), (xmass * cube, ymass * cube, cube, cube))
            if mass[ymass][xmass] == 7 or mass[ymass][xmass] == 14:
                pygame.draw.rect(screen, (200, 200, 0), (xmass * cube, ymass * cube, cube, cube))

#функция проверки выхода объекта за границы по оси x
def proverkX(x,p):
    if p + x >= 0 and p + x <= (wight-1):
        return 1
    else:
        return 0

#проверка, заняты ли кубики, необходимые для объекта
def proverkaFigure(massobj,mass):
    for item in range(0,4):
        if mass[massobj[item][0]][massobj[item][1]] != 0:
            global run
            #заполнение экрана черным
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, screenX + interface, screenY))
            #прорисовка конца игры
            fontLocal = pygame.font.SysFont('arial', 50)
            textLocal = fontLocal.render('The End', True, (255, 255, 255))
            screen.blit(textLocal, (80, 200))
            #обновление экрана
            pygame.display.flip()
            runLocal = True
            while runLocal:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        runLocal = False
                        run = False
            break

#функция проверки возможности движения и движения
def dvizh(x,y,mass,massobj,figure):
    if x!=0 and y==0:
        # условие для движения по оси х
        dvig = 0  # переменная для проверки возможности движения
        if proverkX(x,massobj[0][1]) and proverkX(x,massobj[1][1]) and proverkX(x,massobj[2][1]) and proverkX(x,massobj[3][1]):
            if mass[massobj[0][0]][massobj[0][1] + x] == 0 or mass[massobj[0][0]][massobj[0][1] + x] == figure:
                dvig = dvig + 1
            if mass[massobj[1][0]][massobj[1][1] + x] == 0 or mass[massobj[1][0]][massobj[1][1] + x] == figure:
                dvig = dvig + 1
            if mass[massobj[2][0]][massobj[2][1] + x] == 0 or mass[massobj[2][0]][massobj[2][1] + x] == figure:
                dvig = dvig + 1
            if mass[massobj[3][0]][massobj[3][1] + x] == 0 or mass[massobj[3][0]][massobj[3][1] + x] == figure:
                dvig = dvig + 1
    elif y>0 and x==0:
        # условие для движения вниз
        dvig = 0  # переменная для проверки возможности движения
        if massobj[0][0] + y <= (height - 1) and massobj[1][0] + y <= (height - 1) and massobj[2][0] + y <= (height - 1) and massobj[3][0] + y <= (height - 1):
            if mass[massobj[0][0]+y][massobj[0][1]] == 0 or mass[massobj[0][0]+y][massobj[0][1]] == figure:
                dvig = dvig + 1
            if mass[massobj[1][0]+y][massobj[1][1]] == 0 or mass[massobj[1][0]+y][massobj[1][1]] == figure:
                dvig = dvig + 1
            if mass[massobj[2][0]+y][massobj[2][1]] == 0 or mass[massobj[2][0]+y][massobj[2][1]] == figure:
                dvig = dvig + 1
            if mass[massobj[3][0]+y][massobj[3][1]] == 0 or mass[massobj[3][0]+y][massobj[3][1]] == figure:
                dvig = dvig + 1
    else:
        print('Ошибка')
        return

    # передвижение фигуры
    if dvig == 4:
        mass[massobj[0][0]][massobj[0][1]] = 0
        mass[massobj[1][0]][massobj[1][1]] = 0
        mass[massobj[2][0]][massobj[2][1]] = 0
        mass[massobj[3][0]][massobj[3][1]] = 0
        mass[massobj[0][0]+y][massobj[0][1] + x] = figure
        mass[massobj[1][0]+y][massobj[1][1] + x] = figure
        mass[massobj[2][0]+y][massobj[2][1] + x] = figure
        mass[massobj[3][0]+y][massobj[3][1] + x] = figure
        massobj[0][0] = massobj[0][0] + y
        massobj[1][0] = massobj[1][0] + y
        massobj[2][0] = massobj[2][0] + y
        massobj[3][0] = massobj[3][0] + y
        massobj[0][1] = massobj[0][1] + x
        massobj[1][1] = massobj[1][1] + x
        massobj[2][1] = massobj[2][1] + x
        massobj[3][1] = massobj[3][1] + x

# переменная для работы цикла
run = True

# основной цикл
while run:
    # цикл для проверки на закрытие окна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # задержка
    delay = 1000 / fps
    pygame.time.delay(int(delay))

    # генерация фигуры если предыдущая прекратила падать
    if fall == 0:

        #удаление полностью заполненных строчек
        for ymass in range(0,height):
            strochka = 0
            for xmass in range(0,wight):
                if mass[ymass][xmass]>0:
                    strochka = strochka + 1
            if strochka == 10:
                for ymasss in reversed(range(1,ymass+1)):
                    for xmasss in range(0,wight):
                        mass[ymasss][xmasss] = mass[ymasss - 1][xmasss]
                for x in range(0,wight):
                    mass[0][x] = 0
                score = score + 1

        figure = random.randint(1, 7)

        if figure == 1:
            massobj[0][0] = 0
            massobj[0][1] = 4

            massobj[1][0] = 0
            massobj[1][1] = 5

            massobj[2][0] = 1
            massobj[2][1] = 4

            massobj[3][0] = 1
            massobj[3][1] = 5

            proverkaFigure(massobj,mass)
            figa(massobj,mass,1)

        if figure == 2:
            massobj[0][0] = 0
            massobj[0][1] = 3

            massobj[1][0] = 0
            massobj[1][1] = 4

            massobj[2][0] = 1
            massobj[2][1] = 4

            massobj[3][0] = 1
            massobj[3][1] = 5

            proverkaFigure(massobj,mass)
            figa(massobj,mass,2)

        if figure == 3:
            massobj[0][0] = 0
            massobj[0][1] = 3

            massobj[1][0] = 1
            massobj[1][1] = 3

            massobj[2][0] = 1
            massobj[2][1] = 4

            massobj[3][0] = 1
            massobj[3][1] = 5

            proverkaFigure(massobj,mass)
            figa(massobj,mass,3)

        if figure == 4:
            massobj[0][0] = 1
            massobj[0][1] = 3

            massobj[1][0] = 1
            massobj[1][1] = 4

            massobj[2][0] = 0
            massobj[2][1] = 4

            massobj[3][0] = 0
            massobj[3][1] = 5

            proverkaFigure(massobj,mass)
            figa(massobj,mass,4)

        if figure == 5:
            massobj[0][0] = 1
            massobj[0][1] = 3

            massobj[1][0] = 1
            massobj[1][1] = 4

            massobj[2][0] = 1
            massobj[2][1] = 5

            massobj[3][0] = 0
            massobj[3][1] = 5

            proverkaFigure(massobj,mass)
            figa(massobj,mass,5)

        if figure == 6:
            massobj[0][0] = 1
            massobj[0][1] = 3

            massobj[1][0] = 1
            massobj[1][1] = 4

            massobj[2][0] = 1
            massobj[2][1] = 5

            massobj[3][0] = 1
            massobj[3][1] = 6

            proverkaFigure(massobj,mass)
            figa(massobj,mass,6)

        if figure == 7:
            massobj[0][0] = 1
            massobj[0][1] = 3

            massobj[1][0] = 1
            massobj[1][1] = 4

            massobj[2][0] = 0
            massobj[2][1] = 4

            massobj[3][0] = 1
            massobj[3][1] = 5

            proverkaFigure(massobj,mass)
            figa(massobj,mass,7)

    # проверка на продолжение падения фигуры
    fall1 = 0
    if massobj[0][0] + 1 < height and massobj[1][0] + 1 < height and massobj[2][0] + 1 < height and massobj[3][0] + 1 < height:
        if mass[massobj[0][0] + 1][massobj[0][1]] == 0 or mass[massobj[0][0] + 1][massobj[0][1]] == figure:
            fall1 = fall1 + 1
        if mass[massobj[1][0] + 1][massobj[1][1]] == 0 or mass[massobj[1][0] + 1][massobj[1][1]] == figure:
            fall1 = fall1 + 1
        if mass[massobj[2][0] + 1][massobj[2][1]] == 0 or mass[massobj[2][0] + 1][massobj[2][1]] == figure:
            fall1 = fall1 + 1
        if mass[massobj[3][0] + 1][massobj[3][1]] == 0 or mass[massobj[3][0] + 1][massobj[3][1]] == figure:
            fall1 = fall1 + 1

    #присвоение значения переменной падения
    if fall1 >= 4:
        fall = 1
    else:
        fall = 0

    #задержка падения
    latency = latency + 1
    if latency >= (fps - (fps / 3))/(level) or fall==0:

        # падение фигуры на 1 кватрат вниз
        if fall == 1:
            mass[massobj[0][0]][massobj[0][1]] = 0
            mass[massobj[1][0]][massobj[1][1]] = 0
            mass[massobj[2][0]][massobj[2][1]] = 0
            mass[massobj[3][0]][massobj[3][1]] = 0
            mass[massobj[0][0] + 1][massobj[0][1]] = figure
            mass[massobj[1][0] + 1][massobj[1][1]] = figure
            mass[massobj[2][0] + 1][massobj[2][1]] = figure
            mass[massobj[3][0] + 1][massobj[3][1]] = figure
            massobj[0][0] = massobj[0][0] + 1
            massobj[1][0] = massobj[1][0] + 1
            massobj[2][0] = massobj[2][0] + 1
            massobj[3][0] = massobj[3][0] + 1
        else:
            mass[massobj[0][0]][massobj[0][1]] = figure + 7
            mass[massobj[1][0]][massobj[1][1]] = figure + 7
            mass[massobj[2][0]][massobj[2][1]] = figure + 7
            mass[massobj[3][0]][massobj[3][1]] = figure + 7
        latency = 0

    #считывание нажатий клавиш и движение
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: #влево
        dvizh(-1,0,mass,massobj,figure)
    if keys[pygame.K_RIGHT]: #вправо
        dvizh(1,0,mass,massobj,figure)
    if keys[pygame.K_DOWN]: #внизу(ускорение)
        dvizh(0,1,mass,massobj,figure)
    if keys[32]: #разворот фигуры при нажатии на пробел
        figure1 = mass[massobj[1][0]][massobj[1][1]]
        figa(massobj,mass,0)
        for i in range(0,4):
            if (massobj[i][0]>massobj[1][0]) and (massobj[i][1]>massobj[1][1]): #правый низ
                pomen = massobj[i][1]
                massobj[i][1] = massobj[1][1] - abs(massobj[i][0]-massobj[1][0])
                massobj[i][0] = massobj[1][0] + abs(pomen - massobj[1][1])

            elif (massobj[i][0]<massobj[1][0]) and (massobj[i][1]>massobj[1][1]): #правый верх
                pomen = massobj[i][1]
                massobj[i][1] = massobj[1][1] + abs(massobj[i][0]-massobj[1][0])
                massobj[i][0] = massobj[1][0] + abs(pomen - massobj[1][1])

            elif (massobj[i][0]<massobj[1][0]) and (massobj[i][1]<massobj[1][1]): #левый верх
                pomen = massobj[i][1]
                massobj[i][1] = massobj[1][1] + abs(massobj[i][0]-massobj[1][0])
                massobj[i][0] = massobj[1][0] - abs(pomen - massobj[1][1])

            elif (massobj[i][0]>massobj[1][0]) and (massobj[i][1]<massobj[1][1]): #левый низ
                pomen = massobj[i][1]
                massobj[i][1] = massobj[1][1] - abs(massobj[i][0]-massobj[1][0])
                massobj[i][0] = massobj[1][0] - abs(pomen - massobj[1][1])

            elif  (massobj[i][0]>massobj[1][0]) and (massobj[i][1]==massobj[1][1]): #внизу
                massobj[i][1] = massobj[1][1]-abs(massobj[i][0]-massobj[1][0])
                massobj[i][0] = massobj[1][0]

            elif  (massobj[i][0]<massobj[1][0]) and (massobj[i][1]==massobj[1][1]): #вверху
                massobj[i][1] = massobj[1][1]+abs(massobj[i][0]-massobj[1][0])
                massobj[i][0] = massobj[1][0]

            elif (massobj[i][0]==massobj[1][0]) and (massobj[i][1]>massobj[1][1]): #справа
                massobj[i][0] = massobj[1][0] + abs(massobj[1][1]-massobj[i][1])
                massobj[i][1] = massobj[1][1]

            elif (massobj[i][0]==massobj[1][0]) and (massobj[i][1]<massobj[1][1]): #слева
                massobj[i][0] = massobj[1][0] - abs(massobj[1][1]-massobj[i][1])
                massobj[i][1] = massobj[1][1]

        figa(massobj,mass,figure1)

    #заполнение фона черным
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screenX + interface, screenY))

    #прорисовка полосы интерфейса
    pygame.draw.rect(screen, (255, 255, 255), (screenX, 0, interface, screenY))

    #отрисовка надписи score
    font1 = pygame.font.SysFont('arial', 24)
    text1 = font1.render('Score: ', True, (50, 50, 50))
    screen.blit(text1, (screenX, 0))

    #отрисовка надписи level
    font11 = pygame.font.SysFont('arial', 24)
    text11 = font11.render('Level: ', True, (50, 50, 50))
    screen.blit(text11, (screenX, 50))

    #отрисовка значения очков
    font2 = pygame.font.SysFont('arial', 24)
    text2 = font2.render(str(score), True, (50, 50, 50))
    screen.blit(text2, (screenX, 25))

    #отрисовка значения уровня
    font21 = pygame.font.SysFont('arial', 24)
    text21 = font21.render(str(level), True, (50, 50, 50))
    screen.blit(text21, (screenX, 75))

    #прорисовка поля с кубиками
    otris(mass,screen,cube)

    #прорисовка решетки
    for row in range(cube - 1, screenX - cube, cube):
        pygame.draw.rect(screen, (100, 100, 100), (row, 0, 1, screenY))
    for row in range(cube - 1, screenY - cube, cube):
        pygame.draw.rect(screen, (100, 100, 100), (0, row, screenX, 1))

    #обновление интерфейса
    pygame.display.flip()

    #обновление уровня
    level = score // 10 + 1
