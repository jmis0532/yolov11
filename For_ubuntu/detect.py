import cv2
import math
import supervision as sv
from ultralytics import YOLO
import os

video_path = "/home/jetson/yolov11/test001.mp4"
model_path = "/home/jetson/yolov11/best.engine"

if not os.path.exists(video_path):
    print("❌ 找不到影片，請確認路徑是否正確")
    exit()

if not os.path.exists(model_path):
    print("❌ 找不到模型檔案 .engine，請確認路徑是否正確")
    exit()

model = YOLO(model_path)
class_names = {0: 'GGC', 1: 'WK'}
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
mm_per_pixel = 0.5

def open_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("❌ 無法開啟影片")
        exit()
    return cap

cap = open_video(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
current_frame = 0
paused = False
step_frame = False
last_frame_image = None

def process_frame(frame):
    results = model(frame)
    boxes = results[0].boxes
    annotated_image = frame.copy()
    
    screen_height, screen_width = frame.shape[:2]
    center_x, center_y = screen_width // 2, screen_height // 2
    cross_length = 40

    bottom_distances = []
    for i, box in enumerate(boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        bottom_y = max(y1, y2)
        distance_to_bottom = screen_height - bottom_y
        bottom_distances.append((i, distance_to_bottom))

    sorted_indices = sorted(bottom_distances, key=lambda x: x[1])
    top10 = sorted_indices[:10]
    index_to_w1 = {idx: 10 - rank for rank, (idx, _) in enumerate(top10)}

    w2_weight = 3

    for i, box in enumerate(boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        box_center_x = (x1 + x2) // 2
        box_center_y = (y1 + y2) // 2

        cv2.line(annotated_image, (center_x, center_y), (box_center_x, box_center_y), (0, 125, 0), 2)

        cv2.line(annotated_image, (box_center_x - cross_length, box_center_y),
                 (box_center_x + cross_length, box_center_y), (253, 73, 1), 1)
        cv2.line(annotated_image, (box_center_x, box_center_y - cross_length),
                 (box_center_x, box_center_y + cross_length), (253, 73, 1), 1)

        pixel_distance = math.hypot(box_center_x - center_x, box_center_y - center_y)
        mm_distance = pixel_distance * mm_per_pixel

        dx = box_center_x - center_x
        dy = center_y - box_center_y
        angle_deg = math.degrees(math.atan2(dy, dx))
        if angle_deg < 0:
            angle_deg += 360

        class_id = int(boxes.cls[i].item())
        class_name = class_names.get(class_id, f"Class {class_id}")
        w1 = index_to_w1.get(i, 0)
        w2 = w2_weight if class_name == "WK" else 0
        total_score = w1 + w2

        mid_x = (center_x + box_center_x) // 2
        mid_y = (center_y + box_center_y) // 2
        cv2.putText(annotated_image, f"{class_name}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(annotated_image, f"{mm_distance:.1f}mm", (mid_x + 5, mid_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(annotated_image, f"{angle_deg:.1f}°", (mid_x + 5, mid_y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)
        cv2.putText(annotated_image, f"W1:{w1} W2:{w2} W:{total_score}", (mid_x + 5, mid_y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    cv2.line(annotated_image, (center_x - cross_length, center_y), (center_x + cross_length, center_y), (0, 0, 255), 1)
    cv2.line(annotated_image, (center_x, center_y - cross_length), (center_x, center_y + cross_length), (0, 0, 255), 1)

    detections = sv.Detections.from_ultralytics(results[0])
    labels = [class_names.get(int(class_id), f"class{int(class_id)}") for class_id in detections.class_id]

    annotated_image = bounding_box_annotator.annotate(scene=annotated_image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)

    global current_frame, total_frames
    cv2.putText(annotated_image, f"Frame: {current_frame}/{total_frames}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    return annotated_image

def goto_frame(cap, frame_number):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    return cap, frame if ret else (cap, None)

while True:
    if not paused or step_frame:
        ret, frame = cap.read()
        if not ret:
            print("播放完畢")
            paused = True
            if last_frame_image is not None:
                cv2.imshow('YOLO Video Detection', last_frame_image)
            step_frame = False
            continue

        current_frame += 1
        annotated_image = process_frame(frame)
        cv2.imshow('YOLO Video Detection', annotated_image)
        last_frame_image = annotated_image.copy()
        step_frame = False

    k = cv2.waitKey(0 if paused else 1) & 0xFF

    if k == 27:  # ESC 鍵，結束程式
        break
    elif k == ord(' '):
        paused = not paused
        print("== 暫停 ==" if paused else "== 繼續 ==")
    elif paused:
        if k in [ord('a'), ord('A')]:
            target_frame = max(0, current_frame - 2)
            cap, frame = goto_frame(cap, target_frame)
            if frame is not None:
                current_frame = target_frame + 1
                annotated_image = process_frame(frame)
                cv2.imshow('YOLO Video Detection', annotated_image)
                last_frame_image = annotated_image.copy()
                print(f"⬅ 回上一幀: {current_frame}")
        elif k in [ord('d'), ord('D')]:
            ret, frame = cap.read()
            if ret:
                current_frame += 1
                annotated_image = process_frame(frame)
                cv2.imshow('YOLO Video Detection', annotated_image)
                last_frame_image = annotated_image.copy()
                print(f"➡ 下一幀: {current_frame}")
        elif k in [ord('q'), ord('Q')]:
            # 按 q 回到第一幀
            cap, frame = goto_frame(cap, 0)
            if frame is not None:
                current_frame = 1
                annotated_image = process_frame(frame)
                cv2.imshow('YOLO Video Detection', annotated_image)
                last_frame_image = annotated_image.copy()
                print("🔄 回到第一幀")
        elif k in [ord('s'), ord('S')]:
            step_frame = True
            paused = True

cap.release()
cv2.destroyAllWindows()
