import pygame ## библиотека для окна с графикой
import numpy as np ## для работы с матрицами
from pygame.locals import QUIT ## при нажатии на выход работа программы остановиться


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
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.color('white'), (x, 0), (x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('white'), (0, y), (self.width, y)
    
    

