### Imports ####
import pygame
from framework.scripts.entities.particleclass import Particle
from errors import ObjNameError


#### Class(es) ####
class EnemyManager:
    def __init__(self):
        self.enemy_list = {}

    def add_chef(self, name, enemy):
        if name not in self.enemy_list.keys():
            self.enemy_list[name] = enemy
        else:
            raise ObjNameError(name, "A chef already exists with this name lol")
    
    def remove_chef(self, name):
        if name in self.enemy_list.keys():
            del self.enemy_list[name]
        else:
            raise ObjNameError(name, "No chef with this name exists")

    def remove_all_enemies(self):
        self.enemy_list = {}

    def display_chefs(self, surf, scroll, color=(255,0,0)):
        for i in self.enemy_list:
            self.enemy_list[i].display_chef(surf, scroll)
    
    def animate_chefs(self, frames):
        for i in self.enemy_list:
            self.enemy_list[i].animate(frames)

    def move_chefs(self, rect_list):
        for i in self.enemy_list:
            self.enemy_list[i].move(rect_list)
    
    def collide_player(self, player, part_list, scroll):
        for en in self.enemy_list:
            if player.hit_rect.colliderect(self.enemy_list[en].hit_rect):
                player.current_hp -= 1
                part_list.add_particle(Particle([self.enemy_list[en].hit_rect[0], self.enemy_list[en].hit_rect[0]], 5))
                

class Chef:
    def __init__(self, pos, img, rect=(10, 10), move_h=True):
        if type(img) != list:
            self.img = None
            self.hit_rect = pygame.Rect(pos[0], pos[1], rect[0], rect[1])
            self.collide_rect = pygame.Rect(self.hit_rect.left, self.hit_rect.bottom - size[1] // 2, size[0], size[1] // 2)
        else:
            self.imgs = img
            self.img = self.imgs[0]
            self.hit_rect = pygame.Rect(pos[0], pos[1], self.img.get_width(), self.img.get_height())
            self.collide_rect = pygame.Rect(self.hit_rect[0], self.hit_rect.bottom - self.img.get_height() // 2, self.img.get_width(), self.img.get_height() // 2)
        self.current_frame = 0
        self.anim_frame = 0
        self.move_h = move_h
        if self.move_h:
            self.movement = [1, 0]
        else:
            self.movement = [0, -1]
    
    def display_chef(self, surf, scroll, color=(255, 0, 0)):
        if type(self.img) != pygame.Surface:
            pygame.draw.rect(surf, color, (self.hit_rect[0] - scroll[0], self.hit_rect[1] - scroll[1], self.hit_rect[2], self.hit_rect[3]))
        else:
            surf.blit(self.img, (self.hit_rect[0] - scroll[0], self.hit_rect[1] - scroll[1]))
    
    def animate(self, frames):
        self.img = self.imgs[self.anim_frame]
        if self.current_frame == frames:
            self.anim_frame += 1
            self.current_frame = 0
        else:
            self.current_frame += 1
        if self.anim_frame >= len(self.imgs):
            self.anim_frame = 0  
    
    def move(self, rect_list):
        if self.movement[0] != 0:
            self.collide(rect_list)
        if self.movement[1] != 0:
            self.collide(rect_list)

    def collide(self, rectlist):
        if self.move_h:
            self.hit_rect[0] += self.movement[0]
            self.collide_rect[0] += self.movement[0]
        else:
            self.hit_rect[1] += self.movement[1]
            self.collide_rect[1] += self.movement[1]
        ###########################################
        for rect in rectlist:
            if self.collide_rect.colliderect(rect):
                if self.movement[0] > 0:
                    self.collide_rect.right = rect.left
                    self.hit_rect.right = rect.left
                    self.movement[0] = -self.movement[0]
                elif self.movement[0] < 0:
                    self.collide_rect.left = rect.right
                    self.hit_rect.left = rect.right
                    self.movement[0] = -self.movement[0]
                if self.movement[1] > 0:
                    self.collide_rect.bottom = rect.top
                    self.hit_rect.bottom = rect.top
                    self.movement[1] = -self.movement[1]
                elif self.movement[1] < 0:
                    self.collide_rect.top = rect.bottom
                    self.hit_rect.top = rect.bottom - self.hit_rect[3] // 2
                    self.movement[1] = -self.movement[1]