from Minimax.PointMap import map_points, PieceMap  # Importa mapas de pontos para avaliação de peças
from pieces import Pawn  # Importa a classe Pawn (peão)

class Minimax(object):
    def __init__(self, depth, board, AlphBetaPruning=True, UsePointMaps=True):
        # Inicializa os parâmetros do algoritmo Minimax
        self.depth = depth  # Profundidade máxima para busca
        self.board = board  # Instância do tabuleiro de xadrez
        self.AlphaBetaPruning = AlphBetaPruning  # Habilita/Desabilita a poda Alpha-Beta
        self.UsePointMaps = UsePointMaps  # Habilita/Desabilita uso de mapas de pontos

    def Start(self, depth):
        # Inicia a busca pelo melhor movimento
        bestMove = None  # Armazena o melhor movimento encontrado
        bestScore = -9999  # Inicializa a melhor pontuação
        currentPiece = None  # Peça atual em movimento
        isMaximizer = self.board.player == 1  # Define se o jogador é o maximizador

        if not isMaximizer:
            bestScore *= -1  # Inverte a pontuação para o jogador minimizador

        # Percorre todas as peças do jogador atual
        for pieces in self.board.grid:
            for piece in pieces:
                if piece is not None and piece.color == self.board.player:
                    moves, captures = self.board.GetAllowedMoves(piece, True)  # Obtém movimentos permitidos
                    possibleMoves = captures + moves  # Combina movimentos e capturas
                    for position in possibleMoves:
                        prev_pos = piece.position  # Armazena a posição anterior
                        pion = self.board.MoveSimulation(piece, position)  # Simula o movimento

                        # Chama a função minimax recursivamente para calcular a pontuação
                        score = self.minimax(depth + 1, not isMaximizer, -10000, 10000)
                        # Avalia condições especiais para peões
                        if isinstance(piece, Pawn) and (position.y == 7 or position.y == 0):
                            score += 80
                        elif self.board.isEnPassant(piece, position):
                            score += 10
                        
                        if not isMaximizer:
                            score *= -1  # Inverte a pontuação para o jogador minimizador
                        
                        # Atualiza a melhor pontuação e movimento se necessário
                        if score >= bestScore and isMaximizer:
                            bestScore = score
                            bestMove = position
                            currentPiece = piece

                        # Desfaz o movimento simulado
                        if pion is None:
                            self.board.MoveSimulation(piece, prev_pos)
                        else:
                            self.board.MoveSimulation(piece, prev_pos)
                            self.board.MoveSimulation(pion, position)
        return currentPiece, bestMove  # Retorna a peça atual e o melhor movimento

    def minimax(self, depth, isMaximizer, alpha, beta):
        # Função recursiva do algoritmo Minimax
        if self.depth == depth:
            return self.Evaluate() * -1  # Avalia a posição atual

        if isMaximizer:
            bestScore = -9999  # Inicializa a melhor pontuação
            possibleMoves = self.LegalMoves(1, 7)  # Obtém movimentos legais para o maximizer
            for _index in range(len(possibleMoves) - 1, -1, -1):
                piece = possibleMoves[_index][1]  # Seleciona a peça
                i = possibleMoves[_index][2]  # Posição do movimento
                prev_pos = piece.position  # Armazena a posição anterior
                pion = self.board.MoveSimulation(piece, i)  # Simula o movimento
                score = self.minimax(depth + 1, False, alpha, beta)  # Chama minimax recursivamente
                bestScore = max(bestScore, score)  # Atualiza a melhor pontuação
                if self.AlphaBetaPruning:
                    alpha = max(alpha, bestScore)  # Atualiza alpha para poda
                self.UndoMove(pion, piece, prev_pos, i)  # Desfaz o movimento

                # Verifica se a poda Alpha-Beta pode ser aplicada
                if beta <= alpha and self.AlphaBetaPruning:
                    return bestScore
            return bestScore  # Retorna a melhor pontuação encontrada
        else:
            bestScore = 9999  # Inicializa a melhor pontuação para o minimizer
            possibleMoves = self.LegalMoves(0, 0)  # Obtém movimentos legais para o minimizer
            for _index in range(len(possibleMoves) - 1, -1, -1):
                piece = possibleMoves[_index][1]  # Seleciona a peça
                i = possibleMoves[_index][2]  # Posição do movimento
                prev_pos = piece.position  # Armazena a posição anterior
                currentPiece = self.board.MoveSimulation(piece, i)  # Simula o movimento
                score = self.minimax(depth + 1, True, alpha, beta)  # Chama minimax recursivamente
                bestScore = min(bestScore, score)  # Atualiza a melhor pontuação
                if self.AlphaBetaPruning:
                    beta = min(beta, bestScore)  # Atualiza beta para poda
                self.UndoMove(currentPiece, piece, prev_pos, i)  # Desfaz o movimento
                if beta <= alpha and self.AlphaBetaPruning:
                    return bestScore
            return bestScore  # Retorna a melhor pontuação encontrada

    def Evaluate(self):
        # Avalia o estado atual do tabuleiro
        totalScore = 0  # Inicializa a pontuação total
        for pieces in self.board.grid:
            for piece in pieces:
                if piece is not None:
                    p_map = PieceMap(piece)  # Obtém o mapa de pontos para a peça
                    score = piece.value  # Obtém o valor da peça
                    if self.UsePointMaps:
                        score += p_map[piece.position.y][piece.position.x]  # Adiciona pontos do mapa
                    totalScore += score  # Soma à pontuação total
        return totalScore  # Retorna a pontuação total

    def UndoMove(self, currentPiece, piece, prev_pos, p):
        # Desfaz um movimento
        if currentPiece is None:
            self.board.MoveSimulation(piece, prev_pos)  # Desfaz movimento de peça
        elif currentPiece is not None:
            self.board.MoveSimulation(piece, prev_pos)  # Desfaz movimento da peça atual
            self.board.MoveSimulation(currentPiece, p)  # Desfaz movimento da peça anterior

    def GetMoves(self, piece, position):
        # Obtém os movimentos legais para uma peça
        bestMoves = []  # Armazena os melhores movimentos
        possibleMoves = []  # Armazena todos os movimentos
        moves, captures = self.board.GetAllowedMoves(piece, True)  # Obtém movimentos e capturas
        for pos in captures:
            if self.board.grid[pos.x][pos.y] is not None:
                bestMoves.append([10 * self.board.grid[pos.x][pos.y].value - piece.value, piece, pos])
                if isinstance(piece, Pawn) and (pos.y == position):
                    bestMoves[-1][0] += 90  # Adiciona pontos extras se for um peão
            else:
                bestMoves.append([piece.value, piece, pos])  # Adiciona captura sem valor
        for pos in moves:
            if isinstance(piece, Pawn) and (pos.y == position):
                bestMoves.append([90, piece, pos])  # Adiciona valor alto para movimento de peão
            else:
                bestMoves.append([0, piece, pos])  # Adiciona movimento sem valor
        return possibleMoves, bestMoves  # Retorna todos os movimentos e os melhores

    def LegalMoves(self, color, pos):
        # Obtém todos os movimentos legais para um jogador
        possibleMoves = []  # Armazena movimentos possíveis
        bestMoves = []  # Armazena os melhores movimentos
        for pieces in self.board.grid:
            for piece in pieces:
                if piece is not None and piece.color == color:
                    temp_moves, better_temp_moves = self.GetMoves(piece, pos)  # Obtém movimentos para a peça
                    possibleMoves += temp_moves  # Adiciona movimentos possíveis
                    bestMoves += better_temp_moves  # Adiciona melhores movimentos
        bestMoves.sort(key=lambda key: key[0])  # Ordena os melhores movimentos
        possibleMoves += bestMoves  # Combina todos os movimentos
        return possibleMoves  # Retorna todos os movimentos possíveis
