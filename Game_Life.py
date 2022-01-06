import pygame ## библиотека для окна с графикой
import numpy as np ## для работы с матрицами
from pygame.locals import QUIT ## при нажатии на выход работа программы остановиться
import time

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
            print('используйте разделитель - точку')
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

    def get_next_generation(self, grid: np.ndarray) -> np.ndarray:
        """
        Используя метод next_gen_info, мы получим информацию следующего состояния о каждой клетке. 

        В этом методе мы запускаем next_gen_info для всех клеток и формируем матрицу следующего состояния

        Parametrs:
        ----------
        grid: np.ndarray - матрица текущего состояния

        Returns
        ----------
        self.next_generation - матрица следующего состояния
        """
        for x in range(1, self.width // self.cell_size - 1):
            for y in range(1, self.height // self.cell_size - 1):
                self.next_generation_grid[x][y] = self.next_gen_info(cell = (x, y), grid = grid)
        return self.next_generation_grid

    def run(self, grid: np.ndarray) -> None:
        """
        Запуск игры

        Parametrs:
        ----------
        grid: np.ndarray - матрица первоначального состояния

        Return:
        ----------
        Игровое поле с симуляцией жизни
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Life')
        self.screen.fill(pygame.Color('black'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid(grid)
            self.displaying_lines()
            grid = self.get_next_generation(grid = grid)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


width = 400
height = 400
cell_size = 10
speed = 10

def params_setting() -> None:
    """
    Функция для изменения параметров игры
    """
    global width, height, cell_size, speed
    param = input('Хотите изменить параметры игры? \nДа - True \nНет - False\n')
    while (param != 'True') and (param != 'False'):
        print('Упс! Проверьте правильность ввода')
        time.sleep(1)
        param = input('Хотите изменить параметры игры? \nДа - True \nFalse\n')

    while param == 'True':
        settings = input('\n\nВыберите что хотите изменить: \nШирина окна - 1\nВысота окна - 2\nРазмер клетки - 3\nСкорость игры - 4\nВернуться назад - break\n')
        if settings == '1':
            width = input('Введите ширину окна\n')
        elif settings == '2':
            height = input('Введите высоту окна\n')
        elif settings == '3':
            cell_size = input('Введите размер клетки\n')
        elif settings == '4':
            speed = input('Введите скорость игры\n')
        if settings == 'break':
            break
    
def grid_init() -> None:
    """
    Функция для инициализации матрицы первоначального состояния
    """
    global answer
    answer = input('\n\n\nВыберите тип формирования матрицы: \nСлучайно - True\nСам задам вероятности - False\n')
    while (answer != 'True') and (answer != 'False'):
        print('Упс! Проверьте правильность ввода')
        time.sleep(1)
        answer = input('Выберите тип формирования матрицы: \nСлучайно - True\nСам задам вероятности - False\n')

def start_game() -> None:
    """
    Запускаем игру

    """
    global answer, game
    game = GameLife(width, height, cell_size, speed)

    if answer == 'True':
        grid = game.create_grid()
    else:
        grid = game.create_grid(randomize=answer)
    game.run(grid)

params_setting()
grid_init()
start_game()

print('\n\nNice to meet u. bye')
time.sleep(5)