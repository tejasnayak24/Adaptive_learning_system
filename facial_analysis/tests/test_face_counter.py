"""Multiple-face detection: counting rules, sustained signal, worker thread.

The MediaPipe detector is replaced by scripted results; the rules that
decide what counts as "multiple faces" are tested exactly.
"""

import time

import numpy as np

from face_counter import FaceCounter, FaceCountWorker, MultiFaceTracker, qualifying_count
from monitor import _face_fields


# ---------------------------------------------------------------- counting rule


def test_one_face_counts_as_one():
    assert qualifying_count([(0.30, 0.95)]) == 1


def test_two_close_faces_count_as_two():
    assert qualifying_count([(0.30, 0.95), (0.22, 0.90)]) == 2


def test_small_background_face_is_ignored():
    # A face under 40 % of the student's face width (poster, TV, far away).
    assert qualifying_count([(0.30, 0.95), (0.08, 0.92)]) == 1


def test_low_confidence_detection_is_ignored():
    assert qualifying_count([(0.30, 0.95), (0.28, 0.40)]) == 1


def test_no_faces_counts_as_zero():
    assert qualifying_count([]) == 0


# ---------------------------------------------------------------- sustained signal


def _feed(tracker, counts):
    return [tracker.update(c) for c in counts]


def test_single_or_brief_detections_do_not_raise_the_signal():
    tracker = MultiFaceTracker(window=6, required=5, clear_after=4)
    states = _feed(tracker, [1, 2, 1, 2, 1, 2, 2, 1, 1])
    assert not any(active for active, _, _ in states)


def test_sustained_detection_starts_once_and_clears_after_a_quiet_run():
    tracker = MultiFaceTracker(window=6, required=5, clear_after=4)
    states = _feed(tracker, [2, 2, 2, 2, 2])
    assert states[-1] == (True, True, False)
    # Flicker while active does not end it, and does not restart it.
    states = _feed(tracker, [1, 2, 3, 1, 1, 1])
    assert all(active for active, _, _ in states)
    assert not any(started for _, started, _ in states)
    assert tracker.peak == 3
    active, started, ended = tracker.update(1)
    assert (active, started, ended) == (False, False, True)


def test_signal_needs_a_full_new_window_after_clearing():
    tracker = MultiFaceTracker(window=6, required=5, clear_after=4)
    _feed(tracker, [2] * 5 + [1] * 4)
    assert not tracker.active
    assert not any(active for active, _, _ in _feed(tracker, [2, 2, 2, 2]))
    assert tracker.update(2)[0] is True


# ---------------------------------------------------------------- worker thread


class ScriptedCounter:
    def __init__(self, counts):
        self.counts = list(counts)
        self.seen_shapes = []
        self.closed = False

    def count(self, frame):
        self.seen_shapes.append(frame.shape)
        return self.counts.pop(0) if self.counts else 1

    def close(self):
        self.closed = True


def _wait(predicate, timeout=3.0):
    end = time.time() + timeout
    while time.time() < end:
        if predicate():
            return True
        time.sleep(0.01)
    return False


def test_worker_samples_at_its_own_pace_and_reports_a_fresh_result():
    counter = ScriptedCounter([2] * 10)
    clock = {"t": 100.0}
    worker = FaceCountWorker(counter_factory=lambda: counter, interval=0.5, clock=lambda: clock["t"])
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    try:
        offered = 0
        for _ in range(5):
            assert _wait(lambda: worker._frame is None)
            # Many camera frames arrive; only one per interval is copied.
            results = [worker.offer(frame) for _ in range(30)]
            offered += sum(results)
            assert sum(results) == 1
            assert _wait(lambda: worker._frame is None)
            clock["t"] += 0.5
        assert offered == 5
        latest = worker.latest()
        assert latest == {"face_count": 2, "multiple_faces": True, "peak_face_count": 2}
        clock["t"] += 3.0
        assert worker.latest() is None  # stale results are not reported
    finally:
        worker.stop()
    assert counter.closed


def test_worker_with_unavailable_model_reports_not_measured():
    def broken():
        raise RuntimeError("model missing")

    worker = FaceCountWorker(counter_factory=broken)
    try:
        assert _wait(lambda: worker.error is not None)
        assert worker.offer(np.zeros((10, 10, 3), dtype=np.uint8)) is False
        assert _face_fields(worker) == {"face_count": None, "multiple_faces": None}
    finally:
        worker.stop()


def test_non_image_frames_are_ignored():
    worker = FaceCountWorker(counter_factory=lambda: ScriptedCounter([]))
    try:
        assert worker.offer("frame") is False
    finally:
        worker.stop()


def test_no_worker_means_not_measured():
    assert _face_fields(None) == {"face_count": None, "multiple_faces": None}


# ---------------------------------------------------------------- real detector (no faces)


class _Det:
    def __init__(self, width, score):
        class Box:
            pass

        box = Box()
        box.width = width
        self.location_data = type("L", (), {"relative_bounding_box": box})()
        self.score = [score]


class FakeDetection:
    def __init__(self, detections):
        self.detections = detections
        self.input_shapes = []

    def process(self, rgb):
        self.input_shapes.append(rgb.shape)
        return type("R", (), {"detections": self.detections})()


def test_face_counter_downscales_and_applies_the_rules():
    detection = FakeDetection([_Det(0.3, 0.95), _Det(0.25, 0.9), _Det(0.05, 0.99)])
    counter = FaceCounter(detection=detection, work_width=320)
    assert counter.count(np.zeros((480, 640, 3), dtype=np.uint8)) == 2
    assert detection.input_shapes == [(240, 320, 3)]


def test_real_mediapipe_detector_finds_no_face_in_a_blank_frame():
    counter = FaceCounter()
    try:
        assert counter.count(np.zeros((480, 640, 3), dtype=np.uint8)) == 0
    finally:
        counter.close()
