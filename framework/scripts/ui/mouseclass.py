"""
Any instances of the Mouse class have
to be made inside of a game loop in
order for the position of the mouse
to update
"""

#### Imports ####
import pygame


#### Class(es) ####
class Mouse:
    def __init__(self, pos, img, center=False, rect=(1, 1)):
        if type(img) == pygame.Surface:
            self.img = img
        else:
            self.img = None
        self.centered = center
        self.rect = pygame.Rect(pos[0], pos[1], rect[0], rect[1])

    def display_cursor(self, surf, scroll, color=(0, 255, 0)):
        if self.img != None:
            if self.centered:
                surf.blit(self.img, (self.rect[0] - self.img.get_width() // 2 - scroll[0], self.rect[1] - self.img.get_height() // 2 - scroll[1]))
            else:
                surf.blit(self.img, (self.rect[0] - scroll[0], self.rect[1] - scroll[1]))
        else:
            pygame.draw.rect(surf, color, (self.rect[0] - scroll[0], self.rect[1] - scroll[1], self.rect[2], self.rect[3]))