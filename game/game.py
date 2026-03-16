import pygame  # pygame knihovna pro grafiku a vstupy
import random  # generování náhodných čísel pro umístění mincí
from config import *  # import všech konstant z config.py
from game.player import Player  # import třídy hráče
from game.platform import Platform  # import třídy platformy
from game.coin import Coin  # import třídy mince
from game.enemy import Enemy  # import třídy nepřítele


class Game:
    """Hlavní třída hry. Obsahuje stav hry a řídí smyčku."""

    def __init__(self, screen):
        self.screen = screen  # surface, na který se bude kreslit
        self.clock = pygame.time.Clock()  # hodiny pro řízení FPS
        self.running = True  # příznak, zda má hlavní smyčka běžet
        self.all_sprites = pygame.sprite.Group()  # skupina všech sprite objektů
        self.platforms = pygame.sprite.Group()  # skupina pouze plošin

        # vytvoření hráče na počátečních souřadnicích
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)  # přidá hráče do skupiny všech sprite

        # vytvoření země (podlahy) a dvou dalších plošin
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        p1 = Platform(200, 400, 150, 20)
        p2 = Platform(500, 300, 120, 20)
        # přidání plošin do jejich skupiny i do skupiny všech sprite
        self.platforms.add(ground, p1, p2)
        self.all_sprites.add(ground, p1, p2)

        # příprava mincí: vytvoříme skupinu a náhodně je umístíme na plošiny
        self.coins = pygame.sprite.Group()
        platforms_list = list(self.platforms)  # převod na seznam pro volbu náhodné platformy
        num_coins = 3  # počet mincí v levelu
        coin_radius = 12  # poloměr mince
        for _ in range(num_coins):
            plat = random.choice(platforms_list)  # vybere náhodnou platformu
            margin = 10  # okraj, aby mince nebyla na samém okraji platformy
            min_x = plat.rect.left + margin  # minimální x pro umístění mince
            max_x = plat.rect.right - margin  # maximální x
            if max_x <= min_x:
                cx = plat.rect.centerx  # pokud je prostor malý, umístíme na střed
            else:
                cx = random.randint(min_x, max_x)  # jinak náhodné x v rozsahu
            cy = plat.rect.top - coin_radius  # y nad platformou, aby byla 'na' ní
            coin = Coin(cx, cy, radius=coin_radius)  # vytvoří instanci mince
            self.coins.add(coin)  # přidá minci do skupiny mincí
            self.all_sprites.add(coin)  # přidá minci i do všech sprite

        # stav hry: skóre a životy
        self.score = 0  # aktuální počet sebraných mincí
        self.lives = 3  # počet životů hráče
        # vlajka pro výhru (True pokud hráč sebere všechny mince)
        self.won = False

        # vytvoření nepřátel a jejich přidání
        self.enemies = pygame.sprite.Group()
        ground_y = ground.rect.top  # y-pozice povrchu země (nahoře)
        e1 = Enemy(150, ground_y - 40)  # umístíme nepřítele na zem
        e2 = Enemy(600, ground_y - 40)
        self.enemies.add(e1, e2)  # přidání nepřátel do jejich skupiny
        self.all_sprites.add(e1, e2)  # a zároveň do skupiny všech sprite

    def handle_events(self):
        """Zpracuje všechny události (klávesy, myš, zavření okna)."""
        for event in pygame.event.get():
            evt_name = pygame.event.event_name(event.type)  # čitelný název události

            if event.type == pygame.QUIT:
                self.running = False  # ukončí hlavní smyčku při zavření okna

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                evt_key = pygame.key.name(event.key)  # jméno stisknuté klávesy
                print(f"{evt_name}: {evt_key}")  # debug výpis událostí

            elif event.type == pygame.MOUSEMOTION:
                print(f"{evt_name}: {event.pos}")  # debug pozice myši

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                print(f"{evt_name}: {event.button} at {event.pos}")  # debug tlačítka myši

    def update(self):
        """Aktualizuje herní logiku: hráč, mince, nepřátelé a kolize."""
        game_over = self.player.update(self.platforms)  # update hráče a kontrola, jestli spadl
        if game_over:
            self.running = False  # pokud hráč spadl, zastav hru
            return

        # sběr mincí: detekuje kolizi hráče s mincemi
        collected = pygame.sprite.spritecollide(self.player, self.coins, False)
        if collected:
            for c in collected:
                c.kill()  # odstraní minci z herního světa
            self.score += len(collected)  # přičte počet sebraných mincí
            print(f"Coins collected: {self.score}")  # debug

        # podmínka výhry: všechny mince sebrány
        if len(self.coins) == 0:
            print("You collected all coins! You win!")
            self.won = True
            self.running = False
            return

        # aktualizace nepřátel (pohyb a fyzika)
        for e in list(self.enemies):
            e.update(self.platforms)

        # detekce kolizí hráč vs nepřítel
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            for enemy in enemy_hits:
                # pokud hráč padá dolů a zasáhne nepřítele z vrchu -> sešlápnutí
                if getattr(self.player, 'velocity_y', 0) > 0 and (self.player.rect.bottom - enemy.rect.top) <= 12:
                    enemy.kill()  # odstraní nepřítele
                    self.player.velocity_y = -JUMP_POWER / 1.5  # odraz hráče po sešlápnutí
                    print("Enemy stomped and killed")
                else:
                    # hráč utrpí poškození
                    self.lives -= 1
                    print(f"Player hit! Lives left: {self.lives}")
                    # respawn hráče na startovní pozici
                    self.player.rect.x = 100
                    self.player.rect.y = 100
                    self.player.velocity_x = 0
                    self.player.velocity_y = 0
                    if self.lives <= 0:
                        print("No lives left. Game over.")
                        self.won = False
                        self.running = False

    def draw(self):
        """Vykreslí všechny objekty na obrazovku a přepne buffer."""
        self.screen.fill(SKY_BLUE)  # vyplní pozadí barvou nebe
        for sprite in self.all_sprites:
            sprite.draw(self.screen)  # každý sprite má vlastní draw metodu
        pygame.display.flip()  # aktualizuje obrazovku

    def show_end_screen(self):
        """Zobrazí koncové hlášení (výhra/prohra) a počká krátce nebo na stisk klávesy."""
        # zkus vytvořit font; pokud není inicializovaný, inicializuj modul font
        try:
            font = pygame.font.SysFont(None, 72)
        except Exception:
            pygame.font.init()
            font = pygame.font.SysFont(None, 72)

        # vybere text a barvu podle výsledku
        if self.won:
            text = "You Win!"
            color = (255, 215, 0)
        else:
            text = "Game Over"
            color = (255, 50, 50)

        surf = font.render(text, True, color)  # vytvoří povrch s textem
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # vystředí text

        start = pygame.time.get_ticks()  # čas začátku zobrazení
        showing = True
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    showing = False
                    break
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    showing = False
                    break

            self.screen.fill(SKY_BLUE)  # vykreslí pozadí
            for sprite in self.all_sprites:
                sprite.draw(self.screen)  # vykreslí herní objekty i na koncovém screen
            self.screen.blit(surf, rect)  # vykreslí text
            pygame.display.flip()
            self.clock.tick(FPS)  # omezí cyklus na cílové FPS
            if pygame.time.get_ticks() - start > 3000:
                showing = False  # po 3 sekundách automaticky zavře end screen

    def run(self):
        """Hlavní herní smyčka: zpracování událostí, update a draw dokud running = True."""
        while self.running:
            self.handle_events()  # zpracuj vstupy
            self.update()  # aktualizuj logiku
            self.draw()  # vykresli scény
            self.clock.tick(FPS)  # pauza podle FPS
        # po skončení hlavní smyčky ukáže ukončovací obrazovku
        self.show_end_screen()
        
