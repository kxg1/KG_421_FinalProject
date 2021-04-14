#include <Adafruit_CircuitPlayground.h>

float X, Y, Z;
bool arm;
#define MOVE_THRESHOLD 50
 
void setup() {
  Serial.begin(9600);
  CircuitPlayground.begin();
}
 
void loop() {
arm = CircuitPlayground.slideSwitch();
Serial.println(arm);
if (arm == 1); { 
  
  //CircuitPlayground.clearPixels();
  X = CircuitPlayground.motionX();
  Y = CircuitPlayground.motionY();
  Z = CircuitPlayground.motionZ();
 
   // Get the magnitude (length) of the 3 axis vector
  double storedVector = X*X;
  storedVector += Y*Y;
  storedVector += Z*Z;
  storedVector = sqrt(storedVector);
  Serial.print("Length: "); Serial.println(storedVector);
  
  // wait a bit
  delay(100);
  
  // get new data
  X = CircuitPlayground.motionX();
  Y = CircuitPlayground.motionY();
  Z = CircuitPlayground.motionZ();
  double newVector = X*X;
  newVector += Y*Y;
  newVector += Z*Z;
  newVector = sqrt(newVector);
  Serial.print("New Length: "); Serial.println(newVector);
  
  // is there movement?
  if (abs(10*newVector - 10*storedVector) > MOVE_THRESHOLD) {
     Serial.println("Alarm");
     CircuitPlayground.playTone(500, 500);
       CircuitPlayground.setPixelColor(0, 255,   0,   0);
  CircuitPlayground.setPixelColor(1, 128, 128,   0);
  CircuitPlayground.setPixelColor(2,   0, 255,   0);
  CircuitPlayground.setPixelColor(3,   0, 128, 128);
  CircuitPlayground.setPixelColor(4,   0,   0, 255);
  
  CircuitPlayground.setPixelColor(5, 0xFF0000);
  CircuitPlayground.setPixelColor(6, 0x808000);
  CircuitPlayground.setPixelColor(7, 0x00FF00);
  CircuitPlayground.setPixelColor(8, 0x008080);
  CircuitPlayground.setPixelColor(9, 0x0000FF);
  delay(500);
  CircuitPlayground.clearPixels();

  
    //delay(1000);
  }
  
 
  delay(100);
}
}
