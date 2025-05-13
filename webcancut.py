import cv2
import os
import time

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Can't open the webcam")
    exit()

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"pix: {int(width)} x {int(height)}")

output_dir='output_images'
os.makedirs(output_dir,exist_ok=True)
img_counter=0

while True:
    ret,frame=cap.read()  
    if not ret:
        break

    # cv2.putText(frame, "Press 's' to save, ESC to exit", (10, 30),
                # cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
   
    cv2.imshow('Webcam',frame)
    k=cv2.waitKey(1)
    if k == 27:  # ESC
        print("Escape hit, closing...")
        break
    elif k == ord('s'):
        img_name = os.path.join(output_dir, f"opencv_{time.strftime('%Y%m%d_%H%M%S')}.png")
        cv2.imwrite(img_name, frame)
        print(f"圖片儲存成功:{img_name}")
        img_counter += 1
cap.release()
cv2.destroyAllWindows()