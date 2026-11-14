import time

import voice_alert
import windows_privacy


class _SlowEngine:
    spoken = []

    def __init__(self, *args, **kwargs):
        pass

    def setProperty(self, *args):
        pass

    def getProperty(self, name):
        return []

    def say(self, message):
        _SlowEngine.spoken.append(message)

    def runAndWait(self):
        time.sleep(0.3)

    def stop(self):
        pass


class _FakePyttsx3:
    Engine = _SlowEngine


def test_say_never_blocks_and_speaks_on_worker_thread(monkeypatch):
    monkeypatch.setattr(voice_alert, "pyttsx3", _FakePyttsx3)
    monkeypatch.setattr(voice_alert, "winsound", None)
    _SlowEngine.spoken = []

    voice = voice_alert.VoiceAlert(enabled=True)
    started = time.perf_counter()
    for i in range(5):
        voice.say(f"alert {i}")
    elapsed = time.perf_counter() - started
    assert elapsed < 0.05  # queueing is instant even though speech takes 0.3 s each

    voice.shutdown(timeout=3)
    # The bounded queue drops a stale backlog instead of reading it all out.
    assert 1 <= len(_SlowEngine.spoken) < 5
    assert _SlowEngine.spoken[0] == "alert 0"


def test_disabled_voice_is_silent():
    voice = voice_alert.VoiceAlert(enabled=False)
    voice.say("ignored")
    voice.shutdown()
    assert voice.worker is None


def test_privacy_settings_block_detected(monkeypatch):
    monkeypatch.setattr(windows_privacy.sys, "platform", "win32")
    values = iter(["Allow", "Allow", "Deny"])
    monkeypatch.setattr(windows_privacy, "_read_value", lambda root, key: next(values))

    status = windows_privacy.camera_privacy_status()
    assert status["blocked"] is True
    assert "Desktop apps" in status["reason"]


def test_privacy_settings_allowed_or_unknown(monkeypatch):
    monkeypatch.setattr(windows_privacy.sys, "platform", "win32")
    monkeypatch.setattr(windows_privacy, "_read_value", lambda root, key: "Allow")
    assert windows_privacy.camera_privacy_status()["blocked"] is False

    monkeypatch.setattr(windows_privacy, "_read_value", lambda root, key: None)
    assert windows_privacy.camera_privacy_status()["blocked"] is None
