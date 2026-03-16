import pygame  # import pygame pro práci se sprite a vstupy
import os  # práce se souborovým systémem
from config import *  # načte konfigurační konstanty


class Player(pygame.sprite.Sprite):
    """Třída hráče; dědí od pygame.sprite.Sprite, má obraz, pozici a fyziku."""
    def __init__(self, x, y):
        super().__init__()  # inicializace rodičovské třídy

        image_loaded = False  # příznak, zda se podařilo načíst obrázek
        # preferované přípony obrázků
        supported_exts = (".png", ".jpg", ".jpeg", ".webp")
        scale_factor = 2  # násobitel velikosti obrázku oproti konstantám
        # vyzkouší několik adresářů pro hledání obrázku
        candidate_dirs = [os.path.join(os.getcwd(), "img"), os.path.join(os.path.dirname(os.path.dirname(__file__)), "img")]
        for img_dir in candidate_dirs:
            if not os.path.isdir(img_dir):
                continue  # přeskočí, pokud adresář neexistuje
            # nejprve hledej soubory obsahující 'rashy'
            candidates = [f for f in os.listdir(img_dir) if 'rashy' in f.lower() and f.lower().endswith(supported_exts)]
            if not candidates:
                # pokud žádný neobsahuje 'rashy', vezmi všechny podporované obrázky
                candidates = [f for f in os.listdir(img_dir) if f.lower().endswith(supported_exts)]
            for fname in candidates:
                image_path = os.path.join(img_dir, fname)
                try:
                    loaded = pygame.image.load(image_path)  # načte obrázek
                    try:
                        loaded = loaded.convert_alpha()  # převod pro rychlejší blit s alfa kanálem
                    except Exception:
                        loaded = loaded.convert()
                    loaded.set_colorkey((255, 255, 255))  # průhledná bílá, pokud nějaká
                    loaded = loaded.convert_alpha()
                    target_size = (PLAYER_WIDTH * scale_factor, PLAYER_HEIGHT * scale_factor)
                    try:
                        # pokus o hladké škálování
                        self.image = pygame.transform.smoothscale(loaded, target_size)
                    except Exception:
                        # fallback na základní škálování
                        self.image = pygame.transform.scale(loaded, target_size)
                    print(f"Načten obrázek hráče: {image_path} (zvětšeno {scale_factor}×)")
                    image_loaded = True
                    break
                except (pygame.error, FileNotFoundError) as e:
                    # vypíše chybu a pokračuje v dalších kandidátech
                    print(f"Nepodařilo se načíst {image_path}: {e}")
                    continue
            if image_loaded:
                break

        if not image_loaded:
            # vytvoří jednoduchý barevný obdélník když obrázek není dostupný
            target_size = (PLAYER_WIDTH * scale_factor, PLAYER_HEIGHT * scale_factor)
            self.image = pygame.Surface(target_size, pygame.SRCALPHA).convert_alpha()
            self.image.fill(PLAYER_COLOUR)

        self.rect = self.image.get_rect()  # obdélník pro pozici a kolize
        self.rect.x = x  # počáteční x pozice
        self.rect.y = y  # počáteční y pozice

        self.velocity_x = 0  # horizontální rychlost
        self.velocity_y = 0  # vertikální rychlost

        self.on_ground = False  # zda hráč stojí na zemi

    def update(self, platforms):
        # získá stisknuté klávesy
        keys = pygame.key.get_pressed()
        self.velocity_x = 0  # reset vodorovné rychlosti

        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED  # pohyb doprava

        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED  # pohyb doleva

        # skok: Space, šipka nahoru nebo W; pouze pokud na zemi
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = -JUMP_POWER
            self.on_ground = False

        # přidej gravitaci
        self.velocity_y += GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15  # limit pádu

        # aktualizuj pozici podle rychlosti
        self.rect.x += self.velocity_x
        # omez hráče na obrazovku
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.rect.y += self.velocity_y

        self.on_ground = False  # předpokládáme, že nesedí na zemi, dokud kolize neprokáže opak

        # kontrola kolizí s plošinami
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    # dopad na platformu shora
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    # narazil do spodní strany plošiny při skoku
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        # pokud spadne pod obrazovku, vrací True (game over)
        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        # vykreslí hráče na předaný surface
        screen.blit(self.image, self.rect)

