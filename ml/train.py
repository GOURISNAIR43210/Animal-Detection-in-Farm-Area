from ultralytics import YOLO

# ✅ better model (auto downloads)
model = YOLO("yolov8s.pt")

model.train(
    data="data.yaml",   # ✅ correct path
    epochs=5,
    imgsz=640
)