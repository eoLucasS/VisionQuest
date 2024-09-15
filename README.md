<!-- 
$$$$$$$\                                $$\                                     $$\       $$\
$$  __$$\                               $$ |                                    $$ |      $$ |
$$ |  $$ | $$$$$$\ $$\    $$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$ |      $$$$$$$\  $$\   $$\
$$ |  $$ |$$  __$$\\$$\  $$  |$$  __$$\ $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$ |      $$  __$$\ $$ |  $$ |
$$ |  $$ |$$$$$$$$ |\$$\$$  / $$$$$$$$ |$$ |$$ /  $$ |$$ /  $$ |$$$$$$$$ |$$ /  $$ |      $$ |  $$ |$$ |  $$ |
$$ |  $$ |$$   ____| \$$$  /  $$   ____|$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |  $$ |      $$ |  $$ |$$ |  $$ |
$$$$$$$  |\$$$$$$$\   \$  /   \$$$$$$$\ $$ |\$$$$$$  |$$$$$$$  |\$$$$$$$\ \$$$$$$$ |      $$$$$$$  |\$$$$$$$ |
\_______/  \_______|   \_/     \_______|\__| \______/ $$  ____/  \_______| \_______|      \_______/  \____$$ |
                                                      $$ |                                          $$\   $$ |
                                                      $$ |                                          \$$$$$$  |
                                                      \__|                                           \______/
$$\                                                   $$\                                                          $$\                  $$$$$$\  $$\ $$\
$$ |                                                  $$ |                                                         $$ |                $$  __$$\ \__|$$ |
$$ |     $$\   $$\  $$$$$$$\ $$$$$$\   $$$$$$$\       $$ |      $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$\        $$$$$$$ | $$$$$$\        $$ /  \__|$$\ $$ |$$\    $$\ $$$$$$\
$$ |     $$ |  $$ |$$  _____|\____$$\ $$  _____|      $$ |     $$  __$$\ $$  __$$\ $$  __$$\ $$  _____|      $$  __$$ | \____$$\       \$$$$$$\  $$ |$$ |\$$\  $$  |\____$$\
$$ |     $$ |  $$ |$$ /      $$$$$$$ |\$$$$$$\        $$ |     $$ /  $$ |$$ /  $$ |$$$$$$$$ |\$$$$$$\        $$ /  $$ | $$$$$$$ |       \____$$\ $$ |$$ | \$$\$$  / $$$$$$$ |
$$ |     $$ |  $$ |$$ |     $$  __$$ | \____$$\       $$ |     $$ |  $$ |$$ |  $$ |$$   ____| \____$$\       $$ |  $$ |$$  __$$ |      $$\   $$ |$$ |$$ |  \$$$  / $$  __$$ |
$$$$$$$$\\$$$$$$  |\$$$$$$$\\$$$$$$$ |$$$$$$$  |      $$$$$$$$\\$$$$$$  |$$$$$$$  |\$$$$$$$\ $$$$$$$  |      \$$$$$$$ |\$$$$$$$ |      \$$$$$$  |$$ |$$ |   \$  /  \$$$$$$$ |
\________|\______/  \_______|\_______|\_______/       \________|\______/ $$  ____/  \_______|\_______/        \_______| \_______|       \______/ \__|\__|    \_/    \_______|
                                                                         $$ |
                                                                         $$ |
                                                                         \__|
-->
<h1 align="center">
  Jogo Interativo de Matemática com Visão Computacional <img width="25px" src="https://raw.githubusercontent.com/eoLucasS/portfolio/main/assets/img/icon.svg"/>
</h1>

<p align="center">
  <img alt="Github Top Language" src="https://img.shields.io/github/languages/top/eolucass/VisionQuest?color=00FFFB">
  <img alt="Github Language Count" src="https://img.shields.io/github/languages/count/eolucass/VisionQuest?color=00FFFB">
  <img alt="Repository Size" src="https://img.shields.io/github/repo-size/eolucass/VisionQuest?color=00FFFB">
</p>

<br>

<p align="center">
  <img src="assets/preview.png" width="650" height="338">
</p>

<br>

## 📝 Descrição 

O VisionQuest é uma ferramenta educacional interativa desenvolvida com o objetivo de promover a educação inclusiva e acessível. O projeto utiliza tecnologias de reconhecimento de mãos para criar uma experiência de aprendizagem divertida e inovadora, baseada em conceitos matemáticos fundamentais. Alinhado ao ODS 4 da ONU, o jogo visa assegurar a educação de qualidade, promovendo oportunidades de aprendizagem para todos.

## 🚀 Funcionalidades Desenvolvidas

