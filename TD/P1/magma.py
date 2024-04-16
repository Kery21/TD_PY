import pygame as pg
import constants as c
from magma_data import MAGMA_DATA


class Magma(pg.sprite.Sprite):
    def __init__(self, images, tile_x, tile_y):
        self.upgrade_level = 1
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        self.selected = False
        self.range = MAGMA_DATA[self.upgrade_level-1].get("range")
        self.cooldown = MAGMA_DATA[self.upgrade_level-1].get("cooldown")
        self.last_shot = pg.time.get_ticks()

        self.images = images
        self.image = self.images[self.upgrade_level-1].convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def load_images(self):
        self.image = self.images[self.upgrade_level-1].convert_alpha()


    def upgrade(self):
        self.upgrade_level += 1
        self.range = MAGMA_DATA[self.upgrade_level-1].get("range")
        self.cooldown = MAGMA_DATA[self.upgrade_level-1].get("cooldown")

        self.images[self.upgrade_level-1].convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center