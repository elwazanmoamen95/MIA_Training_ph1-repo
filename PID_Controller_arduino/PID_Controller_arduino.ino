#include "PIDController.h"

const int encoderPinA = 2;
const int encoderPinB = 3;
const int motorPWM = 9;

volatile long count_encoder = 0;
double d_time = 0;
unsigned long last_time = 0;
double Speed = 0;
double desired_Speed = 88;                                                               
double PID_speed = 0;
double alpha = 0.13;                                                                       
double filter = 0;                                                                  

PIDController PID(1.0,0.5,0.1);

void setup() {
  // put your setup code here, to run once:
  pinMode(encoderPinA, INPUT);
  pinMode(encoderPinB, INPUT);
  pinMode(motorPWM, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(encoderPinA), READENCODER, RISING);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long time = millis();
  d_time = (time - last_time) / 1000.0;
  if(d_time > 0){
    Speed = speed();
    PID_speed = PID.control(desired_Speed,Speed,d_time);

    filter = alpha * PID_speed + (1 - alpha) * filter;

    filter = constrain(filter, 0, 255);
    analogWrite(motorPWM, filter);
  
    Serial.print("Speed: ");
    Serial.print(PID_speed);
    Serial.print("smoothed_Speed: ");
    Serial.print(filter);
  }
  last_time = time;
  delay(100);
}
void READENCODER(){
  count_encoder++;
}

double speed(){
  static unsigned long last_count = 0;
  long count = count_encoder;
  double speed = ((count - last_count) / 360.0) * 60.0 / d_time;
  last_count = count;

  return speed;
}