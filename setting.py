import pygame

pygame.init()
pygame.font.init()

class Setting:
    def __init__(self):
        self.boardSize = 8
        self.windowIconSize = 30
        self.width = 1600
        self.height = 900
        self.resolution = (self.width, self.height)
        self.top_offset = 20
        self.spotSize = (self.height - self.top_offset) // self.boardSize
        self.horizontal_offset = self.width // 2 - (self.spotSize * (self.boardSize // 2))
        self.fps = 60
        self.CoordFont = pygame.font.SysFont("jaapokki", 18, bold=True)
        self.highlightOutline = 5
        self.themeIndex = -1
        # CHANGE THE AI DIFFICULTY
        self.AI_DEPTH = 3
        self.themes = [
            # GREEN THEME
            {"dark": (118, 148, 85), "light": (234, 238, 210), "outline": (0, 0, 0)}
        ]

Config = Setting()
