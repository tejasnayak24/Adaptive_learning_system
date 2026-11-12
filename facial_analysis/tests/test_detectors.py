"""Existing detectors, exercised with synthetic landmarks."""

from eye_tracker import EyeTracker
from gaze_tracker import GazeTracker
from head_pose import HeadPoseEstimator
from looking_away import LookingAwayDetector
from synthetic import face
from yawn_detector import YawnDetector


def test_eye_aspect_ratio_open_and_closed():
    tracker = EyeTracker()
    open_result = tracker.process(face(eye_opening=0.03))
    assert open_result["ear"] == 0.3
    assert open_result["eyes_open"] is True

    closed_result = tracker.process(face(eye_opening=0.01))
    assert closed_result["ear"] == 0.1
    assert closed_result["eyes_open"] is False


def test_blink_counted_after_consecutive_closed_frames():
    tracker = EyeTracker()
    for _ in range(EyeTracker.CONSECUTIVE_FRAMES):
        tracker.process(face(eye_opening=0.01))
    result = tracker.process(face(eye_opening=0.03))
    assert result["blink"] is True
    assert result["blink_count"] == 1


def test_gaze_directions():
    gaze = GazeTracker()
    assert gaze.process(face(iris_offset=0.0))["gaze"] == "Center"
    assert gaze.process(face(iris_offset=-0.2))["gaze"] == "Left"
    assert gaze.process(face(iris_offset=0.2))["gaze"] == "Right"


def test_head_pose_directions():
    head = HeadPoseEstimator()
    assert head.process(face())["direction"] == "Forward"
    assert head.process(face(yaw_offset=0.05))["direction"] == "Left"
    assert head.process(face(yaw_offset=-0.05))["direction"] == "Right"
    assert head.process(face(pitch_offset=0.06))["direction"] == "Down"
    assert head.process(face(pitch_offset=-0.06))["direction"] == "Up"


def test_yawn_requires_sustained_open_mouth():
    yawn = YawnDetector()
    for _ in range(yawn.required_frames - 1):
        assert yawn.process(face(mouth_opening=0.08))["yawning"] is False
    assert yawn.process(face(mouth_opening=0.08))["yawning"] is True
    # Closing the mouth ends the yawn.
    assert yawn.process(face(mouth_opening=0.01))["yawning"] is False


def test_looking_away_must_be_sustained():
    detector = LookingAwayDetector(threshold_seconds=2.0)

    glance = detector.process("Left", "Center", now=100.0)
    assert glance["looking_away_instant"] is True
    assert glance["looking_away"] is False

    assert detector.process("Left", "Center", now=101.5)["looking_away"] is False
    assert detector.process("Left", "Center", now=102.1)["looking_away"] is True

    # Looking back resets the timer.
    assert detector.process("Forward", "Center", now=102.5)["looking_away"] is False
    assert detector.process("Forward", "Left", now=103.0)["looking_away"] is False
