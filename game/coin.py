import pygame  # knihovna pro vykreslování a práci se surface/rect
from config import *  # načtení konfigurace a konstant (rozměry, barvy)


class Coin(pygame.sprite.Sprite):
    """Jednoduchá sběratelná mince vykreslená jako kruh."""

    def __init__(self, x, y, radius=12):
        super().__init__()  # inicializace rodičovské třídy Sprite
        diameter = radius * 2  # průměr podle poloměru
        # vytvoří průhledný surface pro kreslení kruhu
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA).convert_alpha()
        # nakreslí zlatý kruh reprezentující minci
        pygame.draw.circle(self.image, (255, 223, 0), (radius, radius), radius)
        # přidá tenčí tmavší obrys pro viditelnost
        pygame.draw.circle(self.image, (200, 160, 0), (radius, radius), radius, 2)
        # získá rect pro pozici a kolize
        self.rect = self.image.get_rect()
        # nastaví střed mince na zadané souřadnice
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self, screen):
        # vykreslí minci na předaný surface (obrazovku)
        screen.blit(self.image, self.rect)
