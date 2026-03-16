import pygame  # pygame pro práci se surface a rect
import os  # práce s filesystemem
import random  # pro náhodný výběr obrázku
from config import *  # načte konstanty


class Enemy(pygame.sprite.Sprite):
    """Jednoduchý nepřítel s horizontální patrolo a gravitační fyzikou."""

    def __init__(self, x, y, width=ENEMY_WIDTH, height=ENEMY_HEIGHT):
        super().__init__()  # init rodiče
        image_loaded = False  # příznak, že se podařilo načíst obrázek
        img_dir = os.path.join(os.getcwd(), "img")  # předpokládaná složka s obrázky
        supported_exts = (".png", ".jpg", ".jpeg", ".webp")  # podporované přípony

        # upřednostní soubory obsahující 'vvd' v názvu, jinak vezme náhodný obrázek
        if os.path.isdir(img_dir):
            candidates = [f for f in os.listdir(img_dir) if 'vvd' in f.lower() and f.lower().endswith(supported_exts)]
            if not candidates:
                candidates = [f for f in os.listdir(img_dir) if f.lower().endswith(supported_exts)]
            if candidates:
                fname = random.choice(candidates)
                try:
                    loaded = pygame.image.load(os.path.join(img_dir, fname)).convert_alpha()
                    # zmenší/škáluje obrázek na požadované rozměry nepřítele
                    self.image = pygame.transform.scale(loaded, (width, height))
                    image_loaded = True
                except Exception:
                    image_loaded = False

        if not image_loaded:
            # fallback: jednoduchý červený obdélník
            self.image = pygame.Surface((width, height)).convert()
            self.image.fill((200, 0, 0))

        self.rect = self.image.get_rect()  # rect pro pozici a kolize
        self.rect.x = x  # počáteční x
        self.rect.y = y  # počáteční y

        # parametry patroly a fyziky
        self.velocity_x = 2  # rychlost pohybu v x
        self.velocity_y = 0  # rychlost v y
        self.patrol_left = x - 80  # levá hranice patroly
        self.patrol_right = x + 80  # pravá hranice patroly

    def update(self, platforms):
        # pohyb do stran
        self.rect.x += self.velocity_x
        if self.rect.left < self.patrol_left or self.rect.right > self.patrol_right:
            # pokud dosáhl hranice, otoč směr
            self.velocity_x = -self.velocity_x
            self.rect.x += self.velocity_x

        # aplikuj gravitaci
        self.velocity_y += GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15  # omez rychlost pádu
        self.rect.y += self.velocity_y

        # stoj na plošinách (pokud dopadá shora)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0

    def draw(self, screen):
        # vykreslení nepřítele
        screen.blit(self.image, self.rect)
