# 2025/05/22 by Summer
# 船艦中心藍十字
# 畫面中心紅十字 
# 1.新增空白鍵暫停功能
# 2.按Q回到第一幀
# 3.按A回到上一幀
# 4.按D回到下一幀
# 2025/05/31 by Summer
# 增加攻擊順序:紅色數字1-10 以邊緣軸y2值計算
# 2028/06/03 by Summer
# 修改攻擊順序:
# 增加權重w1,w2
# w1為距離底部距離，距離越小數字越大(10~1)
# w2為WK出現與否，數字固定為3

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
    results = model(frame)
    detections = sv.Detections.from_ultralytics(results[0])
    annotated_image = frame.copy()

    screen_height, screen_width = frame.shape[:2]
    center_x, center_y = screen_width // 2, screen_height // 2
    cross_length = 10

    mm_per_pixel = 0.264583333  # pixel 對應的毫米

    bottom_distances = []
    for i, box in enumerate(detections.xyxy):
        x1, y1, x2, y2 = map(int, box)
        bottom_y = max(y1, y2)
        distance_to_bottom = screen_height - bottom_y
        bottom_distances.append((i, distance_to_bottom))

    # 根據距離畫面底部排序，距離越近越前面，取前10名分配 w1=1~10
    sorted_indices = sorted(bottom_distances, key=lambda x: x[1])
    top10 = sorted_indices[:10]
    index_to_w1 = {idx: 10 - rank for rank, (idx, _) in enumerate(top10)}

    w2_weight = 3  # WK加權，固定為3

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
        if angle_deg < 0: angle_deg += 360

        mid_x = (center_x + box_center_x) // 2
        mid_y = (center_y + box_center_y) // 2

        # 權重 w1: 根據底部距離
        w1 = index_to_w1.get(i, 0)

        # 權重 w2: WK出現與否 
        class_id = int(detections.class_id[i])
        class_name = model.names[class_id]
        w2 = w2_weight if class_name == "WK" else 0

        total_score = w1 + w2

        # 顯示距離與角度
        cv2.putText(annotated_image, f"{mm_distance:.1f}M", (mid_x + 5, mid_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(annotated_image, f"{angle_deg:.1f}deg", (mid_x + 5, mid_y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)

        # 顯示 w1、w2 與總分
        cv2.putText(annotated_image, f"W1:{w1} W2:{w2} W:{total_score}", (mid_x + 5, mid_y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        annotated_image = bounding_box_annotator.annotate(scene=annotated_image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

        print(f"偵測到 {len(detections)} 個物件")

        # 畫出目前幀數
        cv2.putText(annotated_image, f"Frame: {current_frame} / {total_frames}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255),1)

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
