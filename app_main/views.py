import time

import cv2
from django.http import HttpResponseNotFound
from django.http.response import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# Create your views here.


def index(request):
    """Home page"""
    return render(request=request, template_name="index.html")


def custom_404(request, exception):
    """Chybova stranka jen kdyz DEBUG=False"""
    html = render_to_string("404.html", {"message": str(exception)})
    return HttpResponseNotFound(html)


def cam(request):
    return render(request=request, template_name="cam.html")


def video_stream(request):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return HttpResponse("Kamera není dostupná", status=500)

    def generate():
        while True:
            ret, frame = cap.read()
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

            # 🌙 Pauza 0.5 sekundy mezi snímky (2 FPS místo plného výkonu)
            time.sleep(0.05)

    return StreamingHttpResponse(
        generate(), content_type="multipart/x-mixed-replace; boundary=frame"
    )
