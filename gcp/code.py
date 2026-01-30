import requests
import cv2
from datetime import datetime
from google.cloud import storage

API_URL = "https://edmontontrafficcam.com/Default.aspx/GetCameras"
BUCKET_NAME = "YOUR_BUCKET_NAME"
PREFIX = "traffic_dataset"

storage_client = storage.Client()

def scrape_traffic_cameras(request):
    # (Optional) allow only POST
    # if request.method != "POST":
    #     return ("Method Not Allowed", 405)

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(API_URL, json={}, headers=headers, timeout=30)
        data = response.json().get("d", [])

        bucket = storage_client.bucket(BUCKET_NAME)
        success_count = 0

        for cam in data:
            stream_code = cam.get("StreamCode")
            mms_url = cam.get("MMSUrl")
            forge = cam.get("Forge")

            if not (stream_code and mms_url and forge):
                continue

            video_url = f"https://{mms_url}/{forge}/public/hls/{stream_code}.m3u8"

            cap = cv2.VideoCapture(video_url)
            ret, frame = cap.read()
            cap.release()

            if not ret:
                continue

            # Encode frame to JPEG bytes (no local file needed)
            ok, jpg = cv2.imencode(".jpg", frame)
            if not ok:
                continue

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            object_name = f"{PREFIX}/{stream_code}/{stream_code}_{timestamp}.jpg"

            blob = bucket.blob(object_name)
            blob.upload_from_string(jpg.tobytes(), content_type="image/jpeg")

            success_count += 1

        return (f"Done. Uploaded {success_count} images.", 200)

    except Exception as e:
        return (f"CRITICAL ERROR: {e}", 500)
