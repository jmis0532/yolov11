import os
import cv2
import numpy as np
from ultralytics import YOLO

# === 固定類別名稱 ===
custom_class_names = ["CCG"]
FIXED_CLASS_ID = 0

# === 載入模型 ===
model = YOLO("yolo11x.pt")

# === 設定路徑 ===
input_folder = "C:/Users/User/Desktop/CCG_TEST/"
output_img_folder = "C:/Users/User/Desktop/outputs/"
output_txt_folder = "C:/Users/User/Desktop/outputs/labels/"
os.makedirs(output_img_folder, exist_ok=True)
os.makedirs(output_txt_folder, exist_ok=True)

# === 設定參數 ===
CONF_THRESHOLD = 0.3
SAVE_IMAGE = True

# === 處理所有圖片 ===
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_folder, filename)
        output_img_path = os.path.join(output_img_folder, filename)
        output_txt_path = os.path.join(output_txt_folder, os.path.splitext(filename)[0] + ".txt")

        img = cv2.imread(img_path)
        h, w = img.shape[:2]

        results = model(img)[0]
        boxes_to_save = []

        # 建立遮罩（全黑）
        mask = np.zeros_like(img)

        for i, box in enumerate(results.boxes):
            conf = float(box.conf)
            if conf < CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # 只保留框內的區域（畫到遮罩上）
            cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), thickness=-1)

            # 轉 YOLO 標註格式
            x_center = ((x1 + x2) / 2) / w
            y_center = ((y1 + y2) / 2) / h
            bw = (x2 - x1) / w
            bh = (y2 - y1) / h

            boxes_to_save.append((FIXED_CLASS_ID, x_center, y_center, bw, bh))

        # 遮蔽框外區域（只保留框內）
        masked_img = cv2.bitwise_and(img, mask)

        # 畫框＋文字（可選）
        for i, box in enumerate(results.boxes):
            conf = float(box.conf)
            if conf < CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f"{custom_class_names[FIXED_CLASS_ID]}"
            cv2.rectangle(masked_img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.putText(masked_img, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

        # 儲存 .txt 標註檔
        with open(output_txt_path, "w") as f:
            for (cls_id, xc, yc, bw, bh) in boxes_to_save:
                f.write(f"{cls_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

        if SAVE_IMAGE:
            cv2.imwrite(output_img_path, masked_img)
            print(f"已儲存遮蔽圖片：{output_img_path}")
        print(f"已儲存標註：{output_txt_path}")

cv2.destroyAllWindows()
print("\n所有圖片處理完成（框外區域已遮蔽）")
