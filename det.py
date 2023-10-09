from ultralytics import YOLO
from PIL import Image
import shutil

class Detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, source, device="cuda"):
        results = self.model.predict(source=source, save=True, device=device)
        
        centroids = []
        confidence = []

        for r in results:
            coordinates = (r.boxes.xyxyn).tolist()
            conf = (r.boxes.conf).tolist()
            centroids.extend([[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in coordinates])
            confidence.extend(conf)

        return centroids, confidence

    def show_output_image(self):
        output_img = Image.open("./runs/segment/predict/img.jpg")
        output_img.show()

    def cleanup(self):
        shutil.rmtree("./runs")

# Usage:
if __name__ == "__main__":
    detection = Detection("best.pt")
    centroids, confidence = detection.predict(source="img.jpg", device="cuda")
    print(centroids, confidence)
    detection.show_output_image()
    detection.cleanup()
