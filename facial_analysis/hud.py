"""
On-screen dashboard (HUD) for the Facial Analysis window.

Drawing happens in two passes to keep the FPS high:
  1. every semi-transparent background is drawn on one overlay and
     blended with a single cv2.addWeighted per frame;
  2. text, bars and dots are then drawn solid on top.
Foreground drawing is queued in self._fg during pass 1 and run in pass 2.
"""

import math
import time

import cv2

from config import ALERT_BANNER_SECONDS
from drowsiness_detector import (
    ALERT_EYES_CLOSED,
    ALERT_NO_FACE,
    ALERT_YAWN,
    ALERT_FREQUENT_YAWN,
)


# -----------------------------
# Palette (BGR)
# -----------------------------

WHITE = (240, 240, 240)
MUTED = (165, 165, 165)
PANEL_BG = (28, 24, 22)
TRACK = (70, 70, 70)
DIVIDER = (85, 85, 85)
GREEN = (90, 200, 90)
AMBER = (0, 185, 255)
RED = (60, 60, 235)
BLUE = (235, 160, 50)

# -----------------------------
# Fonts & Layout
# -----------------------------

HEADING_FONT = cv2.FONT_HERSHEY_DUPLEX
BODY_FONT = cv2.FONT_HERSHEY_SIMPLEX
AA = cv2.LINE_AA

OVERLAY_ALPHA = 0.65
MARGIN = 10
PAD = 12
PANEL_WIDTH = 210
COMPACT_WIDTH = 140
BANNER_MIN_WIDTH = 180
FULL_MIN_WIDTH = 440      # smaller frames always use the compact layout
FULL_MIN_HEIGHT = 400
ROW_HEIGHT = 24
STATUS_BAR_HEIGHT = 24
MIN_SCALE = 0.35
PULSE_HZ = 1.5
BORDER_MAX = 8            # stays inside MARGIN so it never covers text

# Alert type -> (banner background, accent color, title, priority)
BANNER_STYLES = {
    ALERT_EYES_CLOSED: ((40, 40, 170), RED, "WAKE UP", 3),
    ALERT_NO_FACE: ((0, 110, 190), AMBER, "ARE YOU THERE?", 2),
    ALERT_FREQUENT_YAWN: ((150, 85, 25), BLUE, "BREAK TIME", 1),
    ALERT_YAWN: ((150, 85, 25), BLUE, "FEELING TIRED?", 1),
}


def score_color(score):

    if score is None:
        return MUTED

    if score >= 70:
        return GREEN

    if score >= 40:
        return AMBER

    return RED


def fit_text(text, font, scale, thickness, max_width):
    """Shrink the scale (then truncate) until the text fits max_width."""

    while scale > MIN_SCALE and text_width(text, font, scale, thickness) > max_width:
        scale -= 0.05

    scale = max(scale, MIN_SCALE)

    if text_width(text, font, scale, thickness) > max_width:
        while len(text) > 1 and text_width(text + "..", font, scale, thickness) > max_width:
            text = text[:-1]
        text = text + ".."

    return text, scale


def wrap_text(text, font, scale, thickness, max_width, max_lines):
    """Greedy word wrap; the last allowed line is truncated if needed."""

    lines = []
    current = ""

    for word in text.split():

        candidate = f"{current} {word}".strip()

        if not current or text_width(candidate, font, scale, thickness) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    if len(lines) > max_lines:
        lines = lines[:max_lines - 1] + [" ".join(lines[max_lines - 1:])]

    return [fit_text(line, font, scale, thickness, max_width)[0] for line in lines]


def text_width(text, font, scale, thickness):

    return cv2.getTextSize(text, font, scale, thickness)[0][0]


