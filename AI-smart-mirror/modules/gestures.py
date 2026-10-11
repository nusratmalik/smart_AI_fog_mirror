import math


class GestureRecognizer:

    def distance(self, p1, p2):

        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def is_finger_extended(
        self,
        landmarks,
        tip,
        pip
    ):

        return landmarks[tip].y < landmarks[pip].y

    def recognize(self, landmarks):

        if landmarks is None:
            return "NONE"

        # Finger tips
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        # Finger joints
        index_pip = landmarks[6]
        middle_pip = landmarks[10]
        ring_pip = landmarks[14]
        pinky_pip = landmarks[18]

        index_extended = self.is_finger_extended(
            landmarks,
            8,
            6
        )

        middle_extended = self.is_finger_extended(
            landmarks,
            12,
            10
        )

        ring_extended = self.is_finger_extended(
            landmarks,
            16,
            14
        )

        pinky_extended = self.is_finger_extended(
            landmarks,
            20,
            18
        )

        # --------------------------------
        # Open Palm
        # --------------------------------

        if (
            index_extended
            and middle_extended
            and ring_extended
            and pinky_extended
        ):
            return "OPEN_PALM"

        # --------------------------------
        # Index Finger
        # --------------------------------

        if (
            index_extended
            and not middle_extended
            and not ring_extended
            and not pinky_extended
        ):
            return "INDEX"

        # --------------------------------
        # Fist
        # --------------------------------

        if (
            not index_extended
            and not middle_extended
            and not ring_extended
            and not pinky_extended
        ):
            return "FIST"

        # --------------------------------
        # Thumbs Up
        # --------------------------------

        thumb_is_up = (
            thumb_tip.y <
            index_pip.y
        )

        if (
            thumb_is_up
            and not index_extended
            and not middle_extended
            and not ring_extended
            and not pinky_extended
        ):
            return "THUMBS_UP"

        return "UNKNOWN"