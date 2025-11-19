import cv2


class ConeDetector:
    def __init__(self, cam_index=0):
        self.cam = cv2.VideoCapture(cam_index)

    def get_frame(self):
        ret, frame = self.cam.read()
        if not ret:
            return None
        return frame
