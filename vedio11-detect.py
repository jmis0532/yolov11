import cv2
import supervision as sv
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# 選擇影片
video_path = filedialog.askopenfilename(
    initialdir=r'H:\github\yolo11\vedio',  
    title="選擇影片",
    filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")]
)

if not video_path:
    print("未選擇影片，結束程式")
    exit()


model = YOLO('yolo11n.pt')  

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()


cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("無法開啟影片")
    exit()


while True:
    ret, frame = cap.read()
    if not ret:
        print("影片播放完畢或讀取失敗")
        break

    
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

    cv2.imshow('YOLO Detection', annotated_image)

    k = cv2.waitKey(1)
    if k % 256 == 27:  
        print("按下 ESC，結束播放")
        break

cap.release()
cv2.destroyAllWindows()
