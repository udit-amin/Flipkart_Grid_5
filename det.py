from ultralytics import YOLO
from PIL import Image
import torch
import shutil

class Detection:
    def __init__(self, path_model):
        self.path_model = path_model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(path_model)
    
    def predict(self, path_img):
        img = Image.open(path_img).convert("RGB")

        results = self.model.predict(source=img, save=True, device=self.device)

        coordinates = []
        confidence = []

        for r in results.pred:
            coordinates.extend((r.xyxy).tolist())
            confidence.extend((r.conf).tolist())
    
        centroids = [[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2, _ in coordinates]

        output_img = Image.open("./runs/segment/predict/image0.jpg")
        output_img.show()
        
        shutil.rmtree("./runs")

        return centroids, confidence

# Create an instance of the Detection class
a = Detection(path_model="your_model_path_here")

# Call the predict method with an image path
centroids, confidence = a.predict("./imgs/img3.jpg")

# Print the centroids and confidence
print("Centroids:", centroids)
print("Confidence:", confidence)
