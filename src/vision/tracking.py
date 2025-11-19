import cv2

# Inicialização do Tracker (CSRT é mais preciso, mas mais lento que KCF)
try:
    rastreador = cv2.TrackerCSRT_create()
except AttributeError:
    rastreador = cv2.legacy.TrackerCSRT_create()
# try:
#     rastreador = cv2.TrackerKCF_create()
# except AttributeError:
#     rastreador = cv2.legacy.TrackerKCF_create()

video = cv2.VideoCapture(0)

# CORREÇÃO 1: Inicializar bbox como None para evitar o erro "NameError"
bbox = None

while True:
    ok, frame = video.read()
    if not ok:
        break

    # CORREÇÃO 2: Capturar a tecla apenas UMA vez por frame
    k = cv2.waitKey(1) & 0xFF

    if k == ord('s'):
        # 1. Seleciona a região de interesse (ROI)
        # Pressione ENTER após selecionar a caixa com o mouse
        bbox = cv2.selectROI("Rastreamento", frame, False)

        # 2. Inicializa o rastreador com o frame atual e a caixa desenhada
        rastreador.init(frame, bbox)

    # Só tenta rastrear se bbox já tiver sido definido (ou seja, não é None)
    if bbox is not None:
        ok, bbox = rastreador.update(frame)

        if ok:
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
        else:
            cv2.putText(frame, "Falha no rastreamento", (100, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow("Rastreamento", frame)

    # Pressione ESC para sair
    if k == 27:
        break

video.release()
cv2.destroyAllWindows()
