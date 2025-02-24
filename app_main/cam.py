from pathlib import Path
from time import sleep

import cv2
from django.conf import settings
from django.http.response import HttpResponse, StreamingHttpResponse

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def video_stream(request, speed: int = 10):
    """video stream"""
    # cap = cv2.VideoCapture(0)
    directory = Path(settings.MEDIA_ROOT)
    current_movie = str(directory.joinpath("sample.mp4"))
    print(current_movie)
    movie = cv2.VideoCapture(current_movie)

    if not movie.isOpened():
        return HttpResponse("Kamera není dostupná", status=500)

    def generate():
        while True:
            ret, frame = movie.read()
            if not ret:
                break

            # Detekce obličejů
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30)
            )

            # Kreslení rámečků kolem obličejů
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

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
