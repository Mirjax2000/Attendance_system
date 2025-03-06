from pathlib import Path
from time import sleep

import cv2
import face_recognition
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.http.response import HttpResponse, StreamingHttpResponse
from rich.console import Console

from .models import FaceVector

cons = Console()

media_directory = Path(settings.MEDIA_ROOT)
files_directory = Path(settings.BASE_DIR / "files")
# yunet je na detekci obliceje
yunet_file: str = "face_detection_yunet_2023mar.onnx"
yunet: str = str(files_directory.joinpath(yunet_file))


class CamSystems:
    """kamerove funkce"""

    def __init__(self):
        self.face_vectors: dict = {}
        self.last_recon_result: dict = {}
        self.cap = cv2.VideoCapture(0)
        self.width: int = int(self.cap.get(3))
        self.height: int = int(self.cap.get(4))
        self.face_detector = cv2.FaceDetectorYN.create(
            model=yunet,
            config="",
            input_size=(self.width, self.height),
            score_threshold=0.9,
            nms_threshold=0.3,
            top_k=1,
            backend_id=cv2.dnn.DNN_BACKEND_OPENCV,
            target_id=cv2.dnn.DNN_TARGET_CPU,
        )
        self.face_rgb = None

    def set_fps(self, speed) -> float:
        """set fps"""
        temp_speed = min(speed, 24)
        speed_: float = 1 / temp_speed
        return speed_

    def face_recon_rectangle(self, frame):
        """Face detector a vykresleni ctverce okolo obliceje"""

        _, faces = self.face_detector.detect(frame)
        if faces is not None:
            for face in faces:
                # Yunet vrací souřadnice obdélníku (x, y, w, h)
                face_array = np.array(face)
                x, y, w, h = (
                    int(face_array[0]),
                    int(face_array[1]),
                    int(face_array[2]),
                    int(face_array[3]),
                )
                # Výřez obličeje - oblast zajmu
                face_roi = frame[y : y + h, x : x + w]
                # Převod na RGB pro face_recognition
                if face_roi.size != 0:
                    self.face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
                    cv2.rectangle(
                        frame, (x, y), (x + w, y + h), (108, 255, 2), 2
                    )

    def cam_generator(self, speed: int = 12):
        """vytvari a pretvari 1 snimek z kamery jako jpeg"""
        while True:
            ret, frame = self.cap.read()

            if not ret:
                cons.log("neni video feed")
                break

            self.face_recon_rectangle(frame)

            # Převod snímku na JPEG
            _, jpeg_frame = cv2.imencode(".jpg", frame)
            jpeg_bytes = jpeg_frame.tobytes()

            # generator snímku
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n\r\n"
            )

            # fps
            fps = self.set_fps(speed)
            sleep(fps)

    def cam_stream(
        self, speed: int = 12
    ) -> HttpResponse | StreamingHttpResponse:
        """video stream na endpointu"""
        if not self.cap.isOpened():
            return HttpResponse("Kamera není dostupná", status=500)

        return StreamingHttpResponse(
            self.cam_generator(speed),
            content_type="multipart/x-mixed-replace; boundary=frame",
        )

    def get_result(self, request) -> JsonResponse:
        """posli vysledek porovnani"""
        if request.method == "POST":
            if hasattr(self, 'last_recon_result') and self.last_recon_result["message"] != "reset":
                return JsonResponse(self.last_recon_result)

            return JsonResponse({"message": "fail"})

        return JsonResponse({"message": "Špatná metoda u porovani"}, status=400)

    def release_camera(self):
        """Uvolní kameru při ukončení"""
        if self.cap.isOpened():
            self.cap.release()

    def __del__(self):
        """uvolni kameru při zničení instance"""
        self.release_camera()
