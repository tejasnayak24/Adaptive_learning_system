import time


class FacePresence:

    def __init__(self):
        self.absent_start = None
        self.absent_duration = 0
        self.status = "Present"

    def update(self, face_found):

        if face_found:
            self.absent_start = None
            self.absent_duration = 0
            self.status = "Present"

        else:
            if self.absent_start is None:
                self.absent_start = time.time()

            self.absent_duration = int(time.time() - self.absent_start)
            self.status = "Absent"

        return {
            "status": self.status,
            "absent_time": self.absent_duration
        }