class Position:
    def __init__(self, x, y):
        # Inicializa a posição com coordenadas x e y
        self.x = x
        self.y = y

    def __eq__(self, other):
        # Método para verificar a igualdade entre duas posições
        if other == None:
            return False  # Se o outro objeto for None, não é igual
        elif self.x == other.x and self.y == other.y:
            return True  # Retorna True se as coordenadas forem iguais
        else:
            return False  # Retorna False caso contrário

    def Compare(self, other):
        # Compara a posição atual com outra posição
        if self.x == other.x and self.y == other.y:
            return True  # Retorna True se as coordenadas forem iguais
        else:
            return False  # Retorna False caso contrário

    def GetCopy(self):
        # Retorna uma cópia da posição atual
        return Position(self.x, self.y)

    def getTuple(self):
        # Retorna as coordenadas como uma tupla
        return (self.x, self.y)

    def __repr__(self):
        # Representação em string da posição
        return f"({self.x}, {self.y})"

def OnBoard(position):
    # Verifica se a posição está dentro dos limites do tabuleiro
    return (position.x >= 0 and position.x < 8) and (position.y >= 0 and position.y < 8)
