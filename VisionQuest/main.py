import os  # Importa o módulo os para interagir com o sistema operacional
import cv2  # Importa OpenCV para manipulação de imagens e vídeo
import math  # Importa math para funções matemáticas
import time  # Importa time para manipulação de tempo
import pygame  # Importa pygame para reprodução de áudio
import mediapipe as mp  # Importa MediaPipe para detecção de mãos
from option_button import OptionButton  # Importa a classe OptionButton
from question_generator import generate_question  # Importa a função para gerar questões
from cartesian_plane import draw_cartesian_plane_with_numbers  # Importa função para desenhar o plano cartesiano
from score_system import ScoreSystem  # Importa a classe ScoreSystem
from game_over_screen import display_game_over_screen  # Importa função para exibir a tela de vitória

mp_drawing = mp.solutions.drawing_utils  # Utilidades de desenho do MediaPipe
mp_hands = mp.solutions.hands  # Solução para detecção de mãos

pygame.mixer.init()  # Inicializa o mixer do pygame para tocar sons

base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório base do arquivo atual
win_sound = pygame.mixer.Sound(os.path.join(base_dir, "..", "assets", "sounds", "win.mp3"))  # Carrega o som de vitória
loss_sound = pygame.mixer.Sound(os.path.join(base_dir, "..", "assets", "sounds", "loss.mp3"))  # Carrega o som de derrota

