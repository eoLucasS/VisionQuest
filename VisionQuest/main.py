import cv2  # Importa a biblioteca OpenCV para manipulação de imagens
import math  # Importa a biblioteca math para funções matemáticas
import time  # Importa time para trabalhar com tempo
import mediapipe as mp  # Importa o MediaPipe para detecção de mãos
from option_button import OptionButton  # Importa a classe OptionButton
from question_generator import generate_question  # Importa a função generate_question
from cartesian_plane import draw_cartesian_plane_with_numbers  # Importa a função para desenhar o plano cartesiano

mp_drawing = mp.solutions.drawing_utils  # Utilidades de desenho do MediaPipe
mp_hands = mp.solutions.hands  # Solução de detecção de mãos do MediaPipe

def main():
    cap = cv2.VideoCapture(0)  # Inicia a captura de vídeo da webcam
    cap.set(3, 1280)  # Define a largura do vídeo
    cap.set(4, 720)  # Define a altura do vídeo
    with mp_hands.Hands(
        max_num_hands=2,  # Permite detectar até 2 mãos
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:  # Configura o detector de mãos
        difficulty_selected = False  # Indica se a dificuldade já foi selecionada
        difficulty = ''  # Variável para armazenar a dificuldade escolhida
        buttons_difficulty = [
            OptionButton((200, 300), 200, 100, 'Facil'),  # Botão para a dificuldade Fácil
            OptionButton((500, 300), 200, 100, 'Medio'),  # Botão para a dificuldade Média
            OptionButton((800, 300), 200, 100, 'Dificil')  # Botão para a dificuldade Difícil
        ]
        while not difficulty_selected:
            success, img = cap.read()  # Captura um frame da webcam
            if not success:
                break  # Encerra o loop se não conseguir capturar
            img = cv2.flip(img, 1)  # Espelha a imagem horizontalmente
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte a imagem para RGB
            results = hands.process(imgRGB)  # Processa a imagem para detectar mãos
            cv2.putText(img, "Selecione a Dificuldade", (350, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)  # Exibe o texto para selecionar a dificuldade
            for button in buttons_difficulty:
                button.draw(img)  # Desenha os botões de dificuldade na tela
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),  # Cor azul ciano para os marcos
                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)   # Cor azul ciano para as conexões
                    )  # Desenha os marcos da mão detectada
                    x = int(hand_landmarks.landmark[8].x * img.shape[1])  # Coordenada x do dedo indicador
                    y = int(hand_landmarks.landmark[8].y * img.shape[0])  # Coordenada y do dedo indicador
                    x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])  # Coordenada x do polegar
                    y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])  # Coordenada y do polegar
                    cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)  # Desenha um círculo azul ciano no dedo indicador
                    cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)  # Desenha um círculo azul ciano no polegar
                    distance = math.hypot(x - x_thumb, y - y_thumb)  # Calcula a distância entre o indicador e o polegar
                    if distance < 40:
                        for button in buttons_difficulty:
                            if button.checkClicking(x, y):
                                difficulty = button.value  # Define a dificuldade escolhida
                                difficulty_selected = True  # Marca que a dificuldade foi selecionada
                                break
            cv2.imshow("VisionQuest - github.com/eoLucasS", img)  # Mostra a imagem na janela
            key = cv2.waitKey(1)
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return  # Encerra o programa se a tecla 'q' for pressionada
        question_data = generate_question(difficulty)  # Gera a primeira questão com base na dificuldade
        feedback = ""  # String para armazenar o feedback ao jogador
        feedback_start_time = 0  # Marca o tempo em que o feedback começou a ser exibido
        new_question_needed = False  # Indica se uma nova questão deve ser gerada
        center = (640, 360)  # Centro do plano cartesiano
        plane_width, plane_height = 35 * 36, 35 * 20  # Dimensões do plano
        step_size = 35  # Tamanho dos passos entre as linhas do grid
        while True:
            success, img = cap.read()  # Captura um frame da webcam
            if not success:
                break
            img = cv2.flip(img, 1)  # Espelha a imagem
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte para RGB
            results = hands.process(imgRGB)  # Processa para detecção de mãos
            if question_data['type'] == 'multiple_choice':
                cv2.rectangle(img, (50, 50), (img.shape[1]-50, 200),
                              (255, 255, 255), cv2.FILLED)  # Desenha o fundo para a pergunta
                cv2.rectangle(img, (50, 50), (img.shape[1]-50, 200),
                              (0, 0, 0), 2)  # Desenha a borda da pergunta
                font_scale = 2  # Escala da fonte para a pergunta
                question = question_data['question']  # Obtém a pergunta atual
                text_size = cv2.getTextSize(question, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]  # Calcula o tamanho do texto
                while text_size[0] > img.shape[1] - 100:
                    font_scale -= 0.1  # Ajusta a escala se o texto for muito grande
                    text_size = cv2.getTextSize(question, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                text_x = (img.shape[1] - text_size[0]) // 2  # Calcula a posição x para centralizar o texto
                text_y = 150  # Posição y para o texto
                cv2.putText(img, question, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)  # Desenha a pergunta na imagem
                options = question_data['options']  # Obtém as opções de resposta
                option_buttons = []
                for i in range(3):
                    xPos = 200 + i * 300
                    yPos = 400
                    option_buttons.append(OptionButton((xPos, yPos), 200, 100, options[i]))  # Cria os botões das opções
                for button in option_buttons:
                    button.draw(img)  # Desenha os botões na imagem
            elif question_data['type'] == 'cartesian_plane':
                draw_cartesian_plane_with_numbers(img, center, plane_width, plane_height, step_size)  # Desenha o plano cartesiano
                question = question_data['question']  # Obtém a pergunta atual
                cv2.putText(img, question, (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)  # Desenha a pergunta no canto superior esquerdo
                x_target, y_target = question_data['target_point']  # Coordenadas do ponto alvo
                screen_x = center[0] + x_target * step_size  # Converte a coordenada x para a posição na tela
                screen_y = center[1] - y_target * step_size  # Converte a coordenada y para a posição na tela
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),  # Cor azul ciano para os marcos
                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=2)   # Cor azul ciano para as conexões
                    )  # Desenha os marcos da mão detectada
                    x = int(hand_landmarks.landmark[8].x * img.shape[1])  # Coordenada x do dedo indicador
                    y = int(hand_landmarks.landmark[8].y * img.shape[0])  # Coordenada y do dedo indicador
                    x_thumb = int(hand_landmarks.landmark[4].x * img.shape[1])  # Coordenada x do polegar
                    y_thumb = int(hand_landmarks.landmark[4].y * img.shape[0])  # Coordenada y do polegar
                    cv2.circle(img, (x, y), 10, (255, 255, 0), cv2.FILLED)  # Desenha um círculo azul ciano no dedo indicador
                    cv2.circle(img, (x_thumb, y_thumb), 10, (255, 255, 0), cv2.FILLED)  # Desenha um círculo azul ciano no polegar
                    distance = math.hypot(x - x_thumb, y - y_thumb)  # Calcula a distância entre o indicador e o polegar
                    if question_data['type'] == 'multiple_choice':
                        if distance < 40 and feedback == "":
                            for button in option_buttons:
                                if button.checkClicking(x, y):
                                    if button.value == question_data['correct_answer']:
                                        feedback = "Voce acertou!"  # Mensagem de acerto
                                        feedback_start_time = time.time()  # Marca o tempo do feedback
                                        new_question_needed = True  # Indica que uma nova questão deve ser gerada
                                    else:
                                        feedback = "Voce errou!"  # Mensagem de erro
                                        feedback_start_time = time.time()
                                    break
                    elif question_data['type'] == 'cartesian_plane':
                        distance_to_point = math.hypot(x - screen_x, y - screen_y)  # Calcula a distância até o ponto alvo
                        if distance_to_point < 20 and feedback == "":
                            feedback = "Voce acertou!"  # Mensagem de acerto
                            feedback_start_time = time.time()
                            new_question_needed = True
                    if feedback != "":
                        if time.time() - feedback_start_time > 2:
                            feedback = ""  # Limpa o feedback após 2 segundos
                            if new_question_needed:
                                question_data = generate_question(difficulty)  # Gera uma nova questão
                                new_question_needed = False
                        else:
                            cv2.putText(img, feedback, (x - 100, y - 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)  # Exibe o feedback na tela
            else:
                feedback = ""  # Limpa o feedback se não houver mão detectada
            cv2.imshow("VisionQuest - github.com/eoLucasS", img)  # Exibe a imagem na janela
            key = cv2.waitKey(1)
            if key == ord('q'):
                break  # Encerra o loop se a tecla 'q' for pressionada
        cap.release()  # Libera a captura da webcam
        cv2.destroyAllWindows()  # Fecha todas as janelas

if __name__ == "__main__":
    main()  # Chama a função principal se o script for executado diretamente