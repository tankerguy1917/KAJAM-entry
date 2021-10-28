#### Imports ####
import pygame, random
from framework.scripts.entities.particleclass import Particle


#### Class(es) ####
class TopDownEntity:
    def __init__(self, img, pos, speed, hp, hp_bar_length=100, hp_change_speed=3, size=(10, 10)):
        if type(img) == list:
            self.imgs = img
            self.img = self.imgs[0]
            self.hit_rect = pygame.Rect(pos[0], pos[1], self.img.get_width(), self.img.get_height())
            self.collide_rect = pygame.Rect(self.hit_rect.left, self.hit_rect.bottom - self.img.get_height() // 2, self.img.get_width(), self.img.get_height() // 2)
        else:
            self.imgs = None
            self.img = None
            self.hit_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
            self.collide_rect = pygame.Rect(self.hit_rect.left, self.hit_rect.bottom - size[1] // 2, size[0], size[1] // 2)
        self.movement = [0, 0]
        self.speed = speed
        self.current_hp = hp
        self.max_hp = hp
        self.hp_bar_length = hp_bar_length
        self.hp_change_speed = hp_change_speed
        self.hp_ratio = self.max_hp / self.hp_bar_length
        self.current_frame = 0
        self.anim_frame = 0
        self.ingredient_list = {}
        self.collected = 0
        self.last_collided = [0, 0]
        self.collide_time = 0

    def show_entity(self, surf, hp_pos, st_pos, frames, scroll, part_imgs, show_hp=False, color=(255, 0, 0)):
        x = random.randint(0, 1)
        if type(self.img) != pygame.Surface:
            pygame.draw.rect(surf, color, (self.hit_rect[0] - scroll[0], self.hit_rect[1] - scroll[1], self.hit_rect[2], self.hit_rect[3]))
        else:
            self.animate(frames)
            surf.blit(self.img, (self.hit_rect[0] - scroll[0], self.hit_rect[1] - scroll[1]))
        if show_hp:
            self.show_health_bar(surf, hp_pos)

    def change_anim(self, new_anims):
        self.imgs = new_anims
        self.anim_frame = 0

    def animate(self, frames):
        self.img = self.imgs[self.anim_frame]
        if self.current_frame == frames:
            self.anim_frame += 1
            self.current_frame = 0
        else:
            self.current_frame += 1
        if self.anim_frame >= len(self.imgs):
            self.anim_frame = 0   

    def move(self, rect_list, ing_manager, en_manager, part_manager, scroll):
        if self.movement[0] != 0:
            self.collide(rect_list)
            self.collide_ingredient(ing_manager)
            self.collide_enemy(en_manager, part_manager, scroll)
        if self.movement[1] != 0:
            self.collide(rect_list)
            self.collide_ingredient(ing_manager)
            self.collide_enemy(en_manager, part_manager, scroll)
        


    def collide(self, rectlist):
        self.hit_rect[0] += self.movement[0]
        self.collide_rect[0] += self.movement[0]
        self.hit_rect[1] += self.movement[1]
        self.collide_rect[1] += self.movement[1]
        ###########################################
        for rect in rectlist:
            if self.collide_rect.colliderect(rect):
                if self.movement[0] > 0:
                    self.collide_rect.right = rect.left
                    self.hit_rect.right = rect.left
                if self.movement[0] < 0:
                    self.collide_rect.left = rect.right
                    self.hit_rect.left = rect.right
                if self.movement[1] > 0:
                    self.collide_rect.bottom = rect.top
                    self.hit_rect.bottom = rect.top
                if self.movement[1] < 0:
                    self.collide_rect.top = rect.bottom
                    self.hit_rect.top = rect.bottom - self.hit_rect[3] // 2

    def collide_ingredient(self, ing_manager):
        for ing in list(ing_manager.ingredient_list.keys()):
            if self.hit_rect.colliderect(ing_manager.ingredient_list[ing].rect):
                self.ingredient_list[ing] = ing_manager.ingredient_list[ing].img
                ing_manager.remove_ingredient(ing)
                self.collected += 1
                if self.current_hp < self.max_hp:
                    self.current_hp += 10
    
    def collide_enemy(self, en_manager, part_manager, scroll):
        for en in en_manager.enemy_list:
            if self.hit_rect.colliderect(en_manager.enemy_list[en].hit_rect):
                self.current_hp -= 5
                if self.movement[0] > 0:
                    self.hit_rect.right = en_manager.enemy_list[en].hit_rect.left - 5
                    self.collide_rect.right = en_manager.enemy_list[en].hit_rect.left - 5
                    part_manager.add_particle(Particle([self.hit_rect.right, self.hit_rect.centery], 5))
                if self.movement[0] < 0:
                    self.hit_rect.left = en_manager.enemy_list[en].hit_rect.right + 5
                    self.collide_rect.left = en_manager.enemy_list[en].hit_rect.right + 5
                    part_manager.add_particle(Particle([self.hit_rect.left, self.hit_rect.centery], 5))
                if self.movement[1] > 0:
                    self.hit_rect.bottom = en_manager.enemy_list[en].hit_rect.top - 5
                    self.collide_rect.bottom = en_manager.enemy_list[en].hit_rect.top - 5
                    part_manager.add_particle(Particle([self.hit_rect.bottom, self.hit_rect.centery], 5))
                if self.movement[1] < 0:
                    self.hit_rect.top = en_manager.enemy_list[en].hit_rect.bottom + 5
                    self.collide_rect.top = en_manager.enemy_list[en].hit_rect.bottom + self.hit_rect[3] // 2
                    part_manager.add_particle(Particle([self.hit_rect.top, self.hit_rect.centery], 5))
    
    def show_ingredients(self, surf):
        x = 0
        for i in self.ingredient_list:
            surf.blit(self.ingredient_list[i], (x * 16 + 9, 20))
            x += 1

    def show_health_bar(self, surf, pos):
        health_bar_rect = pygame.Rect(pos[0], pos[1], self.current_hp // self.hp_ratio, 5)
        ####################################################
        pygame.draw.rect(surf, (200, 200, 200), (pos[0], pos[1], self.hp_bar_length, 5), 5)
        pygame.draw.rect(surf, (255, 0, 0), health_bar_rect)