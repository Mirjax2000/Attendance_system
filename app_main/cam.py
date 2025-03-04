from pathlib import Path
from time import sleep

import cv2
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.http.response import HttpResponse, StreamingHttpResponse
from django.utils.timezone import now
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


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

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
    cap = cv2.VideoCapture(0)
    directory = Path(settings.MEDIA_ROOT)
    global capture_frame
    if not cap.isOpened():
        return HttpResponse("Kamera není dostupná", status=500)

    def generate():
        global capture_frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detekce obličejů
            flip = cv2.flip(frame, 1)
            gray = cv2.cvtColor(flip, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30)
            )

            # Kreslení rámečků kolem obličejů
            for x, y, w, h in faces:
                cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # sejmuti obrazku a vytvoreni vektoru
            if capture_frame:
                for x, y, w, h in faces:
                    # vyber oblasti obliceje
                    face_roi = gray[y : y + h, x : x + w]
                    # resize na 200x200 -> standart resolution pro face recon
                    face_resized = cv2.resize(face_roi, (200, 200))
                    # sejmuti face vektoru a ulozeni do variable
                    new_face_vector = np.array(face_resized, dtype=np.uint8)
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
                    face_recon(new_face_vector, face_vectors)

            # Převod snímku na JPEG
            _, jpeg_frame = cv2.imencode(".jpg", gray)
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
