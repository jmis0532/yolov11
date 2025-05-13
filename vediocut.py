import cv2
import os
import time
import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()


video_path = filedialog.askopenfilename(
    initialdir=r'H:\github\yolo11\vedio',  
    title="選擇影片",
    filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")]
)


if not video_path:
    print("沒有選擇影片，程式終止")
    exit()


cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("無法開啟影片檔案")
    exit()


width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"影片解析度: {int(width)} x {int(height)}")
print(f"影片幀率: {fps:.2f} fps")


output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("影片播放完畢或讀取失敗")
        break

    
    # cv2.putText(frame, "Press 's' to save, ESC to exit", (10, 30),
                # cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Video', frame)
    k = cv2.waitKey(int(1000 / fps)) 

    if k == 27:  
        print("按下 ESC，結束播放")
        break
    elif k == ord('s'):  
        img_name = os.path.join(output_dir, f"frame_{time.strftime('%Y%m%d_%H%M%S')}.png")
        cv2.imwrite(img_name, frame)
        print(f"圖片儲存成功: {img_name}")
        img_counter += 1


cap.release()
cv2.destroyAllWindows()
