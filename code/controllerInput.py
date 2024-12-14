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
            if xboxController.get_button(4) == 1 and xboxController.get_button(5) == 1 and xboxController.get_button(1) == 1:
                backwards = not backwards
                throttleR = 0
                throttleL = 0
                print("Backwards: {}".format(backwards))
                if backwards:
                    print("Der Rückwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    pygame.event.clear()
                elif not backwards:
                    print("Der Vorwärtsgang wird eingelegt, bitte warten...")
                    sleep(10)
                    pygame.event.clear()
#        elif event.type == pygame.JOYAXISMOTION:
#            print("Axis: {}".format(event.axis))
#            print("Axis: {}".format(event.value))
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
    if (xboxController.get_axis(4) > -0.9 or xboxController.get_button(4) == 1):
        # Achse 4 muss normalisiert werden, da sie bei -1 anfängt und bei 1 aufhört -> soll bei 0 anfangen und bis 1 gehen
        normalisedAxisL = (xboxController.get_axis(4) + 1) / 2
        throttleL += normalisedAxisL * (1/(2*fps)) # bei 2 Sekunden soll der Throttle-Wert 1 betragen, wenn Trigger vollständig gedrückt ist
        throttleL -= xboxController.get_button(4) * (1/(2*fps))
        if throttleL > 1:
            throttleL = 1
        if throttleL < 0:
            throttleL = 0
        print("Throttle Left: {}".format(throttleL))

    # Throttle Right
    if (xboxController.get_axis(5) > -0.9 or xboxController.get_button(5) == 1):
        # Achse 4 muss normalisiert werden, da sie bei -1 anfängt und bei 1 aufhört -> soll bei 0 anfangen und bis 1 gehen
        normalisedAxisR = (xboxController.get_axis(5) + 1) / 2
        throttleR += normalisedAxisR * (1/(2*fps)) # bei 2 Sekunden soll der Throttle-Wert 1 betragen, wenn Trigger vollständig gedrückt ist
        throttleR -= xboxController.get_button(5) * (1/(2*fps))
        if throttleR > 1:
            throttleR = 1
        if throttleR < 0:
            throttleR = 0
        print("Throttle Right: {}".format(throttleR))

    # Backwards
    clock.tick(fps)
    

# To-Do: Bedien-Logik implementieren