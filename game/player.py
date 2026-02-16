import pygame
import os
from config import * 

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        image_loaded = False


        for name in ["Rashford","Rashy","Goat"]:
            for ext in ["png","jpg","jpeg", "webp"]:
                try:
                    image_path = os.path.join("img", f"{name}.{ext}")
                    self.image = pygame.image.load(image_path).convert_alpha
                    self.imag = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    print(f"Načten obrázek hráče: {image_path}")
                    image_loaded = True

                    break
                except(pygame.error,FileNotFoundError):
                    print(f"Player nebyl nalezen{pygame.error}")
                    continue

        if not image_loaded:

            self.image = pygame([PLAYER_WIDTH, PLAYER_HEIGHT])
            self.image.fill(PLAYER_COLOUR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_x = 0
        self.velocity_y = 0

        self.on_ground = False
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_POWER
            self.on_ground = False
