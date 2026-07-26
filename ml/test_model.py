from ultralytics import YOLO
import cv2
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

model = YOLO(MODEL_PATH)

VALID_CLASSES = {"dog", "monkey", "goat", "cattle", "wildboar"}


def detect_video_fast(video_path):

    if not os.path.exists(video_path):
        return "No video"

    cap = cv2.VideoCapture(video_path)

    predictions = []

    FRAME_SKIP = 5
    MAX_FRAMES = 50

    frame_id = 0
    processed = 0

    while processed < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1

        if frame_id % FRAME_SKIP != 0:
            continue

        processed += 1

        results = model(frame, conf=0.25, imgsz=416, verbose=False)

        boxes = results[0].boxes
        if boxes is None:
            continue

        for box in boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()

            if label not in VALID_CLASSES:
                continue

            if conf < 0.3:
                continue

            # 🔥 weighted confidence
            weight = conf * 2 if conf > 0.6 else conf

            predictions.append((label, weight))

    cap.release()

    if not predictions:
        return "No animal detected"

    # =============================
    # 🎯 AGGREGATE SCORES
    # =============================
    score_map = defaultdict(float)
    count_map = defaultdict(int)

    for label, weight in predictions:
        score_map[label] += weight
        count_map[label] += 1

    # =============================
    # 🔥 SORT RESULTS
    # =============================
    sorted_labels = sorted(score_map.items(), key=lambda x: x[1], reverse=True)

    best_label, best_score = sorted_labels[0]

    # =============================
    # 🔥 STRONG DOG vs MONKEY FIX
    # =============================
    if "dog" in score_map and "monkey" in score_map:

        dog_score = score_map["dog"]
        monkey_score = score_map["monkey"]

        # 🔥 if close → prefer dog (very important)
        if dog_score >= monkey_score * 0.6:
            best_label = "dog"

        # 🔥 extra rule: dogs appear in more frames usually
        elif count_map["dog"] > count_map["monkey"]:
            best_label = "dog"

    # =============================
    # 🔥 VALIDATION
    # =============================
    total_score = sum(score_map.values())

    if count_map[best_label] < 3:
        return "No animal detected"

    if best_score / total_score < 0.35:
        return "No animal detected"

    return best_label