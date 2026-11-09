# Eye and Head Movement-Based Mouse Cursor Control System

### A Hands-Free Computer Interaction System Using Computer Vision

An assistive technology project designed to help people with physical disabilities or limited hand mobility interact with computers through eye movements, head movements, and blink gestures.

The system uses a standard webcam to detect facial landmarks, track head and eye movements, and translate those movements into mouse cursor actions without requiring a traditional mouse.

Built using **Python, OpenCV, dlib, NumPy, and PyAutoGUI**.

## Video Demonstration

Watch the Eye and Head Movement-Based Mouse Cursor Control System in action.

The demonstration shows hands-free cursor movement using the laptop's webcam.



https://github.com/user-attachments/assets/0cd463e7-72e5-4c52-9a11-ea8ee778dc11



## Project Objectives

The main objectives of this project are to:

- Develop a hands-free mouse control system using a standard webcam.
- Enable cursor movement through head and eye tracking.
- Implement blink-based mouse clicking.
- Reduce dependence on physical mouse devices.
- Improve cursor stability and responsiveness.
- Provide an affordable computer accessibility solution using commonly available hardware.

## Features

### 1. Head Movement Tracking

The system detects the user's head position using facial landmarks.

Head movements control the direction of cursor movement:

- Move head left — cursor moves left.
- Move head right — cursor moves right.
- Move head upward — cursor moves upward.
- Move head downward — cursor moves downward.
- Return to the calibrated neutral position — cursor stops moving.

The improved Version 2 uses velocity-based cursor movement, allowing users to reach different areas of the screen without excessive head movement.

### 2. Eye Movement Tracking

The application detects eye landmarks and estimates pupil positions using computer vision techniques.

Eye movement information contributes to cursor control alongside head movement.

### 3. Blink-Based Mouse Clicking

The system uses the Eye Aspect Ratio (EAR) to detect blink gestures.

| Blink Gesture | Mouse Action |
|---|---|
| Single detected blink | Left click |
| Two quick detected blinks | Double click |
| Three or more quick detected blinks | Right click |

Blink-click functionality is experimental and may require additional calibration to distinguish natural blinks from intentional clicks.

### 4. Personalized Calibration

The system performs an initial calibration to establish the user's neutral head position and eye openness.

This helps adapt the tracking system to individual users.

### 5. Cursor Smoothing

Cursor smoothing reduces unwanted cursor movements caused by minor tracking fluctuations.

### 6. Screen Resolution Adaptation

The system detects the computer's display resolution and adjusts cursor movement accordingly.

### 7. Keyboard Controls

| Key | Function |
|---|---|
| SPACE | Pause or resume cursor control |
| R | Recalibrate tracking |
| C | Enable or disable blink clicking |
| ESC | Exit the application |

Keyboard shortcuts require the application's OpenCV preview window to have focus.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Webcam processing and computer vision |
| dlib | Face detection and facial landmark identification |
| NumPy | Numerical calculations |
| PyAutoGUI | Mouse movement and clicking |

## System Requirements

### Hardware

- Laptop or desktop computer.
- Functional webcam.
- Graphical desktop environment.
- Keyboard for setup and emergency controls.

### Software

- Python 3.10 or newer, subject to dependency compatibility.
- Windows, macOS, or desktop Linux.
- OpenCV, NumPy, dlib, and PyAutoGUI.

**Tested development environment:**

- Operating System: Windows
- Python Version: 3.14.6
- Facial Landmark Library: dlib-bin
- Application Version: 2

Compatibility with other operating systems and Python versions has not yet been fully verified.

