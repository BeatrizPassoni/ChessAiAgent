import pygame  # Importa a biblioteca Pygame para interface gráfica
from pieces import *  # Importa todas as classes de peças
from tools import Position  # Importa a classe Position para manipulação de posições
import math  # Importa a biblioteca math (não utilizada no trecho fornecido)
from Fen import *  # Importa a classe FEN para inicialização do tabuleiro

class Board:
    def __init__(self):
        # Inicializa o estado do tabuleiro e as variáveis do jogo
        self.player = 0  # Jogador atual (0 -> branco, 1 -> preto)
        self.historic = []  # Histórico de movimentos
        self.moveIndex = 1  # Índice do movimento atual
        self.font = pygame.font.SysFont("Consolas", 18, bold=True)  # Fonte para exibição
        self.grid = FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")  # Inicializa o tabuleiro com a FEN padrão
        self.WhiteKing = None  # Rei branco
        self.BlackKing = None  # Rei preto

        # Localiza e define os reis
        for pieces in self.grid:
            for piece in pieces:
                if piece:
                    if piece.color == 0 and piece.code == "k":
                        self.WhiteKing = piece
                    elif piece.color == 1 and piece.code == "k":
                        self.BlackKing = piece
        
        # Variáveis para controle de xeque
        self.checkWhiteKing = False
        self.checkBlackKing = False

        self.winner = None  # Armazena o vencedor
        self.pieceToPromote = None  # Armazena peças a serem promovidas

        # Listas de promoções para peões
        self.whitePromotions = [Queen(Position(0, 0), 0), Bishop(Position(0, 1), 0), Knight(Position(0, 2), 0), Rook(Position(0, 3), 0)]
        self.blackPromotions = [Rook(Position(0, 7), 1), Knight(Position(0, 6), 1), Bishop(Position(0, 5), 1), Queen(Position(0, 4), 1)]

        self.check_message = None  # Mensagem de xeque

    def Forfeit(self):
        # Função para desistir (não implementada)
        pass

    def GetPiece(self, coord):
        # Retorna a peça na posição dada
        return self.grid[coord.x][coord.y]

    def SetPiece(self, position, piece):
        # Define uma peça na posição dada
        self.grid[position.x][position.y] = piece

    def SwitchTurn(self):
        # Troca entre os jogadores
        if self.winner is not None:  # Verifica se o jogo terminou
            return  # Não permite movimento após xeque-mate
        self.player = (self.player + 1) * -1 + 2  # Alterna entre 0 e 1
        self.IsCheckmate()  # Verifica xeque-mate após a troca

    def RecentMove(self):
        # Retorna o último movimento realizado
        return None if not self.historic else self.historic[-1]

    def RecentMovePositions(self):
        # Retorna as posições do último movimento
        if not self.historic or len(self.historic) <= 1:
            return None, None
        pos = self.historic[-1][3]
        oldPos = self.historic[-1][4]
        return pos.GetCopy(), oldPos.GetCopy()

    def AllowedMoveList(self, piece, moves, isAI):
        # Filtra a lista de movimentos permitidos
        allowed_moves = []
        for move in moves:
            if self.VerifyMove(piece, move.GetCopy(), isAI):
                allowed_moves.append(move.GetCopy())
        return allowed_moves

    def GetAllowedMoves(self, piece, isAI=False):
        # Obtém movimentos e capturas permitidos para a peça
        moves, captures = piece.GetMoves(self)
        allowed_moves = self.AllowedMoveList(piece, moves.copy(), isAI)
        allowed_captures = self.AllowedMoveList(piece, captures.copy(), isAI)
        return allowed_moves, allowed_captures

    def Move(self, piece, position):
        # Realiza um movimento
        if position is not None:
            position = position.GetCopy()
            if self.isCastling(piece, position.GetCopy()):
                self.CastleKing(piece, position.GetCopy())
            elif self.isEnPassant(piece, position.GetCopy()):
                self.grid[position.x][piece.position.y] = None  # Remove a peça capturada en passant
                self.MovePiece(piece, position)
                self.historic[-1][2] = piece.code + " EP"
            else:
                self.MovePiece(piece, position)

            # Verifica promoção de peão
            if isinstance(piece, Pawn) and (piece.position.y == 0 or piece.position.y == 7):
                self.pieceToPromote = piece
            else:
                self.SwitchTurn()

            self.Check()  # Verifica xeque
            self.IsCheckmate()  # Verifica xeque-mate
            self.CheckKingCaptured()  # Verifica se um rei foi capturado

    def MovePiece(self, piece, position):
        # Move uma peça para uma nova posição
        position = position.GetCopy()
        captured_piece = self.grid[position.x][position.y]
        self.grid[piece.position.x][piece.position.y] = None  # Remove a peça da posição anterior
        old_position = piece.position.GetCopy()  # Salva a posição antiga
        piece.updatePosition(position)  # Atualiza a posição da peça
        self.grid[position.x][position.y] = piece  # Coloca a peça na nova posição
        self.historic.append([self.moveIndex, piece.color, piece.code, old_position, piece.position, piece])  # Adiciona ao histórico
        piece.previousMove = self.moveIndex
        self.moveIndex += 1
        self.checkBlackKing = False
        self.checkWhiteKing = False

    def VerifyMove(self, piece, move, isAI):
        # Verifica se um movimento é válido
        position = move.GetCopy()
        oldPosition = piece.position.GetCopy()
        captureEnPassant = None
        capturedPiece = self.grid[position.x][position.y]
        
        if self.isEnPassant(piece, position):
            captureEnPassant = self.grid[position.x][oldPosition.y]
            self.grid[position.x][oldPosition.y] = None  # Remove a peça capturada en passant

        self.grid[oldPosition.x][oldPosition.y] = None  # Remove a peça da posição antiga
        self.grid[position.x][position.y] = piece  # Move a peça
        piece.updatePosition(move)

        self.UndoMove(piece, capturedPiece, oldPosition, position)  # Reverte o movimento se necessário
        if captureEnPassant is not None:
            self.grid[position.x][oldPosition.y] = captureEnPassant  # Restaura a peça capturada en passant

        return True  # Movimento sempre permitido

    def UndoMove(self, piece, captured, oldPos, pos):
        # Desfaz um movimento
        self.grid[oldPos.x][oldPos.y] = piece  # Restaura a peça na posição antiga
        self.grid[pos.x][pos.y] = captured  # Restaura a peça capturada
        piece.updatePosition(oldPos)  # Atualiza a posição da peça

    def GetEnemyCaptures(self, player):
        # Obtém movimentos de captura dos inimigos
        captures = []
        for pieces in self.grid:
            for piece in pieces:
                if piece and piece.color != player:
                    moves, piececaptures = piece.GetMoves(self)
                    captures.extend(piececaptures)  # Adiciona as capturas
        return captures

    def isCastling(self, king, position):
        # Verifica se é um movimento de roque
        return isinstance(king, King) and abs(king.position.x - position.x) > 1

    def isEnPassant(self, piece, newPos):
        # Verifica se um movimento é en passant
        if not isinstance(piece, Pawn):
            return False
        moves = piece.EnPassant(self, -1 if piece.color == 0 else 1)  # Define a direção do movimento
        return newPos in moves

    def IsInCheck(self, piece):
        # Verifica se um rei está em xeque
        return isinstance(piece, King) and \
                ((piece.color == 0 and self.checkWhiteKing) or (piece.color == 1 and self.checkBlackKing))

    def CastleKing(self, king, position):
        # Executa um movimento de roque
        position = position.GetCopy()
        if position.x == 2 or position.x == 6:  # Verifica se é roque curto ou longo
            if position.x == 2:
                rook = self.grid[0][king.position.y]
                self.MovePiece(king, position)  # Move o rei
                self.grid[0][rook.position.y] = None  # Remove a torre
                rook.position.x = 3  # Move a torre
            else:
                rook = self.grid[7][king.position.y]
                self.MovePiece(king, position)  # Move o rei
                self.grid[7][rook.position.y] = None  # Remove a torre
                rook.position.x = 5  # Move a torre

            rook.previousMove = self.moveIndex - 1  # Atualiza o movimento anterior da torre
            self.grid[rook.position.x][rook.position.y] = rook
            self.historic[-1][2] = king.code + " C"  # Marca o movimento de roque

    def PromotePawn(self, pawn, choice):
        # Promove um peão
        promotion_pieces = [Queen, Bishop, Knight, Rook]  # Lista de peças para promoção
        self.grid[pawn.position.x][pawn.position.y] = promotion_pieces[choice](pawn.position.GetCopy(), pawn.color)
        self.SwitchTurn()  # Troca de turno
        self.Check()  # Verifica xeque
        self.pieceToPromote = None  # Reseta a promoção

    def MoveSimulation(self, piece, next_pos):
        # Simula um movimento sem efetivar
        if self.grid[next_pos.x][next_pos.y] is None:
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()  # Atualiza a posição
            self.grid[next_pos.x][next_pos.y] = piece  # Coloca a peça na nova posição
            return None
        else:
            prev_piece = self.grid[next_pos.x][next_pos.y]
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()  # Atualiza a posição
            self.grid[next_pos.x][next_pos.y] = piece  # Coloca a peça na nova posição
            return prev_piece

    def Check(self):
        # Verifica se o rei está em xeque
        king = self.WhiteKing if self.player == 0 else self.BlackKing
        in_check = False
        for row in self.grid:
            for piece in row:
                if piece and piece.color != self.player:
                    moves, captures = piece.GetMoves(self)
                    if king.position in moves or king.position in captures:
                        in_check = True

        if self.player == 0:
            self.checkWhiteKing = in_check
        else:
            self.checkBlackKing = in_check

    def IsCheckmate(self):
        # Verifica se é xeque-mate
        king = self.WhiteKing if self.player == 0 else self.BlackKing
        if (self.checkWhiteKing and self.player == 0) or (self.checkBlackKing and self.player == 1):
            pieces = [p for row in self.grid for p in row if p and p.color == self.player]
            for piece in pieces:
                moves, captures = self.GetAllowedMoves(piece)
                if moves or captures:
                    return  # Há movimentos válidos, então não é xeque-mate
            # Se não há movimentos válidos, é xeque-mate
            self.winner = 1 if self.player == 0 else 0
            self.check_message = "Xeque-mate!"  # Mensagem de xeque-mate

    def CheckKingCaptured(self):
        # Verifica se um rei foi capturado
        if self.WhiteKing not in [piece for row in self.grid for piece in row if piece]:
            self.winner = 1  # Rei branco capturado, preto ganha
            self.check_message = "Rei branco capturado! Preto vence!"
        elif self.BlackKing not in [piece for row in self.grid for piece in row if piece]:
            self.winner = 0  # Rei preto capturado, branco ganha
            self.check_message = "Rei preto capturado! Branco vence!"
