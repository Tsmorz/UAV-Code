# UAV-Code

This program helps streamline the initial design phase when creating tiltrotor aircraft. This type of a/c helps fill the need for efficient cargo carring drones that can operate without a runway and/or landing strip.
<img src="https://user-images.githubusercontent.com/83112082/158711492-ad390191-10b6-4bf6-add6-52dd5bcf30c0.jpg" width="60%" height="60%">

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
Numerous studies were used to find relevant equations to create a realistic model. Please use the following thinks to access the original papers. Some files may have a paywall that limit access. \
https://www.researchgate.net/figure/XV-15-tiltrotor-aircraft-layout-Ref-9_fig3_23847162 \
https://www.sciencedirect.com/science/article/pii/S2352146518300383 \
https://books.google.nl/books?id=-PnV2JuLZi4C&pg=PA42&lpg=PA42&dq=power+required+to+hover+watts+per+kg&source=bl&ots=iS07eZFRKr&sig=ACfU3U2BjfLfAVHgaFQWmAX8z5_0TVsmUQ&hl=en&sa=X&ved=2ahUKEwjDx7Pg9ZvyAhWho3EKHU_EAwoQ6AF6BAgeEAM#v=onepage&q=power%20required%20to%20hover%20watts%20per%20kg&f=false \
http://www.epi-eng.com/propeller_technology/selecting_a_propeller.htm \
http://airfoiltools.com/airfoil/details?airfoil=sd7062-il \
https://www.risingup.com/fars/info/part23-337-FAR.shtml 
