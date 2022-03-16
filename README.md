# UAV-Code

This program helps streamline the initial design phase when creating tiltrotor aircraft. This type of a/c helps fill the need for efficient cargo carring drones that can operate without a runway and/or landing strip. \

Edit this file to your chosen airfoil and a/c dimensions:
```
inputs.csv
```

Specific data to the aircraft like mass, wingspan, coefficient of lift, etc
```
ReadInputs.py
```

Main fuction that puts everything together
```
$ python GenerativeDesign.py
```

Skin friction, form, and induced drag calculations
```
$ python AeroDrag.py
```

Power and energy requirements from hovering flight
```
$ python Hover.py
```

Euler beam theory and associated equations
```
$ python Structures.py
```

Iterative process to reduce wing mass
```
$ python WingCalculations.py
```

miscellaneous calculations and tradeoffs
```
$ python UAVdesign.py
```
