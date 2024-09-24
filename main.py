import pygame  # Importa a biblioteca Pygame para desenvolvimento de jogos
import sys  # Importa o módulo sys para manipulação do sistema
from setting import Config  # Importa configurações do jogo
from chess import Chess  # Importa a classe Chess, que gerencia a lógica do jogo

# Função principal que inicializa o jogo
def main():
    pygame.init()  # Inicializa todos os módulos do Pygame
    pygame.font.init()  # Inicializa o módulo de fontes do Pygame
    screen = pygame.display.set_mode(Config.resolution)  # Cria a janela do jogo com a resolução especificada

    # Cria uma instância da classe Chess e inicia o jogo contra o computador
    chess_game = Chess(screen)  # Instancia o jogo de xadrez com a tela definida
    chess_game.vsComputer()  # Chama a função para jogar contra a IA

    pygame.quit()  # Encerra o Pygame
    sys.exit()  # Sai do programa

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()  # Chama a função principal
