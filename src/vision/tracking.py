import cv2
import numpy as np

# --- CONFIGURAÇÃO ---
# A foto que você quer que ele busque
ARQUIVO_REFERENCIA = '/home/kaiketaiao/Desktop/CrossBots/trekking-ai/assets/test_images/cone1.jpeg'
MIN_MATCHES = 10  # Mínimo de pontos coincidentes para considerar que achou

# 1. Inicializa o Detector de Características (SIFT)
sift = cv2.SIFT_create()

# Carrega a imagem de referência e acha os pontos chave
img_ref = cv2.imread(ARQUIVO_REFERENCIA, 0)  # Carrega em escala de cinza
if img_ref is None:
    print(f"Erro: Não encontrei o arquivo {ARQUIVO_REFERENCIA}")
    exit()

kp_ref, desc_ref = sift.detectAndCompute(img_ref, None)

# Inicializa o Matcher (Comparador de pontos)
bf = cv2.BFMatcher()

# Inicializa vídeo
video = cv2.VideoCapture(0)

# Variáveis de controle
rastreando = False
rastreador = None


def criar_rastreador():
    try:
        return cv2.TrackerCSRT_create()
    except AttributeError:
        return cv2.legacy.TrackerCSRT_create()


while True:
    ok, frame = video.read()
    if not ok:
        break

    # Se NÃO estamos rastreando, procuramos o objeto (Modo Busca)
    if not rastreando:
        cv2.putText(frame, "PROCURANDO OBJETO...", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

        # Converte frame atual para cinza
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Acha pontos no frame atual
        kp_frame, desc_frame = sift.detectAndCompute(gray_frame, None)

        # Se houver descritores no frame
        if desc_frame is not None and len(desc_frame) > 0:
            matches = bf.knnMatch(desc_ref, desc_frame, k=2)

            # Filtro de "bons matches" (Lowe's ratio test)
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

            # Se achou pontos suficientes que batem com a foto
            if len(good_matches) > MIN_MATCHES:
                print(f"Objeto encontrado! Matches: {len(good_matches)}")

                # Matemática para descobrir onde o objeto está (Homografia)
                src_pts = np.float32(
                    [kp_ref[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32(
                    [kp_frame[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                if M is not None:
                    h, w = img_ref.shape
                    pts = np.float32(
                        [[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                    dst = cv2.perspectiveTransform(pts, M)

                    # Pega o bounding box (retângulo envolvente) da detecção
                    x_min = int(np.min(dst[:, :, 0]))
                    y_min = int(np.min(dst[:, :, 1]))
                    x_max = int(np.max(dst[:, :, 0]))
                    y_max = int(np.max(dst[:, :, 1]))

                    w_box = x_max - x_min
                    h_box = y_max - y_min

                    # Inicia o Rastreador com essa caixa
                    bbox = (x_min, y_min, w_box, h_box)

                    rastreador = criar_rastreador()  # Recria o rastreador limpo
                    rastreador.init(frame, bbox)
                    rastreando = True

    # Se ESTAMOS rastreando (Modo Tracking)
    else:
        ok, bbox = rastreador.update(frame)

        if ok:
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
            cv2.putText(frame, "Rastreando (CSRT)", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        else:
            # Se o rastreador falhar, voltamos para o modo de busca
            print("Rastreamento perdido. Reiniciando busca.")
            rastreando = False

    cv2.imshow("Auto Tracker", frame)
    if cv2.waitKey(1) & 0XFF == 27:
        break

video.release()
cv2.destroyAllWindows()
