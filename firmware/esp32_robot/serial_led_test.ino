// --- PINO DO LED INTERNO DO ESP32 ---
#define LED 2  // LED interno (na maioria dos ESP32)

void setup() {
  // Inicia a serial
  Serial.begin(115200);

  // Configura o LED como saída
  pinMode(LED, OUTPUT);

  // Começa desligado
  digitalWrite(LED, LOW);

  Serial.println("ESP32 pronto para teste de LED!");
}

void loop() {

  // Verifica se recebeu comando do Python
  if (Serial.available() > 0) {

    String comando = Serial.readStringUntil('\n');
    comando.trim();

    // Liga o LED
    if (comando == "esquerda") {
      digitalWrite(LED, HIGH);
      Serial.println("LED ligado");
    }

    // Desliga o LED
    else if (comando == "direita") {
      digitalWrite(LED, LOW);
      Serial.println("LED desligado");
    }
  }
}
