import cv2
import numpy as np
import sys
import os
import time
from datetime import datetime

import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh
mp_drawing_utils = mp.solutions.drawing_utils

class FaceTrigger:
    """
    A class to handle facial landmark detection and automated photo triggering
    using absolute path management for reliability across different OS/Environments.
    """
    def __init__(self):
        # Initialize MediaPipe Face Mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Thresholds (Normalized coordinates 0.0 - 1.0)
        self.MOUTH_THRESHOLD = 0.05
        self.COOLDOWN_SECONDS = 3
        self.last_capture_time = 0

        # DEFINE ABSOLUTE PATH: Ensures 'captures' folder is created in the script's directory
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.save_dir = os.path.join(self.base_path, 'captures')

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            print(f"[INFO] Created directory: {self.save_dir}")

    def calculate_distance(self, p1, p2):
        """Calculates Euclidean distance between two landmark points."""
        return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

    def process_frame(self, frame):
        """
        Processes the frame to detect gestures and trigger photo capture.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        trigger_detected = False
        action_name = ""

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Landmark indices for inner lips: 13 (Upper), 14 (Lower)
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]
                
                mouth_distance = self.calculate_distance(upper_lip, lower_lip)

                # Detection logic for mouth open gesture
                if mouth_distance > self.MOUTH_THRESHOLD:
                    trigger_detected = True
                    action_name = "Mouth Open"

                # Visualization of mesh
                mp_drawing_utils.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )

        if trigger_detected:
            self.take_photo(frame, action_name)

        return frame

    def take_photo(self, frame, action):
        """
        Saves the frame to a JPG file using an absolute path to avoid 'ghost' files.
        """
        current_time = time.time()
        if current_time - self.last_capture_time > self.COOLDOWN_SECONDS:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.save_dir, f"capture_{timestamp}.jpg")
            
            # Write to disk and verify success
            success = cv2.imwrite(filename, frame)
            
            if success:
                print(f"[SUCCESS] Photo saved at: {filename} (Trigger: {action})")
            else:
                print(f"[ERROR] Could not save photo to path: {filename}")
                
            self.last_capture_time = current_time

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceTrigger()

    cv2.namedWindow('Face Trigger Project', cv2.WINDOW_NORMAL)
    
    cv2.resizeWindow('Face Trigger Project', 1080, 720)
    # -------------------------------------

    print("\n" + "="*40)
    print("FACE TRIGGER SYSTEM ACTIVE")
    print("Commands: Press 'q' to exit")
    print("="*40 + "\n")

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("[ERROR] Camera feed lost.")
                break

            # UX: Flip frame horizontally to act like a mirror
            frame = cv2.flip(frame, 1) 
            processed_frame = detector.process_frame(frame)

            # Display the result
            cv2.imshow('Face Trigger Project', processed_frame)

            # Keyboard logic: Listen for 'q' or 'Q'
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("[INFO] Shutting down...")
                break
                
    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
    finally:
        # Crucial for professional code: always release hardware resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()