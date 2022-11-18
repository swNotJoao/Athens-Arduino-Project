#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

String receivedDataFromPython;
const int parsedDataSize = 7;
int parsedPythonData[parsedDataSize];
const char charToSplitOn = ',';

struct dataPackage {
  byte forward = 0;
  byte backward = 0;
  byte left = 0;
  byte right = 0;
  byte baseServo = 90;
  byte armServo = 90;
  byte armLaser = 0;
};

dataPackage dataTx;
RF24 radio(7, 8); //CE, CSN
const byte address[6] = "00099";


/**
 * This method uses the String receivedDataFromPython to update the int array parsedPythonData.
 * This gets done by splitting the receivedDataFromPython by the char charToSplitOn.
 * This method expects the String receivedDataFromPython to have exactly a parsedDataSize amount of (charToSplitOn - 1) characters.
 */
void parsePythonData() {
  String currentBuildString = String("");
  int counter = 0;
  for (int i = 0; i < receivedDataFromPython.length(); i++) {
    if (receivedDataFromPython.charAt(i) == charToSplitOn) {
      parsedPythonData[counter] = currentBuildString.toInt();
      counter += 1;
      currentBuildString = "";
    } else {
      currentBuildString += receivedDataFromPython.charAt(i);
    }
  }
  parsedPythonData[counter] = currentBuildString.toInt();
}


/**
 * This method uses the int array parsedPythonData to update the dataPackage dataTx.
 */
void updateDataTx() {
  dataTx.forward = parsedPythonData[0];
  dataTx.backward = parsedPythonData[1];
  dataTx.left = parsedPythonData[2];
  dataTx.right = parsedPythonData[3];
  dataTx.baseServo = parsedPythonData[4];
  dataTx.armServo = parsedPythonData[5];
  dataTx.armLaser = parsedPythonData[6];
}

void sendRadioData() {
  radio.write(&dataTx, sizeof(dataPackage));
}


/**
 * This method first parses the String receivedDataFromPython to then update the dataPackage dataTx.
 */
void handleReceivedPythonData() {
  parsePythonData();
  updateDataTx();
  sendRadioData();
}

void sendCurrentDataPacketToPython() {
  Serial.println(dataTx.forward);
  Serial.println(dataTx.backward);
  Serial.println(dataTx.left);
  Serial.println(dataTx.right);
  Serial.println(dataTx.baseServo);
  Serial.println(dataTx.armServo);
  Serial.println(dataTx.armLaser);
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX);
  radio.stopListening();
}


void loop() {
  while (Serial.available() < (parsedDataSize + parsedDataSize));
  delay(5); // to get make sure the full data is received
  receivedDataFromPython = Serial.readString();
  handleReceivedPythonData();
  sendCurrentDataPacketToPython();  // received data getting send back to python
}
