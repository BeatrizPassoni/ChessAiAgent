import pygame
from setting import Config

# Define o tamanho de destaque para as peças
highlight_size = (Config.spotSize + 5, Config.spotSize + 5)

# Carrega as imagens das peças brancas
white_pawn = pygame.image.load("./assets/images/white_pawn.png")
white_bishop = pygame.image.load("./assets/images/white_bishop.png")
white_knight = pygame.image.load("./assets/images/white_knight.png")
white_rook = pygame.image.load("./assets/images/white_rook.png")
white_queen = pygame.image.load("./assets/images/white_queen.png")
white_king = pygame.image.load("./assets/images/white_king.png")

# Carrega as imagens das peças pretas
black_pawn = pygame.image.load("./assets/images/black_pawn.png")
black_bishop = pygame.image.load("./assets/images/black_bishop.png")
black_knight = pygame.image.load("./assets/images/black_knight.png")
black_rook = pygame.image.load("./assets/images/black_rook.png")
black_queen = pygame.image.load("./assets/images/black_queen.png")
black_king = pygame.image.load("./assets/images/black_king.png")

def translate(value, min1, max1, min2, max2):
    # Transforma um valor de uma faixa para outra
    return min2 + (max2 - min2) * ((value - min1) / (max1 - min1))

def GetSprite(piece):
    # Obtém o sprite da peça com base em seu tipo e cor
    sprite = None
    if piece.code == 'p':
        # Se for um peão, seleciona a imagem correspondente
        if piece.color == 0:
            sprite = white_pawn  # Peão branco
        else:
            sprite = black_pawn  # Peão preto
    elif piece.code == 'b':
        # Se for um bispo, seleciona a imagem correspondente
        if piece.color == 0:
            sprite = white_bishop  # Bispo branco
        else:
            sprite = black_bishop  # Bispo preto
    elif piece.code == 'n':
        # Se for um cavalo, seleciona a imagem correspondente
        if piece.color == 0:
            sprite = white_knight  # Cavalo branco
        else:
            sprite = black_knight  # Cavalo preto
    elif piece.code == 'r':
        # Se for uma torre, seleciona a imagem correspondente
        if piece.color == 0:
            sprite = white_rook  # Torre branca
        else:
            sprite = black_rook  # Torre preta
    elif piece.code == 'q':
        # Se for uma rainha, seleciona a imagem correspondente
        if piece.color == 0:
            sprite = white_queen  # Rainha branca
        else:
            sprite = black_queen  # Rainha preta
    else:
        # Se for um rei, seleciona a imagem correspondente
        if piece.color == 0:
            sprite = white_king  # Rei branco
        else:
            sprite = black_king  # Rei preto
    
    # Redimensiona a imagem da peça para o tamanho configurado
    transformed = pygame.transform.smoothscale(sprite, (Config.spotSize, Config.spotSize))
    return transformed
