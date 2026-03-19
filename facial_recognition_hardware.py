# ================================
# SMART FARM SECURITY – LOCAL VERSION
# Shows only Known / Unknown (no cloud)
# ================================

import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
from gpiozero import LED, Buzzer, MotionSensor
from datetime import datetime

# -----------------------------------
# HARDWARE SETUP
# -----------------------------------
pir = MotionSensor(17)
led = LED(18)
buzzer = Buzzer(27)

# Camera setup
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (640, 480)}
    )
)
picam2.start()
time.sleep(1)
print("[INFO] ✅ Camera initialized")

STATUS_FILE = "status.txt"


def write_status(text: str):
    """Write Known / Unknown status to local file."""
    try:
        with open(STATUS_FILE, "w") as f:
            f.write(text)
        print(f"[STATUS] -> {text}")
    except Exception as e:
        print("[STATUS] ❌ Could not write status:", e)


# -----------------------------------
# LOAD FACE ENCODINGS
# -----------------------------------
print("[INFO] Loading encodings...")

with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())

known_face_encodings = data["encodings"]
known_face_names = data["names"]

print(f"[INFO] ✅ Loaded {len(known_face_names)} known faces")

# Set initial status
write_status("No detection yet")


# -----------------------------------
# FACE RECOGNITION FUNCTION
# -----------------------------------
def recognize_faces_in_frame(frame):
    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    locs = face_recognition.face_locations(rgb, model='hog')
    encs = face_recognition.face_encodings(rgb, locs)

    names = []
    for enc in encs:
        matches = face_recognition.compare_faces(known_face_encodings, enc, tolerance=0.50)
        name = "Unknown"

        if len(known_face_encodings) > 0:
            dists = face_recognition.face_distance(known_face_encodings, enc)
            best = np.argmin(dists)
            if matches[best]:
                name = known_face_names[best]

        names.append(name)

    return names


# -----------------------------------
# MAIN LOOP
# -----------------------------------
print("[INFO] ✅ System armed. Waiting for motion...")

try:
    while True:
        pir.wait_for_motion()
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Motion detected")

        led.on()
        time.sleep(1)
        frame = picam2.capture_array()
        led.off()

        names = recognize_faces_in_frame(frame)

        if not names:
            print(" -> Motion detected but NO face found")
            write_status("No face detected")
            time.sleep(1)
            continue

        print("Faces detected:", names)

        if "Unknown" in names:
            print(" -> ⚠ UNKNOWN PERSON! Raising alarm.")
            buzzer.on()
            time.sleep(2)
            buzzer.off()
            write_status("Unknown person detected ⚠")
        else:
            print(" -> ✅ Authorized:", ", ".join(names))
            write_status("Known person detected ✅")

        time.sleep(2)

except KeyboardInterrupt:
    print("\n[INFO] Stopping system...")

finally:
    picam2.stop()
    led.off()
    buzzer.off()
    write_status("System offline")
    print("[INFO] ✅ System offline")
