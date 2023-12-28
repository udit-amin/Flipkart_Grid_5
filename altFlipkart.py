import cv2
import sys
import time
from grblComm import GRBLComms
from yoloDet import Detection

PORT = "COM7"
BAUD_RATE = 115200
CROP_COORDINATES = (150, 0, 500, 481)
TROLLEY = [600, 430]
MODEL_PATH = "best_top.pt"
CAPTURE_PATH = "./imgs/captured_image.jpg"
CROPPED_PATH = "./imgs/cropped_img.jpg"
OFFSET_THRESHOLD = 20  # Define your own offset value based on your requirements

camera = cv2.VideoCapture(0)
detection = Detection(MODEL_PATH)

prev_x, prev_y = None, None  # Initializing previous x and y to None
#use_secondary_detection = False  # Added this line
flag = False



if __name__ == "__main__":
    grbl = GRBLComms(PORT, BAUD_RATE)
    grbl.connect()
    grbl.enableHardLimit()
    grbl.homeMachine()
    grbl.disableHardLimit()

    dontStop = True
    while(dontStop):

        _, frame = camera.read()
        cv2.imwrite(CAPTURE_PATH, frame)
        print(f"Picture captured: {CAPTURE_PATH}")

        cropped_image_path = detection.crop_input_image(CAPTURE_PATH, CROPPED_PATH, CROP_COORDINATES)
        results = detection.predict(source=cropped_image_path, device="cuda")

        # Use the primary detection results[0] by default
        x, y = results[0]

        #detection.show_output_image((x, y))

        #time.sleep(1000000)
        # If using the secondary detection is preferred or the primary detection is too close to the previous one
        #if ((((prev_x is not None) and (prev_y is not None)) and ((abs(x - prev_x) < OFFSET_THRESHOLD) and (abs(y - prev_y) < OFFSET_THRESHOLD)))):
        if (flag == True):

            print("Using secondary detection")
            # Check if results[1] exists to avoid index out of range errors
            if len(results) > 1:
                x, y = results[1]
                #use_secondary_detection = False  # Reset it for the next round
            else:
                print("Secondary detection not found. Using primary detection.")

        #prev_x, prev_y = x, y  # Update the previous x and y after using them for comparison
        if (flag == True):
            flag = False
        else:
            flag = True
            
        x = x * TROLLEY[1]
        y = y * TROLLEY[0]
        x = min(350, x)
        y = min(520, y)
        print("X: ", y, ", Y: ", x)
        detection.show_output_image((x, y))

        detection.cleanup()

        print("Picking up box ", x)
        grbl.moveMachine(y + 30, x + 170)
        
        for remaining in range(8, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining. Attempting Pickup".format(remaining))
            sys.stdout.flush()
            time.sleep(1)

        print("\nGoing to DROPOFF")
        grbl.moveMachine(275, 20)
        
    
    grbl.disconnect()
