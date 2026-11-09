# Mouse using eye and head movement

Camera-based mouse for a desktop computer. Uses head position, approximate pupil position and blink gestures. Experimental assistive technology; not yet validated for accessibility or accuracy.

## Video Demonstration

Watch the Eye and Head Movement Mouse Controller
in action, demonstrating hands-free cursor movement
using head and eye tracking.

https://github.com/user-attachments/assets/81ff332e-543a-4890-9000-0acff4e82e5d

## Requirements

1. **Hardware:** Laptop or desktop computer with a functioning webcam and graphical desktop environment.

2. **Python:** Python 3.10 or newer. The application has been successfully tested on **Python 3.14.6 (Windows)**. Compatibility with other Python versions may depend on library availability.

3. **Operating Systems:** Designed for Windows, macOS and desktop Linux. Currently tested on Windows; compatibility with other operating systems has not yet been verified.

4. **Required Libraries:**
   - OpenCV (`opencv-python`) – Webcam access and image processing.
   - NumPy (`numpy`) – Numerical calculations.
   - dlib (`dlib` or compatible `dlib-bin`) – Facial landmark detection.
   - PyAutoGUI (`pyautogui`) – Cursor movement and mouse clicks.

5. **Facial Landmark Model:** The `shape_predictor_68_face_landmarks.dat` model is required and must be downloaded separately.

6. **Additional Notes:**
   - Windows users running Python 3.14 can use `dlib-bin`, as tested during development.
   - Building `dlib` from source may require CMake and a C++ compiler.
   - macOS users may need to grant Camera and Accessibility permissions.
   - Some Linux Wayland environments restrict automated mouse control; X11 is generally more compatible.
   - Google Colab and standard headless Docker environments cannot directly control the user's local mouse.

## Install

In Terminal / PowerShell, from this folder:

**Windows:**
```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Get the 68-point landmark model from the dlib project (about 100 MB compressed):
https://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

Extract the `.bz2` archive and put `shape_predictor_68_face_landmarks.dat` beside `mouse_controller.py`. Check the model's license before distributing it. The model itself is not included in this package.

```bash
python mouse_controller.py
```

## Use

1. Face the webcam, keep your eyes normally open, look near screen center, and stay still during calibration (35 valid frames).
2. Head movement provides primary cursor control; eye movement fine-tunes it.
3. One detected blink: left click; two quick blinks: double click; three or more: right click. **Natural blinks may trigger clicks**; disable clicking with `C` during initial tests.
4. `SPACE` pause/resume, `R` recalibrate, `C` toggle click gestures, `ESC` quit.
5. PyAutoGUI's emergency failsafe remains **on**: move cursor to screen corner to stop. Keep the preview window visible so ESC can be used.

Adjust `HEAD_GAIN`, `EYE_GAIN`, `SMOOTHING` and `CAMERA` near the top of the script if needed. This implementation maps the user's neutral position to screen center. Tracking quality depends on lighting, camera, and face visibility, and the system is **not yet robust to large user/camera movement**.

## GitHub and Docker

Commit Python files, `README.md`, and `requirements.txt` to GitHub. The `.gitignore` excludes the downloaded landmark model. Docker is not necessary for local use and complicates GUI/webcam access.
