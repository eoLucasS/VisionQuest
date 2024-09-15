import random  # Importa a biblioteca random para gerar valores aleatórios
import math  # Importa a biblioteca math para funções matemáticas

def generate_question(difficulty):
    question_data = {}  # Dicionário para armazenar os dados da questão
    if difficulty == 'Facil':
        question_types = ['arithmetic', 'cartesian_plane']  # Tipos de questões para o nível fácil
    elif difficulty == 'Medio':
        question_types = ['arithmetic', 'sqrt', 'power', 'cartesian_plane']  # Tipos para o nível médio
    elif difficulty == 'Dificil':
        question_types = ['arithmetic', 'sqrt', 'power', 'log', 'linear_equation', 'cartesian_plane']  # Tipos para o nível difícil
    question_type = random.choice(question_types)  # Seleciona aleatoriamente um tipo de questão
    if question_type == 'cartesian_plane':
        x = random.randint(-18, 18)  # Gera uma coordenada x aleatória
        y = random.randint(-10, 10)  # Gera uma coordenada y aleatória
        question = f"Encontre o ponto: ({x}, {y})"  # Monta a pergunta
        question_data['type'] = 'cartesian_plane'  # Define o tipo de questão
        question_data['question'] = question  # Armazena a pergunta
        question_data['target_point'] = (x, y)  # Armazena o ponto alvo
    else:
        question_data['type'] = 'multiple_choice'  # Define o tipo como múltipla escolha
        if question_type == 'arithmetic':
            operations = ['+', '-', '*', '/']  # Operações aritméticas possíveis
            op = random.choice(operations)  # Seleciona uma operação aleatória
            num1 = random.randint(1, 100)  # Gera o primeiro número
            num2 = random.randint(1, 100)  # Gera o segundo número
            if op == '/':
                num2 = random.randint(1, 10)  # Ajusta num2 para evitar divisões complexas
                num1 = num2 * random.randint(1, 10)  # Ajusta num1 para garantir uma divisão exata
            question = f"Quanto e {num1} {op} {num2}?"  # Monta a pergunta
            correct_answer = int(eval(f"{num1}{op}{num2}"))  # Calcula a resposta correta
        elif question_type == 'sqrt':
            num = random.choice([i**2 for i in range(1, 31)])  # Seleciona um quadrado perfeito
            question = f"Quanto e sqrt({num})?"  # Monta a pergunta
            correct_answer = int(math.sqrt(num))  # Calcula a raiz quadrada
        elif question_type == 'power':
            base = random.randint(2, 10)  # Gera a base da potência
            exponent = random.randint(2, 5)  # Gera o expoente
            question = f"Quanto e {base}^{exponent}?"  # Monta a pergunta
            correct_answer = base ** exponent  # Calcula a potência
        elif question_type == 'log':
            base = random.choice([2, 3, 5, 10])  # Seleciona a base do logaritmo
            exponent = random.randint(1, 5)  # Gera o expoente
            num = base ** exponent  # Calcula o logaritmando
            question = f"Quanto e log_{base}({num})?"  # Monta a pergunta
            correct_answer = exponent  # A resposta é o expoente
        elif question_type == 'linear_equation':
            equation_type = random.choice(['addition', 'subtraction', 'multiplication', 'division'])  # Tipo de equação
            if equation_type == 'addition':
                x = random.randint(1, 50)  # Valor de x
                b = random.randint(1, 50)  # Valor de b
                c = x + b  # Calcula c
                question = f"x + {b} = {c}, Quanto e x?"  # Monta a equação
                correct_answer = x  # Resposta correta
            elif equation_type == 'subtraction':
                x = random.randint(1, 50)
                b = random.randint(1, 50)
                c = x - b
                question = f"x - {b} = {c}, Quanto e x?"
                correct_answer = x
            elif equation_type == 'multiplication':
                x = random.randint(1, 20)
                b = random.randint(1, 10)
                c = x * b
                question = f"{b} * x = {c}, Quanto e x?"
                correct_answer = x
            elif equation_type == 'division':
                b = random.randint(1, 10)
                x = random.randint(1, 50)
                c = x / b
                if c.is_integer():
                    c = int(c)
                    question = f"x / {b} = {c}, Quanto e x?"
                    correct_answer = x
                else:
                    return generate_question(difficulty)  # Regera a questão se o resultado não for inteiro
        wrong_answers = set()  # Conjunto para armazenar respostas incorretas
        while len(wrong_answers) < 2:
            wrong = correct_answer + random.choice([-random.randint(1, 10), random.randint(1, 10)])  # Gera uma resposta errada
            if wrong != correct_answer and wrong >= 0:
                wrong_answers.add(wrong)  # Adiciona se for válida
        options = [str(correct_answer)] + [str(w) for w in wrong_answers]  # Combina as respostas
        random.shuffle(options)  # Embaralha as opções
        question_data['question'] = question  # Armazena a pergunta
        question_data['correct_answer'] = str(correct_answer)  # Armazena a resposta correta
        question_data['options'] = options  # Armazena as opções de resposta
    return question_data  # Retorna os dados da questão