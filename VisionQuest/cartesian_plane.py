import cv2

def draw_cartesian_plane_with_numbers(img, center, width, height, step_size):
    # Desenha linhas horizontais e verticais
    color = (0, 0, 0)
    thickness = 1

    # Linhas verticais
    for x in range(int(center[0] - width // 2), int(center[0] + width // 2 + 1), step_size):
        cv2.line(img, (x, int(center[1] - height // 2)), (x, int(center[1] + height // 2)), color, thickness)
        # Numeros no eixo X
        if x != center[0]:
            coord = (x - center[0]) // step_size
            cv2.putText(img, str(coord), (x - 10, center[1] + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Linhas horizontais
    for y in range(int(center[1] - height // 2), int(center[1] + height // 2 + 1), step_size):
        cv2.line(img, (int(center[0] - width // 2), y), (int(center[0] + width // 2), y), color, thickness)
        # Numeros no eixo Y
        if y != center[1]:
            coord = (center[1] - y) // step_size
            cv2.putText(img, str(coord), (center[0] - 30, y + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Desenha os eixos X e Y
    cv2.line(img, (int(center[0] - width // 2), center[1]), (int(center[0] + width // 2), center[1]), (0, 0, 255), 2)
    cv2.line(img, (center[0], int(center[1] - height // 2)), (center[0], int(center[1] + height // 2)), (0, 0, 255), 2)