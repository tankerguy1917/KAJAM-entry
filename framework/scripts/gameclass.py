#### Imports ####
import pygame, json


#### Class(es) ####
class Game:
    def __init__(self, size, fps, bg_color=(0, 0, 0)):
        self.fps = fps
        self.bg_color = bg_color
        self.screen = pygame.Surface(size)
        self.clock = pygame.time.Clock()
        self.rect_list = []
        self.game_map = {}
        self.timer = 0
        self.true_time = 0
        self.font = pygame.font.Font("framework/assets/font/Minecraftia-Regular.ttf", 8)

    def get_map(self, path):
    	file = open(path)
    	self.game_map = json.load(file)
    	for i in self.game_map:
    		if self.game_map[i][2] == True:
    			self.rect_list.append(pygame.Rect(self.game_map[i][1][0] * 16, self.game_map[i][1][1] * 16, 16, 16))

    def display_map(self, imgs, p_loc, scroll):
    	for i in self.game_map:
    		target_coord = (self.game_map[i][1][0], self.game_map[i][1][1])
    		if target_coord[0] * 16 >= p_loc[0] - self.screen.get_width() // 2 or target_coord[0] * 16 <= p_loc[0] + self.screen.get_width() // 2:
    			if target_coord[1] * 16 >= p_loc[1] - self.screen.get_height() // 2 or target_coord[1] * 16 <= p_loc[1] + self.screen.get_height() // 2:
    				self.screen.blit(imgs[self.game_map[i][0]], (self.game_map[i][1][0] * 16 - scroll[0], self.game_map[i][1][1] * 16 - scroll[1]))

    def update(self):
        self.screen.fill(self.bg_color)
        self.clock.tick(self.fps)
        
    def show_timer(self):
        self.screen.blit(self.font.render("Time: " + str(self.true_time), False, (0, 0, 0)), (205, 6))
        self.change_timer()

    def change_timer(self):
        self.timer -= 1
        self.true_time = self.timer // 60