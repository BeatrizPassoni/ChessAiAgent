import pygame
from pieces import *
from tools import Position
import math
from Fen import *

class Board:
    def __init__(self):
        # 0 -> white , 1 -> Black
        self.player = 0
        self.historic = []
        self.moveIndex = 1
        self.font = pygame.font.SysFont("Consolas", 18, bold=True)
        self.grid = FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.WhiteKing = None
        self.BlackKing = None
        for pieces in self.grid:
            for piece in pieces:
                if piece != None:
                    if piece.color == 0 and piece.code == "k":
                        self.WhiteKing = piece
                    elif piece.color == 1 and piece.code == "k":
                        self.BlackKing = piece
        self.checkWhiteKing = False
        self.checkBlackKing = False

        self.winner = None
        self.pieceToPromote = None

        self.whitePromotions = [Queen(Position(0, 0), 0), Bishop(Position(0, 1), 0), Knight(Position(0, 2), 0), Rook(Position(0, 3), 0)]
        self.blackPromotions = [Rook(Position(0, 7), 1), Knight(Position(0, 6), 1), Bishop(Position(0, 5), 1), Queen(Position(0, 4), 1)]

        self.check_message = None  # Adicionar uma variável para armazenar mensagens de xeque

    def Forfeit(self):
        # resign
        pass

    def GetPiece(self, coord):
        return self.grid[coord.x][coord.y]

    def SetPiece(self, position, piece):
        self.grid[position.x][position.y] = piece

    def SwitchTurn(self):
        if self.winner is not None:  # Verificar se o jogo terminou
            return  # Bloqueia o movimento após xeque-mate

        # switch between 0 and 1
        self.player = (self.player + 1) * -1 + 2
        # CHECK IF THE PLAYER LOST OR NOT
        self.IsCheckmate()  # Verifica se há xeque-mate após a troca de turnos

    def RecentMove(self):
        return None if not self.historic else self.historic[-1]

    def RecentMovePositions(self):
        if not self.historic or len(self.historic) <= 1:
            return None, None
        pos = self.historic[-1][3]
        oldPos = self.historic[-1][4]

        return pos.GetCopy(), oldPos.GetCopy()

    def AllowedMoveList(self, piece, moves, isAI):
        allowed_moves = []
        for move in moves:
            if self.VerifyMove(piece, move.GetCopy(), isAI):
                allowed_moves.append(move.GetCopy())
        return allowed_moves

    def GetAllowedMoves(self, piece, isAI=False):
        moves, captures = piece.GetMoves(self)
        allowed_moves = self.AllowedMoveList(piece, moves.copy(), isAI)
        allowed_captures = self.AllowedMoveList(piece, captures.copy(), isAI)
        return allowed_moves, allowed_captures

    def Move(self, piece, position):
        if position != None:
            position = position.GetCopy()
            if self.isCastling(piece, position.GetCopy()):
                self.CastleKing(piece, position.GetCopy())
            elif self.isEnPassant(piece, position.GetCopy()):
                self.grid[position.x][piece.position.y] = None
                self.MovePiece(piece, position)
                self.historic[-1][2] = piece.code + " EP"
            else:
                self.MovePiece(piece, position)

            # Check for promotion
            if type(piece) == Pawn and (piece.position.y == 0 or piece.position.y == 7):
                self.pieceToPromote = piece
            else:
                self.SwitchTurn()

            self.Check()  # Verifica se há xeque
            self.IsCheckmate()  # Verifica se há xeque-mate

            # Verifica se um rei foi capturado
            self.CheckKingCaptured()

    def MovePiece(self, piece, position):
        position = position.GetCopy()
        captured_piece = self.grid[position.x][position.y]
        self.grid[piece.position.x][piece.position.y] = None
        old_position = piece.position.GetCopy()
        piece.updatePosition(position)
        self.grid[position.x][position.y] = piece
        self.historic.append([self.moveIndex, piece.color, piece.code, old_position, piece.position, piece])
        piece.previousMove = self.moveIndex
        self.moveIndex += 1
        self.checkBlackKing = False
        self.checkWhiteKing = False

    def VerifyMove(self, piece, move, isAI):
        position = move.GetCopy()
        oldPosition = piece.position.GetCopy()
        captureEnPassant = None
        capturedPiece = self.grid[position.x][position.y]
        if self.isEnPassant(piece, position):
            captureEnPassant = self.grid[position.x][oldPosition.y]
            self.grid[position.x][oldPosition.y] = None

        self.grid[oldPosition.x][oldPosition.y] = None
        self.grid[position.x][position.y] = piece
        piece.updatePosition(move)

        self.UndoMove(piece, capturedPiece, oldPosition, position)
        if captureEnPassant is not None:
            self.grid[position.x][oldPosition.y] = captureEnPassant

        return True  # Sempre permite o movimento

    def UndoMove(self, piece, captured, oldPos, pos):
        self.grid[oldPos.x][oldPos.y] = piece
        self.grid[pos.x][pos.y] = captured
        piece.updatePosition(oldPos)

    def GetEnemyCaptures(self, player):
        captures = []
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color != player:
                    moves, piececaptures = piece.GetMoves(self)
                    captures = captures + piececaptures
        return captures

    def isCastling(self, king, position):
        return type(king) == King and abs(king.position.x - position.x) > 1

    def isEnPassant(self, piece, newPos):
        if type(piece) != Pawn:
            return False
        moves = None
        if piece.color == 0:
            moves = piece.EnPassant(self, -1)
        else:
            moves = piece.EnPassant(self, 1)
        return newPos in moves

    def IsInCheck(self, piece):
        return type(piece) == King and \
                ((piece.color == 0 and self.checkWhiteKing) or (piece.color == 1 and self.checkBlackKing))

    def CastleKing(self, king, position):
        position = position.GetCopy()
        if position.x == 2 or position.x == 6:
            if position.x == 2:
                rook = self.grid[0][king.position.y]
                self.MovePiece(king, position)
                self.grid[0][rook.position.y] = None
                rook.position.x = 3
            else:
                rook = self.grid[7][king.position.y]
                self.MovePiece(king, position)
                self.grid[7][rook.position.y] = None
                rook.position.x = 5

            rook.previousMove = self.moveIndex - 1
            self.grid[rook.position.x][rook.position.y] = rook
            self.historic[-1][2] = king.code + " C"

    def PromotePawn(self, pawn, choice):
        if choice == 0:
            self.grid[pawn.position.x][pawn.position.y] = Queen(pawn.position.GetCopy(), pawn.color)
        elif choice == 1:
            self.grid[pawn.position.x][pawn.position.y] = Bishop(pawn.position.GetCopy(), pawn.color)
        elif choice == 2:
            self.grid[pawn.position.x][pawn.position.y] = Knight(pawn.position.GetCopy(), pawn.color)
        elif choice == 3:
            self.grid[pawn.position.x][pawn.position.y] = Rook(pawn.position.GetCopy(), pawn.color)

        self.SwitchTurn()
        self.Check()
        self.pieceToPromote = None

    def MoveSimulation(self, piece, next_pos):
        if self.grid[next_pos.x][next_pos.y] == None:
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()
            self.grid[next_pos.x][next_pos.y] = piece
            return None
        else:
            prev_piece = self.grid[next_pos.x][next_pos.y]
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()
            self.grid[next_pos.x][next_pos.y] = piece
            return prev_piece

    def Check(self):
        if self.player == 0:
            king = self.WhiteKing
        else:
            king = self.BlackKing

        in_check = False  # Variável para verificar se o rei está em xeque
        for row in self.grid:
            for piece in row:
                if piece is not None and piece.color != self.player:
                    moves, captures = piece.GetMoves(self)
                    if king.position in moves or king.position in captures:
                        in_check = True

        if self.player == 0:
            self.checkWhiteKing = in_check
        else:
            self.checkBlackKing = in_check

    def IsCheckmate(self):
        if self.player == 0:
            king = self.WhiteKing
        else:
            king = self.BlackKing

        if (self.checkWhiteKing and self.player == 0) or (self.checkBlackKing and self.player == 1):
            # Verifica se existem movimentos para sair do xeque
            pieces = [p for row in self.grid for p in row if p and p.color == self.player]
            for piece in pieces:
                moves, captures = self.GetAllowedMoves(piece)
                if len(moves) > 0 or len(captures) > 0:
                    return  # Ainda há movimentos válidos, então não é xeque-mate

            # Se não há movimentos válidos, é xeque-mate
            self.winner = 1 if self.player == 0 else 0
            self.check_message = "Xeque-mate!"  # Mensagem de xeque-mate

    def CheckKingCaptured(self):
        if self.WhiteKing not in [piece for row in self.grid for piece in row if piece]:
            self.winner = 1  # Rei branco capturado, preto ganha
            self.check_message = "Rei branco capturado! Preto vence!"  # Mensagem de captura
        elif self.BlackKing not in [piece for row in self.grid for piece in row if piece]:
            self.winner = 0  # Rei preto capturado, branco ganha
            self.check_message = "Rei preto capturado! Branco vence!"  # Mensagem de captura
