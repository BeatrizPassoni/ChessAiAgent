from pieces import *
from utils import *
from setting import Config
from tools import Position

def GetFenPieces(character, x, y):
    # Mapeia os caracteres da notação FEN para suas respectivas peças
    FenPieces = {
        "K": King(Position(x, y), 0),  # Rei branco
        "Q": Queen(Position(x, y), 0),  # Rainha branca
        "B": Bishop(Position(x, y), 0),  # Bispo branco
        "N": Knight(Position(x, y), 0),  # Cavalo branco
        "R": Rook(Position(x, y), 0),  # Torre branca
        "P": Pawn(Position(x, y), 0),  # Peão branco

        "k": King(Position(x, y), 1),  # Rei preto
        "q": Queen(Position(x, y), 1),  # Rainha preta
        "b": Bishop(Position(x, y), 1),  # Bispo preto
        "n": Knight(Position(x, y), 1),  # Cavalo preto
        "r": Rook(Position(x, y), 1),  # Torre preta
        "p": Pawn(Position(x, y), 1),  # Peão preto
    }

    # Retorna a peça correspondente ao caractere, se existir
    if character in FenPieces:
        return FenPieces[character]
    else:
        return None  # Retorna None se o caractere não for uma peça válida

# A função de notação FEN retorna uma grade formatada de posições
def FEN(positionstring):
    # Inicializa uma grade vazia
    boardGrid = [[None for i in range(Config.boardSize)] for j in range(Config.boardSize)]
    # Manipula o primeiro campo: posicionamento das peças
    row = 0
    col = 0
    for character in positionstring:
        piece = GetFenPieces(character, row, col)  # Obtém a peça correspondente
        if piece:
            boardGrid[row][col] = piece  # Adiciona a peça à grade
            row += 1  # Move para a próxima linha
        elif character.isnumeric():
            row += int(character)  # Avança linhas de acordo com o número
        elif character == "/":
            col += 1  # Muda para a próxima coluna
            row = 0  # Reseta a linha para o início

    # Esta função FEN não leva em conta a vez do jogador
    # Esta função FEN não está completa
    # Geralmente, uma função FEN considera todos os 6 campos da notação FEN
    # Mas para este caso, só precisamos do primeiro campo para a posição
    return boardGrid  # Retorna a grade de peças

# FEN("")  # Chamada de função comentada
