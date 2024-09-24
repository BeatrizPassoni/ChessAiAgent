import pygame
import sys

from setting import Config  # Importa as configurações do jogo
from tools import OnBoard, Position  # Importa funções utilitárias para manipulação de posições
from board import Board  # Importa a classe Board que gerencia o tabuleiro de xadrez
from Minimax.chessAI import Minimax  # Importa o AI Minimax para os movimentos do computador

class Chess:
    def __init__(self, screen):
        self.screen = screen  # Define a tela para renderização do jogo
        self.clock = pygame.time.Clock()  # Cria um objeto de relógio para gerenciar a taxa de quadros
        self.gameOver = False  # Indica se o jogo acabou
        self.board = Board()  # Inicializa o tabuleiro de xadrez
        self.selectedPiece = None  # Rastreia a peça atualmente selecionada
        self.selectedPieceMoves = None  # Possíveis movimentos da peça selecionada
        self.selectedPieceCaptures = None  # Possíveis capturas da peça selecionada
        self.draggedPiece = None  # Peça que está sendo arrastada pelo mouse
        self.CanBeReleased = False  # Indica se a peça pode ser solta
        self.AdjustedMouse = Position(0, 0)  # Posição do mouse ajustada no tabuleiro
        self.ComputerAI = Minimax(Config.AI_DEPTH, self.board, True, True)  # Inicializa a IA com a profundidade especificada

    def GetFrameRate(self):
        # Retorna a taxa de quadros por segundo (FPS) atual
        return self.clock.get_fps()

    # Loop principal para jogar contra o computador
    def vsComputer(self):
        pygame.event.clear()  # Limpa eventos anteriores
        while not self.gameOver:  # Continua até o jogo acabar
            self.clock.tick(Config.fps)  # Controla a taxa de quadros
            self.screen.fill((0, 0, 0))  # Preenche a tela com preto
            self.getMousePosition()  # Obtém a posição atual do mouse
            self.display()  # Renderiza o estado atual do jogo
            # Executa o movimento do computador se for a vez da IA (1 indica a vez das peças pretas)
            self.ComputerMoves(1)
            if not self.gameOver:
                # Lida com as interações do usuário se o jogo ainda estiver em andamento
                self.HandleEvents()
                # Verifica se o jogo terminou e exibe o vencedor
                self.IsGameOver()

    def display(self):
        # Renderiza o estado do jogo e atualiza a exibição
        self.Render()  # Chama a função de renderização para desenhar tudo
        pygame.display.update()  # Atualiza a superfície de exibição para a tela

    def HandleEvents(self):
        # Lida com as entradas do usuário a partir dos eventos
        for event in pygame.event.get():
            # Verifica se a janela foi fechada
            if event.type == pygame.QUIT:
                self.gameOver = True  # Define o flag de jogo acabado como verdadeiro
                pygame.quit()  # Encerra o pygame
                sys.exit()  # Sai do programa
            # Verifica se a tecla ESC foi pressionada para desistir do jogo
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.board.Forfeit()  # Desiste do jogo
                    self.gameOver = True  # Define o flag de jogo acabado como verdadeiro
            # Verifica cliques do mouse para selecionar ou mover peças
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    self.HandleOnLeftMouseButtonDown()  # Lida com a seleção/movimento da peça
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botão esquerdo do mouse
                    self.HandleOnLeftMouseButtonUp()  # Lida com a colocação da peça

    def ComputerMoves(self, player):
        # Executa o movimento da IA
        if self.board.player == player:  # Verifica se é a vez da IA
            piece, bestmove = self.ComputerAI.Start(0)  # Obtém o melhor movimento da IA
            self.board.Move(piece, bestmove)  # Move a peça no tabuleiro
            # Verifica se um peão precisa ser promovido
            if self.board.pieceToPromote is not None:
                self.board.PromotePawn(self.board.pieceToPromote, 0)  # Promove o peão

    def HandleOnLeftMouseButtonUp(self):
        # Lida com a liberação de uma peça
        self.draggedPiece = None  # Reinicia a peça arrastada
        if self.selectedPiece:  # Verifica se uma peça está selecionada
            # Se a origem da seleção for diferente da posição do mouse ajustada
            if self.selectedOrigin != self.AdjustedMouse:
                # Se a posição ajustada está entre as capturas permitidas
                if self.AdjustedMouse in self.selectedPieceCaptures:
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)  # Move a peça para a captura
                elif self.AdjustedMouse in self.selectedPieceMoves:
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)  # Move a peça para a posição permitida
                self.ReleasePiece()  # Libera a peça selecionada
            elif self.CanBeReleased:
                self.ReleasePiece()  # Libera a peça se puder
            else:
                self.CanBeReleased = True  # Permite a liberação da peça

    def SelectPiece(self, piece):
        # Seleciona uma peça para mover
        if piece is not None and piece.color == self.board.player:  # Verifica se a peça pertence ao jogador
            self.selectedPiece = piece  # Define a peça selecionada
            self.draggedPiece = piece  # Define a peça arrastada como a peça selecionada
            self.selectedPieceMoves, self.selectedPieceCaptures = self.board.GetAllowedMoves(self.selectedPiece)  # Obtém movimentos e capturas permitidas
            self.selectedOrigin = self.AdjustedMouse  # Define a origem da seleção

    def HandleOnLeftMouseButtonDown(self):
        # Lida com a seleção de uma peça ao clicar
        if self.board.pieceToPromote is not None and self.AdjustedMouse.x == self.board.pieceToPromote.position.x:
            choice = self.AdjustedMouse.y  # Escolhe a promoção com base na posição do mouse
            # Promove o peão com base na posição do mouse
            if choice <= 3 and self.board.player == 0:
                self.board.PromotePawn(self.board.pieceToPromote, choice)
                self.display()  # Atualiza a exibição
            elif choice > 3 and self.board.player == 1:
                self.board.PromotePawn(self.board.pieceToPromote, 7 - choice)
                self.display()  # Atualiza a exibição
        else:
            if OnBoard(self.AdjustedMouse):  # Verifica se a posição está no tabuleiro
                piece = self.board.grid[self.AdjustedMouse.x][self.AdjustedMouse.y]  # Obtém a peça na posição ajustada
                if self.selectedPiece == piece:
                    self.draggedPiece = piece  # Se a peça selecionada for a mesma, inicia o arrasto
                else:
                    self.SelectPiece(piece)  # Seleciona a nova peça

    def getMousePosition(self):
        # Obtém a posição do mouse e ajusta para o tabuleiro
        x, y = pygame.mouse.get_pos()  # Obtém a posição do mouse
        x = (x - Config.horizontal_offset) // Config.spotSize  # Ajusta a coordenada x
        y = (y - Config.top_offset // 2) // Config.spotSize  # Ajusta a coordenada y
        self.AdjustedMouse = Position(x, y)  # Atualiza a posição ajustada

    def IsGameOver(self):
        # Verifica se o jogo acabou
        if self.board.winner is not None:  # Se houver um vencedor
            self.gameOver = True  # Define o flag de jogo acabado como verdadeiro
        if self.board.winner == 0:
            winner = "Branco"  # Vencedor é branco
        elif self.board.winner == 1:
            winner = "Preto"  # Vencedor é preto
            self.display()  # Atualiza a exibição
            print("\n\nVencedor = " + winner + "\n\n")  # Exibe o vencedor no console

    def ReleasePiece(self):
        # Libera a peça selecionada
        self.selectedPiece = None  # Reseta a peça selecionada
        self.selectedPieceMoves = None  # Reseta os movimentos permitidos
        self.selectedPieceCaptures = None  # Reseta as capturas permitidas
        self.draggedPiece = None  # Reseta a peça arrastada
        self.selectedOrigin = None  # Reseta a origem da seleção

    def Render(self):
        # Renderiza o tabuleiro e as peças
        self.DrawChessBoard()  # Desenha o tabuleiro
        self.DrawPieces()  # Desenha as peças
        pygame.display.update()  # Atualiza a exibição

    def DrawChessBoard(self):
        # Desenha o tabuleiro de xadrez
        for i in range(Config.boardSize):
            for j in range(Config.boardSize):
                x = i * Config.spotSize + Config.horizontal_offset  # Calcula a posição x do quadrado
                y = j * Config.spotSize + Config.top_offset // 2  # Calcula a posição y do quadrado
                # Define a cor do quadrado com base na soma das coordenadas
                color = (180, 240, 180) if (i + j) % 2 == 0 else (80, 160, 80) 
                pygame.draw.rect(self.screen, color, [x, y, Config.spotSize, Config.spotSize])  # Desenha o quadrado

    def DrawPieces(self):
        # Desenha as peças no tabuleiro
        for x in range(Config.boardSize):
            for y in range(Config.boardSize):
                x_pos = x * Config.spotSize + Config.horizontal_offset  # Posição x da peça
                y_pos = y * Config.spotSize + Config.top_offset // 2  # Posição y da peça
                if self.board.grid[x][y] is not None:  # Se houver uma peça na posição
                    self.screen.blit(self.board.grid[x][y].sprite, (x_pos, y_pos))  # Desenha a peça
