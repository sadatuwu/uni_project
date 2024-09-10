#channel coding with Russ : Space Invaders
import sys
import random
import pygame
from time import sleep
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.sprite import spritecollide
from pygame.sprite import collide_mask
from pygame import mixer

pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)  #~~#~~default parameters
mixer.init()

    
#~~~~define fps
clock = pygame.time.Clock()
fps = 60




screen = pygame.display.set_mode()#(800,500), RESIZABLE)
screen_width , screen_height = screen.get_size()
pygame.display.set_caption("FIRST GAME, UWU ")



#~~~~load sounds:
explosion1_fx = pygame.mixer.Sound("sound/explosion1.wav")
explosion1_fx.set_volume(0.1)

explosion2_fx = pygame.mixer.Sound("sound/explosion2.wav")
explosion2_fx.set_volume(0.1)

laser_fx = pygame.mixer.Sound("sound/laser.wav")
laser_fx.set_volume(0.25)



#~~~~define game global variables:
points = 0

#~~~~my shot
max_bullet = 10
#~~~~alien shot
max_alien_bullets = 30
alien_cooldown = 500 #miliseconds
last_alien_shot = pygame.time.get_ticks()

#~~~~define colors:
red = (255, 0,0)
green = (0,255,0)


#~~~~load image:




#~~~~create spaceship class
class Spaceship(Sprite):
    def __init__(self, x, y, health, alien):
        super().__init__()

        self.alien = alien
        self.image = pygame.image.load("image/spaceship.bmp")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y] ##new syntax
        self.health_start = health
        self.health_remaining = 3 #health
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        #~~~~set movement speed:
        speed = 8
        #~~~~set bullet cooldown:
        cooldown = 100  #in miliseconds

        
        #~~~~get key press
        key = pygame.key.get_pressed() ##new syntax

        if key[pygame.K_LEFT] and self.rect.left > 0 :
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
        #~~#~~my personal addition
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        
        #~~~~shotting:
        #~~~~record current time:
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and (time_now - self.last_shot)> cooldown and len(bullet_group)<max_bullet:  #~~#~~ can't shot another bullet before cooldown
            laser_fx.play()
            bullet=Bullets(self.rect.centerx, self.rect.top, self.alien)
            bullet_group.add(bullet)
            self.last_shot = time_now #~~#~~resets cooldown


        #~~~~creating_mask
        self.mask = pygame.mask.from_surface(self.image)
        #~~#~~mask basically only captures the pixels of the image , not the whole rectangle
        
        
        #~~~~draw helth bar:
        pygame.draw.rect(screen, red, (self.rect.x+5, (self.rect.bottom-5), self.rect.width-10, 5))
        if self.health_remaining > 0.5:
            pygame.draw.rect(screen, green, (self.rect.x+5, (self.rect.bottom-5), (self.rect.width-10)*(self.health_remaining/self.health_start), 5))

        #~~~~spaceship dead:
        elif self.health_remaining<=0:
            explosion1_fx.play()
            self.kill()
            

        
#~~~~create bullet class
class Bullets(Sprite):
    def __init__(self, x, y, alien):
        super().__init__()
        self.alien = alien

        self.image = pygame.image.load("image/my_bullet.bmp")
        #self.color = (50,50,50)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        #self.rect = pygame.Rect( x, y, 5, 20)


    def update(self):
        global points
        speed=5
        self.rect.y -= speed
        if self.rect.bottom < 1 * self.alien.rect.height:
            self.kill()  #~~#~~kills only that specific bullet that's out of screen

        if spritecollide(self, alien_group, True):
            explosion1_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            self.kill()
            points += 1
            

        
        
