import serial
import cv2
import time
import os
from ultralytics import YOLO
from PIL import Image
import shutil
import numpy as np

class Detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, source, device="cuda"):
        results = self.model.predict(source=source, save=True, device=device)
        for r in results:
            coordinates = (r.boxes.xyxyn).tolist()

        centroids = [[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in coordinates]
        return centroids

    def crop_input_image(self, input_image_path, output_image_path, crop_coordinates):
        input_img = Image.open(input_image_path)
        x1, y1, x2, y2 = crop_coordinates
        cropped_img = input_img.crop((x1, y1, x2, y2))
        cropped_img.save(output_image_path)
        return output_image_path

    def show_output_image(self,result):
        output_img = Image.open("./runs/segment/predict/cropped_img.jpg")
        #output_img = np.asarray(output_img)
        #dot_radius = 5
        #dot_color = (0, 255, 0)  # Red color in BGR
        #thickness = -1  # This will fill the circle
        #output_img = cv2.circle(output_img, (int(result[0]), int(result[1])), dot_radius, dot_color, thickness)
        #output_img = Image.fromarray(output_img)

        output_img.show()

    def cleanup(self):
        shutil.rmtree("./runs")
        os.remove("./imgs/captured_image.jpg")
        os.remove("./imgs/cropped_img.jpg")