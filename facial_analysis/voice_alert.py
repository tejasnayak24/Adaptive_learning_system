"""
Voice alerts (beep + text-to-speech) for the Facial Analysis module.

Everything is played on a single background thread so the camera loop
never blocks while an alert is speaking. pyttsx3 is not thread-safe,
so the engine is created and used only inside that worker thread.
"""

import queue
import sys
import threading
import time

from config import (
    VOICE_ALERTS_ENABLED,
    VOICE_RATE,
    VOICE_VOLUME,
    PREFERRED_VOICE_LANGUAGES,
    BEEP_FREQUENCY,
    BEEP_DURATION_MS,
    BEEP_GAP_MS,
)

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import winsound
except ImportError:
    winsound = None


# Windows (SAPI5) voices often have no language code, only a name
# like "Microsoft Zira Desktop - English (United States)".
LANGUAGE_NAMES = {
    "en-in": "india",
    "en-us": "united states",
    "en-gb": "great britain",
}


def pick_voice(voices, preferred=PREFERRED_VOICE_LANGUAGES):
    """Return the first voice matching the preferred languages, in order."""

    for language in preferred:
        for voice in voices:
            if _voice_matches(voice, language):
                return voice

    return None


def _voice_matches(voice, language):

    language = language.lower()

    codes = []

    for code in getattr(voice, "languages", None) or []:
        if isinstance(code, bytes):
            code = code.decode("utf-8", errors="ignore")
        codes.append(str(code))

    # Normalise "TTS_MS_EN-US_ZIRA" / "en_US" to "en-us"
    text = " ".join(
        [voice.id or "", voice.name or ""] + codes
    ).lower().replace("_", "-")

    country = LANGUAGE_NAMES.get(language)

    return language in text or (country is not None and country in text)


class VoiceAlert:

    def __init__(self, enabled=VOICE_ALERTS_ENABLED):

        self.enabled = enabled
        self.worker = None

        # Small queue: if alerts arrive while one is still playing,
        # drop them instead of reading out a stale backlog.
        self.queue = queue.Queue(maxsize=2)

        if not self.enabled:
            return

        if pyttsx3 is None:
            print("Voice Alert: pyttsx3 not installed, alerts will only be printed.")

        self.worker = threading.Thread(target=self._run, daemon=True)
        self.worker.start()

    def say(self, message, beeps=0, beep_ms=BEEP_DURATION_MS):
        """Queue an alert (optionally preceded by beeps). Never blocks the caller."""

        if not self.enabled:
            return

        try:
            self.queue.put_nowait((message, beeps, beep_ms))
        except queue.Full:
            pass

    def shutdown(self, timeout=2.0):
        """Stop the worker thread (waits for the current alert to finish)."""

        if self.worker is None:
            return

        try:
            self.queue.put(None, timeout=timeout)
        except queue.Full:
            return

        self.worker.join(timeout)

    # -----------------------------
    # Worker Thread
    # -----------------------------

    def _run(self):

        engine = self._init_engine()

        while True:

            item = self.queue.get()

            if item is None:
                break

            message, beeps, beep_ms = item

            print(f"[Voice Alert] {message}")

            self._beep(beeps, beep_ms)

            if engine is None:
                continue

            try:
                engine.say(message)
                engine.runAndWait()
            except Exception as e:
                print("Voice Alert Error:", e)

    def _init_engine(self):

        if pyttsx3 is None:
            return None

        # On Windows, SAPI5 needs COM initialised in the thread using it
        try:
            import comtypes
            comtypes.CoInitialize()
        except Exception:
            pass

        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", VOICE_RATE)
            engine.setProperty("volume", VOICE_VOLUME)

            voice = pick_voice(engine.getProperty("voices"))

            if voice is not None:
                engine.setProperty("voice", voice.id)
                print(f"Voice Alert: using voice '{voice.name}'")

            return engine

        except Exception as e:
            print("Voice Alert Error: could not start text-to-speech:", e)
            return None

    def _beep(self, count, duration_ms):

        try:
            for i in range(count):

                if i > 0:
                    time.sleep(BEEP_GAP_MS / 1000)

                if winsound is not None:
                    winsound.Beep(BEEP_FREQUENCY, duration_ms)
                else:
                    sys.stdout.write("\a")
                    sys.stdout.flush()

        except Exception as e:
            print("Voice Alert Error:", e)
