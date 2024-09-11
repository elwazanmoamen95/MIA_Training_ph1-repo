#ifndef PIDCONTROLLER_H
#define PIDCONTROLLER_H

class PIDController {
    private:
        double Kp, Ki, Kd;
        double last_error;
        double summation;

    public:
        PIDController(double p, double i, double d);
        double control(double goal, double current, double d_time);
};

#endif