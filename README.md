# Edilkamin_Remote
Python Code to control Edilkamin pellet stuve (Tiny)

This Python code runs on a raspberry pi with SPI enabled.

It uses the CYRF6936 Chip which seems obsolete :(

I have used this kind of board with some modifications for SPI...
"CC2500 NRF24L01 A7105 CYRF6936 4 In 1 RF Module"

The code has been modified to work through node-red with a deamon block to rx/tx data through stdin/out

There are some unknown parameters still, example is the temperature is not decoded...

However i will use the oven in manual mode, and i can parse the 5 levels of power and i can controll all the buttons.

To-Do is to turn on/off the owen.



