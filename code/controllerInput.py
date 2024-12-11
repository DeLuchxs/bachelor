import pygame
from time import sleep

pygame.init()

joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()


# Print the joystick's name
if len(joysticks) == 0:
    print("Kein Controller gefunden")
else:
    print("Controller verbunden: {}".format(joysticks[0].get_name()))

while True and len(joysticks) > 0:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button: {}".format(event.button))
        elif event.type == pygame.JOYAXISMOTION:
            print("Axis: {}".format(event.axis))
        elif event.type == pygame.JOYHATMOTION:
            print("Hat: {}".format(event.value))
        sleep(0.1)  # Delay to not spam the console

# To-Do: Bedien-Logik implementieren
