import math
import time


class EyeTracker:

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    EAR_THRESHOLD = 0.23
    CONSECUTIVE_FRAMES = 3

    def __init__(self):

        self.counter = 0
        self.total_blinks = 0

        self.start_time = time.time()

    def distance(self, p1, p2):

        return math.sqrt(
            (p1.x-p2.x)**2 +
            (p1.y-p2.y)**2
        )

    def ear(self, eye, landmarks):

        p1 = landmarks[eye[0]]
        p2 = landmarks[eye[1]]
        p3 = landmarks[eye[2]]
        p4 = landmarks[eye[3]]
        p5 = landmarks[eye[4]]
        p6 = landmarks[eye[5]]

        vertical1 = self.distance(p2,p6)
        vertical2 = self.distance(p3,p5)
        horizontal = self.distance(p1,p4)

        return (vertical1+vertical2)/(2*horizontal)

    def process(self, landmarks):

        lm = landmarks.landmark

        left = self.ear(self.LEFT_EYE,lm)
        right = self.ear(self.RIGHT_EYE,lm)

        ear = (left+right)/2

        eyes_open = ear > self.EAR_THRESHOLD

        blink=False

        if ear < self.EAR_THRESHOLD:

            self.counter+=1

        else:

            if self.counter>=self.CONSECUTIVE_FRAMES:

                self.total_blinks+=1
                blink=True

            self.counter=0

        elapsed=(time.time()-self.start_time)/60

        blink_rate=0

        if elapsed>0:

            blink_rate=self.total_blinks/elapsed

        return {

            "ear":round(ear,3),

            "eyes_open":eyes_open,

            "blink":blink,

            "blink_count":self.total_blinks,

            "blink_rate":round(blink_rate,1)

        }