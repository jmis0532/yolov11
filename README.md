由於我使用的是NVIDIA Geforce RTX 3080TI 顯示卡，在所有套件支援的前提下使用以下版本工具

Python 3.9.7

YOLOv11n

其他詳見 requirements.txt

安裝方式概述：

1.建立正確目錄及資料夾 (請參照目錄圖001.jpg)

2.把以下東西拷貝到目錄下 (請參照目錄圖001.jpg)

requirements.txt

packages <==打包好的套件包 下載位置https://drive.google.com/drive/folders/11FA6dMVvL3azhjeAWPuirO85jtni_akS?usp=drive_link

六支.py程式  

YOLOv11n <== 去官網的GITHUB抓  https://github.com/ultralytics/ultralytics

3.執行安裝 pip install --no-index --find-links=packages -r requirements.txt

4.執行安裝 pip install torch==2.1.0+cu118 torchvision==0.16.0+cu118 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118

  vedio11-detect.py (開啟本地影像進行偵測，使用YOLOv11n原始模型)

  vediobest-detect.py (開啟本地影像進行偵測，使用訓練過後模型)

  vediocut.py (開啟本地影像進行截圖，存檔於output_images資料夾)

  webcan11-detect.py (開啟攝影鏡頭進行偵測，使用YOLOv11n原始模型)

  webcanbest-detect.py (開啟攝影鏡頭進行偵測，使用訓練過後模型)

  webcancut.py (開啟攝影鏡頭進行截圖，存檔於output_images資料夾)


