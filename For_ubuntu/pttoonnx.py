#Yolo的pt模型轉ONNX格式 by Summer
 
from ultralytics import YOLO

# 載入YOLO模型
model = YOLO("best.pt")

# 匯出成 ONNX 格式，會自動處理模型結構
model.export(format="onnx")


