#!/usr/bin/python3

import pygame
from constant import *
from sys import exit

class Item(object):

    def __init__(self, x, y, img_asset_path):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.is_visiable = True
        if img_asset_path:
            try:
                self.img = pygame.image.load(img_asset_path)
                self.size = {"x" : self.img.get_width(), 
                             "y" : self.img.get_height()}
            except TypeError:
                print("Error: Unable to load Image")
                exit(-1)
        else:
            self.img = None
            self.size = None

            
    def set_img(self, img):
        self.img = img;
        self.size = {"x" : self.img.get_width(), 
                     "y" : self.img.get_height()}

    def update_position(self):
        self.x += self.x_speed
        self.y += self.y_speed
        return self.boundary_check()

    def get_position(self):
        return (self.x,self.y)

    def boundary_check(self):
        pass
        return True

    def in_collision(self, other):
        if( self.x + self.size["x"] >= other.x and self.x <= other.x + other.size["x"] ):
            if( self.y + self.size["y"] >= other.y and self.y <= other.y + other.size["y"] ):
                return True

        return False

class Spaceship(Item):

    def boundary_check(self):
        if(self.x < 0):
            self.x = 0
        elif(self.x > 736) :
            self.x = 736

        return True

class EnemyLot(object):

    def __init__(self, x, y, img_asset_path):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.enemies = []

        # load image
        img = pygame.image.load(img_asset_path)
        self.enemy_size =  {"x" : img.get_width(), 
                            "y" : img.get_height()}
        self.spaceing   =  {"x" : img.get_width()  + 16,
                            "y" : img.get_height() + 16}

        for i in range(9):
            enemy = Item(x + (i % 3) * self.spaceing["x"],  y + (i // 3) * self.spaceing["y"], None)
            enemy.set_img(img)
            self.enemies.append(enemy)

    def update_position(self):
        self.x += self.x_speed
        self.y += self.y_speed

        for idx, enemy in enumerate(self.enemies):
            enemy.x = self.x + ( idx % 3 )  * self.spaceing["x"]
            enemy.y = self.y + ( idx // 3 ) * self.spaceing["y"]

        return self.boundary_check()

    def draw(self, screen):
        for enemy in self.enemies:
            if(enemy.is_visiable):
                screen.blit(enemy.img, enemy.get_position())

    def boundary_check(self):
        if(self.x < 0):
            self.x_speed = 1
            self.x = 0
            self.y += 20
        elif(self.x > (800 - (self.spaceing["x"] * 3))) :
            self.x_speed = -1 
            self.x = (800 - (self.spaceing["x"] * 3))
            self.y += 20

    def detect_collision(self, bullets):
        for bullet in bullets:
            for enemy in self.enemies:
                if(enemy.is_visiable and enemy.in_collision(bullet)):
                    enemy.is_visiable = False
                    bullets.remove(bullet)
                    break

        for enemy in self.enemies:
            if(enemy.is_visiable):
                return False

        return True


class Bullet(Item):
    def boundary_check(self):
        if(self.x < 0 or 
           self.x > SCREEN_WIDTH or
           self.y < 0 or
           self.y > SCREEN_HEIGHT):
            return False

        return True


class SpaceInvaders(object):

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.player = Spaceship(370, 480, "img/spaceship.png")
        self.enemy  = EnemyLot(370, 50, "img/astroid.png")
        self.enemy.x_speed = 1

        self.running = True
        self.game_over = False
        self.won = False

        self.bullets = []

    def handle_event(self):
        for event in pygame.event.get():
            if( event.type == pygame.QUIT ):
                self.running = False

            if( event.type == pygame.KEYDOWN ) :
                if( event.key == pygame.K_RIGHT):
                    self.player.x_speed = 1
                elif( event.key == pygame.K_LEFT):
                    self.player.x_speed = -1
                elif( event.key == pygame.K_SPACE):
                    bullet = Bullet(self.player.x + 16, self.player.y + 10, "img/missile.png")
                    bullet.y_speed = -1
                    self.bullets.append(bullet)

            if( event.type == pygame.KEYUP ) :
                if( (event.key == pygame.K_RIGHT) or (event.key == pygame.K_LEFT) ):
                    self.player.x_speed = 0
        

    def run(self):
        while self.running:
            self.screen.fill((0,0,150))

            self.handle_event()

            self.player.update_position()
            self.enemy.update_position()

            for bullet in self.bullets:
                in_bound = bullet.update_position()
                if(not in_bound):
                    self.bullets.remove(bullet)

            self.won = self.enemy.detect_collision(self.bullets)

            if(self.enemy.y > 350):
                self.game_over = True

            if(self.won):
                print("Won!!!")
                exit(0)
            if(self.game_over):
                print("GameOver!!!")
                exit(0)

            self.screen.blit(self.player.img, self.player.get_position())
            self.enemy.draw(self.screen)

            for bullet in self.bullets:
                self.screen.blit(bullet.img, bullet.get_position())

            # print(f"bullet count = {len(self.bullets)}")

            pygame.display.update()


game = SpaceInvaders()
game.run()
