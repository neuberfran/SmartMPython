import time
import os, sys
# import SmartDrive class from SmartDrive Library
from SmartDrive import SmartDrive

# Define run variables
SmartDrive = SmartDrive()
speed = 100
duration = 10
degrees = 720
rotations = 2
tacho = 1080
test = 1


# Reset encoder values
SmartDrive.command(SmartDrive.R) 

# Infinite loop
while test == 1:
    
    # Read input battery voltage
    print "Batt: " + str(SmartDrive.GetBattVoltage())
    
    # Read encoder values 
    print "Tach1: " + str(SmartDrive.ReadTachometerPosition(SmartDrive.SmartDrive_Motor_1))
    print "Tach2: " + str(SmartDrive.ReadTachometerPosition(SmartDrive.SmartDrive_Motor_2))
    
    # Run motor for an unlimited time. Uncomment the following line to run the motor for unlimited amount of time
#    SmartDrive.SmartDrive_Run_Unlimited(SmartDrive.SmartDrive_Motor_1, SmartDrive.SmartDrive_Direction_Forward, speed)
    #time.sleep(10)
    
    # Stops the motor. Uncomment the following line to stop the motor.
    #SmartDrive.SmartDrive_Stop(SmartDrive.SmartDrive_Motor_1, SmartDrive.SmartDrive_Next_Action_Brake)
    
    # Runs motor for a specific time determined by the "seconds" variable. Uncomment following line to run for specific amount of time
    #SmartDrive.SmartDrive_Run_ SmartDrive.SmartDrive_Run_Unlimited(SmartDrive.SmartDrive_Motor_1, SmartDrive.SmartDrive_Direction_Forward, speed)
    SmartDrive.SmartDrive_Run_Seconds(SmartDrive.SmartDrive_Motor_1, SmartDrive.SmartDrive_Direction_Forward, speed, duration, SmartDrive.SmartDrive_Completion_Wait_For, SmartDrive.SmartDrive_Next_Action_BrakeHold)   
    
    # Runs motor for a specific amount of degrees determined by the "degrees" variable. Uncomment following line to run for a specific number of degrees
    #SmartDrive.SmartDrive_Run_Degrees(SmartDrive.SmartDrive_Motor_1, SmartDrive.SmartDrive_Direction_Forward, speed, degrees, SmartDrive.SmartDrive_Completion_Wait_For, SmartDrive.SmartDrive_Next_Action_Brake)
    
    # Runs motor for a specific amount of rotations determined by the "rotations" variable. Uncomment following line to run for a specific number of rotations 
    #SmartDrive.SmartDrive_Run_Rotations(SmartDrive.SmartDrive_Motor_1, SmartDrive.SmartDrive_Direction_Reverse, speed, rotations, SmartDrive.SmartDrive_Completion_Wait_For, SmartDrive.SmartDrive_Next_Action_Brake)
    
    # Runs motor to a specific encoder value determined by "tacho" variable. Uncomment following line to run motor to a specific encoder value.
    #SmartDrive.SmartDrive_Run_Tacho(SmartDrive.SmartDrive_Motor_1, speed, tacho, SmartDrive.SmartDrive_Completion_Wait_For, SmartDrive.SmartDrive_Next_Action_Brake)
    #time.sleep(1)
    
    test = test + 1