class HUD:

    def __init__(self, student_id):

        self.student_id = student_id
        self.compact = False
        self.session_start = time.time()
        self.smoothed_fps = None

        # (alert_type, message, expires_at)
        self.banner = None

        self._fg = []

    def toggle_compact(self):

        self.compact = not self.compact

    def show_alert(self, alert_type, message, now=None):
        """Show a banner; a lower-priority alert won't hide a more urgent one."""

        if now is None:
            now = time.time()

        if self.banner is not None and now < self.banner[2]:
            if BANNER_STYLES[alert_type][3] < BANNER_STYLES[self.banner[0]][3]:
                return

        self.banner = (alert_type, message, now + ALERT_BANNER_SECONDS)

    def draw(
        self,
        frame,
        fps,
        backend_connected,
        presence,
        drowsy,
        eye=None,
        head=None,
        gaze=None,
        attention=None,
        now=None
    ):
        """
        Draw the dashboard onto `frame` in place.
        eye / head / gaze / attention are None while no face is detected.
        """

        if now is None:
            now = time.time()

        height, width = frame.shape[:2]

        # Smooth the FPS so the number doesn't flicker
        if self.smoothed_fps is None:
            self.smoothed_fps = fps
        else:
            self.smoothed_fps = 0.9 * self.smoothed_fps + 0.1 * fps

        score = attention["score"] if attention else None

        overlay = frame.copy()
        self._fg = []

        # -----------------------------
        # Pass 1: backgrounds on overlay
        # -----------------------------

        compact = (
            self.compact
            or width < FULL_MIN_WIDTH
            or height < FULL_MIN_HEIGHT
        )

        if compact:
            box = self._compact_score(overlay, score)

        else:
            box = self._panel(
                overlay, height, score, attention, eye, head, gaze,
                presence, drowsy, backend_connected
            )
            self._status_bar(overlay, width, height, now)

        self._banner(overlay, box, width, now)

        # -----------------------------
        # Pass 2: one blend, then solid
        # foreground on top
        # -----------------------------

        cv2.addWeighted(overlay, OVERLAY_ALPHA, frame, 1 - OVERLAY_ALPHA, 0, dst=frame)

        for draw_op in self._fg:
            draw_op(frame)

        if drowsy["drowsy"]:
            self._drowsy_border(frame, width, height, now)

        return frame

    # -----------------------------
    # Components
    # -----------------------------

    def _panel(
        self, overlay, height, score, attention, eye, head, gaze,
        presence, drowsy, backend_connected
    ):

        x0, y0 = MARGIN, MARGIN
        x1 = x0 + PANEL_WIDTH
        left, right = x0 + PAD, x1 - PAD
        inner = right - left

        # Lowest baseline allowed, so nothing spills below the panel
        max_y = height - STATUS_BAR_HEIGHT - MARGIN - PAD

        color = score_color(score)

        # Title
        y = y0 + 26
        self._text("Focus Monitor", (left, y), HEADING_FONT, 0.6, WHITE, max_width=inner)
        self._line((left, y + 10), (right, y + 10))

        # Large score + label
        y += 54
        self._text(
            f"{score}%" if score is not None else "--",
            (left, y), HEADING_FONT, 1.4, color, thickness=2
        )
        self._text_right("ATTENTION", right, y, BODY_FONT, 0.4, MUTED)

        # Progress bar
        y += 12
        self._bar(overlay, left, y, inner, 10, score, color)

        # Status label
        y += 32
        status = attention["status"] if attention else "No Face Detected"
        self._text(status, (left, y), BODY_FONT, 0.55, color, max_width=inner)
        self._line((left, y + 12), (right, y + 12))

        # Detail rows
        if eye is not None:
            eyes_value = ("Open", GREEN) if eye["eyes_open"] else ("Closed", RED)
            blink_value = (f"{eye['blink_rate']:.1f}", WHITE)
        else:
            eyes_value = blink_value = ("--", MUTED)

        if presence["status"] == "Present":
            face_value = ("Present", GREEN)
        else:
            face_value = (f"Absent {presence['absent_time']}s", AMBER)

        rows = [
            ("Eyes", *eyes_value),
            ("Head", head["direction"] if head else "--", WHITE if head else MUTED),
            ("Gaze", gaze["gaze"] if gaze else "--", WHITE if gaze else MUTED),
            ("Blinks/min", *blink_value),
            ("Yawns (session)", str(drowsy["yawn_count"]), WHITE),
            ("Face", *face_value),
        ]

        y += 34

        for label, value, value_color in rows:

            if y > max_y:
                break

            self._row(label, value, value_color, left, right, y)
            y += ROW_HEIGHT

        # Backend row with a status dot
        if y + 14 <= max_y:

            self._line((left, y - 10), (right, y - 10))
            y += 14

            dot_color = GREEN if backend_connected else RED
            value = "Connected" if backend_connected else "Offline"

            self._text("Backend", (left, y), BODY_FONT, 0.5, MUTED)
            value_x = self._text_right(value, right, y, BODY_FONT, 0.5, WHITE)
            self._circle((value_x - 10, y - 5), 5, dot_color)

            y += ROW_HEIGHT

        y1 = min(y - ROW_HEIGHT + PAD + 2, max_y + PAD)
        cv2.rectangle(overlay, (x0, y0), (x1, y1), PANEL_BG, -1)

        return x1, y1

    def _compact_score(self, overlay, score):

        x0, y0 = MARGIN, MARGIN
        x1, y1 = x0 + COMPACT_WIDTH, y0 + 62
        left = x0 + PAD
        inner = COMPACT_WIDTH - 2 * PAD

        color = score_color(score)

        cv2.rectangle(overlay, (x0, y0), (x1, y1), PANEL_BG, -1)

        self._text(
            f"{score}%" if score is not None else "--",
            (left, y0 + 34), HEADING_FONT, 1.0, color, thickness=2
        )
        self._text_right("FOCUS", x1 - PAD, y0 + 34, BODY_FONT, 0.4, MUTED)
        self._bar(overlay, left, y0 + 44, inner, 8, score, color)

        return x1, y1

    def _banner(self, overlay, box, width, now):
        """Draw the alert banner to the right of `box` (its right, bottom edges)."""

        if self.banner is None or now >= self.banner[2]:
            return

        alert_type, message, _ = self.banner
        background, accent, title, _ = BANNER_STYLES[alert_type]

        box_right, box_bottom = box

        x0, y0 = box_right + MARGIN, MARGIN
        x1 = width - MARGIN

        # Too narrow next to the score box -> full width, below it
        if x1 - x0 < BANNER_MIN_WIDTH:
            x0, y0 = MARGIN, box_bottom + MARGIN
        text_left = x0 + 6 + PAD
        text_width_max = x1 - PAD - text_left

        lines = wrap_text(message, BODY_FONT, 0.55, 1, text_width_max, max_lines=3)

        y1 = y0 + PAD + 18 + len(lines) * 22 + 4

        cv2.rectangle(overlay, (x0, y0), (x1, y1), background, -1)

        # Solid accent strip on the left
        self._rect((x0, y0), (x0 + 6, y1), accent)

        y = y0 + PAD + 14
        self._text(title, (text_left, y), HEADING_FONT, 0.55, WHITE, max_width=text_width_max)

        for line in lines:
            y += 22
            self._text(line, (text_left, y), BODY_FONT, 0.55, WHITE)

    def _status_bar(self, overlay, width, height, now):

        y0 = height - STATUS_BAR_HEIGHT

        cv2.rectangle(overlay, (0, y0), (width, height), PANEL_BG, -1)

        elapsed = int(now - self.session_start)
        minutes, seconds = divmod(elapsed, 60)

        info = (
            f"FPS {self.smoothed_fps:.0f}   |   "
            f"Session {minutes:02d}:{seconds:02d}   |   "
            f"Student {self.student_id}"
        )

        baseline = height - 10

        hint = "H compact   Q quit"
        hint_x = self._text_right(hint, width - MARGIN, baseline, BODY_FONT, 0.42, MUTED)

        self._text(
            info, (MARGIN, baseline), BODY_FONT, 0.45, WHITE,
            max_width=hint_x - 2 * MARGIN
        )

    def _drowsy_border(self, frame, width, height, now):

        pulse = 0.5 + 0.5 * math.sin(now * 2 * math.pi * PULSE_HZ)

        thickness = int(3 + (BORDER_MAX - 3) * pulse)
        color = (0, 0, int(150 + 105 * pulse))
        half = thickness // 2

        cv2.rectangle(
            frame,
            (half, half),
            (width - 1 - half, height - 1 - half),
            color,
            thickness,
            AA
        )

    # -----------------------------
    # Drawing helpers (queued for
    # the foreground pass)
    # -----------------------------

    def _bar(self, overlay, x, y, width, height, score, color):

        cv2.rectangle(overlay, (x, y), (x + width, y + height), TRACK, -1)

        if score:
            fill = int(width * max(0, min(score, 100)) / 100)
            self._rect((x, y), (x + fill, y + height), color)

    def _row(self, label, value, value_color, left, right, y):

        self._text(label, (left, y), BODY_FONT, 0.5, MUTED)

        label_width = text_width(label, BODY_FONT, 0.5, 1)
        value_text, value_scale = fit_text(
            value, BODY_FONT, 0.5, 1, right - left - label_width - 8
        )

        self._text_right(value_text, right, y, BODY_FONT, value_scale, value_color)

    def _text(self, text, org, font, scale, color, thickness=1, max_width=None):

        if max_width is not None:
            text, scale = fit_text(text, font, scale, thickness, max_width)

        self._fg.append(
            lambda f: cv2.putText(f, text, org, font, scale, color, thickness, AA)
        )

    def _text_right(self, text, right, y, font, scale, color, thickness=1):
        """Right-align text to x=right; returns its left x."""

        x = right - text_width(text, font, scale, thickness)
        self._text(text, (x, y), font, scale, color, thickness)

        return x

    def _line(self, p1, p2, color=DIVIDER):

        self._fg.append(lambda f: cv2.line(f, p1, p2, color, 1, AA))

    def _rect(self, p1, p2, color):

        self._fg.append(lambda f: cv2.rectangle(f, p1, p2, color, -1))

    def _circle(self, center, radius, color):

        self._fg.append(lambda f: cv2.circle(f, center, radius, color, -1, AA))
