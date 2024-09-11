# include "PIDController.h"

PIDController::PIDController(double p,double i,double d) : Kp(p), Ki(i), Kd(d), last_error(0), summation(0) {}
        
double PIDController::control(double goal, double current, double d_time ) {
  double error = goal - current;
  summation += error * d_time;
  double derivative = (error - last_error)/d_time;
  double result = (Kp * error)+(Ki * summation)+(Kd * derivative);
  last_error = error;

  return result;
}

