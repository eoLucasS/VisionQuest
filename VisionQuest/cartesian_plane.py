import cv2  # Importa a biblioteca OpenCV para manipulação de imagens

def draw_cartesian_plane_with_numbers(img, center, width, height, step_size):
    for i in range(-18, 19):
        x_pos = center[0] + i * step_size  # Calcula a posição x para cada linha vertical
        if 0 <= x_pos < img.shape[1]:
            cv2.line(img, (x_pos, center[1] - height // 2), (x_pos, center[1] + height // 2), (200, 200, 200), 1)  # Desenha a linha vertical
    for i in range(-10, 11):
        y_pos = center[1] - i * step_size  # Calcula a posição y para cada linha horizontal
        if 0 <= y_pos < img.shape[0]:
            cv2.line(img, (center[0] - width // 2, y_pos), (center[0] + width // 2, y_pos), (200, 200, 200), 1)  # Desenha a linha horizontal
    cv2.line(img, (center[0] - width // 2, center[1]), (center[0] + width // 2, center[1]), (0, 0, 0), 2)  # Desenha o eixo X
    cv2.line(img, (center[0], center[1] - height // 2), (center[0], center[1] + height // 2), (0, 0, 0), 2)  # Desenha o eixo Y
    for i in range(-18, 19):
        x_pos = center[0] + i * step_size  # Posição x para as marcações
        if 0 <= x_pos < img.shape[1]:
            cv2.line(img, (x_pos, center[1] - 5), (x_pos, center[1] + 5), (0, 0, 0), 1)  # Desenha as marcações no eixo X
            cv2.putText(img, str(i), (x_pos - 10, center[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  # Escreve os números no eixo X
    for i in range(-10, 11):
        y_pos = center[1] - i * step_size  # Posição y para as marcações
        if 0 <= y_pos < img.shape[0]:
            cv2.line(img, (center[0] - 5, y_pos), (center[0] + 5, y_pos), (0, 0, 0), 1)  # Desenha as marcações no eixo Y
            if i != 0:
                cv2.putText(img, str(i), (center[0] + 10, y_pos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  # Escreve os números no eixo Y