# Toolbox-de-Simulación-para-Análisis-de-Señales-Mixtas

## Project Description
This project is an interactive simulator for PID controllers (Proportional–Integral–Derivative), developed using Python and PyQt5.  

The system allows users to visualize, analyze, and adjust PID parameters while observing the real-time response of the system through dynamic plots.

---

## Key Features
- Intuitive graphical interface developed with PyQt5.
- Manual adjustment of PID parameters: 
    - Kp.
    - Ki.
    - Kd.
- Manual adjustment of input signal parameters: 
    - Step Time.
    - Initial Value.
    - Final Value.
    - Total Time.
    - Sample Time.
- Manual sensor configuration using transfer functions:
    - Numerator (list of coefficients)
    - Denominator (list of coefficients)
- Manual configuration of plant models using transfer functions:
    - Ball and Beam.  
    - DC Motor Speed Control.
    - DC Motor Position Control.  
    - Personalized Plant.
- Graphical visualization tools:
    - Step Response.  
    - Impulse Response.  
    - Bode Plot.  
    - Nyquist Plot.  
    - Root Locus.  
    - Pole-Zero Plot.
- Saving project configurations to a `.txt` file.


---

## Project Structure

```plaintext 
Proyectos/
└── projects/                             # Example project files and templates

Simulator_App/
├── simulation_components/                # Business logic and core simulation engine
│   ├── controller_pid.py                 # PID controller parameters and calculations
│   ├── input.py                          # Input signal parameters and generators
│   ├── output.py                         # Output calculation and response graph generation
│   ├── plant.py                          # Plant models, transfer functions, and input validation
│   └── sensor.py                         # Sensor parameters as transfer functions
│
├── tests/                                # Unit tests for file handling and plant model logic
│   ├── file_tester/
│       ├──BallAndBeamExample.txt
│       ├──DCMotorPositionControlExample.txt
│       ├──DCMotorSpeedControlExample.txt
│       └──PersonalizedPlantExample.txt
│   ├── plant_tester/
│       ├──personalized_plant_tester.py
│       ├──plant_tester.py
│       └──predefined_plant_tester.py
│
├── ui/                                   # Graphical interface design files (Qt Designer)
│   ├── control_editor.ui                 # PID controller configuration interface
│   ├── input_editor.ui                   # Input signal configuration interface
│   ├── output_plotter.ui                 # Response visualization and plotting interface
│   ├── plant_editor.ui                   # Plant model configuration interface
│   ├── project_create.ui                 # Project creation and setup wizard
│   ├── sensor_editor.ui                  # Sensor configuration interface
│   ├── simulator.ui                      # Main simulation workspace
│   └── start.ui                          # Application startup screen
│
├── utils/                                # Shared utilities and helper functions
│   ├── clickable_label.py                # Custom clickable QLabel implementation
│   ├── file_utils.py                     # File operations, saving, and loading utilities
│   └── input_utils.py                    # Input validation and data processing helpers
│
├── views/                                # GUI controllers and view logic
│   ├── control_editor.py                 # Controller for PID editor interface
│   ├── create_project.py                 # Controller for project creation wizard
│   ├── input_editor.py                   # Controller for input signal configuration
│   ├── output_plotter.py                 # Controller for response visualization
│   ├── plant_editor.py                   # Controller for plant model configuration
│   ├── sensor_editor.py                  # Controller for sensor configuration
│   ├── simulator.py                      # Main simulation controller
│   └── start.py                          # Startup screen controller
│
├── build_exe.py                          # Script to build executable distribution
├── main.py                               # Script to launch the simulator
├── docs/                                 # Additional documentation
│   └── Manual_de_Usuario.pdf             # User manual and application guide
├── requirements.txt                      # Project dependencies and packages
└── README.md                             # This file

```
---

## Requirements
- PyQt5==5.15.11: Framework for the .ui files (Graphic User Interface)
- matplotlib==3.10.7: For generating graphs and visualizations
- numpy==2.2.6: For numerical calculations.
- scipy==1.16.0: For advanced mathematical functions and signal processing.
- control==0.10.2: Specific library for control systems (transfer functions)
- Pillow==11.2.1: For image manipulation (used in generating LaTeX equations as images)
- pyinstaller==6.16.0: For creating the executable (used in build_exe.py)

---

### Installation
```bash
pip install -r requirements.txt
```
---

### To run the simulator
#### GUI Mode
To run the code use the following command
```bash
cd .\Simulator_App\
python.exe .\main.py
```

#### Test Mode
To run the tests, change the ****mode**** variable of the ****main**** function of the ****main.py**** file to the value of 2 (line 150).

```bash
mode = 1  # GUI mode, 2 for test mode
```
