- Buch zur CAN-Bus Technologie
- CAN-Bus ist ein serielles Bussystem, das ursprünglich für die Automobilindustrie entwickelt wurde
- asynchron
- 2-Draht-Bus
- 1 Master, mehrere Slaves
- 1 Mbit/s
- 11-Bit Identifier oder nach CAN 2.0B 29-Bit Identifier
- 8 Byte Daten
- 3 verschiedene Übertragungsarten: Standard, Remote, Error
- 2 verschiedene Frame-Formate: Standard, Extended
- 2 verschiedene Protokolle: CAN 2.0A, CAN 2.0B
- 2 verschiedene Geschwindigkeiten: High-Speed, Low-Speed

@book{voss2008comprehensible,
  title={A comprehensible guide to controller area network},
  author={Voss, Wilfried},
  year={2008},
  publisher={Copperhill Media}
}

# CAN-Bus Setup für Testings
- 2 UCAN-Boards
- 1 Raspberry Pi mit Raspberry Pi OS (64-bit)
- 1 Laptop mit Arch Linux
- can-utils
- https://canbus.esoterical.online/Getting_Started.html
- https://wiki.fysetc.com/UCAN/
- bitrate zum Testen: 500000

- CanH: Gelbes Kabel
- CanL: Weißes Kabel
- GND: Schwarzes Kabel

- wenn CanBus aufgesetzt ist, dann cansend und candump verwenden
- cansend can0 123#DEADBEEF (123 ist der Identifier, DEADBEEF sind die Daten in Hexadezimal)
- candump can0