import os  # Interação com o sistema operacional
import cv2  # Manipulação de imagens e vídeo
import math  # Funções matemáticas
import time  # Controle de tempo
import pygame  # Reprodução de áudio
import mediapipe as mp  # Detecção de mãos
import webbrowser  # Para abrir links no navegador
from option_button import OptionButton  # Botões interativos
from question_generator import generate_question  # Gerador de questões
from cartesian_plane import draw_cartesian_plane_with_numbers  # Desenhar plano cartesiano
from score_system import ScoreSystem  # Sistema de pontuação
from game_over_screen import display_game_over_screen  # Tela de vitória
from hint_screen import display_hint_screen  # Tela de dica

mp_drawing = mp.solutions.drawing_utils  # Utilidades de desenho do MediaPipe
mp_hands = mp.solutions.hands  # Solução de detecção de mãos

pygame.mixer.init()  # Inicializa o mixer do pygame

# Diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Carrega os sons
win_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "win.mp3"))  # Som de vitória
loss_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "loss.mp3"))  # Som de derrota

def main():
    # Inicia a captura de vídeo da webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Largura do vídeo
    cap.set(4, 720)  # Altura do vídeo
    with mp_hands.Hands(
        max_num_hands=2,  # Detecta até 2 mãos
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:

        from_game_over = False  # Indica se veio da tela de vitória

        # Carrega a imagem da lâmpada para o botão de dica
        hint_image = cv2.imread(os.path.join(base_dir, "assets", "images", "lampada.png"), cv2.IMREAD_UNCHANGED)
        hint_image = cv2.resize(hint_image, (60, 60))  # Redimensiona para caber no botão

        # Carrega as imagens dos colaboradores
        collaborators = [
            {
                'name': 'Lucas Silva',
                'image': cv2.imread(os.path.join(base_dir, "assets", "images", "lucas_silva.png"), cv2.IMREAD_UNCHANGED),
                'link': 'https://www.linkedin.com/in/lucaslopesdasilva/'
            },
            {
                'name': 'Nycolas Garcia',
                'image': cv2.imread(os.path.join(base_dir, "assets", "images", "nycolas_garcia.png"), cv2.IMREAD_UNCHANGED),
                'link': 'https://www.linkedin.com/in/nycolasagrgarcia/'
            },
            {
                'name': 'Danilo Santos',
                'image': cv2.imread(os.path.join(base_dir, "assets", "images", "danilo_santos.png"), cv2.IMREAD_UNCHANGED),
                'link': 'https://www.linkedin.com/in/danilodoes/'
            },
            {
                'name': 'Breno Melo',
                'image': cv2.imread(os.path.join(base_dir, "assets", "images", "breno_melo.png"), cv2.IMREAD_UNCHANGED),
                'link': 'https://www.linkedin.com/in/breno-melo-53822a20a/'
            }
        ]

        # Redimensiona as imagens dos colaboradores
        for collaborator in collaborators:
            collaborator['image'] = cv2.resize(collaborator['image'], (100, 100))

        # Variáveis para controlar o delay nos cliques
        last_interaction_time = 0  # Para o botão "Jogar" e seleção de dificuldade
        last_collaborator_click_time = 0  # Para as imagens dos colaboradores
        collaborator_click_cooldown = 2  # Cooldown de 2 segundos

        # Loop principal do jogo
        while True:
            # Tela inicial
            game_started = False
            while not game_started:
                success, img = cap.read()
                if not success:
                    break
                img = cv2.flip(img, 1)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Desenha o título com novo estilo
                title_text = "VisionQuest"
                font_scale = 3
                text_size = cv2.getTextSize(title_text, cv2.FONT_HERSHEY_TRIPLEX, font_scale, 5)[0]
                text_x = (img.shape[1] - text_size[0]) // 2
                text_y = 150
                # Sombra do texto
                cv2.putText(img, title_text, (text_x + 2, text_y + 2),
                            cv2.FONT_HERSHEY_TRIPLEX, font_scale, (0, 0, 0), 5)
                # Texto principal
                cv2.putText(img, title_text, (text_x, text_y),
                            cv2.FONT_HERSHEY_TRIPLEX, font_scale, (255, 215, 0), 5)  # Cor dourada

                # Desenha os botões "Jogar" e "Sair" com novo estilo
                play_button = OptionButton((img.shape[1]//2 - 150, 250), 300, 100, 'Jogar')
                exit_button = OptionButton((img.shape[1]//2 - 150, 400), 300, 100, 'Sair')
                play_button.draw(img)
                exit_button.draw(img)

                # Exibe os colaboradores dentro de molduras estilizadas
                start_x = (img.shape[1] - (len(collaborators) * 150 - 20)) // 2
                y_position = 550
                for idx, collaborator in enumerate(collaborators):
                    x_position = start_x + idx * 150
                    collab_image = collaborator['image']
                    img_size = 100
                    x, y = x_position, y_position
                    # Cria uma moldura para o colaborador
                    cv2.rectangle(img, (x - 10, y - 10), (x + img_size + 10, y + img_size + 50), (0, 0, 0), -1)
                    cv2.rectangle(img, (x - 10, y - 10), (x + img_size + 10, y + img_size + 50), (255, 215, 0), 2)
                    # Sobrepõe a imagem com transparência
                    if collab_image.shape[2] == 4:
                        alpha_s = collab_image[:, :, 3] / 255.0
                        alpha_l = 1.0 - alpha_s
                        for c in range(0, 3):
                            img[y:y+img_size, x:x+img_size, c] = (alpha_s * collab_image[:, :, c] +
                                                                  alpha_l * img[y:y+img_size, x:x+img_size, c])
                    else:
                        img[y:y+img_size, x:x+img_size] = collab_image
                    # Cria um botão para o colaborador
                    collab_button = OptionButton((x, y), img_size, img_size, '', link=collaborator['link'])
                    # Armazena o botão no colaborador para uso posterior
                    collaborator['button'] = collab_button
                    # Exibe o nome do colaborador centralizado
                    name = collaborator['name']
                    text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                    text_x = x + (img_size - text_size[0]) // 2
                    cv2.putText(img, name, (text_x, y + img_size + 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                # Processa a entrada das mãos
                results = hands.process(imgRGB)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                        )
                        x = int(hand_landmarks.landmark[8].x * img.shape[1])
                        y = int(hand_landmarks.landmark[8].y * img.shape[0])
                        x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                        y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                        cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                        cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                        distance = math.hypot(x - x_thumb, y - y_thumb)
                        if distance < 40:
                            current_time = time.time()
                            # Verifica se já passou o cooldown para cliques nos colaboradores
                            if current_time - last_collaborator_click_time >= collaborator_click_cooldown:
                                for collaborator in collaborators:
                                    if collaborator['button'].checkClicking(x, y):
                                        last_collaborator_click_time = current_time
                                        # O link será aberto dentro do método checkClicking
                                        break
                            # Verifica se já passou o cooldown para outros cliques
                            if current_time - last_interaction_time >= 0.5:  # Pequeno delay para evitar cliques múltiplos
                                if play_button.checkClicking(x, y):
                                    game_started = True
                                    last_interaction_time = current_time
                                    # Registra o tempo em que "Jogar" foi clicado
                                    last_interaction_time = time.time()
                                    break
                                elif exit_button.checkClicking(x, y):
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return

                cv2.imshow("VisionQuest - github.com/eoLucasS", img)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            # Seleção de dificuldade
            difficulty_selected = False  # Dificuldade selecionada
            difficulty = ''
            button_spacing = 50  # Espaçamento entre botões
            button_width = 200  # Largura do botão
            total_button_width = 3 * button_width + 2 * button_spacing
            start_x = (1280 - total_button_width) // 2  # Posição inicial dos botões

            # Botões de dificuldade
            buttons_difficulty = [
                OptionButton((start_x, 300), button_width, 100, 'Facil'),
                OptionButton((start_x + button_width + button_spacing, 300), button_width, 100, 'Medio'),
                OptionButton((start_x + 2 * (button_width + button_spacing), 300), button_width, 100, 'Dificil')
            ]

            # Delay após tela de vitória
            if from_game_over:
                difficulty_screen_start_time = time.time()
                buttons_active = False
            else:
                buttons_active = True

            while not difficulty_selected:
                success, img = cap.read()  # Lê um frame da webcam
                if not success:
                    break
                img = cv2.flip(img, 1)  # Espelha a imagem
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte para RGB
                results = hands.process(imgRGB)  # Processa a imagem para detectar mãos

                text = "Selecione a Dificuldade"  # Texto da tela
                font_scale = 2  # Escala da fonte
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 3)[0]
                text_x = (img.shape[1] - text_size[0]) // 2  # Centraliza o texto
                text_y = 200
                # Desenha o fundo do texto
                cv2.rectangle(img, (text_x - 20, text_y - 60), (text_x + text_size[0] + 20, text_y + 10),
                              (255, 255, 255), cv2.FILLED)
                # Desenha o texto
                cv2.putText(img, text, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 3)

                for button in buttons_difficulty:
                    button.draw(img)  # Desenha os botões

                if from_game_over and not buttons_active:
                    if time.time() - difficulty_screen_start_time > 5:
                        buttons_active = True

                current_time = time.time()
                # Verifica se já passou o delay de 2 segundos após clicar em "Jogar"
                if current_time - last_interaction_time >= 2:
                    buttons_active = True
                else:
                    buttons_active = False

                if results.multi_hand_landmarks and buttons_active:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                        )
                        x = int(hand_landmarks.landmark[8].x * img.shape[1])
                        y = int(hand_landmarks.landmark[8].y * img.shape[0])
                        x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                        y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                        cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                        cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                        distance = math.hypot(x - x_thumb, y - y_thumb)
                        if distance < 40:
                            for button in buttons_difficulty:
                                if button.checkClicking(x, y):
                                    difficulty = button.value
                                    difficulty_selected = True
                                    from_game_over = False
                                    last_interaction_time = current_time
                                    break

                cv2.imshow("VisionQuest - github.com/eoLucasS", img)  # Exibe a imagem

                key = cv2.waitKey(1)
                if key == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            # Inicia o sistema de pontuação e gera a primeira questão
            score_system = ScoreSystem()
            question_data = generate_question(difficulty)
            feedback = ""
            feedback_start_time = 0
            bonus_feedback = ""
            bonus_start_time = 0
            new_question_needed = False
            center = (640, 360)
            plane_width, plane_height = 35 * 36, 35 * 20
            step_size = 35
            game_over = False
            game_over_start_time = 0
            hint_active = False  # Tela de dica ativa
            hint_button = OptionButton((50, 610), 100, 100, '', image=hint_image)  # Botão de dica

            # Barra de progresso
            progress_bar_max_width = 300  # Largura máxima da barra
            progress_bar_height = 30
            progress_bar_position = (img.shape[1] - progress_bar_max_width - 50, 50)

            while True:
                success, img = cap.read()
                if not success:
                    break
                img = cv2.flip(img, 1)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hands.process(imgRGB)

                if not game_over:
                    if not hint_active:
                        if question_data['type'] == 'multiple_choice':
                            cv2.rectangle(img, (50, 100), (img.shape[1]-50, 250),
                                          (255, 255, 255), cv2.FILLED)
                            cv2.rectangle(img, (50, 100), (img.shape[1]-50, 250),
                                          (0, 0, 0), 2)
                            font_scale = 2
                            question = question_data['question']
                            text_size = cv2.getTextSize(question, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                            while text_size[0] > img.shape[1] - 100:
                                font_scale -= 0.1
                                text_size = cv2.getTextSize(question, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                            text_x = (img.shape[1] - text_size[0]) // 2
                            text_y = 200
                            cv2.putText(img, question, (text_x, text_y),
                                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)
                            options = question_data['options']
                            option_buttons = []
                            for i in range(3):
                                xPos = 200 + i * 300
                                yPos = 400
                                option_buttons.append(OptionButton((xPos, yPos), 200, 100, options[i]))
                            for button in option_buttons:
                                button.draw(img)
                        elif question_data['type'] == 'cartesian_plane':
                            draw_cartesian_plane_with_numbers(img, center, plane_width, plane_height, step_size)
                            question = question_data['question']
                            cv2.putText(img, question, (50, 100),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
                            x_target, y_target = question_data['target_point']
                            screen_x = center[0] + x_target * step_size
                            screen_y = center[1] - y_target * step_size

                            # Remove o ponto vermelho para o jogador não ver
                            # cv2.circle(img, (int(screen_x), int(screen_y)), 10, (0, 0, 255), cv2.FILLED)

                        # Desenha o botão de dica com moldura
                        hint_button.draw(img)
                        cv2.rectangle(img, (50, 610), (150, 710), (0, 0, 0), 2)

                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:
                                mp_drawing.draw_landmarks(
                                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                                )
                                x = int(hand_landmarks.landmark[8].x * img.shape[1])
                                y = int(hand_landmarks.landmark[8].y * img.shape[0])
                                x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                                y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                                cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                                cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                                distance = math.hypot(x - x_thumb, y - y_thumb)
                                if feedback == "":
                                    if hint_button.checkClicking(x, y) and distance < 40:
                                        hint_active = True
                                        break
                                    if question_data['type'] == 'multiple_choice':
                                        if distance < 40:
                                            for button in option_buttons:
                                                if button.checkClicking(x, y):
                                                    if button.value == question_data['correct_answer']:
                                                        feedback = "Voce acertou!"
                                                        feedback_start_time = time.time()
                                                        pygame.mixer.Sound.play(win_sound)
                                                        bonus_awarded = score_system.correct_answer()
                                                        if bonus_awarded:
                                                            bonus_feedback = "Bônus +1!"
                                                            bonus_start_time = time.time()
                                                        new_question_needed = True
                                                    else:
                                                        feedback = "Voce errou!"
                                                        feedback_start_time = time.time()
                                                        pygame.mixer.Sound.play(loss_sound)
                                                        score_system.incorrect_answer()
                                                    break
                                    elif question_data['type'] == 'cartesian_plane':
                                        # Verifica se o dedo indicador está próximo do ponto alvo
                                        distance_to_point = math.hypot(x - screen_x, y - screen_y)
                                        if distance_to_point < 20:
                                            feedback = "Voce acertou!"
                                            feedback_start_time = time.time()
                                            pygame.mixer.Sound.play(win_sound)
                                            bonus_awarded = score_system.correct_answer()
                                            if bonus_awarded:
                                                bonus_feedback = "Bônus +1!"
                                                bonus_start_time = time.time()
                                            new_question_needed = True
                                if feedback != "":
                                    if time.time() - feedback_start_time > 2:
                                        feedback = ""
                                        if new_question_needed:
                                            question_data = generate_question(difficulty)
                                            new_question_needed = False
                                    else:
                                        if feedback == "Voce acertou!":
                                            cv2.putText(img, feedback, (x - 100, y - 50),
                                                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                                        elif feedback == "Voce errou!":
                                            cv2.putText(img, feedback, (x - 100, y - 50),
                                                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                                if bonus_feedback != "":
                                    if time.time() - bonus_start_time > 2:
                                        bonus_feedback = ""
                                    else:
                                        cv2.putText(img, bonus_feedback, (x - 100, y - 80),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 215, 255), 3)
                    else:
                        # Exibe a tela de dica
                        close_button = display_hint_screen(img, question_data['hint'])
                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:
                                mp_drawing.draw_landmarks(
                                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                                )
                                x = int(hand_landmarks.landmark[8].x * img.shape[1])
                                y = int(hand_landmarks.landmark[8].y * img.shape[0])
                                x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                                y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                                cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                                cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                                distance = math.hypot(x - x_thumb, y - y_thumb)
                                if distance < 40:
                                    if close_button.checkClicking(x, y):
                                        hint_active = False
                                        break

                    # Exibe a barra de progresso no canto superior direito
                    progress = score_system.get_score() / score_system.max_score
                    current_bar_width = int(progress_bar_max_width * progress)
                    cv2.rectangle(img, progress_bar_position,
                                  (progress_bar_position[0] + progress_bar_max_width, progress_bar_position[1] + progress_bar_height),
                                  (200, 200, 200), -1)
                    cv2.rectangle(img, progress_bar_position,
                                  (progress_bar_position[0] + current_bar_width, progress_bar_position[1] + progress_bar_height),
                                  (0, 255, 0), -1)
                    cv2.rectangle(img,
                                  (progress_bar_position[0], progress_bar_position[1]),
                                  (progress_bar_position[0] + progress_bar_max_width, progress_bar_position[1] + progress_bar_height),
                                  (0, 0, 0), 2)
                    # Adiciona o texto "BARRA DE PROGRESSÃO"
                    cv2.putText(img, "BARRA DE PROGRESSAO", (progress_bar_position[0] + 10, progress_bar_position[1] + 22),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 2)

                    if score_system.is_game_over():
                        game_over = True
                        game_over_start_time = time.time()
                else:
                    play_again_button, exit_button = display_game_over_screen(img)
                    if time.time() - game_over_start_time > 5:
                        buttons_active = True
                    else:
                        buttons_active = False

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                            )
                            x = int(hand_landmarks.landmark[8].x * img.shape[1])
                            y = int(hand_landmarks.landmark[8].y * img.shape[0])
                            x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                            y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                            cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                            cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                            distance = math.hypot(x - x_thumb, y - y_thumb)
                            if distance < 40 and buttons_active:
                                if play_again_button.checkClicking(x, y):
                                    difficulty_selected = False
                                    from_game_over = True
                                    break
                                elif exit_button.checkClicking(x, y):
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return
                    if not difficulty_selected:
                        break

                cv2.imshow("VisionQuest - github.com/eoLucasS", img)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            if not difficulty_selected:
                continue

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()