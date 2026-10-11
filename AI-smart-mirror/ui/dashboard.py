
import cv2
from datetime import datetime


class SmartDashboard:

    def __init__(self):
        self.background = (24, 34, 44)
        self.card_color = (38, 52, 65)
        self.text_color = (245, 248, 250)
        self.muted_color = (185, 201, 213)
        self.accent_color = (145, 211, 244)

    def draw_text(
        self, image, text, position,
        size=0.7, color=None, thickness=1
    ):
        if color is None:
            color = self.text_color

        cv2.putText(
            image,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            size,
            color,
            thickness,
            cv2.LINE_AA
        )

    def draw_card(self, image, x1, y1, x2, y2):
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            self.card_color,
            -1
        )

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (65, 82, 96),
            1
        )

    def render(self, frame, clarity=0):
        # Create a separate dashboard canvas
        dashboard = frame.copy()
        h, w = dashboard.shape[:2]

        # Background
        dashboard[:] = self.background

        now = datetime.now()
        greeting_hour = now.hour

        if greeting_hour < 12:
            greeting = "Good morning!"
        elif greeting_hour < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"

        # Header
        self.draw_text(
            dashboard,
            "AI SMART MIRROR",
            (25, 35),
            0.55,
            self.accent_color,
            2
        )

        self.draw_text(
            dashboard,
            greeting,
            (25, 78),
            1.0,
            self.text_color,
            2
        )

        self.draw_text(
            dashboard,
            "Your personal daily overview",
            (25, 108),
            0.5,
            self.muted_color
        )

        # Clock card
        self.draw_card(
            dashboard, 20, 130, w - 20, 245
        )

        self.draw_text(
            dashboard,
            "CURRENT TIME",
            (40, 160),
            0.45,
            self.muted_color
        )

        self.draw_text(
            dashboard,
            now.strftime("%I:%M:%S %p"),
            (40, 207),
            1.15,
            self.text_color,
            2
        )

        self.draw_text(
            dashboard,
            now.strftime("%A, %d %B %Y"),
            (40, 230),
            0.48,
            self.muted_color
        )

        # Two information cards
        gap = 15
        card_width = (w - 40 - gap) // 2

        left_x = 20
        right_x = left_x + card_width + gap

        self.draw_card(
            dashboard,
            left_x, 260,
            left_x + card_width, 370
        )

        self.draw_card(
            dashboard,
            right_x, 260,
            right_x + card_width, 370
        )

        self.draw_text(
            dashboard,
            "MIRROR STATUS",
            (left_x + 15, 290),
            0.42,
            self.muted_color
        )

        self.draw_text(
            dashboard,
            f"{clarity:.1f}% clear",
            (left_x + 15, 325),
            0.68,
            self.accent_color,
            2
        )

        status = (
            "Ready"
            if clarity >= 50
            else "Clearing"
        )

        self.draw_text(
            dashboard,
            status,
            (left_x + 15, 350),
            0.45,
            self.text_color
        )

        self.draw_text(
            dashboard,
            "WEATHER",
            (right_x + 15, 290),
            0.42,
            self.muted_color
        )

        self.draw_text(
            dashboard,
            "Not connected",
            (right_x + 15, 325),
            0.55,
            self.text_color
        )

        self.draw_text(
            dashboard,
            "Live weather: coming next",
            (right_x + 15, 350),
            0.36,
            self.muted_color
        )

        # Today's focus
        self.draw_card(
            dashboard, 20, 385, w - 20, h - 45
        )

        self.draw_text(
            dashboard,
            "TODAY'S FOCUS",
            (40, 418),
            0.5,
            self.accent_color,
            1
        )

        self.draw_text(
            dashboard,
            "Placement preparation",
            (40, 455),
            0.6
        )

        self.draw_text(
            dashboard,
            "DSA practice",
            (40, 490),
            0.6
        )

        self.draw_text(
            dashboard,
            "D - Dashboard     M - Mirror     Q - Quit",
            (25, h - 15),
            0.43,
            self.muted_color
        )

        return dashboard
