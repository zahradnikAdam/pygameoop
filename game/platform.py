import pygame  # pygame pro práci se surface/rect
from config import *  # import konstant a nastavení


class Platform(pygame.sprite.Sprite):
    """Statická plošina (obdélník) na které může hráč stát."""

    def __init__(self, x, y, width, height):
        super().__init__()  # inicializace rodiče
        # vytvoří surface o dané velikosti
        self.image = pygame.Surface((width, height)).convert()
        self.image.fill(PLATFORM_COLOR)  # vyplní barvou platformy
        self.rect = self.image.get_rect()  # rect pro pozici/kolize
        self.rect.x = x  # nastaví x
        self.rect.y = y  # nastaví y

    def draw(self, screen):
        # vykreslí plošinu
        screen.blit(self.image, self.rect)