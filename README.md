# Face Trigger Auto-Capture 📸

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

An intelligent computer vision script that uses **MediaPipe Face Mesh** to detect facial landmarks in real-time. It automatically captures and saves a photo when specific gestures (like opening your mouth) are detected.

---

## 💡 About the Project

This project explores the intersection of **Geometry-based Computer Vision** and User Interaction. Instead of using heavy deep learning models for classification, it utilizes 3D facial landmarks to calculate Euclidean distances between specific points on the human face, making it extremely lightweight and fast for edge devices.

![Project Demo](assets/demo.gif)

## 🚀 Key Features

* **Real-time Detection:** High-frequency landmark tracking using MediaPipe.
* **Geometric Triggers:** Mathematical calculation of "aperture" for mouth/eyes.
* **Auto-Save System:** Automatic file naming with timestamps and cooldown logic.
* **Robust Architecture:** Modular code structure following PEP8 standards and OOP principles.
