#只是測試一下攝像頭 by Summer

import cv2

gst_str = (
    "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, "
    "format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! "
    "videoconvert ! video/x-raw, format=BGR ! appsink"
)

cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("❌ 無法開啟 CSI 攝影機")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 無法擷取畫面")
        break
    cv2.imshow("CSI Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
