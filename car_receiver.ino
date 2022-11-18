#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

#define ENGINE_TUNING 2

struct dataPackage {
  byte forward = 0;
  byte backward = 0;
  byte left = 0;
  byte right = 0;
  byte baseServo = 90;
  byte armServo = 90;
  byte armLaser = 0;
};

Servo baseServo, armServo;
int motor1pin1 = 2;
int motor1pin2 = 3;
int motor2pin1 = 4;
int motor2pin2 = 5;

dataPackage datarx;
RF24 radio(7, 8); //CE, CSN
const byte address[6] = "00099";

void safetyReset(){
  datarx.forward = 0;
  datarx.backward = 0;
  datarx.left = 0;
  datarx.right = 0;
}

void stopEngines(){
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}

void moveForward(){
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

  delay(ENGINE_TUNING);
  stopEngines();
}

void moveBackward(){
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

  delay(ENGINE_TUNING);
  stopEngines();
}

void rotateLeft(){
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

  delay(ENGINE_TUNING);
  stopEngines();
}

void rotateRight(){
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

  delay(ENGINE_TUNING);
  stopEngines();
}

void turnLeft(){
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

  delay(ENGINE_TUNING);
  stopEngines();
}

void turnRight(){
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

  delay(ENGINE_TUNING);
  stopEngines();
}

void setup() {
  Serial.begin(115200);

  //Engine
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
  stopEngines();

  //Servos
  baseServo.attach(6);
  armServo.attach(9);

  //Laser
  pinMode(A3, OUTPUT);

  //NRF
  radio.begin();
  radio.openReadingPipe(0, address); // 00002
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening();
}

unsigned long resetTimer = 0, targetResetTime = 0;
void loop() {
  //Motors
  if (datarx.forward){
    if(datarx.left){
      turnLeft();
    }
    else if (datarx.right){
      turnRight();
    }
    else{
      moveForward();
    }
  }
  else if(datarx.backward){
    if(datarx.left){
      turnLeft();
    }
    else if (datarx.right){
      turnRight();
    }
    else{
      moveBackward();
    }
  }
  else if (datarx.left){
    rotateLeft();
  }
  else if (datarx.right){
    rotateRight();
  }
  else{
    stopEngines();
  }

  digitalWrite(A3, datarx.armLaser);
  
  //Servos
  baseServo.write(datarx.baseServo);
  armServo.write(datarx.armServo);

  if (radio.available()) {
    resetTimer = millis();
    targetResetTime = resetTimer + 25;
    radio.read(&datarx, sizeof(dataPackage));
  }
  else{
    if (resetTimer > targetResetTime){
      safetyReset();
    }
  }

  delay(5);
}
