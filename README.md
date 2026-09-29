# UAV-Code

## Summary
This program streamlines the *initial design phase* of a tiltrotor aircraft. This type of aircraft helps fill the need for efficient cargo-carrying drones that can operate without a runway or landing strip. It was built for [AerospaceNU](https://www.aerospacenu.com/), the aerospace club of Northeastern University, during the Fall 2021 semester. The image below shows an example of a prototype that could be built from the outputs.
\
\
<img src="https://user-images.githubusercontent.com/83112082/158711492-ad390191-10b6-4bf6-add6-52dd5bcf30c0.jpg" width="70%" height="70%">

## About the program
The model is intended to be a useful, if approximate, tool for the initial design phase. It is not without assumptions but represents a helpful starting point for novel aircraft design. Some of the physical phenomena that are modeled include:
  - Skin-friction drag with boundary-layer theory
  - Form drag from airfoil data
  - FAA structural loading limits
  - Disk loading to estimate hovering power costs
  - Taper ratio and induced drag
  - Euler bending-beam theory for thin structures (torsion and bending)
  - Battery considerations for electric flight

## Setup
This project uses [uv](https://docs.astral.sh/uv/) and [go-task](https://taskfile.dev/).
1. install `uv` and `task`
2. `git clone https://github.com/Tsmorz/UAV-Code.git`
3. `task init` to create the virtual environment and install the pre-commit hooks

## Running
Edit `inputs.csv` with your chosen airfoil coefficients and aircraft dimensions (mass, wingspan, coefficient of lift, etc.), then run the design sweep:
```bash
task run
```

The package modules are:
  - `uav_design/read_inputs.py` — reads aircraft data (mass, wingspan, lift coefficient, etc.) from `inputs.csv`
  - `uav_design/aero_drag.py` — skin-friction, form, and induced drag calculations
  - `uav_design/hover.py` — power and energy requirements for hovering flight
  - `uav_design/structures.py` — Euler beam theory and associated equations
  - `uav_design/wing_calculations.py` — iterative process to minimize wing mass
  - `uav_design/__main__.py` — puts everything together and produces the plots and terminal output
  - `uav_design/airfoil.py` — standalone airfoil profile plot

## Expected output
The plots below give an example of the expected output. The red dot denotes the ideal starting design to maximize flight duration given the current constraints. Adjust `inputs.csv` to tailor the program to your needs. The far-right image is the expected terminal output — use these dimensions to design the aircraft model.
\
\
Important things to note:
  - The white area in the upper-right corner of each plot is ***beyond the structural limit and the aircraft will fail!***
  - The rotors *always* extend past the wing tips. See the photo above for an example model.
  - The program assumes all structural load is carried by carbon-fiber spars in the wings.

<p float="left">
  <img src="https://user-images.githubusercontent.com/83112082/158713521-fae7395c-5113-4f1f-8e25-9edbd344cf81.png" width="70%" height="70%" />
  <img src="https://user-images.githubusercontent.com/83112082/158713522-7398d7cf-d6ba-4bc4-a7e9-92efdf357db3.png" width="28%" height="28%" />
</p>

## Adding to the repo
1. Create a new branch before making changes:\
`git checkout -b new-branch-name`

2. Track changes as you go:\
`git add file_that_changed`\
`git commit -m "a useful message"`\
`git push`

3. Add unit and integration tests for new functionality in the `tests` directory. Run them with `task test`.

## Cited Works
Numerous studies were used to find relevant equations for a realistic model. Some links may be behind a paywall.
  - https://www.researchgate.net/figure/XV-15-tiltrotor-aircraft-layout-Ref-9_fig3_23847162
  - https://www.sciencedirect.com/science/article/pii/S2352146518300383
  - https://books.google.nl/books?id=-PnV2JuLZi4C&pg=PA42&lpg=PA42&dq=power+required+to+hover+watts+per+kg
  - http://www.epi-eng.com/propeller_technology/selecting_a_propeller.htm
  - http://airfoiltools.com/airfoil/details?airfoil=sd7062-il
  - https://www.risingup.com/fars/info/part23-337-FAR.shtml
