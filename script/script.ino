#include <AccelStepper.h>
#include <Servo.h>

//m - motor
//1..10 - number
//e - end pin
//d - direction pin
//en - enable
boolean done_flag = true;
boolean debug = false;
byte m1e = 2;
byte m2e = 3;
byte m3e = 4;
byte m4e = 5;
byte m5e = 6;
byte m6e = 7;
byte m7e = 8;
byte m8e = 9;
byte m9e = 10;
byte m10e = 11;

byte m1en = 22;
byte m2en = 25;
byte m3en = 28;
byte m4en = 31;
byte m5en = 34;
byte m6en = 37;
byte m7en = 40;
byte m8en = 43;
byte m9en = 46;
byte m10en = 49;

byte m1d = 23;
byte m2d = 26;
byte m3d = 29;
byte m4d = 32;
byte m5d = 35;
byte m6d = 38;
byte m7d = 41;
byte m8d = 44;
byte m9d = 47;
byte m10d = 50;

AccelStepper m1(1, 24, m1d);
AccelStepper m2(1, 27, m2d);
AccelStepper m3(1, 30, m3d);
AccelStepper m4(1, 33, m4d);
AccelStepper m5(1, 36, m5d);
AccelStepper m6(1, 39, m6d);
AccelStepper m7(1, 42, m7d);
AccelStepper m8(1, 45, m8d);
AccelStepper m9(1, 48, m9d);
AccelStepper m10(1, 51, m10d);

void setup() {
  Serial.begin(250000);
  Serial.println("done");
  pinMode(m1en,OUTPUT);
  pinMode(m2en,OUTPUT);
  pinMode(m3en,OUTPUT);
  pinMode(m4en,OUTPUT);
  pinMode(m5en,OUTPUT);
  pinMode(m6en,OUTPUT);
  pinMode(m7en,OUTPUT);
  pinMode(m8en,OUTPUT);
  pinMode(m9en,OUTPUT);
  pinMode(m10en,OUTPUT);
  
  pinMode(m1e,INPUT);
  pinMode(m2e,INPUT);
  pinMode(m3e,INPUT);
  pinMode(m4e,INPUT);
  pinMode(m5e,INPUT);
  pinMode(m6e,INPUT);
  pinMode(m7e,INPUT);
  pinMode(m8e,INPUT);
  pinMode(m9e,INPUT);
  pinMode(m10e,INPUT);

  enableMotors();
//  disableMotors();
}

void enableMotors(){
  digitalWrite(m1en,0);
  digitalWrite(m2en,0);
  digitalWrite(m3en,0);
  digitalWrite(m4en,0);
  digitalWrite(m5en,0);
  digitalWrite(m6en,0);
  digitalWrite(m7en,0);
  digitalWrite(m8en,0);
  digitalWrite(m9en,0);
  digitalWrite(m10en,0);
}


void disableMotors(){
  digitalWrite(m1en,1);
  digitalWrite(m2en,1);
  digitalWrite(m3en,1);
  digitalWrite(m4en,1);
  digitalWrite(m5en,1);
  digitalWrite(m6en,1);
  digitalWrite(m7en,1);
  digitalWrite(m8en,1);
  digitalWrite(m9en,1);
  digitalWrite(m10en,1);
}

void loop() {
  checkDestination();
  m1.run();
  m2.run();
  m3.run();
  m4.run();
  m5.run();
  m6.run();
  m7.run();
  m8.run();
  m9.run();
  m10.run();
}
