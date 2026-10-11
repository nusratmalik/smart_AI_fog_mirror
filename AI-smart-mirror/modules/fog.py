
import cv2
import numpy as np
import time


class FogEffect:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.clear_mask = np.zeros(
            (height, width), dtype=np.uint8
        )

        self.last_wipe_time = time.time()
        self.refog_speed = 8

    def create_fog(self, frame):
        blurred = cv2.GaussianBlur(
            frame, (51, 51), 0
        )

        fog_layer = np.full_like(
            frame, (220, 220, 220)
        )

        return cv2.addWeighted(
            blurred, 0.65,
            fog_layer, 0.35, 0
        )

    def wipe(self, x, y, previous_point=None, radius=55):
        self.last_wipe_time = time.time()

        if previous_point is not None:
            px, py = previous_point

            cv2.line(
                self.clear_mask,
                (px, py), (x, y),
                255, radius * 2
            )

        cv2.circle(
            self.clear_mask,
            (x, y), radius, 255, -1
        )

    def regenerate_fog(self):
        if time.time() - self.last_wipe_time > 3:
            cv2.subtract(
                self.clear_mask,
                np.full_like(
                    self.clear_mask,
                    self.refog_speed
                ),
                dst=self.clear_mask
            )

    def get_result(self, original, foggy):
        smooth_mask = cv2.GaussianBlur(
            self.clear_mask, (31, 31), 0
        )

        alpha = cv2.cvtColor(
            smooth_mask, cv2.COLOR_GRAY2BGR
        ).astype(np.float32) / 255.0

        result = (
            original.astype(np.float32) * alpha
            + foggy.astype(np.float32) * (1 - alpha)
        )

        return np.clip(
            result, 0, 255
        ).astype(np.uint8)

    def get_clarity(self):
        return float(
            np.mean(self.clear_mask) / 255 * 100
        )

    def reset(self):
        self.clear_mask.fill(0)
        self.last_wipe_time = time.time()

