import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import platform
import sys
from time import sleep


pygame.init()

throttleL = 0
previousThrottleL = 0
throttleR = 0
previousThrottleR = 0
rudderAngle = 0
previousRudderAngle = 0
backwardsL = False
backwardsR = False
running = True
clock = pygame.time.Clock()
fps = 60

# Controller-Buttons mapped to Xbox-Controller on Windows
stickL = 0 # Left Stick (Axis 0)
buttonB = 1
buttonLB = 4
buttonRB = 5
triggerLT = 4
triggerRT = 5

# Windows: LB = 4, RB = 5, B = 1, Linux: LB = 6, RB = 7, B = 1
# Windows: LT = 5 LB = 4, Linux: LT = 4 LB = 6
# Achsen 4 und 5 sind auf Linux und Windows jeweils vertauscht
if platform.system() == "Linux":
    buttonLB = 6
    buttonRB = 7
    triggerLT = 5
    triggerRT = 4

joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

# Function to rumble the controller when an axis is at maximum or minimum
def rumbleAtMaximum():
    xboxController.rumble(0.2, 0.2, 100)
    pygame.time.delay(200)
    xboxController.rumble(0.2, 0.2, 100)
    return

# Print the joystick's name
if len(joysticks) == 0:
    print("Kein Controller gefunden")
else:
    print("Controller verbunden ({})".format(joysticks[0].get_name()))
    xboxController = joysticks[0]

while running and len(joysticks) > 0:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if xboxController.get_button(buttonLB) == 1 and xboxController.get_button(buttonRB) == 1 and xboxController.get_button(buttonB) == 1: 
                backwardsL = not backwardsR
                backwardsR = not backwardsR
                throttleR = 0
                throttleL = 0
                print("throttleL: {}".format(throttleL))
                print("throttleR: {}".format(throttleR))
                print("backwardsL: {}".format(backwardsL))
                print("backwardsR: {}".format(backwardsR))
                sys.stdout.flush()
                if backwardsR:
                    print("Der Rückwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    print("Der Rückwärtsgang wurde eingelegt")
                    pygame.event.clear()
                elif not backwardsR:
                    print("Der Vorwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    print("Der Vorwärtsgang wurde eingelegt")
                    pygame.event.clear()
            elif xboxController.get_button(buttonLB) == 1 and xboxController.get_button(buttonB) == 1:
                backwardsL = not backwardsL
                throttleL = 0
                print("throttleL: {}".format(throttleL))
                print("backwardsL: {}".format(backwardsL))
                sys.stdout.flush()
                if backwardsR:
                    print("Der linke Rückwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    print("Der linke Rückwärtsgang wurde eingelegt")
                    pygame.event.clear()
                elif not backwardsR:
                    print("Der linke Vorwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    print("Der linke Vorwärtsgang wurde eingelegt")
                    pygame.event.clear()
            elif xboxController.get_button(buttonRB) == 1 and xboxController.get_button(buttonB) == 1:
                backwardsR = not backwardsR
                throttleR = 0
                print("throttleR: {}".format(throttleR))
                print("backwardsR: {}".format(backwardsR))
                sys.stdout.flush()
                if backwardsR:
                    print("Der rechte Rückwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    print("Der rechte Rückwärtsgang wurde eingelegt")
                    pygame.event.clear()
                elif not backwardsR:
                    print("Der rechte Vorwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    print("Der rechte Vorwärtsgang wurde eingelegt")
                    pygame.event.clear()

#        elif event.type == pygame.JOYAXISMOTION:
#            print("Axis: {}".format(event.axis))
#            print("Axis: {}".format(event.value))
        #elif event.type == pygame.JOYHATMOTION:
            #print("Hat: {}".format(event.value))
    
    # Rudder Angle
    if (xboxController.get_axis(0) < -0.1 or xboxController.get_axis(0) > 0.1):
        rudderAngle += xboxController.get_axis(0) * (1/(2*fps)) # 2*fps, damit wenn der Joystick ganz nach links/rechts gedrückt ist, der Ruderwinkel innerhalb 2 Sekunden bei spezifizierten FPS 1 beträgt
        if (previousRudderAngle < 0 and rudderAngle >= 0) or (previousRudderAngle > 0 and rudderAngle <= 0):
            xboxController.rumble(0.2, 0.2, 100)
        elif (previousRudderAngle < 0.5 and rudderAngle >= 0.5) or (previousRudderAngle > 0.5 and rudderAngle <= 0.5):
            rumbleAtMaximum()
        elif (previousRudderAngle < -0.5 and rudderAngle >= -0.5) or (previousRudderAngle > -0.5 and rudderAngle <= -0.5):
            rumbleAtMaximum()
        elif rudderAngle > 1:
            rudderAngle = 1
            rumbleAtMaximum()
        elif rudderAngle < -1:
            rudderAngle = -1
            rumbleAtMaximum()
        previousRudderAngle = rudderAngle
        print("rudderAngle: {}".format(rudderAngle))
        sys.stdout.flush()
         
    # Throttle Left
    if (xboxController.get_axis(triggerLT) > -0.9 or xboxController.get_button(buttonLB) == 1): 
        # Achse 4 muss normalisiert werden, da sie bei -1 anfängt und bei 1 aufhört -> soll bei 0 anfangen und bis 1 gehen
        normalisedAxisL = (xboxController.get_axis(triggerLT) + 1) / 2
        throttleL += normalisedAxisL * (1/(20*fps)) # bei 20 Sekunden soll der Throttle-Wert 1 betragen, wenn Trigger vollständig gedrückt ist
        throttleL -= xboxController.get_button(buttonLB) * (1/(2*fps))
        #if throttle passes treshold 0.5, rumble
        if (previousThrottleL < 0.5 and throttleL >= 0.5) or (previousThrottleL > 0.5 and throttleL <= 0.5):
            xboxController.rumble(0.2, 0.2, 100)
        elif throttleL > 0.25:
            throttleL = 0.25
            rumbleAtMaximum()
        elif throttleL < 0:
            throttleL = 0
            rumbleAtMaximum()
        previousThrottleL = throttleL
        print("throttleL: {}".format(throttleL))
        sys.stdout.flush()

    # Throttle Right
    if (xboxController.get_axis(triggerRT) > -0.9 or xboxController.get_button(buttonRB) == 1): #Windows: RT = 5 RB = 5, Linux: RT = 4 RB = 7 
        # Achse 4 muss normalisiert werden, da sie bei -1 anfängt und bei 1 aufhört -> soll bei 0 anfangen und bis 1 gehen
        normalisedAxisR = (xboxController.get_axis(triggerRT) + 1) / 2
        throttleR += normalisedAxisR * (1/(20*fps)) # bei 20 Sekunden soll der Throttle-Wert 1 betragen, wenn Trigger vollständig gedrückt ist
        throttleR -= xboxController.get_button(buttonRB) * (1/(2*fps))
        #if throttle passes treshold 0.5, rumble
        if (previousThrottleR < 0.5 and throttleR >= 0.5) or (previousThrottleR > 0.5 and throttleR <= 0.5):
            xboxController.rumble(0.2, 0.2, 100)
        elif throttleR > 0.25:
            throttleR = 0.25
            rumbleAtMaximum()
        elif throttleR < 0:
            throttleR = 0
            rumbleAtMaximum()
        previousThrottleR = throttleR
        print("throttleR: {}".format(throttleR))
        sys.stdout.flush()
    clock.tick(fps)

