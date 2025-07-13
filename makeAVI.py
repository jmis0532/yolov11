import cv2
import os
from tqdm import tqdm

image_folder = r"C:/Users/User/Desktop/PNG-AVI"
output_video = r"C:/Users/User/Desktop/PNG-AVI-output/output.avi"
frame_rate = 30
fourcc = cv2.VideoWriter_fourcc(*'MJPG') # fourcc = 0 不壓縮

# 確保輸出資料夾存在
os.makedirs(os.path.dirname(output_video), exist_ok=True)

# 取得並排序 PNG 圖片
images = [img for img in os.listdir(image_folder) if img.lower().endswith(".png")]
images.sort()

if not images:
    raise Exception("找不到任何 PNG 圖片，請確認資料夾是否正確。")

# 讀第一張圖取得影片尺寸
first_image_path = os.path.join(image_folder, images[0])
frame = cv2.imread(first_image_path)
if frame is None:
    raise Exception(f"無法讀取圖片：{first_image_path}")

height, width, layers = frame.shape
video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

# 合成影片
for img_name in tqdm(images, desc="製作 AVI 中...", unit="frame"):
    img_path = os.path.join(image_folder, img_name)
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"無法讀取圖片：{img_path}")
        continue
    video.write(frame)

video.release()
print("AVI 影片輸出完成：", output_video)
