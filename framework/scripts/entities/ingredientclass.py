#### Imports ####
import pygame
from errors import ObjNameError


#### Class(es) ####
class IngredientManager:
    def __init__(self):
        self.ingredient_list = {}

    def add_ingredient(self, name, ingredient):
        if name not in self.ingredient_list.keys():
            self.ingredient_list[name] = ingredient
        else:
            raise ObjNameError(name, "An ingredient with this name already exists")
    
    def remove_ingredient(self, name):
        if name in self.ingredient_list.keys():
            del self.ingredient_list[name]
        else:
            raise ObjNameError(name, "No ingredient with this name exists")

    def remove_all_ingredients(self):
        self.ingredient_list = {}

    def display_ingredients(self, surf, scroll, color=(255,0,0)):
        for i in self.ingredient_list:
            self.ingredient_list[i].display_ingredient(surf, scroll)


class Ingredient:
    def __init__(self, pos, img, rect=(10, 10)):
        if type(img) != pygame.Surface:
            self.img = None
            self.rect = pygame.Rect(pos[0], pos[1], rect[0], rect[1])
        else:
            self.img = img
            self.rect = pygame.Rect(pos[0], pos[1], self.img.get_width(), self.img.get_height())

    def display_ingredient(self, surf, scroll, color=(255, 0, 0)):
        if type(self.img) != pygame.Surface:
            pygame.draw.rect(surf, color, (self.rect[0] - scroll[0], self.rect[1] - scroll[1], self.rect[2], self.rect[3]))
        else:
            surf.blit(self.img, (self.rect[0] - scroll[0], self.rect[1] - scroll[1]))