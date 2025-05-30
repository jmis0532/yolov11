# 2025/05/22 by Summer
# 船艦中心藍十字
# 畫面中心紅十字 
# 1.新增空白鍵暫停功能
# 2.按Q回到第一幀
# 3.按A回到上一幀
# 4.按D回到下一幀
# 2025/05/31 by Summer
# 增加攻擊順序:紅色數字1-10 以邊緣軸y2值計算





import cv2
import math
import supervision as sv
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

video_path = filedialog.askopenfilename(
    initialdir=r'H:\github\yolo11\vedio',
    title="選擇影片",
    filetypes=[("All Files", "*.*")]
)

if not video_path:
    print("未選擇影片，結束程式")
    exit()

model = YOLO('best.pt')

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

mm_per_pixel = 0.5

def open_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("無法開啟影片")
        exit()
    return cap

cap = open_video(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

paused = False
step_frame = False
current_frame = 0
last_frame_image = None

def process_frame(frame):
    input_frame = frame.copy()
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)

    annotated_image = bounding_box_annotator.annotate(scene=input_frame, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

    h, w, _ = annotated_image.shape
    center_x, center_y = w // 2, h // 2

    cross_length = 20
    cv2.line(annotated_image, (center_x - cross_length, center_y),
        (center_x + cross_length, center_y), (0, 0, 255), 2)
    cv2.line(annotated_image, (center_x, center_y - cross_length),
         (center_x, center_y + cross_length), (0, 0, 255), 2)

    # ==== 新增：計算與畫面下緣距離並排序 ====
    bottom_distances = []
    for i, box in enumerate(detections.xyxy):
        x1, y1, x2, y2 = map(int, box)
        box_center_y = (y1 + y2) // 2
        dist_to_bottom = h - box_center_y
        bottom_distances.append((i, dist_to_bottom))

    # 按照離底部的距離遞增排序（越靠近底部，dist越小，順序數字越小）
    sorted_indices = sorted(bottom_distances, key=lambda x: x[1])
    index_to_rank = {idx: rank + 1 for rank, (idx, _) in enumerate(sorted_indices[:10])}

    # ==== 顯示標註與數字 ====
    for i, box in enumerate(detections.xyxy):
        x1, y1, x2, y2 = map(int, box)
        box_center_x = (x1 + x2) // 2
        box_center_y = (y1 + y2) // 2

        cv2.line(annotated_image, (center_x, center_y), (box_center_x, box_center_y), (0, 125, 0), 2)

        color = (253, 73, 7)
        thickness = 2
        cv2.line(annotated_image, (box_center_x - cross_length, box_center_y),
                 (box_center_x + cross_length, box_center_y), color, thickness)
        cv2.line(annotated_image, (box_center_x, box_center_y - cross_length),
                 (box_center_x, box_center_y + cross_length), color, thickness)

        pixel_distance = math.hypot(box_center_x - center_x, box_center_y - center_y)
        mm_distance = pixel_distance * mm_per_pixel

        dx = box_center_x - center_x
        dy = center_y - box_center_y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        if angle_deg < 0:
            angle_deg += 360

        mid_x = (center_x + box_center_x) // 2
        mid_y = (center_y + box_center_y) // 2

        # 加上排序數字
        rank_num = index_to_rank.get(i, None)
        distance_text = f"{mm_distance:.1f} M"
        if rank_num is not None:
            distance_text += f" #{rank_num}"

        if rank_num is not None:
        # 分離距離與順序數字
            distance_only = f"{mm_distance:.1f} M"
            cv2.putText(annotated_image, distance_only, (mid_x + 5, mid_y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            cv2.putText(annotated_image, f"#{rank_num}", (mid_x + 5 + 80, mid_y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)  # 紅色
            cv2.putText(annotated_image, f"{angle_deg:.1f}deg", (mid_x + 5, mid_y + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)
        else:
            cv2.putText(annotated_image, distance_text, (mid_x + 5, mid_y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            cv2.putText(annotated_image, f"{angle_deg:.1f}deg", (mid_x + 5, mid_y + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)

        cv2.putText(annotated_image, f"Frame: {current_frame}/{total_frames}",
                (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

    return annotated_image

def goto_frame(cap, frame_number):
    cap.release()
    cap = open_video(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if not ret:
        print(f"無法讀取第 {frame_number} 幀")
        return cap, None
    return cap, frame

while True:
    if not paused or step_frame:
        ret, frame = cap.read()
        if not ret:
            print("影片播放完畢")
            paused = True
            if last_frame_image is not None:
                cv2.imshow('YOLO Video Detection', last_frame_image)
            else:
                break
            step_frame = False
            continue

        current_frame += 1
        annotated_image = process_frame(frame)
        cv2.imshow('YOLO Video Detection', annotated_image)
        last_frame_image = annotated_image.copy()
        step_frame = False

    wait_time = 0 if paused else 1
    k = cv2.waitKey(wait_time) & 0xFF

    if k == 27:  # ESC
        print("按下 ESC，結束播放")
        break
    elif k == ord(' '):  # 空白鍵暫停/播放切換
        paused = not paused
        print("== 暫停播放 ==" if paused else "== 繼續播放 ==")
    elif paused:
        if k == ord('a') or k == ord('A'):
            target_frame = max(0, current_frame - 2)
            cap, frame = goto_frame(cap, target_frame)
            if frame is not None:
                current_frame = target_frame + 1
                annotated_image = process_frame(frame)
                cv2.imshow('YOLO Video Detection', annotated_image)
                last_frame_image = annotated_image.copy()
                print(f"== 回上一幀: {current_frame} ==")
        elif k == ord('d') or k == ord('D'):
            ret, frame = cap.read()
            if ret:
                current_frame += 1
                annotated_image = process_frame(frame)
                cv2.imshow('YOLO Video Detection', annotated_image)
                last_frame_image = annotated_image.copy()
                print(f"== 下一幀: {current_frame} ==")
            else:
                print("已到影片末尾")
        elif k == ord('q') or k == ord('Q'):
            cap, frame = goto_frame(cap, 0)
            if frame is not None:
                current_frame = 1
                annotated_image = process_frame(frame)
                cv2.imshow('YOLO Video Detection', annotated_image)
                last_frame_image = annotated_image.copy()
                print("== 回到第一幀 ==")

cap.release()
cv2.destroyAllWindows()