## Installation and Setup

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/MCK-5/eye-head-movement-mouse-control.git
cd eye-head-movement-mouse-control
```

Alternatively, click **Code → Download ZIP** on GitHub and extract the project.

### Step 2: Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Libraries

For the tested Windows Python 3.14 environment:

```bash
python -m pip install --upgrade pip
python -m pip install opencv-python numpy pyautogui dlib-bin
```

On other supported environments, `dlib` may need to be installed instead of `dlib-bin`:

```bash
python -m pip install opencv-python numpy pyautogui dlib
```

Building dlib from source may require CMake and a compatible C++ compiler.

### Step 4: Download the Facial Landmark Model

The application requires the pretrained **68-point facial landmark predictor**.

Download it here:

https://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

Extract the downloaded file to obtain:

`shape_predictor_68_face_landmarks.dat`

Place this file in the same directory as `mouse_controller.py`.

The large pretrained model is not included in this repository.

### Step 5: Run the Application

Open the project directory in a terminal and execute:

```bash
python mouse_controller.py
```

Allow webcam access if requested by your operating system.

### Step 6: Calibrate the System

When the application starts:

1. Sit comfortably in front of the webcam.
2. Face the screen naturally.
3. Keep your head steady during initial calibration.
4. Keep your eyes naturally open.
5. Allow the application to establish its reference position.
6. Begin testing cursor movement using gentle head movements.

For initial testing, keep blink clicking disabled until cursor movement is stable.

## Project Structure

```text
eye-head-movement-mouse-control/
├── mouse_controller.py
├── requirements.txt
├── README.md
└── .gitignore
```

The facial landmark model must be downloaded separately.

## How the System Works

The system follows a computer vision processing pipeline:

**Webcam → Face Detection → Facial Landmark Detection → Head and Eye Tracking → Cursor Control**

1. The webcam captures video frames.
2. OpenCV processes the frames.
3. dlib detects the user's face and facial landmarks.
4. The application estimates head and eye movement relative to calibration.
5. Movement information is converted into cursor commands.
6. PyAutoGUI moves the cursor and performs supported mouse actions.
7. Blink gestures are analyzed for mouse clicking.

The Version 2 movement approach uses directional cursor velocity instead of relying entirely on absolute head-to-screen position mapping.

This improves the ability to navigate toward screen edges while maintaining a comfortable head position.

## Project Status

**Status: Working Prototype — Version 2**

The system has been successfully run on a Windows laptop using Python 3.14.6.

### Completed

- Webcam-based facial landmark detection.
- Head movement cursor control.
- Eye movement tracking.
- Blink gesture detection and mouse-click commands.
- Initial user calibration.
- Cursor smoothing.
- Directional velocity-based cursor movement.
- Screen resolution adaptation.
- Pause, resume, recalibration, and exit controls.

### Current Limitations

- Tracking accuracy depends on webcam quality and lighting.
- Blink detection may interpret natural blinks as intentional clicks.
- Cursor sensitivity may require adjustment for different users.
- Performance may vary across computer hardware and operating systems.
- The system has not yet undergone comprehensive usability testing with its intended user population.

## Future Improvements

Future development will focus on:

1. Improving cursor positioning accuracy.
2. Reducing accidental blink clicks.
3. Improving tracking under different lighting conditions.
4. Supporting users with limited head movement.
5. Measuring cursor accuracy, response time, and blink-detection performance.
6. Conducting usability tests with multiple participants.
7. Improving compatibility across different laptops and operating systems.

## Accessibility and Safety

This project is an experimental assistive technology prototype.

It is intended to explore alternative computer interaction methods for people with limited hand mobility.

It has not yet been clinically validated or extensively tested with users with disabilities.

Users should retain access to conventional input controls or assistance when needed. The system should not be relied upon as the only way to operate a computer until its reliability and accessibility have been properly evaluated.

## Contributing

Contributions, bug reports, testing feedback, and suggestions are welcome.

Developers interested in computer vision, human-computer interaction, and assistive technology are encouraged to contribute toward improving the system.

## Acknowledgements

This project uses open-source computer vision and automation technologies, including OpenCV, dlib, NumPy, and PyAutoGUI.

It also uses the pretrained 68-point facial landmark predictor distributed through dlib.

## Disclaimer

This project is provided for educational, research, and experimental accessibility purposes.

Performance may vary depending on hardware, environmental conditions, user characteristics, and software configuration.
