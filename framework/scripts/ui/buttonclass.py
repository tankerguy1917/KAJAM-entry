"""
All instances of the class Button
should be put into the button_list
of the instance of ButtonManager,
otherwise you will have to maually
display each button
"""
"""
Note that using the ComplexButton class
require you to make sure all of the
functions you plan on using the button
for use *args and **kwargs
"""

#### Imports ####
import pygame
from errors import ObjNameError


#### Class(es) ####
class ButtonManager:
    def __init__(self):
        self.button_list = {}

    def display_buttons(self, surf, color=(255,0,0)):
        for buttons in self.button_list:
            self.button_list[buttons].display_button(surf, color)

    def add_button(self, name, button):
        if name not in self.button_list.keys():
            self.button_list[name] = button
        else:
            raise ObjNameError(name, "A button with this name already exists")
    
    def delete_button(self, name):
        if name in self.button_list.keys():
            del self.button_list[name]
        else:
            raise ObjNameError(name, "No button with this name exists")

    def delete_all_buttons(self):
        self.button_list = {}
    
    def highlight_button(self, mouse, surf, color):
        for button in self.button_list:
            x = pygame.Surface((self.button_list[button].rect[2], self.button_list[button].rect[3]))
            x.fill(color)
            x.set_alpha(150)
            if mouse.rect.colliderect(self.button_list[button]):
                surf.blit(x, (self.button_list[button].rect[0], self.button_list[button].rect[1]))


class SimpleButton:
    def __init__(self, img, loc, rect, func):
        if type(img) == pygame.Surface:
            self.img = img
            self.rect = pygame.Rect(loc[0], loc[1], img.get_width(), img.get_height())
        else:
            self.img = None
            self.rect = pygame.Rect(loc[0], loc[1], rect[0], rect[1])
        self.func = func

    def display_button(self, surf, color=(255, 0, 0)):
        if self.img != None:
            surf.blit(self.img, (self.rect[0], self.rect[1]))
        else:
            pygame.draw.rect(surf, color, self.rect)

    def use_func(self):
        self.func()


class ComplexButton:
    def __init__(self, img, loc, rect, func, *args, **kwargs):
        if type(img) == pygame.Surface:
            self.img = img
            self.rect = pygame.Rect(loc[0], loc[1], img.get_width(), img.get_height())
        else:
            self.img = None
            self.rect = pygame.Rect(loc[0], loc[1], rect[0], rect[1])
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def display_button(self, surf, color=(255, 0, 0)):
        if self.img != None:
            surf.blit(self.img, (self.rect[0], self.rect[1]))
        else:
            pygame.draw.rect(surf, color, self.rect)

    def use_func(self):
        self.func(*self.args, **self.kwargs)