"""Possible-drowsiness alerts (PR #10 logic) and the frame processor."""

import config
from drowsiness_detector import (
    ALERT_EYES_CLOSED,
    ALERT_FREQUENT_YAWN,
    ALERT_NO_FACE,
    ALERT_YAWN,
    DrowsinessDetector,
)
from frame_processor import FrameProcessor, telemetry_from_result
from synthetic import ScriptedDetector, face


def _types(result):
    return [alert["type"] for alert in result["alerts"]]


def test_sustained_eye_closure_triggers_one_alert_then_repeats_after_cooldown():
    d = DrowsinessDetector()
    t = 1000.0

    assert d.update(True, eyes_open=False, now=t)["drowsy"] is False
    # A blink-length closure never alerts.
    assert _types(d.update(True, eyes_open=False, now=t + 1.0)) == []

    at_threshold = d.update(True, eyes_open=False, now=t + config.EYES_CLOSED_ALERT_SECONDS)
    assert at_threshold["drowsy"] is True
    assert _types(at_threshold) == [ALERT_EYES_CLOSED]

    # Within the repeat cooldown: no second alert.
    assert _types(d.update(True, eyes_open=False, now=t + 4.0)) == []
    repeat = d.update(
        True, eyes_open=False, now=t + config.EYES_CLOSED_ALERT_SECONDS + config.DROWSY_ALERT_REPEAT_SECONDS
    )
    assert _types(repeat) == [ALERT_EYES_CLOSED]


def test_wake_up_alert_escalates_and_resets_when_eyes_open():
    d = DrowsinessDetector()
    t = 0.0
    messages = []
    d.update(True, eyes_open=False, now=t)
    for k in range(config.WAKE_UP_ESCALATE_AFTER + 1):
        now = t + config.EYES_CLOSED_ALERT_SECONDS + k * config.DROWSY_ALERT_REPEAT_SECONDS
        messages += [a["message"] for a in d.update(True, eyes_open=False, now=now)["alerts"]]

    assert messages[: config.WAKE_UP_ESCALATE_AFTER] == [config.WAKE_UP_MESSAGE] * config.WAKE_UP_ESCALATE_AFTER
    assert messages[-1] == config.ESCALATED_WAKE_UP_MESSAGE

    opened = d.update(True, eyes_open=True, now=now + 1)
    assert opened["drowsy"] is False
    assert d.wake_alert_count == 0


def test_no_face_alert_after_threshold():
    d = DrowsinessDetector()
    d.update(False, now=0.0)
    assert _types(d.update(False, now=config.NO_FACE_ALERT_SECONDS - 0.1)) == []
    assert _types(d.update(False, now=config.NO_FACE_ALERT_SECONDS)) == [ALERT_NO_FACE]
    # Without a face, eye state is unknown: never reported as drowsy.
    assert d.update(False, eyes_open=False, now=config.NO_FACE_ALERT_SECONDS + 5)["drowsy"] is False


def test_yawn_alerts_respect_gap_and_frequent_yawn_break():
    d = DrowsinessDetector()

    def yawn(at):
        started = d.update(True, yawning=True, now=at)
        d.update(True, yawning=False, now=at + 0.5)
        return _types(started)

    assert yawn(0.0) == [ALERT_YAWN]
    assert yawn(5.0) == []  # inside YAWN_ALERT_MIN_GAP_SECONDS
    assert yawn(20.0) == [ALERT_FREQUENT_YAWN]  # 3 yawns within the window
    assert d.yawn_count == 3


def _processor(detector, brightness=120.0):
    return FrameProcessor(face_detector=detector, brightness_fn=lambda frame: brightness)


def test_processor_reports_stable_face_and_normalised_attention():
    processor = _processor(ScriptedDetector(face()))
    result = None
    for i in range(30):
        result = processor.process(frame=object(), now=100.0 + i * 0.1)

    telemetry = telemetry_from_result(result)
    assert telemetry["face_detected"] is True
    assert telemetry["face_stable"] is True
    assert telemetry["lighting_ok"] is True
    assert 0.0 <= telemetry["attention_score"] <= 1.0
    assert telemetry["attention_score"] == 1.0
    assert telemetry["looking_away"] is False
    assert telemetry["possible_drowsiness"] is False


def test_processor_without_face_reports_no_measurements():
    detector = ScriptedDetector()
    detector.face_visible = False
    telemetry = telemetry_from_result(_processor(detector).process(object(), now=5.0))

    assert telemetry["face_detected"] is False
    assert telemetry["face_stable"] is False
    assert telemetry["attention_score"] is None
    assert telemetry["yawning"] is None
    assert telemetry["possible_drowsiness"] is None


def test_processor_flags_possible_drowsiness_after_sustained_closure():
    processor = _processor(ScriptedDetector(face(eye_opening=0.01)))
    flags = [
        telemetry_from_result(processor.process(object(), now=50.0 + i * 0.25))["possible_drowsiness"]
        for i in range(12)
    ]
    assert flags[0] is False
    assert flags[-1] is True  # closed for 2.75 s


def test_processor_flags_low_light():
    telemetry = telemetry_from_result(_processor(ScriptedDetector(), brightness=20.0).process(object(), now=1.0))
    assert telemetry["lighting_ok"] is False


def test_brief_face_loss_keeps_face_stable_but_long_loss_does_not():
    detector = ScriptedDetector()
    processor = _processor(detector)
    t = 0.0
    for _ in range(30):
        processor.process(object(), now=t)
        t += 0.1

    detector.face_visible = False
    blip = processor.process(object(), now=t)
    assert blip["face_stable"] is True  # 1 missed frame out of ~20

    for _ in range(20):
        t += 0.1
        last = processor.process(object(), now=t)
    assert last["face_stable"] is False
