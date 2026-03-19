# 🌾 Smart Farm Face Recognition Security System

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)
![License](https://img.shields.io/badge/License-MIT-green)

> An IoT & AI-based autonomous surveillance solution designed to protect remote agricultural assets. It uses motion detection to trigger facial recognition, identifying authorized personnel vs. intruders and raising local/cloud alarms.

---

## 📖 Table of Contents
1. [Overview](#-overview)
2. [Hardware Components](#-hardware-components)
3. [Circuit Connection](#-circuit-connection-gpio)
4. [Project Structure](#-project-structure)
5. [Installation](#-installation)
6. [Step-by-Step Execution](#-step-by-step-execution)
7. [Contributors](#-contributors)

---

## 💡 Overview
Agriculture is the backbone of many economies, yet farms located in remote areas face constant threats of theft and vandalism. This system provides **24/7 automated security** using a **Raspberry Pi 4** (or 3B).

**How it works:**
1.  **Motion Detection:** The **PIR Sensor** constantly monitors the area.
2.  **Image Capture:** When motion is detected, the **Pi Camera** captures a frame.
3.  **Face Recognition:** The system uses OpenCV to check if the face is **Authorized** or **Unknown**.
4.  **Action:**
    * **Authorized:** Logs the entry silently.
    * **Unknown:** Triggers the **Buzzer** & **LED** and logs the threat to Firebase.

---

## 🛠 Hardware Components
The system is powered by the following components:

| Component | Quantity | Usage |
|-----------|:--------:|-------|
| **Raspberry Pi 4 / 3B** | 1 | Main processing unit (Edge Computing) |
| **Pi Camera Module** | 1 | Image acquisition |
| **PIR Motion Sensor** | 1 | Detection trigger to wake the system |
| **Active Buzzer** | 1 | Audio alarm system for intruders |
| **Red LED** | 1 | Visual warning and status indicator |
| **Jumper Wires** | Several | Circuit connections |
| **Power Supply (5V)** | 1 | Powers the Raspberry Pi |

---

## 🔌 Circuit Connection (GPIO)
Connect the components to the Raspberry Pi GPIO pins as defined in the main script:

* **PIR Sensor (Signal):** GPIO 17 (Physical Pin 11)
* **Red LED (+):** GPIO 18 (Physical Pin 12)
* **Buzzer (+):** GPIO 27 (Physical Pin 13)
* **VCC:** Pin 2 or 4 (5V)
* **GND:** Pin 6, 9, or 14

---

## 📂 Project Structure
This repository is organized as follows:

```text
├── dataset/                        # Folder containing images of authorized persons
├── licenses/                       # Project license documents
├── encodings.pickle                # Trained face encodings file (Model)
├── facial_recognition_hardware.py  # 🟢 MAIN SCRIPT: Runs the full security system
├── facial_recognition.py           # Basic software-only recognition test
├── image_capture.py                # Script to capture images for new users
├── model_training.py               # Script to train the model on the 'dataset' folder
├── index.html                      # Web Dashboard for Firebase Hosting
├── status.txt                      # Live system log file
├── test_capture.jpg                # Temporary image buffer
└── 1.py                            # Utility test script
```
---
## Installation⚙️ 
**Follow these steps to set up the environment:**
1. Update your Raspberry Pi -> Open the terminal and run -> "Bashsudo apt-get update && sudo apt-get upgrade"
2. Install System Dependencies -> These are required for OpenCV and Dlib to work correctly on the Pi. "Bashsudo apt-get install cmake libopenblas-dev liblapack-dev libjpeg-dev"
3. Install Python LibrariesBashpip3
4. Install opencv-python face_recognition numpy gpiozero picamera2

---

## Step-by-Step Execution🚀 

**Follow these steps to set up and run the project from scratch:**

**Step 1:** Register Authorized Users -> Run the capture script to take photos of the farm owner or workers.Bashpython3 image_capture.py

Enter the name of the person when prompted.

The script will take multiple photos and save them to the dataset/ folder.

**Step 2:** Train the AI ModelOnce images are captured, you need to encode them into a format the AI understands.Bashpython3 model_training.py

This reads images from dataset/ and creates the encodings.pickle file.

**Step 3:** Run the Security SystemStart the main surveillance program. This will turn on the PIR sensor and wait for motion.Bashpython3 facial_recognition_hardware.py

System Behavior:"Waiting for Motion..." (System is Idle).
Motion Detected! -> LED Turns ON -> Camera takes photo.
Processing...If Authorized: Prints "Access Granted" (No Alarm).
If Intruder: Buzzer Sounds 🚨 and prints "Unknown Person Detected".

**Step 4:** View Logs (Optional)You can view the real-time status of the system by opening the text log:Bashcat status.txt

---

## INDIAN INSTITUTE OF TECHNOLOGY ROPAR
Vanya Mangla
