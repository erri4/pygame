# Imports
import pygame as game  
from os.path import join
import random

# general setup
game.init() # Initializes all Pygame modules.
width, height = 1280, 720 # Sets the dimensions of the game window.
display = game.display.set_mode((width, height), game.RESIZABLE) # Creates the game window with the specified size and makes it resizable.
game.display.set_caption("reef and liam's game") # Sets the title of the window.

# Game Variables
speed = 10
running = True
clock = game.time.Clock()

# Creating a Player Surface
player_surf = game.Surface((100,200)) # We create a surface for the player and fill it with an orange color.
player_surf.fill("orange")
player_direction = game.math.Vector2(1,0.3)
player_speed = 300

#importing an image
player = game.image.load(join("5games", "space shooter", "images", "player.png")).convert_alpha()  # Loads images for the player 
player_rect= player.get_frect(center = (width / 2,height / 2)) # sets the player position in this case its in the center
object = game.image.load(join("5games", "space shooter", "images", "star.png")).convert_alpha()
object_positions = [(random.randint(0 , width),random.randint(0,height)) for i in range (20)]
meteor = game.image.load(join("5games", "space shooter", "images", "meteor.png"))
meteor_rect = meteor.get_frect(center = (width / 2,height /2))
laser = game.image.load(join("5games", "space shooter", "images", "laser.png"))
laser_rect = laser.get_frect(bottomleft = ( 20 ,height - 20))

while running:
    #event loop
    dt = clock.tick() / 1000
    for event in game.event.get(): #checks for events if user closes this window we running to be false
        if event.type == game.QUIT:
            running = False
    
    # draw the game
    display.fill("grey") #We fill the background with grey and draw the stars, meteor, and laser on the display.
    for pos in object_positions:
        display.blit(object, pos)
    display.blit(meteor,(meteor_rect))  
    display.blit(laser,(laser_rect))
    
    # Player Movement
    player_rect.center += player_direction * player_speed * dt
    if player_rect.right >= width:
        player_direction = -player_direction
    # player rendering        
    display.blit(player,(player_rect)) # Draws the player image at the updated position.
    game.display.update() # Refreshes the display to show the latest changes.

# Quit Pygame
game.quit()        