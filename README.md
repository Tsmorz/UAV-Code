# UAV-Code

This program helps streamline the initial design phase when creating tiltrotor aircraft.\

Edit this file to your chosen airfoil and a/c dimensions:
```
inputs.csv
```
Specific data to the aircraft like mass, wingspan, coefficient of lift, etc
```
ReadInputs.py
```
GenerativeDesign.py - main fuction that puts everything together\
AeroDrag.py - skin friction, form, and induced drag calculations\
Hover.py - power and energy requirements from hovering flight\
Structures.py - Euler beam theory and associated equations\
WingCalculations.py - iterative process to reduce wing mass\
UAVdesign.py - miscellaneous calculations and tradeoffs
