"""
Adaptive Learning System (Aegis)
Facial Analysis Module -- local camera agent

Features:

- Face Detection
- Eye Tracking (EAR)
- Blink Detection
- Gaze Detection
- Head Pose Estimation
- Attention Scoring
- Looking Away Detection (sustained)
- Yawning Detection
- Face Presence Detection
- Possible-drowsiness alerts (sustained eye closure) with voice alerts
- On-screen Dashboard (HUD)
- Session Logging

Usage:

    python main.py            # run the camera agent (normal use)
    python main.py --preview  # local camera preview only, no backend

In agent mode the webcam stays OFF until the Aegis website starts a
learning session. The website pairs with this agent through
http://127.0.0.1:8765; the student id is never configured here -- the
backend derives it from the session token.
"""

import argparse
import signal
import sys
import time

from config import AGENT_HOST, AGENT_PORT, SHOW_HUD


def run_agent(display):
    from agent_server import AgentServer
    from monitor import MonitoringController
    from voice_alert import VoiceAlert

    voice = VoiceAlert()
    controller = MonitoringController(voice=voice, display=display)

    try:
        server = AgentServer(controller).start()
    except OSError as exc:
        print(
            f"Could not listen on http://{AGENT_HOST}:{AGENT_PORT} ({exc}).\n"
            "Is another Aegis camera agent already running?",
            file=sys.stderr,
        )
        return 1

    print(f"Aegis camera agent ready on http://{AGENT_HOST}:{server.port}")
    print("The webcam stays off until you start a lesson on the Aegis website.")
    print("Press Ctrl+C to quit.")

    def _stop(*_):
        controller.shutdown()

    signal.signal(signal.SIGINT, _stop)

    try:
        controller.run_forever()
    except KeyboardInterrupt:
        controller.shutdown()
    finally:
        server.stop()
        voice.shutdown()

    return 0


def run_preview():
    """Standalone preview of every detector, without the backend."""
    import cv2

    from camera import Camera, CameraError
    from frame_processor import FrameProcessor
    from hud import HUD
    from logger import SessionLogger
    from voice_alert import VoiceAlert

    try:
        camera = Camera()
    except CameraError as exc:
        print(f"Camera error ({exc.code}): {exc.message}", file=sys.stderr)
        return 1

    processor = FrameProcessor()
    hud = HUD("preview")
    voice = VoiceAlert()
    logger = SessionLogger()

    prev_time = time.time()
    last_log_time = time.time()

    try:
        while True:
            frame = camera.read_frame()
            if frame is None:
                break

            now = time.time()
            result = processor.process(frame, now=now)

            for alert in result["drowsy"]["alerts"]:
                voice.say(alert["message"], beeps=alert["beeps"], beep_ms=alert["beep_ms"])
                hud.show_alert(alert["type"], alert["message"])

            if result["face_detected"] and now - last_log_time >= 1:
                logger.log(
                    attention=result["attention"]["score"],
                    status=result["attention"]["status"],
                    head_direction=result["head"]["direction"],
                    eyes_open=result["eye"]["eyes_open"],
                    blink_count=result["eye"]["blink_count"],
                    blink_rate=result["eye"]["blink_rate"],
                )
                last_log_time = now

            elapsed = now - prev_time
            fps = 1 / elapsed if elapsed > 0 else 0
            prev_time = now

            if SHOW_HUD:
                hud.draw(
                    result["frame"],
                    fps=fps,
                    backend_connected=False,
                    presence=result["presence"],
                    drowsy=result["drowsy"],
                    eye=result["eye"],
                    head=result["head"],
                    gaze=result["gaze"],
                    attention=result["attention"],
                )

            cv2.imshow("Aegis Facial Analysis - Preview", result["frame"])
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("h"):
                hud.toggle_compact()
    finally:
        voice.shutdown()
        camera.release()
        cv2.destroyAllWindows()

    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Aegis facial analysis camera agent")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show a local camera preview without connecting to the backend",
    )
    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Agent mode without the on-screen camera window",
    )
    args = parser.parse_args(argv)

    if args.preview:
        return run_preview()
    return run_agent(display=SHOW_HUD and not args.no_window)


if __name__ == "__main__":
    raise SystemExit(main())