#~~~~create aliens class
class Aliens(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("image/alien.bmp") #~~#~~Skip: randomly choosing alien image: part4, 1:30
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction =1
        self.y = float(self.rect.y)
        self.screen_rect = screen.get_rect()
        self.x = float(self.rect.x)



    def get_alienNumberX (self):
        available_space_x = screen_width - 2 * self.rect.width
        number_alien_x = int(available_space_x / (2 * self.rect.width))
        return number_alien_x

    


    def update(self):
        self.rect.x  += self.move_direction

        #~~#~~personal addition,
        self.y +=0.2
        self.rect.y = self.y
        
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

        for _alien in alien_group.sprites():
            if spritecollide(_alien, spaceship_group, False):
                explosion1_fx.play()
                explosion = explosion = Explosion(spaceship.rect.centerx, spaceship.rect.centery, 3)
                explosion_group.add(explosion)
                spaceship.health_remaining = 0
        if self.rect.top > screen_height:
            self.kill()
            


#~~~~create Alien_Bullet class
class Alien_Bullets(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("image/alien_bullet.bmp")
        #self.color = (50,50,50)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        #self.rect = pygame.Rect( x, y, 5, 20)


    def update(self):
        speed=2
        self.rect.y += speed
        if self.rect.bottom >  screen_height:
            self.kill()  #~~#~~kills only that specific bullet that's out of screen
        if spritecollide(self, spaceship_group, False, collide_mask):    #~~#~~only collides with the spaceship mask (created in Spaceship update())

            explosion2_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
            self.kill()
            spaceship.health_remaining -=0.5
        
        if spaceship.health_remaining < 0.5:
            if spritecollide(self, spaceship_group, False):
                explosion = explosion = Explosion(spaceship.rect.centerx, spaceship.rect.centery, 3)
                explosion_group.add(explosion)
                spaceship.health_remaining = 0

        '''
        if len(spaceship_group)==0:
            sleep(2)
            run = False
        '''  
        

#~~~~create Explosion class:
class Explosion(Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        
        self.images = []  #emptylist

        for num in range(1,3):
            img = pygame.image.load(f"image/exp{num}.bmp")
            if size == 1:
                img = pygame.transform.scale(img, (20,20))
            if size == 2:
                img = pygame.transform.scale(img, (40,40))
            if size == 3:
                img = pygame.transform.scale(img, (100,100))

            #add image to the list
            self.images.append(img)
        #outofloop

        self.index = 0           
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosion_speed = 5
        #explosion animation
        self.counter +=1

        if self.counter >= explosion_speed and (self.index < len(self.images)-1):
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #remove explosion after animation complete
        if (self.index >= len(self.images)-1) and (self.counter >=explosion_speed):
            self.kill()


       

#~~~~~~~~~~~~~~~MAIN :

#~~~~create sprite groups
spaceship_group = Group()
bullet_group = Group()
alien_group = Group()
alien_bullet_group = Group()
explosion_group = Group()


#~~~~create alien:

rows=1
def create_aliens():
    global rows
    alien = Aliens(0,0)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    for row in range (rows):
        for column in range(alien.get_alienNumberX()):
            alien = Aliens(0,0)
            alien.x = alien_width + 2 * alien_width * column
            alien.rect.x = alien.x
            alien.y = -alien_height*rows + row*70
            alien.rect.y = alien.rect.y
            alien_group.add(alien)



#create_aliens() 



#~~~~create alien bullets:
def create_alien_bullets():
    global last_alien_shot
    time_now = pygame.time.get_ticks()
    #shooting:
    if (time_now - last_alien_shot > alien_cooldown) and (len(alien_bullet_group)<max_alien_bullets) and (len(alien_group)>0)  :
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------


'''
def create_Alien():
    alien.x = self.alien_width + 2 * self.alien_width * alien_number
    alien.rect.x = alien.x
    self.alien_fleet.add(alien)



def create_alienFleet(self):
    # Create the first row of aliens.
    #self.alien_fleet.add(self.alien)
        
    for alien_number in range(self.get_alienNumberX()):
            
        self.create_Alien(alien_number)



'''
def check_game_exit():
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE :
            pygame.quit()
            sys.exit()



def wave_message(rows):

    font = pygame.font.Font('image/game_font.ttf', 100)
    text = font.render(f'wave {rows}', False, (255,255,255))
    rect = text.get_rect()
    rect.center = (screen_width//2 , screen_height//2 -50)
    screen.blit(text, rect)
    pygame.display.flip()

def countdown(text, timer):
    font = pygame.font.Font('image/game_font.ttf', 50)
    text = font.render(text, False, (255,255,255))
    rect = text.get_rect()
    rect.center = (screen_width//2 , screen_height//2 + 50)
    screen.blit(text, rect)
    pygame.display.flip()

def show_points(): #need_bg is either True or False
    global points
    font = pygame.font.Font('image/game_font.ttf', 30)
    text = font.render(f'{points}', True, (255,0,0))  
    rect = text.get_rect()
    screen.blit(text, rect)




#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
alien= Aliens(0,0)
#~~~~create spaceship
health=3
spaceship = Spaceship(int(screen_width/2) , screen_height -70, health, alien)
spaceship_group.add(spaceship)



bg = pygame.image.load("image/bg.bmp")
bg = pygame.transform.scale(bg, (screen_width, screen_height))


#run = True
while True:
    
    screen.blit(bg, (0,0))
    clock.tick(fps)
    
    #'''
    if len(alien_group)==0:
        alien_bullet_group.empty()
        timer =3
        while timer>0:
            check_game_exit()
            screen.blit(bg, (0,0))
            spaceship_group.draw(screen)
            wave_message(rows)
            #pygame.display.flip()
            countdown(f'Starts in : {timer}', timer)
            sleep(1)
            timer -=1
            
        create_aliens()
        rows += 1
    #'''
    show_points()       

    

    

    #~~~~create random alien bullets:
    create_alien_bullets()
    
    
    #~~~~event handlers
    check_game_exit()



    #~~~~update spaceship:
    spaceship.update()

    #~~~~update sprite group:
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()
    explosion_group.update()
    

    #~~~~draw sprite groups:
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

        

    #print(len(bullet_group))

    #~~~~refreshing display
    pygame.display.flip()
    
    if len(spaceship_group)==0:
        break
    #pygame.display.update()

#outofloop:

#print("outofloop")
sleep(2)

#---------------------

timer =10
while timer >0:
    check_game_exit()
    screen.blit(bg, (0,0))
    font1 = pygame.font.Font('image/game_font.ttf', 100)
    text1 = font1.render(f'TOTAL SCORE : {points}', True, (255,255,255))
    rect1 = text1.get_rect()
    rect1.center = (screen_width//2 , screen_height//2 - 100)
    screen.blit(text1, rect1)

    font2 = pygame.font.Font('image/game_font.ttf', 20)
    text2 = font2.render('PRESS ESC TO QUIT', True, (255,255,255))
    rect2 = text2.get_rect()
    rect2.center = (screen_width//2 , screen_height//2 + 200)
    screen.blit(text2, rect2)
    
    pygame.display.flip()
    countdown(f'Game ends in: {timer}', timer)
    sleep(1)
    timer -=1



pygame.quit()
sys.exit()
