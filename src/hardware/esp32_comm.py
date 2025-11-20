import serial
import time
import serial.tools.list_ports


class ESP32Comm:
    def __init__(self, baud=115200):
        self.ser = None

        port = self.auto_detect_port()
        if port is None:
            print("[ERROR] ESP32 NÃO encontrado em nenhuma porta!")
            return

        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            print(f"[SUCCESS] ESP32 conectado na porta {port}!")
        except Exception as e:
            print(f"[ERROR] Erro ao conectar no ESP32: {e}")
            self.ser = None

    def auto_detect_port(self):
        print("[INFO] Procurando ESP32 nas portas...")

        ports = serial.tools.list_ports.comports()

        for p in ports:
            desc = p.description.lower()
            hwid = p.hwid.lower()
            name = p.device.lower()

            print("Encontrado:", p.device, "|", p.description)

            # Casos mais comuns
            if "esp" in desc or "esp" in hwid:
                return p.device

            if "cp210" in desc or "cp210" in hwid:
                return p.device

            if "ch340" in desc or "ch910" in desc:
                return p.device

            if "ttyusb" in name or "ttyacm" in name:
                return p.device

            if "usb serial" in desc:
                return p.device

        return None

    def send(self, command):
        # print('Tentou enviar')
        # print(f'ser: {self.ser}')
        if self.ser:
            try:
                msg = str(command) + "\n"
                print(f"[HARDWARE] Envio: {msg}")
                self.ser.write(msg.encode())
            except Exception as e:
                print(f"[HARDWARE] Erro de envio: {e}")
