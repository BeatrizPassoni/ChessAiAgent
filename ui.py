import pygame

class TextUI:
    def __init__(self, screen, text, x, y, fontSize, color):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = x
        self.fontSize = fontSize
        self.color = color
        self.font = pygame.font.SysFont("Arial", self.fontSize)
        self.centered = False