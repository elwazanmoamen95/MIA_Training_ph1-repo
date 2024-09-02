#include <Wire.h>

#define MPU6050_ADDR 0x68
#define PWR_MGMT_1 0x6B
#define GYRO_CONFIG 0x1B
#define GYRO_ZOUT_H 0x47
#define ACCEL_XOUT_H 0x3B
#define ACCEL_YOUT_H 0x3D
#define ALPHA 0.98

float accelX, accelY;
float gyroZ;
float yaw = 0.0;
float dt = 0.01;  // time step
float gyroZ_offset = 0.0;
unsigned long previousTime;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Wake up MPU6050
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(PWR_MGMT_1);
  Wire.write(0);
  Wire.endTransmission();

  setGyroRange();
  calibrateGyro();
  
  previousTime = millis();
}

void loop() {
  unsigned long currentTime = millis();
  dt = (currentTime - previousTime) / 1000.0;
  previousTime = currentTime;

  readMPU6050Data();

  float accelAngleZ = atan2(accelY, accelX) * 180 / PI; 

  yaw = ALPHA * ((gyroZ - gyroZ_offset) * dt) + (1.0 - ALPHA) * accelAngleZ;

  Serial.print("Yaw: ");
  Serial.println(yaw);
  delay(10);
}

void readMPU6050Data() {
  // Read accelerometer X and Y data
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(ACCEL_XOUT_H);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 4, true); 
  accelX = (Wire.read() << 8 | Wire.read()) / 16384.0;
  accelY = (Wire.read() << 8 | Wire.read()) / 16384.0;

  // Read gyroscope Z data
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(GYRO_ZOUT_H);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 2, true); 
  gyroZ = (Wire.read() << 8 | Wire.read()) / 131.0;
}

void calibrateGyro() {
  int numReadings = 1000;
  float sum = 0;

  for (int i = 0; i < numReadings; i++) {
    readMPU6050Data();
    sum += gyroZ;
    delay(3); 
  }
  gyroZ_offset = sum / numReadings; //avg offset
}

void setGyroRange() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(GYRO_CONFIG);
  Wire.write(0x00); // ±250°/s
  Wire.endTransmission();
}
