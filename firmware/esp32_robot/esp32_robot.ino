// --- DEFINIÇÃO DOS PINOS (Mude conforme sua montagem) ---
// Exemplo usando Driver Ponte H (L298N ou similar)

// Motor A (Esquerda)
#define ENA 13  // PWM (Velocidade)
#define IN1 12
#define IN2 14

// Motor B (Direita)
#define ENB 25  // PWM (Velocidade)
#define IN3 26
#define IN4 27

// Velocidade (0 a 255)
int velocidade = 180; 

void setup() {
  // 1. Inicia a Serial com o MESMO valor do Python (115200)
  Serial.begin(115200);
  
  // 2. Configura pinos como saída
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Garante que começa parado
  parar();
  
  Serial.println("ESP32 Trekking Pronto!");
}

void loop() {
  // Verifica se o Python enviou algo
  if (Serial.available() > 0) {
    
    // Lê a linha inteira até o \n (que o Python manda automaticamente)
    String comando = Serial.readStringUntil('\n');
    
    // Remove espaços em branco extras (trim)
    comando.trim();

    // --- INTERPRETAÇÃO DOS COMANDOS ---
    if (comando == "frente") {
      frente();
    }
    else if (comando == "esquerda") {
      esquerda();
    }
    else if (comando == "direita") {
      direita();
    }
    else if (comando == "parar") {
      parar();
    }
  }
}

// --- FUNÇÕES DE MOVIMENTO ---

void frente() {
  // Motor A Frente
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, velocidade);

  // Motor B Frente
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, velocidade);
}

void esquerda() {
  // Para virar à esquerda, motor A vai para trás, B para frente (Giro no eixo)
  // OU Motor A para e B vai para frente (Curva suave)
  
  // Exemplo: Giro no próprio eixo (Tank Turn)
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH); // Trás
  analogWrite(ENA, velocidade);

  digitalWrite(IN3, HIGH); // Frente
  digitalWrite(IN4, LOW);
  analogWrite(ENB, velocidade);
}

void direita() {
  // Giro no próprio eixo para a direita
  digitalWrite(IN1, HIGH); // Frente
  digitalWrite(IN2, LOW);
  analogWrite(ENA, velocidade);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH); // Trás
  analogWrite(ENB, velocidade);
}

void parar() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}