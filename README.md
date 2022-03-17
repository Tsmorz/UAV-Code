# UAV-Code

This program helps streamline the initial design phase when creating tiltrotor aircraft. This type of a/c helps fill the need for efficient cargo carring drones that can operate without a runway and/or landing strip.
<img src="https://user-images.githubusercontent.com/83112082/158711492-ad390191-10b6-4bf6-add6-52dd5bcf30c0.jpg" width="80%" height="80%">

## Using the program
Edit this file to your chosen airfoil and a/c dimensions:
```
inputs.csv
```
Main fuction that puts everything together:
```
$ python GenerativeDesign.py
```

  - ReadInputs.py - Specific data to the aircraft like mass, wingspan, coefficient of lift, etc.:
  - AeroDrag.py - Skin friction, form, and induced drag calculations:
  - Hover.py - Power and energy requirements from hovering flight:
  - Structures.py - Euler beam theory and associated equations
  - WingCalculations.py - Iterative process to reduce wing mass:
  - UAVdesign.py - miscellaneous calculations and tradeoffs:

## Expected output

## Cited Works
Numerous studies were used to find relevant equations to create a realistic model. Please use the following thinks to access the original papers. Some files may have a paywall that limit access.
