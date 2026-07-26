from ultralytics import YOLO
import cv2
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

model = YOLO(MODEL_PATH)


def detect_video_fast(video_path):
    """
    Improved detection:
    - Fix goat vs cattle confusion
    - Better wildboar detection
    - Balanced scoring
    """

    if not os.path.exists(video_path):
        return "No animal detected"

    cap = cv2.VideoCapture(video_path)

    # ---------- SETTINGS ----------
    FRAME_SKIP = 3
    MAX_FRAMES = 50
    IMG_SIZE = 640
    CONF = 0.35   # lower global threshold

    score_map = defaultdict(float)
    count_map = defaultdict(int)

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

        # ---------- PREPROCESS ----------
        frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

        blur = cv2.GaussianBlur(frame, (3, 3), 0)
        frame = cv2.addWeighted(frame, 1.2, blur, -0.2, 0)

        # ---------- YOLO ----------
        results = model(frame, conf=CONF, imgsz=IMG_SIZE, verbose=False)

        boxes = results[0].boxes
        if boxes is None or len(boxes) == 0:
            continue

        for box in boxes:

            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            label = model.names[cls_id].lower().strip()

            if label == "cow":
                label = "cattle"

            if label not in ["wildboar", "dog", "cattle", "monkey", "goat"]:
                continue

            # ---------- CLASS CONF ----------
            min_conf = {
                "wildboar": 0.30,
                "dog": 0.45,
                "cattle": 0.45,
                "monkey": 0.50,
                "goat": 0.40
            }

            if conf < min_conf[label]:
                continue

            # ---------- BOX AREA ----------
            x1, y1, x2, y2 = box.xyxy[0]
            area = float((x2 - x1) * (y2 - y1))

            if area > 50000:
                size_boost = 1.15
            elif area > 20000:
                size_boost = 1.08
            else:
                size_boost = 1.0

            # ---------- BALANCED WEIGHTS ----------
            weights = {
                "wildboar": 2.0,
                "dog": 1.7,
                "cattle": 1.1,   # reduced
                "monkey": 1.1,
                "goat": 1.5      # increased
            }

            score = conf * weights[label] * size_boost

            score_map[label] += score
            count_map[label] += 1

    cap.release()

    # ---------- NO DETECTION ----------
    if not score_map:
        return "No animal detected"

    # ---------- FRAME BONUS ----------
    for label in score_map:
        score_map[label] += count_map[label] * 0.25

    # ---------- SPECIAL PRIORITY RULES ----------

    # Wildboar strong rule
    if "wildboar" in score_map and count_map["wildboar"] >= 1:
        if score_map["wildboar"] > max(score_map.values()) * 0.85:
            return "wildboar"

    # Goat vs cattle correction (VERY IMPORTANT FIX)
    if "goat" in score_map and "cattle" in score_map:
        if score_map["goat"] >= score_map["cattle"] * 0.85:
            return "goat"

    # Cattle rule (more strict now)
    if "cattle" in score_map and count_map["cattle"] >= 2:
        if score_map["cattle"] > max(score_map.values()) * 0.90:
            return "cattle"

    # ---------- FINAL DECISION ----------
    best_label = max(score_map, key=score_map.get)

    # relaxed condition (previously too strict)
    if count_map[best_label] < 1:
        return "No animal detected"

    return best_label