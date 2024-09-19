class ScoreSystem:
    def __init__(self, max_score=10):
        self.score = 0  # Pontuação atual do jogador
        self.consecutive_correct = 0  # Contador de acertos consecutivos
        self.max_score = max_score  # Pontuação máxima
        self.game_over = False  # Indica se o jogador atingiu a pontuação máxima

    def correct_answer(self):
        self.score += 1  # Incrementa a pontuação em 1 para cada acerto
        self.consecutive_correct += 1  # Incrementa o contador de acertos consecutivos
        bonus_awarded = False  # Flag para verificar se o bônus foi concedido
        if self.consecutive_correct % 3 == 0:
            self.score += 1  # Concede 1 ponto extra a cada 3 acertos consecutivos
            bonus_awarded = True  # Marca que o bônus foi concedido
        if self.score >= self.max_score:
            self.score = self.max_score  # Limita a pontuação ao máximo
            self.game_over = True  # Marca que o jogo acabou
        return bonus_awarded  # Retorna se o bônus foi concedido

    def incorrect_answer(self):
        self.consecutive_correct = 0  # Reseta o contador de acertos consecutivos

    def get_score(self):
        return self.score  # Retorna a pontuação atual

    def reset(self):
        self.score = 0
        self.consecutive_correct = 0
        self.game_over = False

    def is_game_over(self):
        return self.game_over