import time
import pygame
import random
import ctypes
import os.path
import sqlite3
from pygame.locals import *
import sys, pygame, pygame.mixer
from workWithDB import WorkWithDB

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
WIDTH, HEIGHT = screensize[0], screensize[1]

pygame.init()

pygame.display.set_caption("Paw-paw")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# загрузка изображений
hero1 = pygame.image.load("data\\images\\cat1.png").convert_alpha()
hero2 = pygame.image.load("data\\images\\cat2.png").convert_alpha()
bulletpicture = pygame.image.load("data\\images\\bullet.png").convert_alpha()
bulletpicture = pygame.transform.scale(bulletpicture, (5, 21))

# загрузка звуков
shot = pygame.mixer.Sound("data\\music\\shot.wav")
shot.set_volume(0.4)
reload_gun = pygame.mixer.Sound("data\\music\\reload.wav")
reload_gun.set_volume(0.4)
out_bullets = pygame.mixer.Sound("data\\music\\out_pistol.wav")
out_bullets.set_volume(0.4)
bg_music = pygame.mixer.Sound("data\\music\\bg_music.wav")
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# создание переменных с задним фоном
d = {}
for x in range(1, 5):
    d["bg{0}".format(x)] = pygame.transform.scale(
        pygame.image.load(f"data\\images\\paw_bg{x}.png").convert_alpha(),
        (WIDTH, HEIGHT),
    )
hero_x, hero_y = WIDTH // 2, HEIGHT // 2


# стартовый экран
def start_screen():
    fon = pygame.transform.scale(
        pygame.image.load("data\\images\\fon.jpg").convert_alpha(), (WIDTH, HEIGHT)
    )
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(1)


# класс мишени
class Target:
    # движущаяся или статичная, номер дорожки
    def __init__(self, shoot_range, moving=False):
        self.moving = moving

    def hit(self, shoot_range):
        ...

    def spawn(self):
        ...


# класс главного героя
class HeroCat:
    # счёт, открытые тиры, разброс , магазин пистолета, ценность попадания
    score = 0
    shoot_ranges = 1
    spread = [-1, 3]
    magazine = 7
    price = 1

    def __init__(self, score, shoot_ranges, spread, magazine, price):
        HeroCat.shoot_ranges = shoot_ranges
        HeroCat.score = score
        HeroCat.spread = [int(str(spread)[:-1]), int(str(spread)[-1])]
        HeroCat.magazine = magazine
        HeroCat.price = price


class Button:
    def __init__(self):
        self.btn = 0


# вызов стартового экрана
start_screen()

# проверка наличия БД с прогрессом
# и вызов класса ГГ c обычной/загруженной информацией
shoot_ranges = 0
if not os.path.isfile("data\progress.db"):
    WorkWithDB.create_database()
    WorkWithDB.add_elem("player", [0, 0, -13, 7, 1])
    HeroCat(0, 0, -13, 7, 1)
else:
    info = [x for x in WorkWithDB.load_info("player")][0]
    shoot_ranges = info[1]
    HeroCat(info[0], info[1], info[2], info[3], info[4])

font = pygame.font.Font(None, 30)
running = True
bullets = []


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == MOUSEBUTTONDOWN:
            # стрельба при наличии патронов
            if len(bullets) < HeroCat.magazine:
                shot.play()
                bullets.append([hero_x + 20, hero_y - 15])
            else:
                out_bullets.play()
        elif event.type == pygame.KEYDOWN:
            # перезарядка
            if event.key == pygame.K_r:
                reload_gun.play()
                bullets = []
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    key_pressed_is = pygame.key.get_pressed()

    # передвижение персонажа
    if key_pressed_is[K_a]:
        if hero_x - 5 >= 0:
            hero_x -= 5
    if key_pressed_is[K_d]:
        if hero_x + 5 <= WIDTH - 50:
            hero_x += 5
    if key_pressed_is[K_w]:
        if hero_y - 5 >= 0:
            hero_y -= 5
    if key_pressed_is[K_s]:
        if hero_y + 5 <= HEIGHT - 93:
            hero_y += 5

    mx, my = pygame.mouse.get_pos()

    # обновление позиции пули
    for b in range(len(bullets)):
        bullets[b][1] -= 10
        if b % 2:
            bullets[b][0] += random.randrange(HeroCat.spread[0], HeroCat.spread[1])
        else:
            bullets[b][0] -= random.randrange(HeroCat.spread[0], HeroCat.spread[1])

    for bullet in bullets[:]:
        if bullet[0] < 0:
            bullets.remove(bullet)

    # отрисовка фона, игрока, пулей
    screen.fill(pygame.Color(0, 0, 0))
    screen.blit(d[f"bg{HeroCat.shoot_ranges + 1}"], (0, 0))
    screen.blit(hero1, (hero_x, hero_y))
    for bullet in bullets:
        screen.blit(bulletpicture, pygame.Rect(bullet[0], bullet[1], 0, 0))

    # отображение счёта игрока
    string_rendered = font.render(f"SCORE: {HeroCat.score}", 1, pygame.Color("green"))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 5
    intro_rect.x = 5
    screen.blit(string_rendered, intro_rect)

    pygame.display.flip()
    clock.tick(60)

# обновление информации в БД
HeroCat.spread = int("".join(list(map(str, HeroCat.spread))))
info = [
    HeroCat.score,
    HeroCat.shoot_ranges,
    HeroCat.spread,
    HeroCat.magazine,
    HeroCat.price,
]
WorkWithDB.overwrite("player", info)
