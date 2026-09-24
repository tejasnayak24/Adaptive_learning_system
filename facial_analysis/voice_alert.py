"""
Voice alerts (beep + text-to-speech) for the Facial Analysis module.

Everything is played on a single background thread so the camera loop
never blocks while an alert is speaking. pyttsx3 is not thread-safe,
so the engine is created and used only inside that worker thread.
"""

import queue
import sys
import threading

from config import (
    VOICE_ALERTS_ENABLED,
    VOICE_RATE,
    VOICE_VOLUME,
    BEEP_FREQUENCY,
    BEEP_DURATION_MS,
)

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import winsound
except ImportError:
    winsound = None


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

    def say(self, message, beep=False):
        """Queue an alert. Never blocks the caller."""

        if not self.enabled:
            return

        try:
            self.queue.put_nowait((message, beep))
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

            message, beep = item

            print(f"[Voice Alert] {message}")

            if beep:
                self._beep()

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
            return engine

        except Exception as e:
            print("Voice Alert Error: could not start text-to-speech:", e)
            return None

    def _beep(self):

        try:
            if winsound is not None:
                winsound.Beep(BEEP_FREQUENCY, BEEP_DURATION_MS)
            else:
                sys.stdout.write("\a")
                sys.stdout.flush()

        except Exception as e:
            print("Voice Alert Error:", e)
