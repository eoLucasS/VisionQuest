import cv2  # Importa a biblioteca OpenCV para manipulação de imagens

class OptionButton:
    def __init__(self, pos, width, height, value):
        self.pos = pos  # Posição (x, y) do botão na tela
        self.width = width  # Largura do botão
        self.height = height  # Altura do botão
        self.value = value  # Texto ou valor exibido no botão

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (240, 240, 240), cv2.FILLED)  # Desenha o fundo do botão
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (200, 200, 200), 3)  # Desenha a borda do botão
        font_scale = 2  # Escala inicial da fonte do texto
        text_size = cv2.getTextSize(self.value, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]  # Calcula o tamanho do texto
        while text_size[0] > self.width - 20:
            font_scale -= 0.1  # Diminui a escala da fonte se o texto for muito largo
            text_size = cv2.getTextSize(self.value, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]  # Recalcula o tamanho do texto
        text_x = self.pos[0] + (self.width - text_size[0]) // 2  # Calcula a posição x do texto para centralizar
        text_y = self.pos[1] + (self.height + text_size[1]) // 2  # Calcula a posição y do texto para centralizar
        cv2.putText(img, self.value, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (50, 50, 50), 2)  # Desenha o texto no botão

    def checkClicking(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
           self.pos[1] < y < self.pos[1] + self.height:  # Verifica se o ponto (x, y) está dentro do botão
            return True  # Retorna True se estiver dentro do botão
        else:
            return False  # Retorna False caso contrário