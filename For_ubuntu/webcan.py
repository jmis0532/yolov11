#使用CSI攝像頭，如果用的是USB的，註解的部分改一下 by Summer


import cv2
import math
import supervision as sv
from ultralytics import YOLO

# ====== 載入模型 ======
model_path = "/home/jetson/yolov11/best.engine"
try:
    model = YOLO(model_path)
except Exception as e:
    print(f"❌ 無法載入模型: {e}")
    exit()

# ====== 手動定義 class 名稱對照表 ======
class_names = {0: 'GGC', 1: 'WK'}

# ====== Supervision 繪圖工具 ======
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# ====== 實體距離換算（每像素幾 mm） ======
mm_per_pixel = 0.5

# ====== 開啟預設usb攝影機 (index=0) ======
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("❌ 無法開啟攝影機")
#     exit()

# ====== 改用 Jetson CSI 攝影機 ======
gst_str = (
    "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, "
    "format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! "
    "videoconvert ! video/x-raw, format=BGR ! appsink"
)
cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("❌ 無法開啟 CSI 攝影機")
    exit()    

# 由於 webcam 無法事先知道總幀數，這裡只顯示「目前取得的幀數」
current_frame = 0
paused = False
step_frame = False
last_frame_image = None

def process_frame(frame):
    """
    使用 YOLO model 偵測並在畫面上繪製：
    - 物件的 bounding box 和標籤
    - 物件中心與畫面中心的連線 (綠線)
    - 物件中心處的十字 (橘色)
    - 物件中心到畫面中心之距離(mm)與角度(deg)
    - W1/W2 權重與總分
    - 畫面中心十字 (紅線)
    - 畫面左上角顯示當前幀編號
    """
    results = model(frame)
    boxes = results[0].boxes
    annotated_image = frame.copy()
    
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2
    cross_length = 40

    # 計算每個 box 距離畫面底部的距離 (用於 W1 排名)
    bottom_distances = []
    for i, box in enumerate(boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        bottom_y = max(y1, y2)
        dist_to_bottom = h - bottom_y
        bottom_distances.append((i, dist_to_bottom))

    sorted_indices = sorted(bottom_distances, key=lambda x: x[1])
    top10 = sorted_indices[:10]
    index_to_w1 = {idx: 10 - rank for rank, (idx, _) in enumerate(top10)}
    w2_weight = 3

    for i, box in enumerate(boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        box_cx = (x1 + x2) // 2
        box_cy = (y1 + y2) // 2

        # 綠色線：畫面中心 → 物件中心
        cv2.line(annotated_image, (center_x, center_y), (box_cx, box_cy), (0, 125, 0), 2)

        # 橘色十字：畫在物件中心
        cv2.line(annotated_image, (box_cx - cross_length, box_cy),
                 (box_cx + cross_length, box_cy), (253, 73, 1), 1)
        cv2.line(annotated_image, (box_cx, box_cy - cross_length),
                 (box_cx, box_cy + cross_length), (253, 73, 1), 1)

        # 計算距離與角度
        pixel_dist = math.hypot(box_cx - center_x, box_cy - center_y)
        mm_dist = pixel_dist * mm_per_pixel

        dx = box_cx - center_x
        dy = center_y - box_cy
        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360

        class_id = int(boxes.cls[i].item())
        class_name = class_names.get(class_id, f"Class {class_id}")
        w1 = index_to_w1.get(i, 0)
        w2 = w2_weight if class_name == "WK" else 0
        total_score = w1 + w2

        mid_x = (center_x + box_cx) // 2
        mid_y = (center_y + box_cy) // 2
        cv2.putText(annotated_image, f"{class_name}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(annotated_image, f"{mm_dist:.1f}mm", (mid_x + 5, mid_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(annotated_image, f"{angle:.1f}°", (mid_x + 5, mid_y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)
        cv2.putText(annotated_image, f"W1:{w1} W2:{w2} W:{total_score}", (mid_x + 5, mid_y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # 畫面中心紅十字
    cv2.line(annotated_image, (center_x - cross_length, center_y),
             (center_x + cross_length, center_y), (0, 0, 255), 1)
    cv2.line(annotated_image, (center_x, center_y - cross_length),
             (center_x, center_y + cross_length), (0, 0, 255), 1)

    # 畫出 bounding box 與 label
    detections = sv.Detections.from_ultralytics(results[0])
    labels = [class_names.get(int(cid), f"class{int(cid)}") for cid in detections.class_id]
    annotated_image = bounding_box_annotator.annotate(scene=annotated_image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)

    # 在左上角顯示目前幀數
    global current_frame
    cv2.putText(annotated_image, f"Frame: {current_frame}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    return annotated_image


while True:
    if not paused or step_frame:
        ret, frame = cap.read()
        if not ret:
            print("❌ 無法擷取影像 (camera disconnected?)")
            break

        current_frame += 1
        annotated = process_frame(frame)
        cv2.imshow('YOLO Webcam Detection', annotated)
        last_frame_image = annotated.copy()
        step_frame = False

    k = cv2.waitKey(0 if paused else 1) & 0xFF

    if k in [ord('q'), ord('Q')]:
        # 按 q 離開程式
        break
    elif k == ord(' '):
        # 空白鍵：暫停/繼續
        paused = not paused
        print("== 暫停 ==" if paused else "== 繼續 ==")
    elif paused:
        if k in [ord('s'), ord('S')]:
            # s 鍵：逐幀顯示 (在 paused 狀態下)
            step_frame = True
            paused = True
        # 取消「a/d 回上一幀、下一幀」的功能，因為 webcam 無法向後跳
        # 如果想針對「拍照」或「另存圖片」再做自訂，也可以在這裡加新的按鍵處理

cap.release()
cv2.destroyAllWindows()
