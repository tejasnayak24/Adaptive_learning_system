"""Multiple-face detection, kept separate from the attention pipeline.

The attention, eye, gaze, head-pose, yawn and drowsiness measurements come
from MediaPipe Face Mesh on the student's face (``face_detector.py``) and
are not touched here. This module runs MediaPipe *Face Detection*
(BlazeFace, already part of the installed ``mediapipe``) on a downscaled
copy of a frame about twice a second, in its own thread, and only counts
faces.

* ``FaceCounter`` counts *qualifying* faces in one frame: detection
  confidence of at least ``MULTI_FACE_MIN_CONFIDENCE`` and a width of at
  least ``MULTI_FACE_MIN_RELATIVE_SIZE`` of the largest face, so small
  faces far behind the student (a poster, a television) do not count.
* ``MultiFaceTracker`` turns per-sample counts into a *sustained* signal:
  "multiple faces" starts only after two or more faces in most samples of
  a window (about 3 s) and clears after a run of samples below two, so a
  single-frame glitch or someone walking past does not raise a warning.
* ``FaceCountWorker`` runs the counter off the camera loop, so the 30 fps
  attention measurements keep their pace.

Nothing is stored or sent except the count and a yes/no signal. Frames
stay in memory and are discarded. Seeing another face is not evidence of
misconduct (a parent helping is normal); the signal is informational.
"""

import threading
import time
from collections import deque

from config import (
    MULTI_FACE_CLEAR_SAMPLES,
    MULTI_FACE_INTERVAL_SECONDS,
    MULTI_FACE_MIN_CONFIDENCE,
    MULTI_FACE_MIN_RELATIVE_SIZE,
    MULTI_FACE_REQUIRED_SAMPLES,
    MULTI_FACE_RESULT_MAX_AGE_SECONDS,
    MULTI_FACE_WINDOW_SAMPLES,
    MULTI_FACE_WORK_WIDTH,
)


def qualifying_count(boxes, min_confidence=MULTI_FACE_MIN_CONFIDENCE, min_relative=MULTI_FACE_MIN_RELATIVE_SIZE):
    """Count faces from ``(width, confidence)`` pairs (width as a frame fraction)."""
    confident = [w for (w, score) in boxes if score >= min_confidence and w > 0]
    if not confident:
        return 0
    largest = max(confident)
    return sum(1 for w in confident if w >= largest * min_relative)


class FaceCounter:
    """Counts qualifying faces in a BGR frame with MediaPipe Face Detection."""

    def __init__(self, detection=None, work_width=MULTI_FACE_WORK_WIDTH):
        if detection is None:
            import mediapipe as mp

            # model_selection=0: short-range model, for faces within ~2 m.
            detection = mp.solutions.face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=min(0.5, MULTI_FACE_MIN_CONFIDENCE)
            )
        self.detection = detection
        self.work_width = work_width

    def count(self, frame):
        import cv2

        height, width = frame.shape[:2]
        if width > self.work_width:
            scale = self.work_width / width
            frame = cv2.resize(frame, (self.work_width, int(height * scale)), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.detection.process(rgb)
        boxes = []
        for det in results.detections or []:
            box = det.location_data.relative_bounding_box
            boxes.append((float(box.width), float(det.score[0]) if det.score else 0.0))
        return qualifying_count(boxes)

    def close(self):
        try:
            self.detection.close()
        except Exception:
            pass


class MultiFaceTracker:
    """Sustained multiple-face signal from per-sample face counts (pure logic)."""

    def __init__(
        self,
        window=MULTI_FACE_WINDOW_SAMPLES,
        required=MULTI_FACE_REQUIRED_SAMPLES,
        clear_after=MULTI_FACE_CLEAR_SAMPLES,
    ):
        self.window = window
        self.required = required
        self.clear_after = clear_after
        self.samples = deque(maxlen=window)
        self.active = False
        self.below_run = 0
        self.peak = 0

    def update(self, count):
        """Add one sample. Returns ``(active, started, ended)``."""
        multiple = count >= 2
        self.samples.append(multiple)
        started = ended = False
        if not self.active:
            if sum(self.samples) >= self.required:
                self.active = True
                self.below_run = 0
                self.peak = count
                started = True
        else:
            self.peak = max(self.peak, count)
            self.below_run = 0 if multiple else self.below_run + 1
            if self.below_run >= self.clear_after:
                self.active = False
                self.samples.clear()
                ended = True
        return self.active, started, ended

    def reset(self):
        self.samples.clear()
        self.active = False
        self.below_run = 0
        self.peak = 0


class FaceCountWorker:
    """Runs a face counter about twice a second, off the camera loop.

    ``offer(frame, now)`` is called for every camera frame; it only copies
    the frame when a new sample is due and the worker is idle, so the
    camera loop never waits. ``latest(now)`` returns the newest result if
    it is fresh, else ``None`` (not measured).
    """

    def __init__(self, counter_factory=FaceCounter, interval=MULTI_FACE_INTERVAL_SECONDS, clock=time.monotonic):
        self.counter_factory = counter_factory
        self.interval = interval
        self.clock = clock
        self.tracker = MultiFaceTracker()
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._frame = None
        self._last_offer = None
        self._result = None
        self._result_at = None
        self._error = None
        self.samples = 0
        self.busy_seconds = 0.0
        self._thread = threading.Thread(target=self._run, name="aegis-face-count", daemon=True)
        self._thread.start()

    def offer(self, frame, now=None):
        if not hasattr(frame, "shape") or not hasattr(frame, "copy"):
            return False  # not an image (e.g. a synthetic test camera)
        now = self.clock() if now is None else now
        with self._lock:
            if self._frame is not None or self._error is not None:
                return False
            if self._last_offer is not None and now - self._last_offer < self.interval:
                return False
            self._last_offer = now
            self._frame = frame.copy()
        self._wake.set()
        return True

    def latest(self, now=None):
        now = self.clock() if now is None else now
        with self._lock:
            if self._result is None or self._result_at is None:
                return None
            if now - self._result_at > MULTI_FACE_RESULT_MAX_AGE_SECONDS:
                return None
            return dict(self._result)

    @property
    def error(self):
        return self._error

    def _run(self):
        try:
            counter = self.counter_factory()
        except Exception as exc:  # model could not load: the feature is off
            with self._lock:
                self._error = f"face counter unavailable: {exc}"
            return
        try:
            while not self._stop.is_set():
                self._wake.wait(0.5)
                self._wake.clear()
                with self._lock:
                    frame = self._frame
                if frame is None:
                    continue
                started_at = time.perf_counter()
                try:
                    count = counter.count(frame)
                except Exception:
                    count = None
                self.busy_seconds += time.perf_counter() - started_at
                with self._lock:
                    self._frame = None
                    if count is None:
                        continue
                    self.samples += 1
                    active, started, ended = self.tracker.update(count)
                    self._result = {
                        "face_count": count,
                        "multiple_faces": active,
                        "peak_face_count": self.tracker.peak if active else None,
                    }
                    self._result_at = self.clock()
        finally:
            close = getattr(counter, "close", None)
            if close:
                close()

    def stop(self, timeout=2.0):
        self._stop.set()
        self._wake.set()
        self._thread.join(timeout)
