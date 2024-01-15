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

hero1 = pygame.image.load("data\\cat3.png").convert_alpha()
hero2 = pygame.image.load("data\\cat4.png").convert_alpha()
bulletpicture = pygame.image.load("data\\bullet.png").convert_alpha()
bulletpicture = pygame.transform.scale(bulletpicture, (5, 21))

shot = pygame.mixer.Sound("data\\shot.wav")
reload_gun = pygame.mixer.Sound("data\\reload.wav")
out_bullets = pygame.mixer.Sound("data\\out_pistol.wav")

d = {}
for x in range(1, 6):
    d["bg{0}".format(x)] = pygame.transform.scale(
        pygame.image.load(f"paw_bg{x}.png").convert_alpha(), (WIDTH, HEIGHT)
    )
hero_x, hero_y = WIDTH // 2, HEIGHT // 2


def start_screen():
    fon = pygame.transform.scale(
        pygame.image.load("fon.jpg").convert_alpha(), (WIDTH, HEIGHT)
    )
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(1)


class Target:
    # движущаяся или статичная, номер дорожки
    def __init__(self, shoot_range, moving=False):
        self.moving = moving

    def hit(self, shoot_range):
        ...

    def spawn(self):
        ...


class HeroCat:
    # счёт, открытые тиры
    def __init__(self, score, shoot_ranges):
        self.score = score
        self.shoot_ranges = shoot_ranges

    def add_score(self):
        # Guest(, )
        # if Target.moving:
        # points =
        # else
        # points = * 2
        # workWithDB.add_score(username, )
        ...


class Bullet:
    # разброс(пикс.), координаты появления((x0, y0))
    # разброс будет больше в 2 раза, т.к. может быть -(влево) и +(вправо)
    def __init__(self, spread, coords):
        self.coords = (random.range(coords[0] - spread, coords[0] + spread), HEIGHT)

    def remove():
        ...


class Button:
    def __init__(self):
        self.btn = 0


start_screen()

shoot_ranges = 0
if not os.path.isfile("progress.db"):
    WorkWithDB.create_database()
    WorkWithDB.add_elem("aksenianets", [0, 0])
    HeroCat(0, 0)
else:
    info = [x for x in WorkWithDB.load_info("aksenianets")][0]
    shoot_ranges = info[1]
    HeroCat(info[0], info[1])

running = True
bullets = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if len(bullets) <= 7:
                shot.play()
                bullets.append([hero_x + 20, hero_y - 15])
            else:
                out_bullets.play()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reload_gun.play()
                bullets = []

    key_pressed_is = pygame.key.get_pressed()

    if key_pressed_is[K_a]:
        if hero_x - 5 >= 0:
            hero_x -= 5
    if key_pressed_is[K_d]:
        if hero_x + 5 <= WIDTH - 80:
            hero_x += 5
    if key_pressed_is[K_w]:
        if hero_y - 5 >= 0:
            hero_y -= 5
    if key_pressed_is[K_s]:
        if hero_y + 5 <= HEIGHT - 80:
            hero_y += 5

    mx, my = pygame.mouse.get_pos()

    for b in range(len(bullets)):
        bullets[b][1] -= 10

    for bullet in bullets[:]:
        if bullet[0] < 0:
            bullets.remove(bullet)

    screen.fill(pygame.Color(0, 0, 0))
    screen.blit(d[f"bg{shoot_ranges + 1}"], (0, 0))
    screen.blit(hero1, (hero_x, hero_y))
    for bullet in bullets:
        screen.blit(bulletpicture, pygame.Rect(bullet[0], bullet[1], 0, 0))

    pygame.display.flip()
    clock.tick(60)
