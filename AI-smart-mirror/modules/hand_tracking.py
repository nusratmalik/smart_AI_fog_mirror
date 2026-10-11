
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:
    def __init__(self):
        model_path = "models/hand_landmarker.task"

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = (
            vision.HandLandmarker.create_from_options(options)
        )

        self.timestamp = 0
        self.prev_x = None
        self.prev_y = None
        self.smoothing = 0.35

    def get_hand_landmarks(self, frame):
        rgb_frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp += 1

        result = self.detector.detect_for_video(
            mp_image, self.timestamp
        )

        if not result.hand_landmarks:
            self.prev_x = None
            self.prev_y = None
            return None

        return result.hand_landmarks[0]

    def get_index_finger(self, frame, landmarks):
        if landmarks is None:
            self.prev_x = None
            self.prev_y = None
            return None

        h, w = frame.shape[:2]
        index = landmarks[8]

        raw_x = max(0, min(w - 1, int(index.x * w)))
        raw_y = max(0, min(h - 1, int(index.y * h)))

        if self.prev_x is None or self.prev_y is None:
            self.prev_x = raw_x
            self.prev_y = raw_y
        else:
            alpha = self.smoothing

            self.prev_x = int(
                alpha * raw_x + (1 - alpha) * self.prev_x
            )
            self.prev_y = int(
                alpha * raw_y + (1 - alpha) * self.prev_y
            )

        return self.prev_x, self.prev_y

    def draw_landmarks(self, frame, landmarks):
        if landmarks is None:
            return

        h, w = frame.shape[:2]

        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

        points = [
            (int(p.x * w), int(p.y * h))
            for p in landmarks
        ]

        for start, end in connections:
            cv2.line(
                frame, points[start], points[end],
                (0, 200, 0), 2
            )

        for point in points:
            cv2.circle(
                frame, point, 3, (0, 255, 0), -1
            )

    def close(self):
        self.detector.close()