def main():
    cap = cv2.VideoCapture(0)  # Inicia a captura de vídeo da webcam
    cap.set(3, 1280)  # Define a largura do vídeo para 1280 pixels
    cap.set(4, 720)  # Define a altura do vídeo para 720 pixels
    with mp_hands.Hands(
        max_num_hands=2,  # Detecta até 2 mãos
        min_detection_confidence=0.7,  # Confiança mínima para detecção
        min_tracking_confidence=0.7) as hands:  # Confiança mínima para rastreamento

        from_game_over = False  # Indica se o usuário veio da tela de vitória

        while True:
            difficulty_selected = False  # Indica se a dificuldade foi selecionada
            difficulty = ''  # Variável para armazenar a dificuldade escolhida
            button_spacing = 50  # Espaçamento entre os botões
            button_width = 200  # Largura dos botões
            total_button_width = 3 * button_width + 2 * button_spacing  # Largura total dos botões com espaçamento
            start_x = (1280 - total_button_width) // 2  # Calcula a posição inicial dos botões para centralizar

            # Cria os botões de dificuldade
            buttons_difficulty = [
                OptionButton((start_x, 300), button_width, 100, 'Facil'),  # Botão para dificuldade Fácil
                OptionButton((start_x + button_width + button_spacing, 300), button_width, 100, 'Medio'),  # Médio
                OptionButton((start_x + 2 * (button_width + button_spacing), 300), button_width, 100, 'Dificil')  # Difícil
            ]

            # Se veio da tela de vitória, inicia o delay
            if from_game_over:
                difficulty_screen_start_time = time.time()  # Marca o tempo inicial
                buttons_active = False  # Desativa os botões inicialmente
            else:
                buttons_active = True  # Botões ativos imediatamente se não veio da tela de vitória

            while not difficulty_selected:
                success, img = cap.read()  # Lê um frame da webcam
                if not success:
                    break  # Encerra o loop se não conseguir ler
                img = cv2.flip(img, 1)  # Espelha a imagem horizontalmente
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte a imagem para RGB
                results = hands.process(imgRGB)  # Processa a imagem para detectar mãos

                text = "Selecione a Dificuldade"  # Texto a ser exibido
                font_scale = 2  # Escala da fonte
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 3)[0]  # Tamanho do texto
                text_x = (img.shape[1] - text_size[0]) // 2  # Centraliza o texto horizontalmente
                text_y = 200  # Posição vertical do texto
                # Desenha um retângulo branco atrás do texto
                cv2.rectangle(img, (text_x - 20, text_y - 60), (text_x + text_size[0] + 20, text_y + 10),
                              (255, 255, 255), cv2.FILLED)
                # Escreve o texto na imagem
                cv2.putText(img, text, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 3)

                for button in buttons_difficulty:
                    button.draw(img)  # Desenha os botões de dificuldade

                # Verifica se deve ativar os botões após o delay
                if from_game_over and not buttons_active:
                    if time.time() - difficulty_screen_start_time > 5:  # Se passaram 5 segundos
                        buttons_active = True  # Ativa os botões

                if results.multi_hand_landmarks and buttons_active:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Desenha os marcos e conexões das mãos
                        mp_drawing.draw_landmarks(
                            img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                        )
                        # Coordenadas do dedo indicador
                        x = int(hand_landmarks.landmark[8].x * img.shape[1])
                        y = int(hand_landmarks.landmark[8].y * img.shape[0])
                        # Coordenadas do polegar
                        x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                        y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                        # Desenha círculos nos dedos
                        cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                        cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                        # Calcula a distância entre indicador e polegar
                        distance = math.hypot(x - x_thumb, y - y_thumb)
                        if distance < 40:  # Se a distância é pequena (pinça)
                            for button in buttons_difficulty:
                                if button.checkClicking(x, y):  # Verifica se está clicando em um botão
                                    difficulty = button.value  # Define a dificuldade escolhida
                                    difficulty_selected = True  # Marca que a dificuldade foi selecionada
                                    from_game_over = False  # Reseta o indicador
                                    break  # Sai do loop dos botões

                cv2.imshow("VisionQuest - github.com/eoLucasS", img)  # Mostra a imagem na janela

                key = cv2.waitKey(1)  # Espera 1ms por uma tecla
                if key == ord('q'):
                    cap.release()  # Libera a webcam
                    cv2.destroyAllWindows()  # Fecha todas as janelas
                    return  # Encerra o programa

            score_system = ScoreSystem()  # Inicializa o sistema de pontuação
            question_data = generate_question(difficulty)  # Gera a primeira questão
            feedback = ""  # Feedback ao jogador
            feedback_start_time = 0  # Tempo do feedback
            bonus_feedback = ""  # Feedback do bônus
            bonus_start_time = 0  # Tempo do feedback do bônus
            new_question_needed = False  # Indica se precisa de nova questão
            center = (640, 360)  # Centro do plano cartesiano
            plane_width, plane_height = 35 * 36, 35 * 20  # Dimensões do plano
            step_size = 35  # Tamanho dos passos no plano
            game_over = False  # Indica se o jogo acabou
            game_over_start_time = 0  # Tempo em que a tela de vitória apareceu

            while True:
                success, img = cap.read()  # Lê um frame da webcam
                if not success:
                    break  # Encerra o loop se não conseguir ler
                img = cv2.flip(img, 1)  # Espelha a imagem
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte para RGB
                results = hands.process(imgRGB)  # Processa a imagem para detectar mãos

                if not game_over:
                    if question_data['type'] == 'multiple_choice':
                        # Desenha o fundo para a pergunta
                        cv2.rectangle(img, (50, 50), (img.shape[1]-50, 200),
                                      (255, 255, 255), cv2.FILLED)
                        # Desenha a borda da pergunta
                        cv2.rectangle(img, (50, 50), (img.shape[1]-50, 200),
                                      (0, 0, 0), 2)
                        font_scale = 2  # Escala da fonte
                        question = question_data['question']  # Pergunta atual
                        # Calcula o tamanho do texto
                        text_size = cv2.getTextSize(question, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                        # Ajusta a escala da fonte se necessário
                        while text_size[0] > img.shape[1] - 100:
                            font_scale -= 0.1
                            text_size = cv2.getTextSize(question, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                        text_x = (img.shape[1] - text_size[0]) // 2  # Centraliza o texto
                        text_y = 150  # Posição vertical do texto
                        # Desenha a pergunta na imagem
                        cv2.putText(img, question, (text_x, text_y),
                                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)
                        options = question_data['options']  # Opções de resposta
                        option_buttons = []
                        for i in range(3):
                            xPos = 200 + i * 300  # Posição horizontal do botão
                            yPos = 400  # Posição vertical do botão
                            # Cria os botões de opção
                            option_buttons.append(OptionButton((xPos, yPos), 200, 100, options[i]))
                        for button in option_buttons:
                            button.draw(img)  # Desenha os botões
                    elif question_data['type'] == 'cartesian_plane':
                        # Desenha o plano cartesiano
                        draw_cartesian_plane_with_numbers(img, center, plane_width, plane_height, step_size)
                        question = question_data['question']  # Pergunta atual
                        # Desenha a pergunta na imagem
                        cv2.putText(img, question, (50, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
                        x_target, y_target = question_data['target_point']  # Ponto alvo
                        # Converte as coordenadas para a tela
                        screen_x = center[0] + x_target * step_size
                        screen_y = center[1] - y_target * step_size

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Desenha os marcos e conexões das mãos
                            mp_drawing.draw_landmarks(
                                img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                            )
                            # Coordenadas do dedo indicador
                            x = int(hand_landmarks.landmark[8].x * img.shape[1])
                            y = int(hand_landmarks.landmark[8].y * img.shape[0])
                            # Coordenadas do polegar
                            x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                            y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                            # Desenha círculos nos dedos
                            cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                            cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                            # Calcula a distância entre indicador e polegar
                            distance = math.hypot(x - x_thumb, y - y_thumb)
                            if question_data['type'] == 'multiple_choice':
                                if distance < 40 and feedback == "":
                                    for button in option_buttons:
                                        if button.checkClicking(x, y):
                                            if button.value == question_data['correct_answer']:
                                                feedback = "Voce acertou!"  # Mensagem de acerto
                                                feedback_start_time = time.time()  # Marca o tempo do feedback
                                                pygame.mixer.Sound.play(win_sound)  # Toca o som de vitória
                                                # Atualiza a pontuação e verifica se há bônus
                                                bonus_awarded = score_system.correct_answer()
                                                if bonus_awarded:
                                                    bonus_feedback = "Bonus +1!"  # Mensagem de bônus
                                                    bonus_start_time = time.time()
                                                new_question_needed = True  # Precisa de nova questão
                                            else:
                                                feedback = "Voce errou!"  # Mensagem de erro
                                                feedback_start_time = time.time()
                                                pygame.mixer.Sound.play(loss_sound)  # Toca o som de derrota
                                                score_system.incorrect_answer()  # Reseta acertos consecutivos
                                            break
                            elif question_data['type'] == 'cartesian_plane':
                                # Calcula a distância até o ponto alvo
                                distance_to_point = math.hypot(x - screen_x, y - screen_y)
                                if distance_to_point < 20 and feedback == "":
                                    feedback = "Voce acertou!"  # Mensagem de acerto
                                    feedback_start_time = time.time()
                                    pygame.mixer.Sound.play(win_sound)  # Toca o som de vitória
                                    bonus_awarded = score_system.correct_answer()
                                    if bonus_awarded:
                                        bonus_feedback = "Bonus +1!"
                                        bonus_start_time = time.time()
                                    new_question_needed = True
                            if feedback != "":
                                if time.time() - feedback_start_time > 2:
                                    feedback = ""  # Limpa o feedback após 2 segundos
                                    if new_question_needed:
                                        question_data = generate_question(difficulty)  # Gera nova questão
                                        new_question_needed = False
                                else:
                                    if feedback == "Voce acertou!":
                                        # Exibe mensagem de acerto
                                        cv2.putText(img, feedback, (x - 100, y - 50),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                                    elif feedback == "Voce errou!":
                                        # Exibe mensagem de erro
                                        cv2.putText(img, feedback, (x - 100, y - 50),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                            if bonus_feedback != "":
                                if time.time() - bonus_start_time > 2:
                                    bonus_feedback = ""  # Limpa o feedback do bônus
                                else:
                                    # Exibe mensagem de bônus
                                    cv2.putText(img, bonus_feedback, (x - 100, y - 80),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 215, 255), 3)
                    else:
                        feedback = ""  # Limpa o feedback se não detectar mãos

                    # Exibe a pontuação atual
                    score_text = f"Pontuacao: {score_system.get_score()}"
                    cv2.putText(img, score_text, (img.shape[1] - 250, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

                    if score_system.is_game_over():
                        game_over = True  # Marca que o jogo acabou
                        game_over_start_time = time.time()  # Marca o tempo da tela de vitória
                else:
                    # Exibe a tela de vitória
                    play_again_button, exit_button = display_game_over_screen(img)
                    if time.time() - game_over_start_time > 5:
                        buttons_active = True  # Ativa os botões após 5 segundos
                    else:
                        buttons_active = False  # Botões desativados inicialmente

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Desenha os marcos e conexões das mãos
                            mp_drawing.draw_landmarks(
                                img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)
                            )
                            # Coordenadas do dedo indicador
                            x = int(hand_landmarks.landmark[8].x * img.shape[1])
                            y = int(hand_landmarks.landmark[8].y * img.shape[0])
                            # Coordenadas do polegar
                            x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])
                            y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])
                            # Desenha círculos nos dedos
                            cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)
                            cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)
                            # Calcula a distância entre indicador e polegar
                            distance = math.hypot(x - x_thumb, y - y_thumb)
                            if distance < 40 and buttons_active:
                                if play_again_button.checkClicking(x, y):
                                    difficulty_selected = False  # Volta para seleção de dificuldade
                                    from_game_over = True  # Indica que veio da tela de vitória
                                    break
                                elif exit_button.checkClicking(x, y):
                                    cap.release()  # Libera a webcam
                                    cv2.destroyAllWindows()  # Fecha todas as janelas
                                    return  # Encerra o programa
                    if not difficulty_selected:
                        break  # Sai do loop para voltar à seleção de dificuldade

                cv2.imshow("VisionQuest - github.com/eoLucasS", img)  # Exibe a imagem na janela
                key = cv2.waitKey(1)
                if key == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            if not difficulty_selected:
                continue  # Volta para o início do loop para selecionar a dificuldade

    cap.release()  # Libera a webcam
    cv2.destroyAllWindows()  # Fecha todas as janelas

if __name__ == "__main__":
    main()  # Chama a função principal