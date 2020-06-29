import RPi.GPIO as GPIO
class servo:
    def __init__(self):
        # duty cycle limits for servos, these should be adjusted for specific position of your servos once connected to gimbal
        self.limit = {'x': {'max': 4.5, 'med': 2.9, 'min': 2}, 'y': {'max': 11.9, 'med': 7.9, 'min': 5.5}}
        self.maxAngle = {'x': 8.0, 'y': 17.0}

        self.servoXpin = 11
        self.servoYpin = 13        
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servoXpin, GPIO.OUT)
        GPIO.setup(self.servoYpin, GPIO.OUT)

        self.servoX = GPIO.PWM(self.servoXpin, 50)
        self.servoY = GPIO.PWM(self.servoYpin, 50)

        self.servoX.start(self.limit['x']['med'])
        self.servoY.start(self.limit['y']['med'])

        GPIO.output(self.servoYpin, True)   
        GPIO.output(self.servoXpin, True)

 
    def moveServo(self, angleX, angleY):
        self.servoX.ChangeDutyCycle(self.angleToDutyCycle(angleX, 'x'))
        self.servoY.ChangeDutyCycle(self.angleToDutyCycle(angleY, 'y'))

    def angleToDutyCycle(self, angle, axis):
        dutyCycle = 0 
    
        if angle > 0: 
            if angle > self.maxAngle[axis]:
                dutyCycle = self.limit[axis]['max']
            else:
                dutyCycle = (angle / self.maxAngle[axis]) * (self.limit[axis]['max'] - self.limit[axis]['med']) + self.limit[axis]['med']
        else:
            if angle < -1 * self.maxAngle[axis]:
                dutyCycle = self.limit[axis]['min']
            else: 
                dutyCycle = (angle / self.maxAngle[axis]) * (self.limit[axis]['med'] - self.limit[axis]['min']) + self.limit[axis]['med']
        
        return dutyCycle
