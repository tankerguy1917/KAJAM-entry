#### Imports ####
import pygame, sys
from pygame.locals import *
from framework.scripts.gameclass import Game
from framework.scripts.ui.mouseclass import Mouse
from framework.scripts.ui.buttonclass import ButtonManager, SimpleButton
from framework.scripts.entities.entityclass import TopDownEntity
from framework.scripts.entities.enemy.chef import Chef, EnemyManager
from framework.scripts.entities.particleclass import Particle, ParticleManager
from framework.scripts.entities.ingredientclass import IngredientManager, Ingredient
from framework.assets.Images import ui_imgs, player_imgs, tile_imgs, ing_imgs, enemy_imgs, particle_imgs # NOTE: These are all of the sprites/images

pygame.init()


#### Setup ####
WIN = (500, 300)
screen = pygame.display.set_mode(WIN, 0, 32)
pygame.mouse.set_visible(False)
game = Game((WIN[0] // 2, WIN[1] // 2), 60, bg_color=(50,70,70))
game.get_map("framework/assets/maps/level1.json")
button_manager = ButtonManager()
ingredient_manager = IngredientManager()
enemy_manager = EnemyManager()
particle_manager = ParticleManager()


#### Main menu loop ####
def main_menu():
    ### 
    pygame.display.set_caption("Main Menu | Chef Royale")

    ### Button setup
    button_manager.delete_all_buttons()
    button_manager.add_button("start_button", SimpleButton(ui_imgs["start_button1"], (game.screen.get_width() // 2 - 16, 50), (31, 13), level1)) # For testing

    ### Scroll setup
    scroll = [0, 0]

    while True:
        ### Mouse setup
        mx, my = pygame.mouse.get_pos()
        mouse = Mouse((mx // 2, my // 2), ui_imgs["cursor1"])

        ### Rendering
        game.update() # NOTE: Render everything after this
        game.screen.blit(ui_imgs["logo"], (75, -30))
        button_manager.display_buttons(game.screen)
        button_manager.highlight_button(mouse, game.screen, (0, 0, 0))
        mouse.display_cursor(game.screen, scroll)

        ### Checking for events
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    for button in button_manager.button_list:
                        if mouse.rect.colliderect(button_manager.button_list[button]):
                            button_manager.button_list[button].use_func()
        
        ### Updates the screen
        screen.blit(pygame.transform.scale(game.screen, WIN), (0, 0))
        pygame.display.update()


#### Level 1 ####
def level1():
    ### Level indicator
    pygame.display.set_caption("Level 1 | Chef Royale")

    ### Map setup
    game.rect_list = []
    game.get_map("framework/assets/maps/level1.json")

    ### Timer setup
    game.timer = 120 * 60

    ### Player setup
    player = TopDownEntity(player_imgs["idle"], (16, 16), 1, 100)

    ### Scroll setup
    true_scroll = [0, 0]

    ### Enemy setup
    enemy_manager.remove_all_enemies()

    ### Ingredient setup
    ingredient_manager.remove_all_ingredients()
    ingredient_manager.add_ingredient("i1", Ingredient((32, 16), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i2", Ingredient((64, 64), ing_imgs["tomato1"]))
    ingredient_manager.add_ingredient("i3", Ingredient((112, 16), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i4", Ingredient((160, 96), ing_imgs["tomato1"]))


    ### Amount of ingredients needed to pass level
    ing_amount = len(ingredient_manager.ingredient_list)
   
   ### Checks if player is alive or not
    while player.current_hp > 0:
        if game.timer > 0:
            ### Checks if player beat level
            if player.collected == ing_amount:
                level2()

            ### This is so that the player stays in the center of the screen
            true_scroll[0] += (player.hit_rect.x - true_scroll[0] - (game.screen.get_width() // 2 - player.hit_rect[2] // 2)) / 20
            true_scroll[1] += (player.hit_rect.y - true_scroll[1] - (game.screen.get_height() // 2 - player.hit_rect[3] // 2)) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            ### Mouse setup
            mx, my = pygame.mouse.get_pos()
            mouse = Mouse((mx // 2 + scroll[0], my // 2 + scroll[1]), ui_imgs["cursor1"])

            ### Rendering
            game.update()
            game.display_map(tile_imgs, (player.hit_rect[0], player.hit_rect[1]), scroll)
            game.show_timer()

            ingredient_manager.display_ingredients(game.screen, scroll)

            enemy_manager.display_chefs(game.screen, scroll)
            enemy_manager.move_chefs(game.rect_list)
            enemy_manager.collide_player(player, particle_manager, scroll)
            enemy_manager.animate_chefs(20)

            player.show_entity(game.screen, (10, 10), (10, 17), 8, scroll, particle_imgs, show_hp=True)
            player.show_ingredients(game.screen)
            player.move(game.rect_list, ingredient_manager, enemy_manager, particle_manager, scroll)

            mouse.display_cursor(game.screen, scroll)

            ### Checking for events
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        main_menu()
                    if e.key == K_a or e.key == K_LEFT:
                        player.movement = [-player.speed, 0]
                        player.change_anim(player_imgs["left"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [player.speed, 0]
                        player.change_anim(player_imgs["right"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, -player.speed]
                        player.change_anim(player_imgs["up"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, player.speed]
                        player.change_anim(player_imgs["down"])
                if e.type == KEYUP:
                    if e.key == K_a or K_LEFT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    
            ### Updates screen
            screen.blit(pygame.transform.scale(game.screen, WIN), (0, 0))
            pygame.display.update()

        ### If timer runs out, go to main menu
        else:
            main_menu()
    ### If player is dead, go back to the main menu
    else:
        main_menu()


#### Level 2 ####
def level2():
    ### Level indicator
    pygame.display.set_caption("Level 2 | Chef Royale")

    ### Map setup
    game.rect_list = []
    game.get_map("framework/assets/maps/level2.json")

    ### Timer setup
    game.timer = 100 * 60

    ### Player setup
    player = TopDownEntity(player_imgs["idle"], (16, 16), 1, 100)

    ### Scroll setup
    true_scroll = [0, 0]

    ### Enemy setup
    enemy_manager.remove_all_enemies()
    enemy_manager.add_chef("c1", Chef((32, 32), enemy_imgs["idle"], move_h=False))
    enemy_manager.add_chef("c2", Chef((80, 91), enemy_imgs["idle"], move_h=True))

    ### Particle setup
    particle_manager.remove_all_particles()

    ### Ingredient setup
    ingredient_manager.remove_all_ingredients()
    ingredient_manager.add_ingredient("i1", Ingredient((16, 48), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i2", Ingredient((80, 112), ing_imgs["tomato1"]))
    ingredient_manager.add_ingredient("i3", Ingredient((192, 48), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i4", Ingredient((192, 112), ing_imgs["tomato1"]))

    ### Amount of ingredients needed to pass level
    ing_amount = len(ingredient_manager.ingredient_list)
   
   ### Checks if player is alive or not
    while player.current_hp > 0:
        if game.timer > 0:
            ### Checks if player beat level
            if player.collected == ing_amount:
                level3()

            ### This is so that the player stays in the center of the screen
            true_scroll[0] += (player.hit_rect.x - true_scroll[0] - (game.screen.get_width() // 2 - player.hit_rect[2] // 2)) / 20
            true_scroll[1] += (player.hit_rect.y - true_scroll[1] - (game.screen.get_height() // 2 - player.hit_rect[3] // 2)) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            ### Mouse setup
            mx, my = pygame.mouse.get_pos()
            mouse = Mouse((mx // 2 + scroll[0], my // 2 + scroll[1]), ui_imgs["cursor1"])

            ### Rendering
            game.update()
            game.display_map(tile_imgs, (player.hit_rect[0], player.hit_rect[1]), scroll)
            game.show_timer()

            ingredient_manager.display_ingredients(game.screen, scroll)

            enemy_manager.display_chefs(game.screen, scroll)
            enemy_manager.move_chefs(game.rect_list)
            enemy_manager.collide_player(player, particle_manager, scroll)
            enemy_manager.animate_chefs(20)

            player.show_entity(game.screen, (10, 10), (10, 17), 8, scroll, particle_imgs, show_hp=True)
            player.show_ingredients(game.screen)
            player.move(game.rect_list, ingredient_manager, enemy_manager, particle_manager, scroll)

            particle_manager.show_particles(game.screen, scroll)

            mouse.display_cursor(game.screen, scroll)

            ### Checking for events
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        main_menu()
                    if e.key == K_a or e.key == K_LEFT:
                        player.movement = [-player.speed, 0]
                        player.change_anim(player_imgs["left"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [player.speed, 0]
                        player.change_anim(player_imgs["right"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, -player.speed]
                        player.change_anim(player_imgs["up"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, player.speed]
                        player.change_anim(player_imgs["down"])
                if e.type == KEYUP:
                    if e.key == K_a or K_LEFT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    
            ### Updates screen
            screen.blit(pygame.transform.scale(game.screen, WIN), (0, 0))
            pygame.display.update()

        ### If timer runs out, go to main menu
        else:
            main_menu()
    ### If player is dead, go back to the main menu
    else:
        main_menu()


#### Level 3 ####
def level3():
    ### Level indicator
    pygame.display.set_caption("Level 3 | Chef Royale")

    ### Map setup
    game.rect_list = []
    game.get_map("framework/assets/maps/level3.json")

    ### Timer setup
    game.timer = 80 * 60

    ### Player setup
    player = TopDownEntity(player_imgs["idle"], (16, 16), 1, 100)

    ### Scroll setup
    true_scroll = [0, 0]

    ### Enemy setup
    enemy_manager.remove_all_enemies()
    enemy_manager.add_chef("c1", Chef((96, 32), enemy_imgs["idle"], move_h=False))
    enemy_manager.add_chef("c2", Chef((160, 106), enemy_imgs["idle"], move_h=False))
    enemy_manager.add_chef("c3", Chef((80, 106), enemy_imgs["idle"]))


    ### Ingredient setup
    ingredient_manager.remove_all_ingredients()
    ingredient_manager.add_ingredient("i1", Ingredient((16, 112), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i2", Ingredient((80, 112), ing_imgs["tomato1"]))
    ingredient_manager.add_ingredient("i3", Ingredient((96, 48), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i4", Ingredient((144, 112), ing_imgs["tomato1"]))

    ### Amount of ingredients needed to pass level
    ing_amount = len(ingredient_manager.ingredient_list)
   
   ### Checks if player is alive or not
    while player.current_hp > 0:
        if game.timer > 0:
            ### Checks if player beat level
            if player.collected == ing_amount:
                level4()

            ### This is so that the player stays in the center of the screen
            true_scroll[0] += (player.hit_rect.x - true_scroll[0] - (game.screen.get_width() // 2 - player.hit_rect[2] // 2)) / 20
            true_scroll[1] += (player.hit_rect.y - true_scroll[1] - (game.screen.get_height() // 2 - player.hit_rect[3] // 2)) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            ### Mouse setup
            mx, my = pygame.mouse.get_pos()
            mouse = Mouse((mx // 2 + scroll[0], my // 2 + scroll[1]), ui_imgs["cursor1"])

            ### Rendering
            game.update()
            game.display_map(tile_imgs, (player.hit_rect[0], player.hit_rect[1]), scroll)
            game.show_timer()

            ingredient_manager.display_ingredients(game.screen, scroll)

            enemy_manager.display_chefs(game.screen, scroll)
            enemy_manager.move_chefs(game.rect_list)
            enemy_manager.collide_player(player, particle_manager, scroll)
            enemy_manager.animate_chefs(20)

            player.show_entity(game.screen, (10, 10), (10, 17), 8, scroll, particle_imgs, show_hp=True)
            player.show_ingredients(game.screen)
            player.move(game.rect_list, ingredient_manager, enemy_manager, particle_manager, scroll)

            mouse.display_cursor(game.screen, scroll)

            ### Checking for events
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        main_menu()
                    if e.key == K_a or e.key == K_LEFT:
                        player.movement = [-player.speed, 0]
                        player.change_anim(player_imgs["left"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [player.speed, 0]
                        player.change_anim(player_imgs["right"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, -player.speed]
                        player.change_anim(player_imgs["up"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, player.speed]
                        player.change_anim(player_imgs["down"])
                if e.type == KEYUP:
                    if e.key == K_a or K_LEFT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    
            ### Updates screen
            screen.blit(pygame.transform.scale(game.screen, WIN), (0, 0))
            pygame.display.update()

        ### If timer runs out, go to main menu
        else:
            main_menu()
    ### If player is dead, go back to the main menu
    else:
        main_menu()


#### Level 4 ####
def level4():
    ### Level indicator
    pygame.display.set_caption("Level 4 | Chef Royale")

    ### Map setup
    game.rect_list = []
    game.get_map("framework/assets/maps/level4.json")

    ### Timer setup
    game.timer = 200 * 60

    ### Player setup
    player = TopDownEntity(player_imgs["idle"], (16, 16), 1, 100)

    ### Scroll setup
    true_scroll = [0, 0]

    ### Enemy setup
    enemy_manager.remove_all_enemies()
    enemy_manager.add_chef("c1", Chef((80, 25), enemy_imgs["idle"]))
    enemy_manager.add_chef("c2", Chef((144, 55), enemy_imgs["idle"]))
    enemy_manager.add_chef("c3", Chef((208, 75), enemy_imgs["idle"]))
    enemy_manager.add_chef("c4", Chef((64, 105), enemy_imgs["idle"]))

    ### Ingredient setup
    ingredient_manager.remove_all_ingredients()
    ingredient_manager.add_ingredient("i1", Ingredient((32, 32), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i2", Ingredient((128, 96), ing_imgs["tomato1"]))
    ingredient_manager.add_ingredient("i3", Ingredient((48, 112), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i4", Ingredient((112, 48), ing_imgs["tomato1"]))
    ingredient_manager.add_ingredient("i5", Ingredient((192, 16), ing_imgs["carrot1"]))
    ingredient_manager.add_ingredient("i6", Ingredient((224, 112), ing_imgs["tomato1"]))

    ### Amount of ingredients needed to pass level
    ing_amount = len(ingredient_manager.ingredient_list)
   
   ### Checks if player is alive or not
    while player.current_hp > 0:
        if game.timer > 0:
            ### Checks if player beat level
            if player.collected == ing_amount:
                win_screen()

            ### This is so that the player stays in the center of the screen
            true_scroll[0] += (player.hit_rect.x - true_scroll[0] - (game.screen.get_width() // 2 - player.hit_rect[2] // 2)) / 20
            true_scroll[1] += (player.hit_rect.y - true_scroll[1] - (game.screen.get_height() // 2 - player.hit_rect[3] // 2)) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            ### Mouse setup
            mx, my = pygame.mouse.get_pos()
            mouse = Mouse((mx // 2 + scroll[0], my // 2 + scroll[1]), ui_imgs["cursor1"])

            ### Rendering
            game.update()
            game.display_map(tile_imgs, (player.hit_rect[0], player.hit_rect[1]), scroll)
            game.show_timer()

            ingredient_manager.display_ingredients(game.screen, scroll)

            enemy_manager.display_chefs(game.screen, scroll)
            enemy_manager.move_chefs(game.rect_list)
            enemy_manager.collide_player(player, particle_manager, scroll)
            enemy_manager.animate_chefs(20)

            player.show_entity(game.screen, (10, 10), (10, 17), 8, scroll, particle_imgs, show_hp=True)
            player.show_ingredients(game.screen)
            player.move(game.rect_list, ingredient_manager, enemy_manager, particle_manager, scroll)

            mouse.display_cursor(game.screen, scroll)

            ### Checking for events
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        main_menu()
                    if e.key == K_a or e.key == K_LEFT:
                        player.movement = [-player.speed, 0]
                        player.change_anim(player_imgs["left"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [player.speed, 0]
                        player.change_anim(player_imgs["right"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, -player.speed]
                        player.change_anim(player_imgs["up"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, player.speed]
                        player.change_anim(player_imgs["down"])
                if e.type == KEYUP:
                    if e.key == K_a or K_LEFT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_d or e.key == K_RIGHT:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_w or e.key == K_UP:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    if e.key == K_s or e.key == K_DOWN:
                        player.movement = [0, 0]
                        player.change_anim(player_imgs["idle"])
                    
            ### Updates screen
            screen.blit(pygame.transform.scale(game.screen, WIN), (0, 0))
            pygame.display.update()

        ### If timer runs out, go to main menu
        else:
            main_menu()
    ### If player is dead, go back to the main menu
    else:
        main_menu()


#### Win screen ####
def win_screen():
    pygame.display.set_caption("Win screen | Chef Royale")

    game.rect_list = []
    enemy_manager.remove_all_enemies()
    ingredient_manager.remove_all_ingredients()

    ### Button setup
    button_manager.delete_all_buttons()
    button_manager.add_button("b1", SimpleButton(ui_imgs["main_menu_button"], (102, 50), (31, 13), main_menu))

    ### Displays that the player won
    win_message = game.font.render("You Win!!!", False, (0, 0, 0))

    while True:
        ### Mouse_setup
        mx, my  = pygame.mouse.get_pos()
        mouse = Mouse((mx // 2, my // 2), ui_imgs["cursor1"])

        ### Rendering
        game.update()
        game.screen.blit(pygame.transform.scale(win_message, (win_message.get_width() * 2, win_message.get_height() * 2)), (85, 15))
        button_manager.display_buttons(game.screen)
        button_manager.highlight_button(mouse, game.screen, (0, 0, 0))
        mouse.display_cursor(game.screen, [0, 0])

        ### Event checking
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    for button in button_manager.button_list:
                        if mouse.rect.colliderect(button_manager.button_list[button]):
                            button_manager.button_list[button].use_func()
        
        screen.blit(pygame.transform.scale(game.screen, WIN), (0, 0))
        pygame.display.update()


#### Runs the program ####
main_menu()