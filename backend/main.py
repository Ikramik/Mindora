import os
import shutil
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


app = FastAPI(title="Izri AI Local Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Allows React to talk to this API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp_uploads", exist_ok=True)

load_dotenv()  

RUNPOD_URL = os.getenv("RUNPOD_URL")
SECRET_KEY = os.getenv("RUNPOD_SECRET_KEY")

# Add this temporarily to debug:
print(f"DEBUG - RUNPOD_URL loaded as: {RUNPOD_URL}")
# Note: If RunPod Pod ID changed, update this URL! Otherwise, keep it as is.
RUNPOD_URL = os.getenv("RUNPOD_URL")
SECRET_KEY = os.getenv("RUNPOD_SECRET_KEY")  # This should match the key in RunPod server code

@app.post("/api/upload-video")
async def upload_video(file: UploadFile = File(...)):
    print(f"\n--- NEW COMMERCIAL UPLOADED: {file.filename} ---")
    video_path = f"temp_uploads/{file.filename}"
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        print("Uploading to RunPod GPU for Neural Inference...")
        with open(video_path, "rb") as video_file:
            # We pack the file AND the secret password into the payload
            files = {"file": (file.filename, video_file, "video/mp4")}
            data = {"api_key": SECRET_KEY} 
            
            response = requests.post(RUNPOD_URL, files=files, data=data)
            response.raise_for_status() 
            ai_data = response.json()
            
        print("Success! Data received from Cloud.")
        return {
            "status": "success",
            "activation_data": ai_data["activation_data"]
        }
        
    except Exception as e:
        print(f"FAILED to connect to RunPod: {e}")
        return {"status": "error", "message": "Failed to reach Cloud GPU."}
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)