### 1. Reconhecimento de Mãos e Gestos

- **Bibliotecas Utilizadas**: MediaPipe e OpenCV para reconhecimento de mãos em tempo real.
- **Detecção Ambidestra**: O sistema reconhece ambas as mãos simultaneamente.
- **Gestos Interativos**: O gesto de pinça é utilizado para seleção e interação com os botões do jogo.
- **Aprimoramento Visual**: Personalização da cor dos marcadores de mãos para azul ciano, proporcionando uma interface mais limpa e intuitiva.

### 2. Geração de Questões Matemáticas

- **Três Níveis de Dificuldade**: Fácil, Médio e Difícil, atendendo diferentes níveis de conhecimento.
- **Tipos de Questões**:
  - Operações aritméticas (adição, subtração, multiplicação e divisão).
  - Equações do primeiro grau.
  - Potências, raízes quadradas e logaritmos.
  - Identificação de pontos em um plano cartesiano interativo.

### 3. Interface Interativa

- **Botões Virtuais**: Seleção de respostas e níveis de dificuldade via botões interativos.
- **Plano Cartesiano Dinâmico**: Um plano cartesiano é desenhado dinamicamente com grid e numeração dos eixos, permitindo que os usuários encontrem pontos específicos.
- **Feedback Imediato**: Feedback visual instantâneo ao usuário, indicando acertos e erros.

### 4. Estrutura Modular

- **Módulos Separados**:
  - `option_button.py`: Manipulação de botões interativos.
  - `question_generator.py`: Geração das perguntas com base na dificuldade.
  - `cartesian_plane.py`: Desenho e interação com o plano cartesiano.
  - `main.py`: Integra todos os módulos para gerenciar o fluxo do jogo.

## 📚 Bibliotecas e Ferramentas

- [Python](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://github.com/google-ai-edge/mediapipe)
- [NumPy](https://numpy.org/)
- [Visual Studio Code](https://code.visualstudio.com/)

## 💡 Avanços Realizados

- **Integração Completa do Plano Cartesiano**: Agora, os usuários podem interagir diretamente com o plano cartesiano, identificando pontos solicitados nas perguntas.
- **Detecção Melhorada de Mãos**: A detecção de mãos foi aprimorada, suportando interações com ambas as mãos.
- **Feedback em Tempo Real**: O jogo oferece feedback imediato, proporcionando uma experiência de aprendizado mais engajante.

## 📊 Alinhamento com a Ementa Acadêmica

O projeto aborda diversos tópicos da ementa acadêmica de matemática, incluindo:

- Aritmética de Inteiros
- Álgebra Linear
- Produto Cartesiano (plano cartesiano interativo)
- Operações com potências e logaritmos

## 🔗 Links

<p align="left">

 <a href="https://www.linkedin.com/in/lucaslopesdasilva/" alt="Linkedin">
  <img src="https://img.shields.io/badge/-Linkedin-000?style=for-the-badge&logo=Linkedin&logoColor=0A66C2&link=https://www.linkedin.com/in/lucaslopesdasilva"/> 
 </a>
  
 <a href="https://twitter.com/eoLucasS114" alt="Twitter">
  <img src="https://img.shields.io/badge/-Twitter-000?style=for-the-badge&logo=Twitter&logoColor=1DA1F2&link=https://twitter.com/eoLucasS114"/> 
 </a>

 <a href="https://portfolio-lucaslopes.vercel.app" alt="Portfolio">
  <img src="https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=FFF&link=https://portfolio-lucaslopes.vercel.app"/>
 </a>

 </p>
 
## 💻 Colaboradores<br>
<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/lucaslopesdasilva/">
        <img src="https://avatars.githubusercontent.com/u/119815116?v=4" width="100px;" /><br>
        <sub>
          <b>Lucas Silva</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/nycolasagrgarcia/">
        <img src="https://avatars.githubusercontent.com/u/127459801?v=4" width="100px;" /><br>
        <sub>
          <b>Nycolas Garcia</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/danilodoes/">
        <img src="https://avatars.githubusercontent.com/u/110133245?v=4" width="100px;" /><br>
        <sub>
          <b>Danilo Santos</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPlyqvw8T_cZvq5gRM59jqm8KIE44_ugokQ&s">
        <img src="https://avatars.githubusercontent.com/u/44868973?v=4" width="100px;" /><br>
        <sub>
          <b>Letícia Araujo</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

-----

<h3 align="center"> Desenvolvido por <a href="https://www.linkedin.com/in/lucaslopesdasilva/">Lucas Lopes da Silva</a> ☕</h3>