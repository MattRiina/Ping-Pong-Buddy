# Ping-Pong-Buddy

An automated ping pong assistant/buddy that will help you improve your game by adapting to your personal needs. It uses a combination of hardware and software to maximize training efficiency.

## Goals
1.	Design and create a basic automated ping pong ball launcher
2.	Allow the user to control the specifications of ball delivery 
3.	Automatic adjustment to ball delivery based on computer vision
4.	Try to make lightweight design of the launcher + user friendly interface

## Installation Instructions
- Download or clone this repository locally
- Create an empty conda environment
```console
conda create --name <NAME>
```
- Activate the conda environment
```console
conda activate <NAME>
```
- Install conda environment requirements from conda-requirements.txt
```console
conda install --file conda-requirements.txt
```
- Install pip requirements from pip-requirements.txt
```console
pip install -r pip-requirements.txt
```
## RaspberryPi Setup Instructions
1.  Obtain Necessary Equipment: RaspberryPi, L298N Motor Controller, 5V DC Motor, Misc Wires
2.  Setup Wiring according to the PingPongBuddy sketch, however if further clarification is needed:  
    - Attatch negative side of battery pack to the 12V port on the L298N and ground to ground
    - Connect L298N ground to RaspberryPi Ground Pin
    - Connect ENA to GPIO 25, IN1 to GPIO 23, and IN2 to GPIO 24
    - Connect L298N OUT1 to Motor(-) and L298N OUT2 to Motor(+)
3.  Flash SD Card with new image in preparation for installation 
4.  Boot the RaspberryPi with SD Card inserted
5.  Using the Raspbian terminal run Ping-Pong-Buddy\src\RaspberryPi\basic_controller.py
6.  Now the motor can be controlled through different commands:
    - r starts the motor at 50 percent power
    - q stops the motor
    - x exits the program and cleans up the GPIO
    - h runs the motor at high which is 80 percent 
    - m runs the motor at medium which is 50 percent
    - l runs the motor at low which is 25 percent
    - 0-100 will run the motor at that percentage(80-100 for sustained periods will burn a 5V DC motor)
## License
This work is licensed under 2 licenses: MIT License and CERN-OHL-P Open Hardware License. The MIT License applies to all software components of the project, and a copy of this license can be found under the src directory. The CERN-OHL-P Open Hardware License applies to all hardware components and engineering design components of the project, which can be found in the engineering-design directory. 
