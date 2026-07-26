from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import os
import uuid

from ml.detect_video import detect_video_fast

# ================= TWILIO SETUP =================
try:
    from twilio.rest import Client
    TWILIO_ENABLED = True
except ImportError:
    TWILIO_ENABLED = False


# ================= TWILIO CONFIG =================
# ✅ TEMP: Hardcoded for testing (replace with env later)
import os

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
USER_NUMBER = os.getenv("USER_NUMBER")


RESULTS = {}


# ================= HOME =================
def home(request):
    return render(request, "home.html")


# ================= DETECTION =================
def detect(request):

    if request.method == "POST":

        video1 = request.FILES.get("video1")
        video2 = request.FILES.get("video2")

        unique_id = str(uuid.uuid4())

        paths = []
        urls = []

        # SAVE VIDEOS
        for video in [video1, video2]:
            if video:
                filename = f"{unique_id}_{video.name}"
                path = os.path.join(settings.MEDIA_ROOT, filename)

                with open(path, "wb+") as f:
                    for chunk in video.chunks():
                        f.write(chunk)

                paths.append(path)
                urls.append(settings.MEDIA_URL + filename)

        results = []

        # DETECTION
        for p in paths:
            try:
                r = detect_video_fast(p)
                print("🎯 VIDEO RESULT:", r)

                if not r or r.strip() == "":
                    r = "No animal detected"

                results.append(r)

            except Exception as e:
                print("❌ DETECTION ERROR:", e)
                results.append("Error")

        if not results:
            results = ["No animal detected"]

        # STORE RESULTS
        RESULTS[unique_id] = {
            "animals": results,
            "videos": urls
        }

        # ================= SMS ALERT =================
        danger_animals = ["boar", "goat", "wildboar", "dog", "monkey"]

        unique_animals = set(results)

        for animal in unique_animals:
            print("🔍 Checking animal:", animal)

            # ✅ partial match
            if any(d in animal.lower() for d in danger_animals):
                print("⚠️ Danger detected:", animal)
                send_sms_safe(animal)

        return redirect(f"/result/?id={unique_id}")

    return render(request, "detection.html")


# ================= RESULT PAGE =================
def result_page(request):
    id = request.GET.get("id")
    return render(request, "result.html", {"id": id})


# ================= API =================
def get_result(request, id):
    data = RESULTS.get(id, {})
    return JsonResponse(data)


# ================= SMS FUNCTION =================
def send_sms_safe(animal):

    print("🚀 SMS FUNCTION CALLED")

    if not TWILIO_ENABLED:
        print("❌ Twilio not installed")
        return

    # ✅ CHECK CONFIG
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER, USER_NUMBER]):
        print("❌ Missing Twilio configuration")
        return

    try:
        print("🔐 SID:", TWILIO_SID)
        print("🔐 TOKEN (first 5):", TWILIO_TOKEN[:5])

        client = Client(TWILIO_SID.strip(), TWILIO_TOKEN.strip())

        message = client.messages.create(
            body=f"⚠️ ALERT: {animal.upper()} detected near your crops!",
            from_=TWILIO_NUMBER,
            to=USER_NUMBER
        )

        print("✅ SMS SENT")
        print("📩 SID:", message.sid)
        print("📊 STATUS:", message.status)

    except Exception as e:
        print("❌ SMS ERROR:", str(e))