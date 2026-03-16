import pygame  # importuje knihovnu pygame pro grafiku a vstupy
from config import *  # importuje všechna nastavení a konstanty z config.py
from game.game import Game  # importuje třídu Game, která řídí hru


def main():
    pygame.init()  # inicializuje všechny moduly pygame
    # vytvoří okno s rozměry definovanými v configu
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Rashfordík")  # nastaví název okna

    game = Game(screen)  # vytvoří instanci hry a předá jí povrch (screen)
    game.run()  # spustí hlavní herní smyčku

    pygame.quit()  # ukončí pygame a uvolní zdroje


if __name__ == "__main__":
    main()  # spustí hlavní funkci, pokud je soubor spuštěn přímo