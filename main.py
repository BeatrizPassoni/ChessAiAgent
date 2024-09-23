import pygame
import sys
from setting import Config
from chess import Chess

def main():
    # initialize pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(Config.resolution)

    # load and set icon of the main window
    loaded_icon = pygame.image.load("./assets/images/white_knight.png")
    main_icon = pygame.transform.smoothscale(loaded_icon, (Config.windowIconSize, Config.windowIconSize))
    pygame.display.set_icon(main_icon)

    # Initialize Chess game directly
    chess_game = Chess(screen)
    chess_game.vsComputer()  # Start the game against the computer

    # quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
