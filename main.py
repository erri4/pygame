import pygame as game  
from os.path import join
import random


game.init() 
screen = game.display.set_mode()
width, height = screen.get_size()[0] - 100, screen.get_size()[1] - 100
display = game.display.set_mode((width, height), game.RESIZABLE)
game.display.set_caption("reef and liam's game") 


speed = 10
running = True
clock = game.time.Clock()


player_surf = game.Surface((100,200)) 
player_surf.fill("orange")
player_direction = game.math.Vector2()
player_speed = 300


player = game.image.load(join("5games", "space shooter", "images", "player.png")).convert_alpha()
player_rect= player.get_frect(center = (width / 2,height / 2)) 
object = game.image.load(join("5games", "space shooter", "images", "star.png")).convert_alpha()
object_positions = [(random.randint(0 , width),random.randint(0,height)) for i in range (20)]
meteor = game.image.load(join("5games", "space shooter", "images", "meteor.png"))
meteor_rect = meteor.get_frect(center = (width / 2,height /2))
laser = game.image.load(join("5games", "space shooter", "images", "laser.png"))
laser_rect = laser.get_frect(bottomleft = ( 20 ,height - 20))

while running:
    dt = clock.tick() / 1000
    for event in game.event.get(): 
        if event.type == game.QUIT:
            running = False
        

    keys = game.key.get_pressed()
    player_direction.x = int(keys[game.K_RIGHT]) - int(keys[game.K_LEFT])
    player_direction.y = int(keys[game.K_DOWN]) - int(keys[game.K_UP])
    player_direction = player_direction.normalize() if player_direction else player_direction  
    player_rect.center += player_direction * player_speed * dt 
    recent_keys = game.key.get_just_pressed()
    a = recent_keys[game.K_SPACE]
    if a:
        print("fire laser")
    display.fill("grey")
    for pos in object_positions:
        display.blit(object, pos)
    display.blit(meteor,(meteor_rect))  
    display.blit(laser,(laser_rect))
    
           
    display.blit(player,(player_rect)) 
    game.display.update()

game.quit()