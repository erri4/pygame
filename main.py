import pygame as game
import os
import random


game.init()

width, height = 640, 310

display = game.display.set_mode((width, height), game.RESIZABLE)

icon = game.image.load('reef.jpg').convert()
player = game.image.load(os.path.join('5games', 'space shooter', 'images', 'player.png')).convert_alpha()
star_path = os.path.join('5games', 'space shooter', 'images', 'star.png')

game.display.set_caption("reef and liam's game")
game.display.set_icon(icon)

running = True
surf = game.Surface((100, 100))
surf.fill((255, 0, 0))

while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
            break
    
    if running == False:
        break

    for i in range(20):
        globals()[f'star{i}'] = game.image.load(star_path).convert_alpha()
        display.fill((0, 255, 0))
        pos = (random.randint(0, width), random.randint(0, height))
        display.blit(globals()[f'star{i}'], pos)
    game.display.update()

game.quit()
