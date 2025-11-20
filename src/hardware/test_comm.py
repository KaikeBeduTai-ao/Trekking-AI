import sys
import os
import time

# --- 1. CONFIGURAÇÃO DE CAMINHO (O Segredo está aqui) ---
# Precisamos fazer isso ANTES de importar qualquer coisa do projeto

# Pega o diretório atual (.../src/hardware)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Pega o diretório pai (.../src)
src_path = os.path.dirname(current_dir)

# Adiciona 'src' ao Python. Agora ele enxerga 'utils' e 'hardware'
sys.path.append(src_path)

# --- 2. IMPORTAÇÕES DO PROJETO ---
# Agora que o caminho está configurado, podemos importar
try:
    # Tenta importar do caminho absoluto (mais seguro)
    from hardware.esp32_comm import ESP32Comm
    import utils.constants as constants
except ImportError:
    # Fallback caso esteja rodando de dentro da pasta hardware sem o path configurado corretamente
    from esp32_comm import ESP32Comm
    # Se falhar o utils aqui, é porque o path realmente não funcionou


def teste_sequencial():
    print("="*40)
    print("   TESTE DE COMUNICAÇÃO SERIAL ESP32")
    print("="*40)

    # 1. Inicializa a conexão usando a constante
    print(
        f"\n[1] Tentando conectar (Baudrate: {constants.SERIAL_BAUDRATE})...")
    esp = ESP32Comm(baud=constants.SERIAL_BAUDRATE)

    if not esp.ser:
        print("\n[FALHA CRÍTICA] Não foi possível conectar.")
        print("Verifique:")
        print(" - O cabo USB está conectado?")
        print(" - O driver CP210x ou CH340 está instalado?")
        return

    print("\n[2] Conexão estabelecida! Iniciando loop de envio...")
    print("O ESP32 deve reagir a cada 2 segundos.\n")

    # Lista de comandos usando as CONSTANTES reais
    comandos_teste = [
        constants.CMD_FRENTE,
        constants.CMD_ESQUERDA,
        constants.CMD_DIREITA,
        "teste_aleatorio",
        constants.CMD_PARAR
    ]

    try:
        for i, cmd in enumerate(comandos_teste):
            print(f" -> Envio {i+1}/{len(comandos_teste)}: '{cmd}'")
            esp.send(cmd)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário.")

    finally:
        print("\n[3] Finalizando teste.")
        esp.send(constants.CMD_PARAR)
        if esp.ser:
            esp.ser.close()
        print("Conexão fechada.")


if __name__ == "__main__":
    teste_sequencial()
