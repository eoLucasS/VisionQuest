import cv2  # Manipulação de imagens
from option_button import OptionButton  # Botões interativos

def display_hint_screen(img, hint_text):
    # Desenha uma tela semitransparente
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (img.shape[1], img.shape[0]), (255, 255, 255), -1)
    alpha = 0.8
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # Desenha um quadro para a dica
    frame_x = 100
    frame_y = 100
    frame_width = img.shape[1] - 200
    frame_height = img.shape[0] - 200
    cv2.rectangle(img, (frame_x, frame_y), (frame_x + frame_width, frame_y + frame_height),
                  (200, 200, 200), cv2.FILLED)
    cv2.rectangle(img, (frame_x, frame_y), (frame_x + frame_width, frame_y + frame_height),
                  (0, 0, 0), 2)

    # Ajusta o tamanho do texto da dica
    font_scale = 1.0
    max_text_width = frame_width - 40
    text_size = cv2.getTextSize(hint_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
    while text_size[0] > max_text_width:
        font_scale -= 0.1
        text_size = cv2.getTextSize(hint_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]

    # Centraliza o texto da dica
    text_x = frame_x + (frame_width - text_size[0]) // 2
    text_y = frame_y + (frame_height) // 2
    cv2.putText(img, hint_text, (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)

    # Botão para fechar a dica
    button_width = 200
    button_height = 80
    button_x = frame_x + (frame_width - button_width) // 2
    button_y = frame_y + frame_height - button_height - 20

    close_button = OptionButton((button_x, button_y), button_width, button_height, "Fechar")
    close_button.draw(img)

    return close_button