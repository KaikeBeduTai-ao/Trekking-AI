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
git clone [https://github.com/seu-usuario/trekking-ai.git](https://github.com/seu-usuario/trekking-ai.git)
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
