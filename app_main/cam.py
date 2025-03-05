"""funkce pro ovladani camstreamu"""

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
yunet: str = str(files_directory.joinpath("face_detection_yunet_2023mar.onnx"))
# flag z fetche z tlacitka SCAN
capture_frame: bool = False
recon_result: dict = {}


def get_vectors_from_db() -> dict:
    """get vectors form db"""
    face_vectors_from_db = FaceVector.objects.values(
        "employee__slug", "face_vector"
    )

    face_vectors_ = {}
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


face_vectors = get_vectors_from_db()


def porovnani(vektor1, vektor2):
    """Porovnávací algoritmus"""

    return np.linalg.norm(vektor1 - vektor2)


def face_recon(vektor1, vectors_from_db):
    """Porovnání nového vektoru se všemi uloženými"""
    vectors: dict = vectors_from_db
    best_match = None
    min_distance = float("inf")
    threshold = 0.6  # Experimentálně nastavit, podle přesnosti modelu

    for name, stored_vector in vectors.items():
        distance = porovnani(vektor1, stored_vector)
        print(f"{name}: {distance:.4f}")

        if distance < min_distance:
            min_distance = distance
            best_match = name

    # Vyhodnocení výsledku
    if min_distance < threshold:
        cons.log(f"Rozpoznán: {best_match} (Vzdálenost: {min_distance:.4f})")
        return {"name": best_match, "message": "success"}
    cons.log("Neznámý obličej!")
    return {"message": "error", "name": "neznamy oblicej"}


def get_result(request) -> JsonResponse:
    """posli vysledek porovnani"""
    global recon_result
    if request.method == "POST":
        if recon_result["message"] == "success":
            return JsonResponse(recon_result)
        elif recon_result["message"] == "error":
            return JsonResponse({"message": "nebyl face vektor"})

        return JsonResponse({"message": "fail"})

    return JsonResponse({"message": "Špatná metoda u porovani"}, status=400)


def capture_photo(request) -> JsonResponse:
    """capture img"""
    global capture_frame, recon_result
    if request.method == "POST":
        recon_result = {"message": "reset"}
        capture_frame = True

        return JsonResponse({"message": "success"})

    return JsonResponse({"message": "fail"}, status=400)


def cam_stream(request, speed: int = 12):
    """video stream"""
    # na flag z fetche
    global capture_frame, recon_result
    # video init
    cap = cv2.VideoCapture(0)
    width, height = int(cap.get(3)), int(cap.get(4))
    if not cap.isOpened():
        return HttpResponse("Kamera není dostupná", status=500)
    # Yunet
    face_detector = cv2.FaceDetectorYN.create(
        yunet, "", (width, height), 0.9, 0.3, 1
    )

    def generate():
        global capture_frame, recon_result
        while True:
            ret, frame = cap.read()

            if not ret:
                cons.log("neni video feed")
                break

            # flip = cv2.flip(frame, 1)
            # Detekce obličejů pomocí Yunet
            _, faces = face_detector.detect(frame)

            # Pokud jsou detekovány obličeje
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
                        face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
                        cv2.rectangle(
                            frame, (x, y), (x + w, y + h), (108, 255, 2), 2
                        )

                        # sejmuti obrazku a vytvoreni vektoru
                        if capture_frame:
                            global recon_result
                            # Získání 128-dim vektoru obličeje
                            face_encoding = face_recognition.face_encodings(
                                face_rgb, num_jitters=2, model="large"
                            )
                            if face_encoding:
                                new_face_vector = face_encoding[0]
                                cons.log("Vektor sejmut!")
                                recon_result = face_recon(
                                    new_face_vector, face_vectors
                                )

                            else:
                                recon_result = {
                                    "message": "error",
                                    "name": "vektor nesejmuto",
                                }
                                cons.log("Face vektor nesejmut")

                            capture_frame = False  # Reset flagu

            # Převod snímku na JPEG
            _, jpeg_frame = cv2.imencode(".jpg", frame)
            jpeg_bytes = jpeg_frame.tobytes()

            # Odeslání snímku jako část MJPEG streamu
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n\r\n"
            )

            temp_speed = min(speed, 24)
            speed_: float = 1 / temp_speed

            sleep(speed_)

    return StreamingHttpResponse(
        generate(), content_type="multipart/x-mixed-replace; boundary=frame"
    )
