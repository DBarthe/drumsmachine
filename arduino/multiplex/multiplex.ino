
// =============== ANALOG MULTIPLEXING ============
const int analogPin = A0;

const int numSelectPins = 4;
const int selectPins[] = {2,3,4,5};
const int delayAfterSelect = 15;

const int numInputs = 6;
const int toleranceDelta = 2;
int inputValues[] = {0,0,0,0,0,0};
int changesBitmap = 0x11F;

void analogmuxSetup() {
  for (int i = 0; i < numSelectPins; i++) {
    pinMode(selectPins[i], OUTPUT);
  }
}

int selectInput(int index) {
  for (int i = 0; i < numSelectPins; i++) {
    digitalWrite(selectPins[i], (index & 1) ? HIGH : LOW);
    index >>= 1;
  }
}

int readInput(int index) {
  selectInput(index);
  delay(delayAfterSelect);
  return analogRead(analogPin);
}

void refresh() {
  for (int i = 0; i < numInputs; i++) {
    int newValue = readInput(i);
    if (abs(newValue - inputValues[i]) >= toleranceDelta) {
      inputValues[i] = newValue;
      changesBitmap |= (1 << i);
    }
  }
}

void printChanges() {
  int changesCopy = changesBitmap;
  for (int i = 0; i < numInputs; i++) {
    if (changesCopy & 1) {
      Serial.print(i);Serial.print(" = ");Serial.println(inputValues[i]);       
    }
    changesCopy >>= 1;
  }
}

void flushChanges() {
  changesBitmap = 0x0;
}

// =============== ETHERNET, UDP and OSC ===================
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>
#include <OSCBundle.h>

EthernetUDP Udp;
IPAddress ip(10, 0, 0, 3); // local ip
IPAddress outIp(10, 0, 0, 2); // remote ip
const unsigned int outPort = 9999; // remote osc port
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

void ethernetSetup() {
  Ethernet.begin(mac,ip);
  Udp.begin(8888); // random source port
}

// "/pot/x" (works for less than 10 analog input)
char addrBuffer[7] = "/pot/x";
void sendChangesOverOsc() {

  if (changesBitmap == 0) {
    return ;
  }

  OSCBundle bundle;
  for (int i = 0; i < numInputs; i++) {
    if (changesBitmap & 1) {
      addrBuffer[5] = '0' + (int8_t)i;
      bundle.add(addrBuffer).add((int32_t)inputValues[i]);
    }
    changesBitmap >>= 1;
  }
  
  Udp.beginPacket(outIp, outPort);
  bundle.send(Udp);
  Udp.endPacket();
  bundle.empty();
}

// =============== MAIN ===================

void setup() {
  analogmuxSetup();
  ethernetSetup();
  Serial.begin(9600);
}

void loop() {
  refresh();
  sendChangesOverOsc();
  // delay(50);
}
