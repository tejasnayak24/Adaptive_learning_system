import threading
import requests
from datetime import datetime

from config import API_URL


class APIClient:

    def _send(self, payload):

        try:
            requests.post(
                API_URL,
                json=payload,
                timeout=2
            )

        except Exception as e:
            print("Backend Error:", e)

    def send_attention_data(
        self,
        student_id,
        attention_score,
        status,
        eyes_open,
        head_direction,
        looking_away,
        yawning
    ):

       
        payload = {
            "student_id": student_id,
            "attention_score": attention_score,
            "status": status,
            "eyes_open": eyes_open,
            "head_direction": head_direction
        }
        

        threading.Thread(
            target=self._send,
            args=(payload,),
            daemon=True
        ).start()