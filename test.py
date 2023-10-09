from ultralytics import YOLO
from PIL import Image
import torch
import shutil

model = YOLO("best.pt")
results = model.predict(source="img.jpg", save=True, device="cuda")

centroids = []
confidence = []

for r in results:
    coordinates = (r.boxes.xyxyn).tolist()
    conf = (r.boxes.conf).tolist()
    centroids.extend([[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in coordinates])
    confidence.extend(conf)

print(centroids, confidence)

output_img = Image.open("./runs/segment/predict/img.jpg")
output_img.show()
        
shutil.rmtree("./runs")