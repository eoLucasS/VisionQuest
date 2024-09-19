import cv2
from option_button import OptionButton

def display_game_over_screen(img):
    # Desenha uma tela semitransparente sobre a imagem
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (img.shape[1], img.shape[0]), (255, 255, 255), -1)
    alpha = 0.8  # Transparência
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # Desenha um quadro para a mensagem e botões
    frame_x = 200
    frame_y = 150
    frame_width = img.shape[1] - 400
    frame_height = img.shape[0] - 300
    cv2.rectangle(img, (frame_x, frame_y), (frame_x + frame_width, frame_y + frame_height), (200, 200, 200), cv2.FILLED)
    cv2.rectangle(img, (frame_x, frame_y), (frame_x + frame_width, frame_y + frame_height), (0, 0, 0), 2)

    # Mensagem de vitória sem acentos
    text = "Parabens! Voce atingiu a pontuacao maxima!"
    font_scale = 1.5  # Escala inicial da fonte
    max_text_width = frame_width - 40  # Margem dentro do quadro

    # Ajusta a escala da fonte para caber no quadro
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 3)[0]
    while text_size[0] > max_text_width:
        font_scale -= 0.1
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 3)[0]

    text_x = frame_x + (frame_width - text_size[0]) // 2
    text_y = frame_y + 100
    cv2.putText(img, text, (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 3)

    # Cria botões "Jogar Novamente" e "Sair"
    button_width = 300
    button_height = 100
    button_spacing = 50
    total_button_width = 2 * button_width + button_spacing
    button_x = frame_x + (frame_width - total_button_width) // 2
    button_y = text_y + 50

    play_again_button = OptionButton((button_x, button_y), button_width, button_height, "Jogar Novamente")
    exit_button = OptionButton((button_x + button_width + button_spacing, button_y), button_width, button_height, "Sair")

    play_again_button.draw(img)
    exit_button.draw(img)

    return play_again_button, exit_button