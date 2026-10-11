import cv2
import time

from modules.fog import FogEffect
from modules.gestures import GestureRecognizer
from modules.hand_tracking import HandTracker
from ui.dashboard import SmartDashboard


# ==========================================
# CAMERA SETUP
# ==========================================

import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("DirectShow failed; trying Media Foundation...")
    cap.release()
    cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit

time.sleep(2)

frame = None

for attempt in range(30):
    ret, candidate = cap.read()

    if ret and candidate is not None and candidate.size > 0:
        frame = candidate
        break

    time.sleep(0.2)

if frame is None:
    print("ERROR: No camera frames received.")
    cap.release()
    raise SystemExit

print("Webcam working:", frame.shape)

frame = cv2.flip(frame, 1)
height, width, _ = frame.shape



# ==========================================
# READ FIRST FRAME
# ==========================================

ret, frame = cap.read()

if not ret or frame is None:
    print("ERROR: Could not read webcam frame.")
    cap.release()
    exit()

print("First frame received:", frame.shape)


# Mirror the frame
frame = cv2.flip(frame, 1)

height, width, _ = frame.shape


# ==========================================
# INITIALIZE MODULES
# ==========================================

fog = FogEffect(
    width,
    height
)

hand_tracker = HandTracker()

gesture_recognizer = GestureRecognizer()

previous_finger = None
dashboard = SmartDashboard()
show_dashboard = False


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    # --------------------------------------
    # Read webcam
    # --------------------------------------

    ret, frame = cap.read()

    if not ret or frame is None:
        print("WARNING: Could not read frame.")
        continue

    # Mirror webcam
    frame = cv2.flip(frame, 1)

    # Keep original frame
    original = frame.copy()


    # --------------------------------------
    # Create fog
    # --------------------------------------

    foggy = fog.create_fog(
        original
    )


    # --------------------------------------
    # HAND DETECTION
    # --------------------------------------

    landmarks = hand_tracker.get_hand_landmarks(
        frame
    )


    # --------------------------------------
    # GESTURE RECOGNITION
    # --------------------------------------

    gesture = gesture_recognizer.recognize(
        landmarks
    )


    # Draw hand landmarks
    hand_tracker.draw_landmarks(
        frame,
        landmarks
    )


    # --------------------------------------
    # INDEX FINGER
    # --------------------------------------

    finger = None

    if landmarks is not None:

        finger = hand_tracker.get_index_finger(
            frame,
            landmarks
        )


    # --------------------------------------
    # WIPE MIRROR
    # --------------------------------------

    if gesture == "INDEX" and finger is not None:

        x, y = finger

        # Reject unusually large tracking jumps
        max_jump = 100

        if previous_finger is not None:

            px, py = previous_finger

            distance = (
                (x - px) ** 2
                + (y - py) ** 2
            ) ** 0.5

            if distance <= max_jump:
                fog.wipe(
                    x,
                    y,
                    previous_point=previous_finger,
                    radius=65
                )
            else:
                # Start a new stroke instead of drawing
                # a long unwanted line
                fog.wipe(
                    x,
                    y,
                    radius=65
                )

        else:
            fog.wipe(
                x,
                y,
                radius=65
            )

        previous_finger = (x, y)

        # Show finger position
        cv2.circle(
            frame,
            (x, y),
            10,
            (0, 255, 0),
            -1
        )

    else:
        previous_finger = None


    # --------------------------------------
    # FIST = RESET
    # --------------------------------------

    if gesture == "FIST":

        fog.reset()


    # --------------------------------------
    # FOG REGENERATION
    # --------------------------------------

    fog.regenerate_fog()


    # --------------------------------------
    # CREATE FINAL MIRROR
    # --------------------------------------

    output = fog.get_result(
        original,
        foggy
    )


    # --------------------------------------
    # CALCULATE CLARITY
    # --------------------------------------

    clarity = fog.get_clarity()


    # ======================================
    # USER INTERFACE
    # ======================================

    cv2.putText(
        output,
        "AI SMART MIRROR",
        (30, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )


    cv2.putText(
        output,
        "Move your finger to wipe the mirror",
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


    cv2.putText(
        output,
        f"Gesture: {gesture}",
        (30, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        output,
        f"Mirror Clarity: {clarity:.1f}%",
        (30, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        output,
        "R - Reset     Q - Quit",
        (30, height - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    
    # ======================================
    # DISPLAY AND KEYBOARD
    # ======================================

    if show_dashboard:
        print("Rendering dashboard...", flush=True)
        display_frame = dashboard.render(output, clarity)
    else:
        display_frame = output

    cv2.imshow("AI Smart Mirror", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("d"):
        print("Opening dashboard...", flush=True)
        show_dashboard = True

    elif key == ord("m"):
        print("Returning to mirror...", flush=True)
        show_dashboard = False

    elif key == ord("r"):
        fog.reset()
        previous_finger = None

    elif key == ord("q"):
        break



# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()

hand_tracker.close()

print("AI Smart Mirror stopped.")