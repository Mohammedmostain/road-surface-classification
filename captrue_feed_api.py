import requests
import cv2  # OpenCV
import time
import os
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "https://edmontontrafficcam.com/Default.aspx/GetCameras"
OUTPUT_FOLDER = "traffic_dataset"

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def scrape_traffic_cameras():
    print("1. Fetching camera list from API...")
    
    # This headers dictionary mimics a real browser request
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # We send an empty POST request to get the full JSON list
        response = requests.post(API_URL, json={}, headers=headers)
        data = response.json().get('d', []) # The list is hidden inside the 'd' key
        
        print(f"   Found {len(data)} cameras active on the network.")

        success_count = 0
        
        # 2. Iterate through every camera found
        for cam in data:
            stream_code = cam.get('StreamCode')
            mms_url = cam.get('MMSUrl')
            forge = cam.get('Forge')
            description = cam.get('PrimaryRoad')

            if not (stream_code and mms_url and forge):
                continue

            # Construct the HLS Streaming URL based on the JS logic you found:
            # s = "https://" + t + "/" + e + "/public/hls/" + n + ".m3u8"
            video_url = f"https://{mms_url}/{forge}/public/hls/{stream_code}.m3u8"
            
            # 3. Use OpenCV to Capture a Single Frame
            print(f"   Capturing: {description}...", end=" ")
            
            cap = cv2.VideoCapture(video_url)
            ret, frame = cap.read() # Read one frame
            
            if ret:
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{OUTPUT_FOLDER}/{stream_code}_{timestamp}.jpg"
                
                # Save the frame as an image
                cv2.imwrite(filename, frame)
                print(f"✅ Saved.")
                success_count += 1
            else:
                print(f"❌ Failed (Stream offline).")
            
            # Release the video connection immediately to be polite
            cap.release()

        print(f"\nScrape Complete. Downloaded {success_count} images.")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")

if __name__ == "__main__":
    scrape_traffic_cameras()