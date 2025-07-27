Hand Gesture Volume Control using OpenCV & Mediapipe

This is a Python-based computer vision project that allows you to **control your system's volume using hand gestures
captured through a webcam. It uses MediaPipe for hand tracking and pycaw(AndreMiras) to interface with the system audio.

---

## Features

* Real-time hand tracking using [Google MediaPipe](https://google.github.io/mediapipe/).
* Detects 21 hand landmarks to track finger movement.
* Maps distance between thumb and index finger to system volume.
* Live volume bar & percentage indicator.
* Smooth performance with FPS display.

---

## Technologies Used

* Python 3.10(Only works for 3.7 to 3.10).
* OpenCV for video stream processing.
* Mediapipe for hand detection and landmarks.
* Math for distance calculation.
* pycaw for system audio control on Windows.

---

## Project Structure

```
├── HTMFinalModule.py         # Custom Hand Tracking Module
├── VolumeControl.py          # Main application file
├── README.md                 # This file!
```

---

## How It Works

1. The webcam captures your hand in real-time.
2. MediaPipe detects the hand and gives landmark coordinates.
3. The distance between the thumb tip (landmark 4) and index tip (landmark 8) is calculated.
4. This distance is mapped to a volume range using `numpy.interp()`.
5. The system volume is adjusted via pycaw.
6. Visual feedback is shown with circles, a line, a volume bar, and volume %.

---

## Installation

1. Clone the Repository

```bash
git clone https://github.com/yourusername/HandGestureVolumeControl.git
cd P1_Volume_Hand_Gesture_Control
```

### 2. Install Dependencies

```bash
pip install opencv-python mediapipe numpy pycaw comtypes
```

> Make sure you're on Windows, as `pycaw` is Windows-specific.

---

## Run the Project

1. Make sure your webcam is connected and working.
2. Run the main Python script:

```bash
python VolumeControl.py
```

---

## Notes

* Hand must be in frame and visible to MediaPipe.
* The system audio range is mapped between 30 to 190 pixels of finger distance.
* For best results, keep your hand around mid-distance from the camera.
* Works best with one hand in the frame.

---

## References

* [Mediapipe Documentation](https://google.github.io/mediapipe/)
* [pycaw GitHub Repository](https://github.com/AndreMiras/pycaw)

---

## Credits

Developed by: Balaram Pai H
Mentorship / Guidance :FreeCodeCampOrg

---

