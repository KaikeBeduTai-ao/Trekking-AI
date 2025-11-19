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
            name = p.device.lower()
            desc = p.description.lower()

            # Windows: COM3, COM4...
            if "usb" in desc or "uart" in desc or "cp210" in desc or "ch340" in desc:
                return p.device

            # Linux: /dev/ttyUSB0 ou /dev/ttyACM0
            if "ttyusb" in name or "ttyacm" in name:
                return p.device

            # MacOS: /dev/cu.usbserial, /dev/cu.usbmodem
            if "cu.usb" in name:
                return p.device

        return None

    def send(self, data):
        if not self.ser:
            return

        msg = str(data) + "\n"
        self.ser.write(msg.encode())
