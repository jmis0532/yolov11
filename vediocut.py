# 2025/05/22 by Summer
# 影像截圖工具vediocut.py 
# 1.新增空白建暫停功能
# 2.按Q回到第一幀
# 3.按A回到上一幀
# 4.按D回到下一幀
# 5.按S存至output_images\png

import cv2
import os
import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

video_path = filedialog.askopenfilename(
    initialdir=r'H:\github\yolov11\vedio',
    title="選擇影片",
    filetypes=[("All Files", "*.*")]
)

if not video_path:
    print("未選擇影片，結束程式")
    exit()

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("無法開啟影片")
    exit()

output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

paused = False
step_frame = False
go_back_one_frame = False

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

frame_cache = []  # 存 (frame_num, frame_image)
frame_index = -1  # 指向目前播放的 frame_cache 位置

current_display_img = None  # 用來存當前顯示影像，方便截圖

def draw_frame(frame, frame_num):
    resized = cv2.resize(frame, (640, 640))
    zoomed = cv2.resize(resized, (960, 960), interpolation=cv2.INTER_LINEAR)
    cv2.putText(zoomed, f"Frame: {frame_num}/{total_frames}",
                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 255), 4)
    return zoomed

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            print("影片播放完畢")
            paused = True
            if frame_cache:
                current_display_img = frame_cache[-1][1]
                cv2.imshow('Video Player', current_display_img)
            continue

        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        zoomed = draw_frame(frame, current_frame)
        cv2.imshow('Video Player', zoomed)

        frame_cache.append((current_frame, zoomed))
        frame_index = len(frame_cache) - 1

        if len(frame_cache) > 100:
            frame_cache.pop(0)
            frame_index -= 1

        current_display_img = zoomed  # 更新目前顯示影像

    else:
        if go_back_one_frame:
            if frame_index > 0:
                frame_index -= 1
                prev_frame_num, prev_frame_img = frame_cache[frame_index]
                cv2.imshow('Video Player', prev_frame_img)
                print(f"== 回上一幀: {prev_frame_num} ==")
                current_display_img = prev_frame_img
            else:
                print("已是第一幀，無法回上一幀")
            go_back_one_frame = False

        elif step_frame:
            if frame_index < len(frame_cache) - 1:
                frame_index += 1
                next_frame_num, next_frame_img = frame_cache[frame_index]
                cv2.imshow('Video Player', next_frame_img)
                print(f"== 下一幀 (cache): {next_frame_num} ==")
                current_display_img = next_frame_img
            else:
                ret, frame = cap.read()
                if not ret:
                    print("已到影片尾，無法前進")
                else:
                    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    zoomed = draw_frame(frame, current_frame)
                    frame_cache.append((current_frame, zoomed))
                    frame_index += 1
                    cv2.imshow('Video Player', zoomed)
                    print(f"== 下一幀 (new): {current_frame} ==")
                    current_display_img = zoomed
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
        if k == ord('a') or k == ord('A'):  # 回上一幀
            go_back_one_frame = True
        elif k == ord('d') or k == ord('D'):  # 下一幀
            step_frame = True
        elif k == ord('q') or k == ord('Q'):  # 回到第一幀
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_cache.clear()
            frame_index = -1
            ret, frame = cap.read()
            if ret:
                current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                zoomed = draw_frame(frame, current_frame)
                cv2.imshow('Video Player', zoomed)
                frame_cache.append((current_frame, zoomed))
                frame_index = 0
                current_display_img = zoomed
                print("== 回到第一幀 ==")
    if k == k == ord('s') or k == ord('S'): # 截圖
        if current_display_img is not None:
            img_name = os.path.join(output_dir, f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png")
            cv2.imwrite(img_name, current_display_img)
            print(f"圖片儲存成功: {img_name}")
        else:
            print("無可截圖的畫面")

cap.release()
cv2.destroyAllWindows()
