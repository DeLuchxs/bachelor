import pygame
from time import sleep

pygame.init()

throttleL = 0
throttleR = 0
rudderAngle = 0
backwards = False
running = True
clock = pygame.time.Clock()
fps = 60

joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()


# Print the joystick's name
if len(joysticks) == 0:
    print("Kein Controller gefunden")
else:
    print("Controller verbunden: {}".format(joysticks[0].get_name()))
    xboxController = joysticks[0]

while running and len(joysticks) > 0:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button: {}".format(event.button))
#        elif event.type == pygame.JOYAXISMOTION and event.axis == 0:
#           print("Axis: {}".format(event.value))
        elif event.type == pygame.JOYHATMOTION:
            print("Hat: {}".format(event.value))
    
    # Rudder Angle
    if (xboxController.get_axis(0) < -0.1 or xboxController.get_axis(0) > 0.1):
        rudderAngle += xboxController.get_axis(0) * (1/(2*fps)) # 2*fps, damit wenn der Joystick ganz nach links/rechts gedrückt ist, der Ruderwinkel innerhalb 2 Sekunden bei spezifizierten FPS 1 beträgt
        if rudderAngle > 1:
            rudderAngle = 1
        elif rudderAngle < -1:
            rudderAngle = -1
        print("Rudder: {}".format(rudderAngle))
         
    # Throttle Left
    if (xboxController.get_axis(4) > 0.1 or xboxController.get_button(4) == 1) and not backwards:
        throttleL += xboxController.get_axis(4) * (1/(2*fps)) # bei 2 Sekunden soll der Throttle-Wert 1 betragen, wenn Trigger vollständig gedrückt ist
        print(format(xboxController.get_axis(4)))   # Deadzone-Test: Axis fängt bei -1 an und geht bis 1 -> soll bei 0 anfangen und bis 1 gehen
        throttleL -= xboxController.get_button(4) * (1/(2*fps))
        if throttleL > 1:
            throttleL = 1
        if throttleL < 0:
            throttleL = 0
        print("Throttle Left: {}".format(throttleL))
    clock.tick(fps)
    

# To-Do: Bedien-Logik implementieren