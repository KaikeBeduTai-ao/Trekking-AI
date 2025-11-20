import cv2
import sys
import os
import numpy as np  # Necessário para transparência

# --- IMPORTAÇÃO DOS MÓDULOS ---
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    from hardware.esp32_comm import ESP32Comm
    from utils.constants import CMD_FRENTE, CMD_ESQUERDA, CMD_DIREITA, CMD_PARAR
    usa_serial = True
except ImportError:
    print("[AVISO] Rodando em modo SIMULAÇÃO.")
    usa_serial = False
    CMD_FRENTE, CMD_ESQUERDA, CMD_DIREITA, CMD_PARAR = "FRENTE", "ESQUERDA", "DIREITA", "PARAR"

# --- CONFIGURAÇÃO VISUAL ---
LARGURA_ZONA_CENTRAL = 0.30
# Cores (B, G, R)
COR_BRANCO = (255, 255, 255)
COR_PRETO_TRANS = (0, 0, 0)
COR_DESTAQUE = (255, 200, 0)  # Ciano/Azulzinho para interface
COR_ALERTA = (0, 0, 255)      # Vermelho para erros

# Inicializa Serial
esp = None
if usa_serial:
    esp = ESP32Comm(baud=115200)

# Inicializa Tracker
try:
    rastreador = cv2.TrackerCSRT_create()
except AttributeError:
    rastreador = cv2.legacy.TrackerCSRT_create()

video = cv2.VideoCapture(0)
bbox = None
ultimo_comando = ""


