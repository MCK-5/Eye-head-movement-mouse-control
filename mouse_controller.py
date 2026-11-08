from pathlib import Path
import time

import cv2
import dlib
import numpy as np
import pyautogui

MODEL = Path(__file__).with_name("shape_predictor_68_face_landmarks.dat")
CAMERA = 0
DEAD_ZONE = 0.012          
HEAD_SPEED = 2200          
EYE_SPEED = 350            
HEAD_RANGE = (0.10, 0.10) 
SMOOTHING = 0.30          
EAR_FACTOR = 0.70
BLINK_WINDOW = 0.55
CALIBRATION_FRAMES = 35

LEFT, RIGHT = list(range(36, 42)), list(range(42, 48))
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0


def ear(eye):
    vertical = np.linalg.norm(eye[1] - eye[5]) + np.linalg.norm(eye[2] - eye[4])
    horizontal = 2 * np.linalg.norm(eye[0] - eye[3])
    return vertical / horizontal if horizontal else 0


def pupil(gray, eye):
    x, y, w, h = cv2.boundingRect(eye.astype(np.int32))
    if w < 8 or h < 5 or x < 0 or y < 0 or x+w > gray.shape[1] or y+h > gray.shape[0]:
        return None
    patch = cv2.GaussianBlur(gray[y:y+h, x:x+w], (3, 3), 0)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [eye.astype(np.int32) - (x, y)], 255)
    _, dark = cv2.threshold(patch, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    dark = cv2.bitwise_and(dark, mask)
    contours, _ = cv2.findContours(dark, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    m = cv2.moments(max(contours, key=cv2.contourArea))
    return np.array([m["m10"] / m["m00"] / w, m["m01"] / m["m00"] / h]) if m["m00"] else None


def measure(gray, predictor, face):
    pts = np.array([(p.x, p.y) for p in predictor(gray, face).parts()], dtype=float)
    openness = (ear(pts[LEFT]) + ear(pts[RIGHT])) / 2
    eyes = [pupil(gray, pts[idx]) for idx in (LEFT, RIGHT)]
    visible = [p for p in eyes if p is not None]
    gaze = np.mean(visible, axis=0) if visible else None
    # Normalized nose position in the mirrored camera image.
    head = pts[30] / [gray.shape[1], gray.shape[0]]
    return head, gaze, openness


def main():
    if not MODEL.exists():
        raise SystemExit(f"Missing {MODEL.name} beside mouse_controller.py")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(str(MODEL))
    camera = cv2.VideoCapture(CAMERA)
    if not camera.isOpened():
        raise SystemExit("Cannot open webcam; check permissions or try CAMERA = 1")

    screen = np.array(pyautogui.size(), dtype=float)
    cursor = np.array(pyautogui.position(), dtype=float)
    base_head = base_gaze = threshold = None
    calibration = []
    velocity = np.zeros(2)
    paused, clicks_enabled = False, False  # Enable clicking after testing movement
    closed_frames = blink_count = 0
    was_closed = False
    last_blink = 0.0
    last_frame = time.monotonic()

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                break
            now = time.monotonic()
            dt = min(now - last_frame, 0.08)
            last_frame = now
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray, 0)

            if faces:
                face = max(faces, key=lambda f: f.width() * f.height())
                head, gaze, openness = measure(gray, predictor, face)
                if threshold is None:
                    if gaze is not None and openness > 0.12:
                        calibration.append((head, gaze, openness))
                    if len(calibration) >= CALIBRATION_FRAMES:
                        base_head = np.median([s[0] for s in calibration], axis=0)
                        base_gaze = np.median([s[1] for s in calibration], axis=0)
                        threshold = np.median([s[2] for s in calibration]) * EAR_FACTOR
                        print("Calibration complete. Move your head gently; C enables clicks.")
                elif not paused:
                    closed_frames = closed_frames + 1 if openness < threshold else 0
                    closed = closed_frames >= 2
                    if closed and not was_closed:
                        blink_count = blink_count + 1 if now - last_blink < BLINK_WINDOW else 1
                        last_blink = now
                    was_closed = closed

                    if not closed:
                        offset = head - base_head
                        # Proportional velocity, with a central dead zone.
                        direction = np.sign(offset) * np.maximum(np.abs(offset) - DEAD_ZONE, 0)
                        wanted = HEAD_SPEED * np.clip(direction / HEAD_RANGE, -1, 1)
                        if gaze is not None:
                            eye_offset = np.clip((gaze - base_gaze) * 2, -1, 1)
                            wanted += EYE_SPEED * eye_offset
                        velocity += SMOOTHING * (wanted - velocity)
                        cursor = np.clip(cursor + velocity * dt, [2, 2], screen - 3)
                        pyautogui.moveTo(*cursor.astype(int), _pause=False)
                    if blink_count and now - last_blink > BLINK_WINDOW and not closed:
                        if clicks_enabled:
                            if blink_count == 1:
                                pyautogui.click(_pause=False)
                            elif blink_count == 2:
                                pyautogui.doubleClick(interval=0.1, _pause=False)
                            else:
                                pyautogui.rightClick(_pause=False)
                        blink_count = 0
            else:
                velocity[:] = 0
                closed_frames = blink_count = 0
                was_closed = False

            status = (f"CALIBRATING {len(calibration)}/{CALIBRATION_FRAMES}" if threshold is None
                      else "PAUSED" if paused else "RUNNING")
            cv2.putText(frame, f"{status} | clicks {'ON' if clicks_enabled else 'OFF'}", (10, 26),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            cv2.putText(frame, "ESC exit | SPACE pause | R recalibrate | C clicks", (10, 54),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow("Eye + Head Mouse", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            if key in (ord("r"), ord("R")):
                calibration.clear()
                base_head = base_gaze = threshold = None
                velocity[:] = 0
                blink_count = closed_frames = 0
                was_closed = False
                paused = False
            elif key == 32:
                paused = not paused
                velocity[:] = 0
                blink_count = closed_frames = 0
                was_closed = False
            elif key in (ord("c"), ord("C")):
                clicks_enabled = not clicks_enabled
                blink_count = 0
    except pyautogui.FailSafeException:
        print("Emergency stop: pointer reached a screen corner")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
