import random  # Para gerar numeros aleatorios

def generate_question(difficulty):
    question_types = ['multiple_choice', 'cartesian_plane']
    question_type = random.choice(question_types)

    if difficulty == 'Facil':
        if question_type == 'multiple_choice':
            # Questoes faceis de adicao ou subtracao
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            operation = random.choice(['+', '-'])
            if operation == '+':
                question_text = f"Quanto e {num1} + {num2}?"
                correct_answer = str(num1 + num2)
                hint = 'Para somar, junte as quantidades dos dois numeros.'
            else:
                question_text = f"Quanto e {num1} - {num2}?"
                correct_answer = str(num1 - num2)
                hint = 'Para subtrair, tire o segundo numero do primeiro.'
            options = [correct_answer,
                       str(int(correct_answer) + random.randint(1, 5)),
                       str(int(correct_answer) - random.randint(1, 5))]
            random.shuffle(options)
            question_data = {
                'type': 'multiple_choice',
                'question': question_text,
                'options': options,
                'correct_answer': correct_answer,
                'hint': hint
            }
        else:
            # Questoes faceis do plano cartesiano
            x_target = random.randint(-5, 5)
            y_target = random.randint(-5, 5)
            question_text = f"Toque no ponto ({x_target}, {y_target})."
            hint = 'Lembre-se: o primeiro numero e X (horizontal) e o segundo e Y (vertical).'
            question_data = {
                'type': 'cartesian_plane',
                'question': question_text,
                'target_point': (x_target, y_target),
                'hint': hint
            }
    elif difficulty == 'Medio':
        if question_type == 'multiple_choice':
            # Questoes medias de multiplicacao ou divisao
            num1 = random.randint(2, 10)
            num2 = random.randint(2, 10)
            operation = random.choice(['*', '/'])
            if operation == '*':
                question_text = f"Quanto e {num1} x {num2}?"
                correct_answer = str(num1 * num2)
                hint = 'Multiplicacao e como somar o primeiro numero varias vezes.'
            else:
                num1 = num1 * num2
                question_text = f"Quanto e {num1} / {num2}?"
                correct_answer = str(num1 // num2)
                hint = 'Divisao e quantas vezes o divisor cabe no dividendo.'
            options = [correct_answer,
                       str(int(correct_answer) + random.randint(1, 5)),
                       str(max(0, int(correct_answer) - random.randint(1, 5)))]
            random.shuffle(options)
            question_data = {
                'type': 'multiple_choice',
                'question': question_text,
                'options': options,
                'correct_answer': correct_answer,
                'hint': hint
            }
        else:
            # Questoes medias do plano cartesiano
            x_target = random.randint(-8, 8)
            y_target = random.randint(-5, 5)
            question_text = f"Toque no ponto ({x_target}, {y_target})."
            hint = 'Lembre-se: o primeiro numero e X (horizontal) e o segundo e Y (vertical).'
            question_data = {
                'type': 'cartesian_plane',
                'question': question_text,
                'target_point': (x_target, y_target),
                'hint': hint
            }
    elif difficulty == 'Dificil':
        if question_type == 'multiple_choice':
            # Questoes dificeis de logaritmo ou raiz quadrada
            question_subtype = random.choice(['log', 'raiz'])
            if question_subtype == 'log':
                base = random.randint(2, 5)
                exponent = random.randint(2, 4)
                result = base ** exponent
                question_text = f"Qual e o logaritmo base {base} de {result}?"
                correct_answer = str(exponent)
                hint = 'Lembre-se: log base b de b^x e igual a x.'
            else:
                num = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
                question_text = f"Qual e a raiz quadrada de {num}?"
                correct_answer = str(int(num ** 0.5))
                hint = 'Procure um numero que multiplicado por si mesmo resulta no numero dado.'
            options = [correct_answer,
                       str(int(correct_answer) + random.randint(1, 3)),
                       str(max(1, int(correct_answer) - random.randint(1, 3)))]
            random.shuffle(options)
            question_data = {
                'type': 'multiple_choice',
                'question': question_text,
                'options': options,
                'correct_answer': correct_answer,
                'hint': hint
            }
        else:
            # Questoes dificeis do plano cartesiano
            x_target = random.randint(-10, 10)
            y_target = random.randint(-7, 7)
            question_text = f"Toque no ponto ({x_target}, {y_target})."
            hint = 'Lembre-se: o primeiro numero e X (horizontal) e o segundo e Y (vertical).'
            question_data = {
                'type': 'cartesian_plane',
                'question': question_text,
                'target_point': (x_target, y_target),
                'hint': hint
            }
    else:
        # Pergunta padrao
        question_data = {
            'type': 'multiple_choice',
            'question': 'Pergunta padrao',
            'options': ['Opcao 1', 'Opcao 2', 'Opcao 3'],
            'correct_answer': 'Opcao 1',
            'hint': 'Esta e uma dica padrao.'
        }
    return question_data