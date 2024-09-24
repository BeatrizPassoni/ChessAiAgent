import pygame

# Inicializa o Pygame e o sistema de fontes
pygame.init()
pygame.font.init()

class Setting:
    def __init__(self):
        # Define o tamanho do tabuleiro
        self.boardSize = 8
        # Define o tamanho do ícone da janela
        self.windowIconSize = 30
        # Define a largura da janela
        self.width = 1600
        # Define a altura da janela
        self.height = 900
        # Define a resolução da janela
        self.resolution = (self.width, self.height)
        # Define a margem superior do tabuleiro
        self.top_offset = 20
        # Calcula o tamanho de cada casa do tabuleiro
        self.spotSize = (self.height - self.top_offset) // self.boardSize
        # Calcula o deslocamento horizontal para centralizar o tabuleiro
        self.horizontal_offset = self.width // 2 - (self.spotSize * (self.boardSize // 2))
        # Define os quadros por segundo (FPS) para a janela
        self.fps = 60
        # Inicializa a fonte para coordenadas
        self.CoordFont = pygame.font.SysFont("jaapokki", 18, bold=True)
        # Define o contorno de destaque
        self.highlightOutline = 5
        # Índice do tema (para uso futuro)
        self.themeIndex = -1
        # Define a profundidade da IA (dificuldade da IA)
        self.AI_DEPTH = 3

# Cria uma instância da classe Setting
Config = Setting()
