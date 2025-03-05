from pathlib import Path
from time import sleep

import cv2
import face_recognition
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.http.response import HttpResponse, StreamingHttpResponse
from rich.console import Console

from .models import Employee, FaceVector

cons = Console()

face_vectors_from_db = FaceVector.objects.all()

face_vectors = {}
if face_vectors_from_db.exists():
    for face_vector in face_vectors_from_db:
        face_vectors[face_vector.employee.slug] = np.array(
            face_vector.face_vector
        )
    cons.log(face_vectors)
else:
    cons.log("Tabulka FaceVector je prazdna")
    face_vectors = {}


capture_frame: bool = False


def porovnani(vektor1, vektor2):
    """Porovnávací algoritmus"""

    return np.linalg.norm(vektor1 - vektor2)


def face_recon(vektor1, vectors_from_db):
    """Porovnání nového vektoru se všemi uloženými"""
    vektors = vectors_from_db
    best_match = ""
    min_distance = float("inf")
    threshold = 0.0  # Experimentálně nastavit, podle přesnosti modelu

    for name, stored_vector in vektors.items():
        distance = porovnani(vektor1, stored_vector)
        print(f"{name}: {distance:.4f}")

        if distance < min_distance:
            min_distance = distance
            best_match = name

    # Vyhodnocení výsledku
    if min_distance < threshold:
        print(f"Rozpoznán: {best_match} (Vzdálenost: {min_distance:.4f})")
    else:
        print("Neznámý obličej!")


def capture_photo(request):
    """capture img"""
    global capture_frame
    if request.method == "POST":
        capture_frame = True

        return JsonResponse({"message": "Snímek bude zachycen"})
    return JsonResponse({"error": "Špatná metoda"}, status=400)


def cam_stream(request, speed: int = 12):
    """video stream"""
    # na flag z fetche
    global capture_frame
    # dir init
    media_directory = Path(settings.MEDIA_ROOT)
    files_directory = Path(settings.BASE_DIR / "files")
    # video init
    cap = cv2.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))
    if not cap.isOpened():
        return HttpResponse("Kamera není dostupná", status=500)
    # Yunet path
    yunet: str = str(
        files_directory.joinpath("face_detection_yunet_2023mar.onnx")
    )
    # Yunet
    face_detector = cv2.FaceDetectorYN.create(
        yunet, "", (width, height), 0.9, 0.3, 1
    )

    def generate():
        global capture_frame
        while True:
            ret, frame = cap.read()
            if not ret:
                cons.log("neni video feed")
                break

            # Detekce obličejů
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
                    face_roi = frame[y:y+h, x:x+w]
                    # Převod na RGB pro face_recognition
                    face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)

        
                    # Nakreslíme obdélník kolem obličeje
                    cv2.rectangle(
                        frame, (x, y), (x + w, y + h), (108, 255, 2), 2
                    )


            # sejmuti obrazku a vytvoreni vektoru
            if capture_frame:
                # Získání 128-dim vektoru obličeje
                face_encoding = face_recognition.face_encodings(face_rgb)
                # try:
                #     employee = Employee.objects.get(
                #         slug="kerel-smachka"
                #     )  # Najde zaměstnance podle slug
                #     face_vector_entry, created = (
                #         FaceVector.objects.update_or_create(
                #             employee=employee,  # Odkaz na zaměstnance
                #             defaults={
                #                 "face_vector": new_face_vector
                #             },  # Aktualizace sloupce face_vector
                #         )
                #     )
                #     if created:
                #         cons.log(
                #             "Nový FaceVector vytvořen pro 'kerel-smachka'"
                #         )
                #     else:
                #         cons.log(
                #             "FaceVector aktualizován pro 'kerel-smachka'"
                #         )

                # except Employee.DoesNotExist:
                #     cons.log("Zaměstnanec 'kerel-smachka' nebyl nalezen.")
                #     cons.log(f"face vektor: sejmuto")

                capture_frame = False  # Reset flagu
                # face_recon(new_face_vector, face_vectors)

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
