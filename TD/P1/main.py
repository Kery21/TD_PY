import pygame as pg                   #import pygame
import json                           #import json
from enemy import Enemy               #import class Enemy from enemy.py
from world import World               #import class World from world.py
from turret import Turret             #import class Turret from turret.py
from sniper import Sniper             #import class Sniper from sniper.py
from freeze import Freeze             #import class Freeze from freeze.py
from magma import Magma               #import class Magma from magma.py
from button import Button             #import class Button from button.py
from turret_data import TURRET_DATA   #import turret properties from turret_data,py
from sniper_data import SNIPER_DATA   #import sniper properties from sniper_data.py
from freeze_data import FREEZE_DATA   #import freeze properties from freeze_data.py
from magma_data import MAGMA_DATA     #import magma properties from magma_data.py
from enemy_data import ENEMY_DATA     #import enemy properties from enemy_data.py
import constants as c                 #import constans from constans.py
import random as r                    #import random

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#game variables
game_over = False
game_outcome = 0  # -1 is loss & 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
last_minion_spawn = pg.time.get_ticks()
placing_turrets = False
placing_snipers = False
placing_freezs = False
placing_magmas = False
selected_turret = None
selected_sniper = None
selected_freeze = None
selected_magma = None
NFT = {}
enemy_types = ["weak", "medium"]

#load images
#map
map_image = pg.image.load('P1/levels/level.png').convert_alpha()
#turret spritesheets
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
  turret_sheet = pg.image.load(f'P1/assets/images/turrets/turret_{x}.png').convert_alpha()
  turret_spritesheets.append(turret_sheet)
#sniper spritesheets
sniper_spritesheets = []
for x in range (1, c.SNIPER_LEVELS + 1):
  sniper_sheet = pg.image.load(f'P1/assets/images/sniper_guns/sniper_gun_{x}.png').convert_alpha()
  sniper_spritesheets.append(sniper_sheet)
#freeze spritesheets
freeze_spritesheets = []
for x in range (1, c.FREEZE_LEVELS + 1):
  freeze_sheet = pg.image.load(f'P1/assets/images/freeze_guns/freeze_gun_{x}.png').convert_alpha()
  freeze_spritesheets.append(freeze_sheet)
#magma images
magma_images = []
for x in range (1, c.MAGMA_LEVELS + 1):
  magma_image = pg.image.load(f'P1/assets/images/magma_towers/magma_tower_{x}.png').convert_alpha()
  magma_images.append(magma_image)
