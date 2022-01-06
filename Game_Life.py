from typing import ClassVar
import pygame ## библиотека для окна с графикой
import numpy as np ## для работы с матрицами
from pygame.locals import QUIT
from pygame.time import Clock ## при нажатии на выход работа программы остановиться


## создадим класс, в котором будет вся логика и интерфейс
class GameLife:
    """
    Class of Game
    """
    def __init__(self, width: int = 800, height: int = 800, cell_size: int = 10, speed: int = 10) -> None:
        """
        Создаем окно, в котором будет отображаться графика

        Parametrs:
        ---------------
        width: int64 - ширина окна (пикс.), по умолч. 800
        height: int64 - высота она (пикс.), по умолч. 800
        cell_size: int64 - высота и ширина игровой клетки (пикс.), по умолч. 10
        speed: int64 - скорость протекания игры, по умолч. 10
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # создадим переменные, отвечающие за кол-во клеток по горизонтали и вертикали
        self.w = self.width // self.cell_size
        self.h = self.height // self.cell_size

        # зададим размеры окна
        self.resolution = width, height

        # создаем окно
        self.screen = pygame.display.set_mode(self.resolution)

        ## создадим массив следующего состояния, заполненный нулями.
        # дальше в программе он будет меняться согласно условиям игры
        self.next_generation_grid = np.zeros(shape=(self.w, self.h))

        self.speed = speed

    def displaying_lines(self) -> None:
        """
        Рисуем сетку

        Получим поле, разбитое на self.w * self.h клеток
        """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def create_grid(self, randomize: bool = True) -> np.ndarray:
        """
        Создаем матрицу, в которой будет заложено первоначальное состояние системы (0 и 1).

        Parametrs:
        -------------
        randomize: bool - по умолч. True - состояние генерируется случайно. False - ввод вероятностей появления 1 и 0
        ## Сумма вероятностей 0 и 1 строго равна единице

        Return:
        -------------
        grid: np.ndarray - матрица первоначального состояния
        """

        if randomize == True:
            grid = np.random.randint(0, 2, (self.h, self.w))
            return grid
        else:
            first_proba = input('Введите вероятность появления 1 ')
            zeros_proba = input('Введите вероятность появления 0 ')
            while float(first_proba) + float(zeros_proba) != 1:
                print('Сумма вероятностей должна быть равна 1')
                first_proba = input('Введите вероятность появления 1 ')
                zeros_proba = input('Введите вероятность появления 0 ')
            grid = np.random.choice((0,1), size=(self.h, self.w), replace=True, p=(zeros_proba, first_proba))
            return grid

    def draw_grid(self, grid) -> None:
        """
        Раскраска клеток, в которых есть жизнь
        """
        for y in range(0, self.w):
            for x in range(0, self.h):
                if grid[y][x] == 1:
                    pygame.draw.rect(self.screen, color = pygame.Color('red'), rect = (self.cell_size * x, self.cell_size * y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, color = pygame.Color('white'), rect = (self.cell_size * x, self.cell_size * y, self.cell_size, self.cell_size))

    def next_gen_info(self, cell: tuple, grid: np.ndarray) -> np.array:
        """
        Возвращает информацию о том, что случится с клеткой в следующем поколении согласно правилам игры

        Parameters
        ----------
        cell : tuple - кортеж коррдинат клеток, для которой необходимо получить состояние следующего поколения

        Returns
        ----------
        1 - останется жива или зародится новая жизнь
        0 - умрет или клетка остается пустой
        """
        self.cell = cell
        count = 0
        for i in range(self.cell[1] - 1, self.cell[1] + 2):
            for j in range(self.cell[0] - 1, self.cell[0] + 2):
                if grid[i][j] == 1:
                    count += 1

        if grid[self.cell[0]][self.cell[1]] == 1:
            count -= 1
            if count == 2 or count == 3:
                return 1
            return 0
        else:
            if count == 3:
                return 1
            return 0

