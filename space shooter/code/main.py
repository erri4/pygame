import pygame as game  
from os.path import join
import random


class Player(game.sprite.Sprite): 
    def __init__(self, groups): 
        super().__init__(groups)
        self.image = game.image.load(join("images", "player.png")).convert_alpha()  
        self.rect = self.image.get_frect(center = (width / 2,height / 2)) 
        self.player_direction = game.math.Vector2() 
        self.player_speed = 400
        
        #cooldown 
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200
        

        # mask
        self.mask = game.mask.from_surface(self.image)



    def laser_timer(self):
        if not self.can_shoot:
            current_time = game.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                 self.can_shoot = True

    def update(self,dt):
        keys = game.key.get_pressed() 
        self.player_direction.x = int(keys[game.K_RIGHT]) - int(keys[game.K_LEFT])
        self.player_direction.y = int(keys[game.K_DOWN]) - int(keys[game.K_UP]) 
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction 
        self.rect.center += self.player_direction * self.player_speed * dt 

        recent_keys = game.key.get_just_pressed() 
        if recent_keys[game.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites,laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = game.time.get_ticks()
            laser_sound.play()
        self.laser_timer()
        
class Star(game.sprite.Sprite): 
    def __init__(self,groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center =(random.randint(0,width),random.randint(0, height)))
        
class Laser(game.sprite.Sprite): 
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self,dt): 
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
        self.image = game.transform.rotate(laser_surf, 90)

class Meteor(game.sprite.Sprite): 
    def __init__(self, surf, pos ,groups):
        super().__init__(groups)
        self.original_surface = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = game.time.get_ticks()
        self.life_time = 3000
        self.direction = game.Vector2(random.uniform(-0.5, 0.5) ,1)
        self.speed = random.randint(400,500)
        self.rotation_speed = random.randint(40,80)
        self.rotation = 0
        
        
    def update(self, dt): 
        self.rect.center += self.direction * self.speed * dt
        if game.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = game.transform.rotozoom(self.original_surface, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class MeteorAnimatedExplosion(game.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

def display_score():
    global bonus_points, b, display_bonus, bonus_start_time, bonus_display_time

    # setting the score
    current_time = game.time.get_ticks() // 100
    bonus_points = current_time + b 
    text_surf = score_font.render(str(current_time), False, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom=(width / 2, height - 50))
    display_surface.blit(text_surf, text_rect)
    game.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 20).move(0, -8), 7, 10)

    # setting bonus score
    text_surf1 = bonus_score_font.render("+Bonus 20 Points!",False,(240, 240, 240))
    text_rect1 = text_surf1.get_frect(midbottom =((width / 2)-5, height -110))
    if display_bonus:
        display_surface.blit(text_surf1,text_rect1)
        if bonus_start_time == 0:  
            bonus_start_time = game.time.get_ticks()
        if game.time.get_ticks() - bonus_start_time > bonus_display_time:
            display_bonus = False  
            bonus_start_time = 0          
        
def collisions():
    global running, b, display_bonus

    # checking for collision between the player and the meteor
    collision_sprite = game.sprite.spritecollide(player, meteor_sprites, True, game.sprite.collide_mask)
    if collision_sprite:
        running = False

    # checking for collision betwwen the laser and the meteor
    for laser in laser_sprites:
        collided_sprite = game.sprite.spritecollide(laser, meteor_sprites, True, game.sprite.collide_mask)
        if collided_sprite:
            b += 20
            display_bonus =True
            laser.kill()
            MeteorAnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

# general setup 
game.init() 
width, height = 1280, 720 
display_surface = game.display.set_mode((width, height), game.RESIZABLE) 
game.display.set_caption("space shooter") 
speed = 10
running = True
clock = game.time.Clock()

# game variables
random_number = random.randint(1,10)
display_bonus = False
bonus_points = 0
b = 0
bonus_display_time = 500  
bonus_start_time = 0

# image imports 
star_surf = game.image.load(join("images", "star.png")).convert_alpha()
meteor_surf = game.image.load(join("images", "meteor.png")).convert_alpha()
laser_surf = game.image.load(join("images", "laser_assets",f"{random_number}.png")).convert_alpha()
score_font = game.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
bonus_score_font = game.font.Font(join('images','Oxanium-Bold.ttf'), 25)
explosion_frames = [game.image.load(join('images','explosion', f'{pictures}.png')).convert_alpha() for pictures in range(21)]

# sound imports
laser_sound = game.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.25)
explosion_sound = game.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.1)
game_music = game.mixer.Sound(join('audio', 'game_music.wav'))

# volume setting
game_music.set_volume(0.4)
game_music.play(loops = -1 )

# sprites
all_sprites = game.sprite.Group()
meteor_sprites = game.sprite.Group()
laser_sprites = game.sprite.Group()
for i in range(30):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# custom event (timer) 
meteor_event = game.event.custom_type()
game.time.set_timer(meteor_event, 300)


while running: 
    dt = clock.tick() / 1000
    #event loop
    for event in game.event.get(): 
        if event.type == game.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0, width), random.randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))
    # Updates all sprites in the game
    all_sprites.update(dt)
    collisions()

    # draw the game
    display_surface.fill('#000000') 
    display_score()     
    all_sprites.draw(display_surface)
    

    game.display.update() 


game.quit()