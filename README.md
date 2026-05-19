# Flipkart Grid 5.0 — Robotics Challenge

**Runner-Up | Flipkart Grid 5.0 Finals**

Autonomous CNC Gantry system that detects boxes in a trolley using computer vision and places them on a conveyor belt — built entirely with a budget consumer webcam, no depth sensor.

---

## The Challenge

Flipkart Grid 5.0 Robotics challenged teams to build a fully autonomous pick-and-place system. Given a trolley containing boxes of varying types and positions, the robot had to:

1. Identify each box and its location in real time
2. Command a CNC Gantry to move to the box
3. Pick it up and drop it onto a conveyor belt

The key constraint: no specialised hardware. Our system used a standard webcam mounted above the trolley and solved the spatial problem purely through computer vision — YOLO detection on a cropped ROI, followed by coordinate scaling from pixel space to physical gantry coordinates.

---

## System Architecture

```
Budget Webcam (top-mounted)
        │
        ▼
  Crop to trolley ROI  (150, 0, 500, 481)
        │
        ▼
  YOLO Detection (best_top.pt)
  → returns normalised box centroids [0–1]
        │
        ▼
  Coordinate Scaling
  x_physical = centroid_x × 430mm  (trolley width)
  y_physical = centroid_y × 600mm  (trolley depth)
        │
        ▼
  GRBLComms → CNC Gantry (COM7, 115200 baud)
  → move to box position
  → 8s pickup window
  → move to dropoff (275, 20)
        │
        ▼
  Repeat
```

---

## Hardware

| Component | Detail |
|-----------|--------|
| Motion system | CNC Gantry (GRBL controller) |
| Camera | Standard budget webcam, top-mounted |
| Serial connection | COM7, 115200 baud |
| Compute | CUDA-capable GPU (inference on device) |
| Trolley area | 600 × 430 mm |

---

## Key Files

| File | Purpose |
|------|---------|
| [altFlipkart.py](altFlipkart.py) | **Main pipeline** — camera capture, detection, gantry control loop |
| [grblComm.py](grblComm.py) | GRBL serial communication class (connect, home, move, Z-axis) |
| [yoloDet.py](yoloDet.py) | YOLO inference wrapper — predicts box centroids, crops ROI, cleanup |
| [best_top.pt](best_top.pt) | Final trained YOLO model weights |
| [environment.yml](environment.yml) | Conda environment (Python 3.9, PyTorch 2.1, CUDA 11.8) |
| [data/](data/) | 101 training images captured from the competition setup |

---

## Setup

```bash
# 1. Create the conda environment
conda env create -f environment.yml
conda activate grid

# 2. Create the image temp directory expected by the pipeline
mkdir imgs

# 3. Connect the GRBL controller and set the COM port in altFlipkart.py
#    PORT = "COM7"  (change to your port, e.g. /dev/ttyUSB0 on Linux)

# 4. Run
python altFlipkart.py
```

---

## Pipeline Details

The main loop in `altFlipkart.py`:

1. **Capture** — grab a frame from the webcam
2. **Crop** — slice to the trolley ROI to reduce noise and improve detection accuracy
3. **Detect** — run YOLO inference; returns normalised centroids sorted by confidence
4. **Alternate detections** — a toggle flag alternates between primary and secondary detections each cycle, preventing the gantry from revisiting the same box
5. **Scale** — multiply normalised coords by physical trolley dimensions; clamp to safe limits (x ≤ 350, y ≤ 520)
6. **Move** — send `G00` command to gantry with pickup offsets (+30, +170)
7. **Pick** — 8-second window for the gripper/suction to engage
8. **Drop** — move to fixed dropoff position (275, 20) on the conveyor belt
9. **Cleanup** — remove temp images, loop

---

## Archive

Older iterations and experiments are preserved in [`archive/`](archive/):

- `archive/iterations/` — `Flipkart.py` (original), `newFLipkart.py` (intermediate)
- `archive/models/` — earlier YOLO checkpoints (`best.pt`, `best_1.pt`)
- `archive/experiments/orientation/` — box rotation angle detection experiments (not integrated)
