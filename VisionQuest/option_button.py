import cv2
import webbrowser  # Importa o módulo para abrir links no navegador

class OptionButton:
    def __init__(self, position, width, height, value, image=None, link=None):
        self.position = position
        self.width = width
        self.height = height
        self.value = value
        self.image = image
        self.link = link  # Novo atributo link

    def draw(self, img):
        x, y = self.position
        if self.image is not None:
            # Redimensiona a imagem para caber no botão
            resized_image = cv2.resize(self.image, (self.width, self.height))
            # Verifica se a imagem tem canal alfa
            if resized_image.shape[2] == 4:
                alpha_s = resized_image[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for c in range(0, 3):
                    img[y:y+self.height, x:x+self.width, c] = (alpha_s * resized_image[:, :, c] +
                                                               alpha_l * img[y:y+self.height, x:x+self.width, c])
            else:
                img[y:y+self.height, x:x+self.width] = resized_image
        else:
            # Desenha o botão
            cv2.rectangle(img, (x, y), (x+self.width, y+self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, (x, y), (x+self.width, y+self.height), (0, 0, 0), 2)
            # Desenha o texto
            text_size = cv2.getTextSize(self.value, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
            text_x = x + (self.width - text_size[0]) // 2
            text_y = y + (self.height + text_size[1]) // 2
            cv2.putText(img, self.value, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

    def checkClicking(self, x, y):
        btn_x, btn_y = self.position
        if btn_x <= x <= btn_x + self.width and btn_y <= y <= btn_y + self.height:
            if self.link:
                webbrowser.open(self.link)  # Abre o link no navegador padrão
            return True
        return False