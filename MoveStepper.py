from ESP32RestSerialAPI import ESP32Client
import time

steps = 1000

#perform a lateral shift in the x direction
serialport1 = 'COM8'
Motor = ESP32Client(serialport=serialport1)
#Motor.move_stepper(steps=(10, -10, 0), speed=100, is_absolute=False, is_blocking=True)

#.move_stepper((2000, 0, 0), speed=100, is_absolute=False, is_blocking=True)
#Motor.move_stepper(steps=(10, 0, 0), speed=100, is_absolute=False, is_blocking=True)
#time.sleep(2)
print("Move in X")

Motor.move_stepper(steps=(0, 1000, 0), speed=200, is_absolute=False, is_blocking=True)

#Motor.move_stepper(steps=(1000, -1000, 0), speed=100, is_absolute=False, is_blocking=True)

#print("Move in Y")
#Motor.move_stepper(steps=(0, 2000, 0), speed=100, is_absolute=False, is_blocking=True)
print("Move in -X")
#Motor.move_stepper(steps=(+4000, 0, 0), speed=100, is_absolute=False, is_blocking=True)
#print("Move in -Y")
#Motor.move_stepper(steps=(0, -2000, 0), speed=100, is_absolute=False, is_blocking=True)

'''
print("Move in Y")
Motor.move_stepper((0, 2000, 0), speed=100, is_absolute=False, is_blocking=True)

print("Move in -X")
Motor.move_stepper((-2000, 0, 0), speed=100, is_absolute=False, is_blocking=True)

print("Move in -Y")
Motor.move_stepper((0, -2000, 0), speed=100, is_absolute=False, is_blocking=True)
'''

'''
Motor.move_stepper(axis=1, steps=-steps, speed=100, is_absolute=False, is_blocking=True)
print("Move in X")
#time.sleep(max(6, 3*steps//1000))

Motor.move_stepper(axis=2, steps=+steps, speed=100, is_absolute=False, is_blocking=True)
print("Move in y")
#time.sleep(max(6, 3*steps//1000))

Motor.move_stepper(axis=1, steps=+steps, speed=100, is_absolute=False, is_blocking=True)
print("Move in X")
#time.sleep(max(6, 3*steps//1000))

Motor.move_stepper(axis=2, steps=-steps, speed=100, is_absolute=False, is_blocking=True)
print("Move in y")
#time.sleep(max(6, 3*steps//1000))
'''