# Agente Inteligente: Bot de Xadrez 

## 1. Descrição Geral

Este projeto tem como objetivo a implementação das funcionalidades essenciais do jogo de xadrez, visando explorar conceitos de agentes inteligentes e aplicar algoritmos de inteligência artificial na lógica dos jogos. Trata-se de um jogo de xadrez desenvolvido em Python, utilizando a biblioteca Pygame para a gestão da interface gráfica. O principal intuito é proporcionar uma experiência de jogo completa, permitindo que os usuários enfrentem uma inteligência artificial.
 
## 2. Estrutura do Projeto

Abaixo está uma visão geral dos principais módulos e arquivos do projeto, incluindo suas funções e interações:

### 2.1 Módulos e Classes Principais

- **main.py**: Este é o ponto de entrada do projeto. É responsável por iniciar o jogo, gerenciar o loop principal e coordenar as interações entre as peças, tabuleiro e inteligência artificial.

- **chessAI.py**: Este arquivo contém a implementação da inteligência artificial do jogo de xadrez. Utiliza algoritmos de busca, como minimax, para tomar decisões de movimento.

- **chess.py**: Define a classe `Chess`, que gerencia a lógica do jogo de xadrez e a interface gráfica utilizando Pygame. É responsável por inicializar o tabuleiro, lidar com a interação do usuário, renderizar o estado do jogo e integrar a inteligência artificial baseada no algoritmo Minimax com poda Alfa-Beta para executar movimentos estratégicos contra o jogador.

- **board.py**: Define a classe `Board`, que representa o tabuleiro de xadrez. É responsável por armazenar o estado atual das peças, gerenciar os movimentos e aplicar as regras do jogo, incluindo cheques, xeque-mate e empates.

- **pieces/**: Este diretório contém as implementações de cada peça de xadrez, seguindo o conceito de herança para evitar redundância e maximizar a reutilização de código. Cada peça tem movimentos específicos implementados nas seguintes classes:
  - **base.py**: Define a classe `BasePiece`, que serve como classe pai para todas as outras peças. Ela contém atributos e métodos comuns, como posição e validação básica de movimentos.
  - **pawn.py, rook.py, knight.py, bishop.py, queen.py, king.py**: Estas classes representam, respectivamente, as peças peão, torre, cavalo, bispo, rainha e rei. Cada classe implementa as regras específicas de movimento da sua peça e estende a classe `BasePiece`.

- **PointMap.py**: Este arquivo é responsável por gerenciar a conversão de coordenadas entre a representação gráfica e a lógica interna do tabuleiro, facilitando a interação entre a interface gráfica e a lógica do jogo.

- **setting.py**: Contém a classe `Settings`, que define as configurações do jogo, como tamanho do tabuleiro, cores e outras opções visuais e de comportamento.

- **tools.py**: Este arquivo possui funções e utilitários para manipulação das posições no tabuleiro, tais como validar movimentos e calcular posições possíveis.

- **utils.py**: Inclui funções auxiliares que são utilizadas em diversos pontos do projeto. Elas ajudam a reduzir a repetição de código e a manter a organização e clareza da lógica principal.

### 2.2 Relação entre Classes e Módulos

O projeto foi desenvolvido com uma abordagem orientada a objetos para facilitar a extensão e manutenção do código. Cada classe de peça implementa métodos para validar movimentos específicos, enquanto `Board` e `chess` gerenciam o estado do jogo e a interação entre peças. A classe de inteligência artificial (`chessAI`) acessa o `Board` para calcular e escolher movimentos.

## 3. Requisitos

Para executar o projeto, são necessários:

- Python 3.x
- Pygame (versão 2.0 ou superior)

## 4. Instalação

Siga os passos abaixo para clonar e executar o projeto:

1. Clone o repositório:
   ```bash
   git clone https://github.com/BeatrizPassoni/ChessAiAgent

2. Navegue até o diretório do projeto:
   ```bash
   cd projeto_xadrez

3. Instale a biblioteca pygame
   ```bash
   pip install pygame

## 5. Execução

1. Para iniciar o jogo, execute o seguinte comando: 

   ```bash
   python main.py

## 6. Funcionalidades

- **Movimentação Completa das Peças**: Cada peça move-se de acordo com as regras oficiais do xadrez.
- **Inteligência Artificial**: Implementação de um algoritmo de IA que permite que o jogador jogue contra o computador.
- **Validação de Movimentos**: Movimentos ilegais são detectados e impedidos por `Board` e `chess`.

## 7. Inteligência Artificial do Jogo

A inteligência artificial (IA) do jogo de xadrez é baseada no algoritmo Minimax com poda Alfa-Beta. 

### 7.1 Minimax com Poda Alfa-Beta

- **Algoritmo Minimax**: O algoritmo minimax é usado para tomar decisões no jogo simulando os movimentos do jogador e do oponente. A ideia é maximizar a melhor jogada para o jogador enquanto minimiza a melhor resposta do oponente, garantindo que o jogo avance da forma mais vantajosa possível para o agente. Cada estado do tabuleiro é avaliado de acordo com uma função de utilidade, que mede o quão favorável aquele estado é para o jogador.

- **Poda Alfa-Beta**: A poda alfa-beta é uma técnica de otimização aplicada ao algoritmo minimax para reduzir a quantidade de estados que precisam ser avaliados. Com a poda, muitos ramos da árvore de decisão são ignorados, especialmente aqueles que não podem afetar a decisão final. Isso resulta em uma IA que é mais rápida e eficiente, possibilitando uma análise mais profunda em menos tempo.

### 7.2 Agente Inteligente de Utilidade

O agente implementado neste projeto pode ser considerado um **agente inteligente de utilidade**, pois ele toma decisões que maximizam o valor de uma função de utilidade. A função de utilidade usada pela IA mede o valor de cada configuração do tabuleiro considerando diferentes aspectos, como:
- Material (quantidade e valor das peças em jogo)
- Controle de posições importantes (como o centro do tabuleiro)
- Segurança do rei

Esses fatores são combinados para calcular a melhor jogada possível em um determinado estado do tabuleiro, levando a uma estratégia mais sofisticada e ponderada.

## 8. Conclusão

Este projeto oferece uma experiência integral do jogo de xadrez, integrando uma interface gráfica intuitiva a uma inteligência artificial que utiliza algoritmos clássicos de otimização. A implementação do algoritmo Minimax com poda Alfa-Beta assegura a eficiência da IA, enquanto a aplicação do conceito de agentes de utilidade possibilita decisões estratégicas fundamentadas em diversos fatores do jogo. Com futuras melhorias, como o aprimoramento da IA e ajustes visuais, o projeto poderá proporcionar ainda mais profundidade e prazer aos jogadores.
