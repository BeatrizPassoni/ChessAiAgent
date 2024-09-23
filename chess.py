import pygame
import sys
import time

from setting import Config
from tools import OnBoard, Position
from board import Board
from Minimax.chessAI import Minimax
import ui

class Chess:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.board = Board()
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.CanBeReleased = False
        self.AdjustedMouse = Position(0, 0)
        self.gameOverBackground = pygame.image.load("./assets/images/gameOver.jpg")
        self.gameOverBackground = pygame.transform.smoothscale(self.gameOverBackground, Config.resolution)
        self.gameOverHeader = ui.TextUI(self.screen, "GAME OVER", Config.width//2, Config.height//6, 140, (255, 255, 255))
        self.gameOverHeader.centered = True
        self.winnerText = ui.TextUI(self.screen, "White Won the game", Config.width//2, Config.height//2, 200, (190, 255, 180))
        self.winnerText.centered = True

        self.ComputerAI = Minimax(Config.AI_DEPTH, self.board, True, True)

    def GetFrameRate(self):
        return self.clock.get_fps()

    def vsComputer(self):
        pygame.event.clear()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.screen.fill((0, 0, 0))
            self.getMousePosition()
            pygame.display.set_caption("Chess : VS Computer " + str(int(self.GetFrameRate())))
            self.display()
            self.ComputerMoves(1)
            if not self.gameOver:
                self.HandleEvents()
                self.IsGameOver()

    def display(self):
        self.Render()
        pygame.display.update()

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.board.Forfeit()
                    self.gameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.HandleOnLeftMouseButtonDown()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.HandleOnLeftMouseButtonUp()

    def ComputerMoves(self, player):
        if self.board.player == player:
            piece, bestmove = self.ComputerAI.Start(0)
            self.board.Move(piece, bestmove)
            if self.board.pieceToPromote is not None:
                self.board.PromotePawn(self.board.pieceToPromote, 0)

    def HandleOnLeftMouseButtonUp(self):
        self.draggedPiece = None
        if self.selectedPiece:
            if self.selectedOrigin != self.AdjustedMouse:
                if self.AdjustedMouse in self.selectedPieceCaptures:
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)
                elif self.AdjustedMouse in self.selectedPieceMoves:
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)
                self.ReleasePiece()
            elif self.CanBeReleased:
                self.ReleasePiece()
            else:
                self.CanBeReleased = True

    def SelectPiece(self, piece):
        if piece is not None and piece.color == self.board.player:
            self.selectedPiece = piece
            self.draggedPiece = piece
            self.selectedPieceMoves, self.selectedPieceCaptures = self.board.GetAllowedMoves(self.selectedPiece)
            self.selectedOrigin = self.AdjustedMouse

    def HandleOnLeftMouseButtonDown(self):
        if self.board.pieceToPromote is not None and self.AdjustedMouse.x == self.board.pieceToPromote.position.x:
            choice = self.AdjustedMouse.y
            if choice <= 3 and self.board.player == 0:
                self.board.PromotePawn(self.board.pieceToPromote, choice)
                self.display()
            elif choice > 3 and self.board.player == 1:
                self.board.PromotePawn(self.board.pieceToPromote, 7 - choice)
                self.display()
        else:
            if OnBoard(self.AdjustedMouse):
                piece = self.board.grid[self.AdjustedMouse.x][self.AdjustedMouse.y]
                if self.selectedPiece == piece:
                    self.draggedPiece = piece
                else:
                    self.SelectPiece(piece)

    def getMousePosition(self):
        x, y = pygame.mouse.get_pos()
        x = (x - Config.horizontal_offset) // Config.spotSize
        y = (y - Config.top_offset // 2) // Config.spotSize
        self.AdjustedMouse = Position(x, y)

    def IsGameOver(self):
        if self.board.winner is not None:
            self.gameOver = True
            self.display()
            self.gameOverWindow()

    def ReleasePiece(self):
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.selectedOrigin = None

    def Render(self):
        self.DrawChessBoard()
        self.DrawPieces()
        pygame.display.update()

    def DrawChessBoard(self):
        for i in range(Config.boardSize):
            for j in range(Config.boardSize):
                x = i * Config.spotSize + Config.horizontal_offset
                y = j * Config.spotSize + Config.top_offset // 2
                color = (180, 240, 180) if (i + j) % 2 == 0 else (80, 160, 80)  # Fixed green theme
                pygame.draw.rect(self.screen, color, [x, y, Config.spotSize, Config.spotSize])

    def DrawPieces(self):
        for x in range(Config.boardSize):
            for y in range(Config.boardSize):
                x_pos = x * Config.spotSize + Config.horizontal_offset
                y_pos = y * Config.spotSize + Config.top_offset // 2
                if self.board.grid[x][y] is not None:
                    self.screen.blit(self.board.grid[x][y].sprite, (x_pos, y_pos))

    def gameOverWindow(self):
        time.sleep(2)
        self.screen.blit(self.gameOverBackground, (0, 0))
        self.gameOverHeader.Draw()
        if self.board.winner == 0:
            self.winnerText.text = "White Won"
            self.screen.blit(self.board.WhiteKing.sprite, (Config.width//2 - Config.spotSize // 2, Config.height//3))
        elif self.board.winner == 1:
            self.winnerText.text = "Black Won"
            self.screen.blit(self.board.BlackKing.sprite, (Config.width//2 - Config.spotSize // 2, Config.height//3))
        else:
            self.winnerText.text = "DRAW"

        self.gameOverHeader.Draw()
        self.winnerText.Draw()
        pygame.display.update()
        time.sleep(3)
        self.board = Board()