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
        self.cap = cv2.VideoCapture(0)
        self.database = Database()
        self.utility = Utility()
        self.face_vectors: dict = self.database.get_vectors_from_db()
        self.last_recon_result: dict = {}
        self.face_detector = self.create_detector()
        self.face_rgb = None

    def create_detector(self):
        """Create face detector"""
        width: int = int(self.cap.get(3))
        height: int = int(self.cap.get(4))
        face_detector = cv2.FaceDetectorYN.create(
            model=yunet,
            config="",
            input_size=(width, height),
            score_threshold=0.9,
            nms_threshold=0.3,
            top_k=1,
            backend_id=cv2.dnn.DNN_BACKEND_OPENCV,
            target_id=cv2.dnn.DNN_TARGET_CPU,
        )
        return face_detector

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
                else:
                    self.face_rgb = None
        else:
            self.face_rgb = None

    def cam_generator(self, speed: int = 12):
        """vytvari a pretvari 1 snimek z kamery jako jpeg"""
        while True:
            ret, frame = self.cap.read()

            if not ret:
                cons.log("neni video feed")
                empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                _, jpeg_frame = cv2.imencode(".jpg", empty_frame)
                jpeg_bytes = jpeg_frame.tobytes()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + jpeg_bytes
                    + b"\r\n\r\n"
                )
                continue

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
            fps = self.utility.set_fps(speed)
            sleep(fps)

    def cam_stream(
        self, speed: int = 12
    ) -> HttpResponse | StreamingHttpResponse:
        """video stream na endpointu"""
        if not self.cap.isOpened():
            cons.log("Kamera neni dostupna")
            return HttpResponse("Kamera není dostupná", status=500)

        return StreamingHttpResponse(
            self.cam_generator(speed),
            content_type="multipart/x-mixed-replace; boundary=frame",
        )

    def face_recon(self, vektor1, vectors_from_db):
        """Porovnání nového vektoru se všemi uloženými"""
        vectors: dict = vectors_from_db
        best_match = None
        min_distance = float("inf")
        threshold = 0.6  # Experimentálně nastavit, podle přesnosti modelu

        for name, stored_vector in vectors.items():
            distance = self.utility.porovnani(vektor1, stored_vector)
            print(f"{name}: {distance:.4f}")

            if distance < min_distance:
                min_distance = distance
                best_match = name

        # Vyhodnocení výsledku
        if min_distance < threshold:
            cons.log(
                f"Rozpoznán: {best_match} (Vzdálenost: {min_distance:.4f})"
            )
            return {"name": best_match, "message": "success"}
        cons.log("Neznámý obličej!")
        return {"message": "neznamy oblicej"}

    def get_result(self):
        """posli vysledek porovnani"""
        if self.face_rgb is None:
            cons.log("face rgb je None, protoze neni rectangle")
            return {"message": "no-face-detected"}

        face_encoding = face_recognition.face_encodings(
            self.face_rgb, num_jitters=2, model="large"
        )

        if face_encoding:
            new_face_vector = face_encoding[0]
            cons.log("Vektor sejmut!")
            self.last_recon_result = self.face_recon(
                new_face_vector, self.face_vectors
            )

        else:
            self.last_recon_result = {
                "message": "no-face-detected",
            }
            cons.log("Face vektor nesejmut")

        self.face_rgb = None
        cons.log(self.last_recon_result)
        return self.last_recon_result

    def release_camera(self):
        """Uvolní kameru při ukončení"""
        if self.cap.isOpened():
            self.cap.release()

    def __del__(self):
        """uvolni kameru při zničení instance"""
        self.release_camera()


class Database:
    """Databse methods"""

    def get_vectors_from_db(self) -> dict:
        """get vectors form db"""
        face_vectors_from_db = FaceVector.objects.values(
            "employee__slug", "face_vector"
        )

        face_vectors_: dict = {}
        if face_vectors_from_db:
            for face_vector in face_vectors_from_db:
                face_vectors_[face_vector["employee__slug"]] = np.array(
                    face_vector["face_vector"]
                )

            cons.log(
                f"Loaded face vectors for employees: {list(face_vectors_.keys())}"
            )
            return face_vectors_

        cons.log("Tabulka FaceVector je prazdna")
        return face_vectors_


class Utility:
    """Utility classes"""

    @staticmethod
    def porovnani(vektor1, vektor2):
        """Porovnávací algoritmus"""
        return np.linalg.norm(vektor1 - vektor2)

    @staticmethod
    def set_fps(speed) -> float:
        """set fps"""
        temp_speed = min(speed, 24)
        speed_: float = 1 / temp_speed
        return speed_
