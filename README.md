# Trekking AI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![ESP32](https://img.shields.io/badge/Hardware-ESP32-red?style=for-the-badge&logo=espressif&logoColor=white)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green?style=for-the-badge&logo=opencv&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)

**Sistema para competição de trekking usando Notebook + ESP32.**

Este projeto integra visão computacional e sistemas embarcados para criar um carrinho autônomo capaz de identificar cones e navegar automaticamente.

---

## Funcionalidades

* **Controle Híbrido:** Processamento pesado no Notebook e controle de motores no ESP32.
* **Visão Computacional:** Detecção de cones e obstáculos usando OpenCV.
* **Interface Gráfica:** Monitoramento e debug em tempo real com PyGame.
* **Comunicação Serial:** Troca de dados rápida entre Python e o microcontrolador via PySerial.
* **Navegação:** Algoritmos de decisão para desvio e seguimento de rota.

---

## Dependências

Antes de começar, certifique-se de ter o **Python 3.x** instalado. As principais bibliotecas utilizadas são:

* `opencv-python` (Processamento de imagem)
* `pygame` (Interface e input)
* `pyserial` (Comunicação com ESP32)
* `numpy` (Cálculos matemáticos)

---

## Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/KaikeBeduTai-ao/Trekking-AI.git
cd trekking-ai
```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

---

## ⚠️ Solução de Problemas (Troubleshooting)

### 1. **Erro: "Metadata generation failed" ou "Unknown compiler"**
    
  **Sintoma**: Ao rodar o `pip install`, aparece um erro vermelho gigante mencionando falha na construção do **NumPy** ou **Meson build system**. 
          
  **Causa**: Você está usando uma versão muito recente do Python (ex: 3.14) que não possui binários pré-compilados para as bibliotecas. O Windows tenta compilar manualmente e falha. Solução:
  
  1. Desinstale o Python atual ou instale o Python 3.12.8.
          
  2. Apague a pasta `venv` antiga.
          
  3. Recrie o ambiente forçando a versão correta: `py -3.12 -m venv venv`.

### 2. **Erro no Windows: "Running scripts is disabled on this system"**

  Se ao tentar ativar o ambiente virtual (`venv`) você receber um erro em vermelho dizendo que a execução de scripts foi desabilitada:

  1. Abra o PowerShell e execute o comando abaixo para liberar permissões para seu usuário:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  2. Tente ativar o venv novamente:
  ```powershell
  .\venv\Scripts\activate
  ```

---

## Configuração do Hardware (Firmware)

O código C++ para o ESP32 está localizado na pasta `firmware/`. Você precisará da Arduino IDE configurada para ESP32.
**Estrutura:**

* `firmware/esp32_robot/`: Código oficial para controle dos motores.

* `firmware/tests/`: Códigos para teste de LED e comunicação.

**Como carregar:**
1. Conecte o ESP32 ao computador via USB.
2. Abra o arquivo `firmware/esp32_robot/esp32_robot.ino` na Arduino IDE.
3. Verifique as definições dos pinos no início do arquivo (`IN1`, `IN2`, etc.) e ajuste conforme sua montagem.
4. Selecione a placa e a porta correta e clique em **Upload**.

   **Atenção**: Certifique-se de fechar o "Serial Monitor" da Arduino IDE antes de rodar o script Python, caso contrário a porta USB estará ocupada.


## Como Usar

Com o ESP32 conectado e o ambiente Python configurado.
1. **Execute o programa principal:**
```bash
python src/main.py
```
2. **O Sistema irá abrir duas janelas:**
   * **Visão Computacional (OpenCV)**: Mostra a imagem da câmera.
   * **Radar (Pygame)**: Mostra a representação gráfica das zonas e do objeto.
3. **Iniciando o Rastreamento:**
   * Aponte a câmera para o objeto que deseja seguir (ex: um cone).
   * Clique na janela da Câmera para focar.
   * Pressione a tecla `s`. A imagem irá congelar.
   * Com o mouse, desenhe um retângulo ao redor do objeto.
   * Pressione `ENTER` para confirmar.
4. **Operação:**
   * O robô começará a enviar comandos (`frente`, `esquerda`, `direita`) para o ESP32 automaticamente baseando-se na posição do objeto na tela.
5. **Parar:**
   * Pressione `ESC` para encerrar o programa e parar o robô.

## Estrutura do Projeto
```bash
trekking-ai/
├── firmware/           # Código C++ (Arduino/ESP32)
├── src/                # Código Fonte Python
│   ├── hardware/       # Driver de comunicação Serial
│   ├── navigation/     # Lógica de decisão de movimento
│   ├── ui/             # Interface gráfica (Pygame)
│   ├── utils/          # Constantes e configuracões
│   ├── vision/         # Algoritmos de Rastreamento (OpenCV)
│   └── main.py         # Arquivo principal
└── README.md           # Documentação
```