#individual weapon image for mouse cursor
cursor_turret = pg.image.load('P1/assets/images/turrets/cursor_turret.png').convert_alpha()
cursor_sniper = pg.image.load('P1/assets/images/sniper_guns/cursor_sniper_gun.png').convert_alpha()
cursor_freeze = pg.image.load('P1/assets/images/freeze_guns/cursor_freeze.png').convert_alpha()
cursor_magma = pg.image.load('P1/assets/images/magma_towers/magma_tower_1.png').convert_alpha()
#enemies
enemy_images = {
  "weak": pg.image.load('P1/assets/images/enemies/enemy_1.png').convert_alpha(),
  "medium": pg.image.load('P1/assets/images/enemies/enemy_2.png').convert_alpha(),
  "strong": pg.image.load('P1/assets/images/enemies/enemy_3.png').convert_alpha(),
  "elite": pg.image.load('P1/assets/images/enemies/enemy_4.png').convert_alpha(),
  "boss": pg.image.load('P1/assets/images/enemies/boss.png').convert_alpha(),
  "SP_boss": pg.image.load('P1/assets/images/enemies/SP_boss.png').convert_alpha()
}
#buttons
buy_turret_image = pg.image.load('P1/assets/images/buttons/buy_turret.png').convert_alpha()
buy_sniper_gun_image = pg.image.load('P1/assets/images/buttons/buy_sniper_gun.png').convert_alpha()
buy_freeze_gun_image = pg.image.load('P1/assets/images/buttons/buy_freeze_gun.png').convert_alpha()
buy_magma_image = pg.image.load('P1/assets/images/buttons/buy_magma.png').convert_alpha()
cancel_image = pg.image.load('P1/assets/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('P1/assets/images/buttons/upgrade_turret.png').convert_alpha()
upgrade_sniper_image = pg.image.load('P1/assets/images/buttons/upgrade_sniper.png').convert_alpha()
upgrade_magma_image = pg.image.load('P1/assets/images/buttons/upgrade_magma.png').convert_alpha()
upgrade_freeze_image = pg.image.load('P1/assets/images/buttons/upgrade_freeze.png').convert_alpha()
begin_image = pg.image.load('P1/assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('P1/assets/images/buttons/restart.png').convert_alpha()
fast_forward_image = pg.image.load('P1/assets/images/buttons/fast_forward.png').convert_alpha()
#gui
heart_image = pg.image.load("P1/assets/images/gui/heart.png").convert_alpha()
coin_image = pg.image.load("P1/assets/images/gui/coin.png").convert_alpha()

#load json data for level
with open('P1/levels/level.tmj') as file:
  world_data = json.load(file)

#load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def display_data():
  #draw panel
  pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
  #display data
  draw_text("LEVEL: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 55, 15)
  screen.blit(heart_image, (c.SCREEN_WIDTH + 20, 55))
  draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 55, 60)
  screen.blit(coin_image, (c.SCREEN_WIDTH + 120, 55))
  draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 155, 60)



  

def create_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  #calculate the sequential number of the tile
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  #check if that tile is grass
  if world.tile_map[mouse_tile_num] == 7:
    if (mouse_tile_x, mouse_tile_y) not in NFT:
      new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
      turret_group.add(new_turret)
      #deduct cost of turret
      world.money -= c.BUY_COST
      NFT[(mouse_tile_x, mouse_tile_y)] = "nft"

def create_sniper(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  if world.tile_map[mouse_tile_num] == 7:
    if (mouse_tile_x, mouse_tile_y) not in NFT:
      new_sniper = Sniper(sniper_spritesheets, mouse_tile_x, mouse_tile_y)
      sniper_group.add(new_sniper)
      world.money -= c.BUY_COST2
      NFT[(mouse_tile_x, mouse_tile_y)] = "nft"


def create_freeze(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  if world.tile_map[mouse_tile_num] == 7:
    if (mouse_tile_x, mouse_tile_y) not in NFT:
      new_freeze = Freeze(freeze_spritesheets, mouse_tile_x, mouse_tile_y)
      freeze_group.add(new_freeze)
      world.money -= c.BUY_COST3
      NFT[(mouse_tile_x, mouse_tile_y)] = "nft"

def create_magma(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  if world.tile_map[mouse_tile_num] == 7:
    if (mouse_tile_x, mouse_tile_y) not in NFT:
      new_magma = Magma(magma_images, mouse_tile_x, mouse_tile_y)
      magma_group.add(new_magma)
      world.money -= c.BUY_COST4
      NFT[(mouse_tile_x, mouse_tile_y)] = "nft"


def select_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      return turret
    
def select_sniper(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for sniper in sniper_group:
    if (mouse_tile_x, mouse_tile_y) == (sniper.tile_x, sniper.tile_y):
      return sniper
    
def select_freeze(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for freeze in freeze_group:
    if (mouse_tile_x, mouse_tile_y) == (freeze.tile_x, freeze.tile_y):
      return freeze
    
def select_magma(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for magma in magma_group:
    if (mouse_tile_x, mouse_tile_y) == (magma.tile_x, magma.tile_y):
      return magma


def clear_selection():
  for turret in turret_group:
    turret.selected = False
  for sniper in sniper_group:
    sniper.selected = False
  for freeze in freeze_group:
    freeze.selected = False
  for magma in magma_group:
    magma.selected = False

#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()
sniper_group = pg.sprite.Group()
freeze_group = pg.sprite.Group()
magma_group = pg.sprite.Group()

#create buttons
turret_button = Button(c.SCREEN_WIDTH + 36, 120, buy_turret_image, True)
sniper_button = Button(c.SCREEN_WIDTH + 36, 240, buy_sniper_gun_image, True)
freeze_button = Button(c.SCREEN_WIDTH + 36, 360, buy_freeze_gun_image, True)
magma_button = Button(c.SCREEN_WIDTH + 36, 480, buy_magma_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 57, 180, cancel_image, True)
IIcancel_button = Button(c.SCREEN_WIDTH + 57, 300, cancel_image, True)
IIIcancel_button = Button(c.SCREEN_WIDTH + 57, 420, cancel_image, True)
IVcancel_button = Button(c.SCREEN_WIDTH + 57, 540, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 7, 180, upgrade_turret_image, True)
IIupgrade_button = Button(c.SCREEN_WIDTH + 7, 300, upgrade_sniper_image, True)
IIIupgrade_button = Button(c.SCREEN_WIDTH + 7, 420, upgrade_freeze_image, True)
IVupgrade_button = Button(c.SCREEN_WIDTH + 7, 540, upgrade_magma_image, True)
begin_button = Button(c.SCREEN_WIDTH + 26, 660, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 19, 660, fast_forward_image, False)

#game loop
run = True
while run:

  clock.tick(c.FPS)

  #########################
  # UPDATING SECTION
  #########################

  BS_SP_CD = c.BOSS_SUPER_COOLDOWN / world.game_speed
  SP_CD = c.SPAWN_COOLDOWN / world.game_speed

  if game_over == False:
    #check if player has lost
    if world.health <= 0:
      game_over = True
      game_outcome = -1 #loss
    #check if player has won
    if world.level > c.TOTAL_LEVELS:
      game_over = True
      game_outcome = 1 #win

    #update groups
    enemy_group.update(world)
    turret_group.update(enemy_group, world)
    sniper_group.update(enemy_group, world)
    freeze_group.update(enemy_group, world)
    magma_group.update()

    #highlight selected turret
    if selected_turret:
      selected_turret.selected = True

    if selected_sniper:
      selected_sniper.selected = True

    if selected_freeze:
      selected_freeze.selected = True

    if selected_magma:
      selected_magma.selected = True

  #########################
  # DRAWING SECTION
  #########################

  #draw level
  world.draw(screen)

  #draw groups
  enemy_group.draw(screen)
  for turret in turret_group:
    turret.draw(screen)
  for sniper in sniper_group:
    sniper.draw(screen)
  for freeze in freeze_group:
    freeze.draw(screen)
  for enemy in enemy_group:
    enemy.draw_health_bar(screen)
  magma_group.draw(screen)

  display_data()

  if game_over == False:
    #check if the level has been started or not
    if level_started == False:
      if begin_button.draw(screen):
        level_started = True
    else:
      #fast forward option
      world.game_speed = 1
      if fast_forward_button.draw(screen):
        world.game_speed = 2
      #spawn enemies
      if pg.time.get_ticks() - last_enemy_spawn > SP_CD:
        if world.spawned_enemies < len(world.enemy_list):
          enemy_type = world.enemy_list[world.spawned_enemies]
          enemy = Enemy(enemy_type, world.waypoints, enemy_images)
          enemy_group.add(enemy)
          world.spawned_enemies += 1
          last_enemy_spawn = pg.time.get_ticks()

      if pg.time.get_ticks() - last_minion_spawn > BS_SP_CD:
        for enemy in enemy_group:
          if enemy.HP_steal == 5:
            enemy_type = r.choice(enemy_types)
            nearest_wayp = enemy.find_nearest_wayp()
            new_enemy = Enemy(enemy_type, world.waypoints[world.waypoints.index(nearest_wayp):], enemy_images)
            enemy_group.add(new_enemy)
            last_minion_spawn = pg.time.get_ticks()
            break

    #check if the wave is finished
    if world.check_level_complete() == True:
      world.money += c.LEVEL_COMPLETE_REWARD
      world.level += 1
      c.level += 1
      level_started = False
      last_enemy_spawn = pg.time.get_ticks()
      world.reset_level()
      world.process_enemies()

    #draw buttons
    #button for placing turrets
    #for the "turret button" show cost of turret and draw the button


    if freeze_button.draw(screen) and placing_turrets == False and placing_snipers == False and placing_magmas == False:
      placing_freezs = True
    if placing_freezs == True:
      cursor_rect = cursor_freeze.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursor_rect.center = cursor_pos
      if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(cursor_freeze, cursor_rect)
      if IIIcancel_button.draw(screen):
        placing_freezs = False
    if selected_freeze:
      if selected_freeze.upgrade_level < c.FREEZE_LEVELS:
        if IIIupgrade_button.draw(screen):
          if world.money >= FREEZE_DATA[selected_freeze.upgrade_level-1].get("upgrade_cost"):
            selected_freeze.upgrade()
            world.money -= FREEZE_DATA[selected_freeze.upgrade_level-1].get("upgrade_cost")
        draw_text("-" + str(FREEZE_DATA[selected_freeze.upgrade_level].get("upgrade_cost")), text_font, "red", c.SCREEN_WIDTH + 170, 405)


    if sniper_button.draw(screen) and placing_turrets == False and placing_freezs == False and placing_magmas == False:
      placing_snipers = True
    if placing_snipers == True:
      cursor_rect = cursor_sniper.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursor_rect.center = cursor_pos
      if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(cursor_sniper, cursor_rect)
      if IIcancel_button.draw(screen):
        placing_snipers = False
    if selected_sniper:
      if selected_sniper.upgrade_level < c.SNIPER_LEVELS:
        if IIupgrade_button.draw(screen):
          if world.money >= SNIPER_DATA[selected_sniper.upgrade_level-1].get("upgrade_cost"):
            selected_sniper.upgrade()
            world.money -= SNIPER_DATA[selected_sniper.upgrade_level-1].get("upgrade_cost")
        draw_text("-" + str(SNIPER_DATA[selected_sniper.upgrade_level].get("upgrade_cost")), text_font, "red", c.SCREEN_WIDTH + 170, 285)


    if magma_button.draw(screen) and placing_turrets == False and placing_freezs == False and placing_snipers == False:
      placing_magmas = True
    if placing_magmas == True:
      cursor_rect = cursor_magma.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursor_rect.center = cursor_pos
      if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(cursor_magma, cursor_rect)
      if IVcancel_button.draw(screen):
        placing_magmas = False
    if selected_magma:
      if selected_magma.upgrade_level < c.MAGMA_LEVELS:
        if IVupgrade_button.draw(screen):
          if world.money >= MAGMA_DATA[selected_magma.upgrade_level-1].get("upgrade_cost"):
            selected_magma.upgrade()
            world.money -= MAGMA_DATA[selected_magma.upgrade_level-1].get("upgrade_cost")
        draw_text("-" + str(MAGMA_DATA[selected_magma.upgrade_level].get("upgrade_cost")), text_font, "red", c.SCREEN_WIDTH + 170, 525)


    if turret_button.draw(screen) and placing_snipers == False and placing_freezs == False and placing_magmas == False:
      placing_turrets = True
    #if placing turrets then show the cancel button as well
    if placing_turrets == True:
      #show cursor turret
      cursor_rect = cursor_turret.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursor_rect.center = cursor_pos
      if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(cursor_turret, cursor_rect)
      if cancel_button.draw(screen):
        placing_turrets = False
    #if a turret is selected then show the upgrade button
    if selected_turret:
      #if a turret can be upgraded then show the upgrade button
      if selected_turret.upgrade_level < c.TURRET_LEVELS:
        #show cost of upgrade and draw the button
        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 190))
        if upgrade_button.draw(screen):
          if world.money >= TURRET_DATA[selected_turret.upgrade_level-1].get("upgrade_cost"):
            selected_turret.upgrade()
            world.money -= TURRET_DATA[selected_turret.upgrade_level-1].get("upgrade_cost")
        draw_text("-" + str(TURRET_DATA[selected_turret.upgrade_level].get("upgrade_cost")), text_font, "red", c.SCREEN_WIDTH + 170, 165)
            
  else:
    pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
    if game_outcome == -1:
      draw_text("GAME OVER", large_font, "grey0", 310, 230)
    elif game_outcome == 1:
      draw_text("YOU WIN!", large_font, "grey0", 315, 230)
    #restart level
    if restart_button.draw(screen):
      game_over = False
      level_started = False
      placing_turrets = False
      placing_snipers = False
      placing_freezs = False
      placing_magmas = False
      selected_turret = None
      selected_sniper = None
      selected_freeze = None
      selected_magma = None
      last_enemy_spawn = pg.time.get_ticks()
      world = World(world_data, map_image)
      world.process_data()
      world.process_enemies()
      #empty groups
      enemy_group.empty()
      turret_group.empty()
      sniper_group.empty()
      freeze_group.empty()
      magma_group.empty()
      

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False
    #mouse click
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      #check if mouse is on the game area
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
        #clear selected turrets, snipers
        selected_turret = None
        selected_sniper = None
        selected_freeze = None
        selected_magma = None
        clear_selection()
        if placing_magmas == True and placing_turrets == False and placing_freezs == False and placing_snipers == False:
          if world.money >= c.BUY_COST4:
            create_magma(mouse_pos)
        else:
          selected_magma = select_magma(mouse_pos)

        if placing_snipers == True and placing_turrets == False and placing_freezs == False and placing_magmas == False:
          if world.money >= c.BUY_COST2:
            create_sniper(mouse_pos)
        else:
          selected_sniper = select_sniper(mouse_pos)

        if placing_turrets == True and placing_snipers == False and placing_freezs == False and placing_magmas == False:
          #check if there is enough money for a turret
          if world.money >= c.BUY_COST:
            create_turret(mouse_pos)
        else:
          selected_turret = select_turret(mouse_pos)

        if placing_freezs == True and placing_snipers == False and placing_turrets == False and placing_magmas == False:
          if world.money >= c.BUY_COST3:
            create_freeze(mouse_pos)
        else:
          selected_freeze = select_freeze(mouse_pos)
        
        


  #update display
  pg.display.flip()

pg.quit()