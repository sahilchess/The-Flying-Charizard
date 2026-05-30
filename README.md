# The Flying Charizard ✈️🔥

A custom STM32-based flight controller PCB with Charizard-themed artwork etched into the board layers.

## Overview

The Flying Charizard is a fully custom PCB designed around the **STM32F722RETx** microcontroller for flight control applications.  
It combines practical avionics hardware with Pokémon-inspired PCB art across copper and silkscreen layers.

## Features

- STM32 microcontroller (**STM32F722RETx**)
- USB-C power and communication
- Battery charge management (**RA9357RNER**)
- Buck-boost converter (**TPS63070RNNR**) for stable power delivery
- Barometric pressure sensor (**BMP390**)
- Accelerometer / gyroscope (**KN-45696**) for IMU
- Dual crystal oscillators
- SD card interface
- 2x servo headers
- Reset and boot buttons
- LiPo battery connector (BAT+)
- Custom Charizard copper art across F.Cu and B.Cu layers

## Schematic Sections

| Block | Component |
|---|---|
| MCU | STM32F722RETx |
| USB-C | TYPE-C 16PIN 2MD |
| Pressure Sensor | BMP390 |
| IMU | KN-45696 (Accel/Gyro) |
| Battery Charger | RA9357RNER |
| Buck-Boost | TPS63070RNNR |
| Power Switch | LM951130 |
| SD Card | OLA-Z2869250 |

## PCB

Designed in **KiCad** as a **2-layer board** with Charizard artwork embedded in copper pours and silkscreen.

The artwork includes:
- Charizard
- Dragonite
- Charmander
- Mega Charizard X

## Gallery

### Schematic
![Flying Charizard Schematic](https://github.com/user-attachments/assets/e8cedde8-4e2f-497d-a7bc-f2348ae0f9e5)

### PCB / Artwork
![Flying Charizard Image 2](https://github.com/user-attachments/assets/c17d0629-d628-4ca1-aa61-8ae5192a36dd)
![Flying Charizard Image 3](https://github.com/user-attachments/assets/3bd425a6-6317-418f-bb13-c0635d95ccf1)
![Flying Charizard Image 4](https://github.com/user-attachments/assets/5f8d3567-23b5-46ab-8119-b7c7b759da8f)

## Getting Started

1. Clone this repository.
2. Open `hardware/The Flying Charizard.kicad_pro` in KiCad.
3. Generate/export Gerbers from KiCad for fabrication output.

## Author

[@Sahild](https://github.com/Sahild)
