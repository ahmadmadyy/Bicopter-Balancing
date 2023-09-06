#include <Servo.h>
Servo right_Esc;
Servo left_Esc;
float loopDuration, time, prevDuration;
float u, leftSignal, rightSignal, e, prev_e;
float integralVal=0;
double throttle=1030 ; 

void setup() {
  Serial.begin(115200);
  right_Esc.attach(3); 
  left_Esc.attach(5); 
  time = millis(); 
  left_Esc.writeMicroseconds(1000); 
  right_Esc.writeMicroseconds(1000);
  delay(7000); 
  }

void loop() {
    if (Serial.available() > 0) {
    char num = Serial.read();
    if(num=='A')
    {
      left_Esc.writeMicroseconds(1060);
      delay(3000);
    }
    if(num == 'B')
    {
      right_Esc.writeMicroseconds(1060);
      delay(3000);
    }
    //left_Esc.writeMicroseconds(1060);
    //right_Esc.writeMicroseconds(1065);
   delay(2000);
}
}
