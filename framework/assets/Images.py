#### Imports ####
import pygame

a = pygame.display.set_mode((0, 0)) ## Ignore this ##

#### UI images (buttons, icons, etc) ###
ui_imgs = {
    "cursor1" : pygame.image.load("framework/assets/images/ui/cursor1.png").convert(),
    "start_button1" : pygame.image.load("framework/assets/images/ui/start_button1.png").convert(),
    "logo" : pygame.image.load("framework/assets/images/menu/logomaybe.png").convert(),
    "main_menu_button" : pygame.image.load("framework/assets/images/ui/main_menu.png").convert(),
}
for i in ui_imgs:
    ui_imgs[i].set_colorkey((255, 255, 255))


#### Particle images ####
particle_imgs = {
    "particle1" : [
        pygame.image.load("framework/assets/images/particles/hit_sparks1_1.png").convert(),
        pygame.image.load("framework/assets/images/particles/hit_sparks1_2.png").convert()]
}
for i in particle_imgs:
    for x in range(len(particle_imgs[i])):
        particle_imgs[i][x].set_colorkey((255, 255, 255))


#### Enemy sprites ####
enemy_imgs = {
            "idle" : [
            pygame.image.load("framework/assets/images/sprite/enemy/chef_idle1.png").convert(),
            pygame.image.load("framework/assets/images/sprite/enemy/chef_idle2.png").convert()]
}
for i in enemy_imgs:
    for x in range(len(enemy_imgs[i])):
        enemy_imgs[i][x].set_colorkey((255, 255, 255))

#### Character sprites ####
player_imgs = {
            "idle" : [
            pygame.image.load("framework/assets/images/sprite/player/idle1.png").convert(),
            pygame.image.load("framework/assets/images/sprite/player/idle2.png").convert()],
            "right" : [
            pygame.image.load("framework/assets/images/sprite/player/right1.png").convert(),
            pygame.image.load("framework/assets/images/sprite/player/right2.png").convert()],
            "left" : [
            pygame.transform.flip(pygame.image.load("framework/assets/images/sprite/player/right1.png").convert(), True, False),
            pygame.transform.flip(pygame.image.load("framework/assets/images/sprite/player/right2.png").convert(), True, False)],
            "up" : [
            pygame.image.load("framework/assets/images/sprite/player/right1.png").convert(),
            pygame.image.load("framework/assets/images/sprite/player/right2.png").convert()],
            "down" : [
            pygame.image.load("framework/assets/images/sprite/player/right1.png").convert(),
            pygame.image.load("framework/assets/images/sprite/player/right2.png").convert()]
            }
for i in player_imgs:
    for x in range(len(player_imgs[i])):
        player_imgs[i][x].set_colorkey((255, 255, 255))

#### Tiles (Floors, walls, etc) ####
tile_imgs = {
    "oven_tile1" : pygame.image.load("framework/assets/images/tiles/oven_tile1.png").convert(),
    "grill_tile1" : pygame.image.load("framework/assets/images/tiles/grill_tile1.png").convert(),
    "tile1" : pygame.image.load("framework/assets/images/tiles/tile1.png").convert(),
    "tile2" : pygame.image.load("framework/assets/images/tiles/tile2.png").convert(),
    "tile3" : pygame.image.load("framework/assets/images/tiles/tile3.png").convert(),
    "shelf_tile" : pygame.image.load("framework/assets/images/tiles/shelf_tile.png").convert()
}
for i in tile_imgs:
    tile_imgs[i].set_colorkey((255, 255, 255))

#### Ingredient images ####
ing_imgs = {
    "carrot1" : pygame.image.load("framework/assets/images/sprite/ingredient/carrot_sprite.png").convert(),
    "tomato1" : pygame.image.load("framework/assets/images/sprite/ingredient/tomato_sprite.png").convert()
}

enmy_imgs = {
  
}

for i in ing_imgs:
    ing_imgs[i].set_colorkey((255, 255, 255))

#### Misc images ####
misc_imgs = {}