def desenhar_overlay_minimalista(frame, limites, comando):
    """Desenha a interface com transparência"""
    h, w, _ = frame.shape
    lim_esq, lim_dir = limites

    # 1. Cria uma cópia para desenhar formas transparentes
    overlay = frame.copy()

    # --- GUIAS VERTICAIS DISCRETAS ---
    # Desenha linhas finas e brancas com pouca opacidade para marcar o corredor
    cv2.line(overlay, (lim_esq, 0), (lim_esq, h), (255, 255, 255), 1)
    cv2.line(overlay, (lim_dir, 0), (lim_dir, h), (255, 255, 255), 1)

    # --- BARRA DE STATUS INFERIOR (GLASS) ---
    # Cria uma faixa preta transparente no fundo
    cv2.rectangle(overlay, (0, h - 60), (w, h), (0, 0, 0), -1)

    # Se houver um comando ativo (esquerda/direita), ilumina o lado correspondente suavemente
    if comando == CMD_ESQUERDA:
        cv2.rectangle(overlay, (0, 0), (lim_esq, h),
                      (0, 255, 255), -1)  # Amarelo suave
    elif comando == CMD_DIREITA:
        cv2.rectangle(overlay, (lim_dir, 0), (w, h),
                      (0, 255, 255), -1)  # Amarelo suave
    elif comando == CMD_FRENTE:
        # Luz verde sutil no centro
        cv2.rectangle(overlay, (lim_esq, 0), (lim_dir, h), (0, 255, 0), -1)

    # Aplica a transparência (Mistura overlay com original)
    # alpha=0.7 para imagem original, beta=0.3 para o overlay (30% de opacidade)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

    # --- TEXTOS (Sólidos, desenhados DEPOIS da transparência) ---
    fonte = cv2.FONT_HERSHEY_SIMPLEX

    # Texto centralizado na barra inferior
    texto_status = f"STATUS: {comando.upper()}"
    tamanho = cv2.getTextSize(texto_status, fonte, 0.7, 1)[0]
    centro_x = (w - tamanho[0]) // 2

    cv2.putText(frame, texto_status, (centro_x, h - 20),
                fonte, 0.7, COR_BRANCO, 1, cv2.LINE_AA)

    # Indicadores de direção (Setas minimalistas)
    if comando == CMD_ESQUERDA:
        cv2.putText(frame, "<", (20, h//2), fonte,
                    2, COR_BRANCO, 2, cv2.LINE_AA)
    elif comando == CMD_DIREITA:
        cv2.putText(frame, ">", (w - 50, h//2), fonte,
                    2, COR_BRANCO, 2, cv2.LINE_AA)
    elif comando == CMD_FRENTE:
        cv2.putText(frame, "^", (w//2 - 15, 50), fonte,
                    2, COR_BRANCO, 2, cv2.LINE_AA)

    return frame


def desenhar_mira_elegante(frame, x, y, w, h):
    # Desenha apenas os cantos (brackets) em vez de um quadrado fechado
    tam_canto = 15
    cor = COR_DESTAQUE
    th = 2  # Espessura

    # Canto Superior Esquerdo
    cv2.line(frame, (x, y), (x + tam_canto, y), cor, th)
    cv2.line(frame, (x, y), (x, y + tam_canto), cor, th)

    # Canto Superior Direito
    cv2.line(frame, (x + w, y), (x + w - tam_canto, y), cor, th)
    cv2.line(frame, (x + w, y), (x + w, y + tam_canto), cor, th)

    # Canto Inferior Esquerdo
    cv2.line(frame, (x, y + h), (x + tam_canto, y + h), cor, th)
    cv2.line(frame, (x, y + h), (x, y + h - tam_canto), cor, th)

    # Canto Inferior Direito
    cv2.line(frame, (x + w, y + h), (x + w - tam_canto, y + h), cor, th)
    cv2.line(frame, (x + w, y + h), (x + w, y + h - tam_canto), cor, th)

    # Ponto central discreto
    centro_x, centro_y = x + w//2, y + h//2
    cv2.circle(frame, (centro_x, centro_y), 2, cor, -1)


# --- LOOP PRINCIPAL ---
print("\n--- VISÃO MINIMALISTA INICIADA ---")
print("'s' para rastrear | 'ESC' para sair")

while True:
    ok, frame = video.read()
    if not ok:
        break

    h, w, _ = frame.shape

    # Define as zonas
    centro_x = w // 2
    margem = int(w * LARGURA_ZONA_CENTRAL / 2)
    lim_esq = centro_x - margem
    lim_dir = centro_x + margem

    # Leitura de tecla
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):
        bbox = cv2.selectROI("Navegacao", frame, False)
        rastreador.init(frame, bbox)
    elif k == 27:  # ESC
        if usa_serial and esp:
            esp.send(CMD_PARAR)
        break

    comando_atual = CMD_PARAR

    # --- LÓGICA ---
    if bbox is not None:
        ok, bbox = rastreador.update(frame)
        if ok:
            (x, y, bw, bh) = [int(v) for v in bbox]
            obj_cx = x + (bw // 2)

            # Navegação
            if obj_cx < lim_esq:
                comando_atual = CMD_ESQUERDA
            elif obj_cx > lim_dir:
                comando_atual = CMD_DIREITA
            else:
                comando_atual = CMD_FRENTE

            # Desenha interface
            desenhar_overlay_minimalista(
                frame, (lim_esq, lim_dir), comando_atual)
            desenhar_mira_elegante(frame, x, y, bw, bh)
        else:
            desenhar_overlay_minimalista(frame, (lim_esq, lim_dir), CMD_PARAR)
            cv2.putText(frame, "OBJETO PERDIDO", (w//2 - 100, h//2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, COR_ALERTA, 2)
    else:
        # Tela de espera (Standby)
        desenhar_overlay_minimalista(frame, (lim_esq, lim_dir), "AGUARDANDO")
        cv2.putText(frame, "PRESSIONE 'S' PARA INICIAR", (w//2 - 180,
                    h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COR_BRANCO, 1)

    # --- ENVIO SERIAL ---
    if comando_atual != ultimo_comando:
        if usa_serial and esp:
            esp.send(comando_atual)
        ultimo_comando = comando_atual

    cv2.imshow("Navegacao", frame)

video.release()
cv2.destroyAllWindows()
