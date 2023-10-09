from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
import torch
import shutil
from ultralytics import YOLO
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Detection:
    def __init__(self, path_model):
        self.path_model = path_model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(path_model)
    
    def predict(self, img):
        results = self.model.predict(source=img, save=True, device=self.device)

        centroids = []
        confidence = []

        for r in results:
            coordinates = (r.boxes.xyxyn).tolist()
            conf = (r.boxes.conf).tolist()
            centroids.extend([[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in coordinates])
            confidence.extend(conf)

        return centroids, confidence

detector = Detection("./best.pt")

## Get Predictions based on uploaded file

@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        img = Image.open(io.BytesIO(await file.read())).convert("RGB")
        centroids, confidence = detector.predict(img)

        return {"centroids": centroids, "confidence": confidence}
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
