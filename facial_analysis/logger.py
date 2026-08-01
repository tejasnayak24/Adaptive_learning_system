import csv
import os
from datetime import datetime


class SessionLogger:

    def __init__(self):

        self.filename = "logs/session_log.csv"

        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp",
                    "Attention",
                    "Status",
                    "Head Direction",
                    "Eyes Open",
                    "Blink Count",
                    "Blink Rate"
                ])

    def log(
        self,
        attention,
        status,
        head_direction,
        eyes_open,
        blink_count,
        blink_rate
    ):

        with open(self.filename, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                attention,
                status,
                head_direction,
                eyes_open,
                blink_count,
                blink_rate
            ])