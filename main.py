import pygame as game


icon = game.image.load('reef.jpg')
player = game.image.load('5games/space shooter/images/player.png')
game.init()
width, height = 640, 310

display = game.display.set_mode((width, height), game.RESIZABLE)
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

    display.fill((0, 255, 0))
    display.blit(surf, (100, 150))
    game.display.update()

game.quit()
