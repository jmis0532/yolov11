import os
import cv2
from ultralytics import YOLO

# === 固定類別名稱 ===
custom_class_names = ["CCG"]
class_name_to_id = {name: i for i, name in enumerate(custom_class_names)}

# === 載入模型 ===
model = YOLO("yolo11x.pt")

# === 設定路徑 ===
input_folder = "C:/Users/User/Desktop/CCG_TEST/"
output_img_folder = "C:/Users/User/Desktop/outputs/"
output_txt_folder = "C:/Users/User/Desktop/outputs/labels/"
os.makedirs(output_img_folder, exist_ok=True)
os.makedirs(output_txt_folder, exist_ok=True)

# === 參數設定 ===
CONF_THRESHOLD = 0.3
SAVE_IMAGE = True
FIXED_CLASS_ID = 0  # 因為只有一個類別 CCG → 類別ID為 0

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

        for i, box in enumerate(results.boxes):
            conf = float(box.conf)
            if conf < CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # 固定使用類別 "CCG"（class_id = 0）
            class_id = FIXED_CLASS_ID

            # 歸一化座標
            x_center = ((x1 + x2) / 2) / w
            y_center = ((y1 + y2) / 2) / h
            bw = (x2 - x1) / w
            bh = (y2 - y1) / h

            boxes_to_save.append((class_id, x_center, y_center, bw, bh))

            if SAVE_IMAGE:
                label = f"{custom_class_names[class_id]}"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(img, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

        # 儲存 .txt
        with open(output_txt_path, "w") as f:
            for (cls_id, xc, yc, bw, bh) in boxes_to_save:
                f.write(f"{cls_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")
        print(f"已輸出標註: {output_txt_path}")

        if SAVE_IMAGE:
            cv2.imwrite(output_img_path, img)
            print(f"已儲存圖片: {output_img_path}")

cv2.destroyAllWindows()
print("\n類別固定為：CCG（class_id=0）")
print("所有圖片皆已處理完畢！")
