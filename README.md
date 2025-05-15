由於我使用的是NVIDIA Geforce RTX 3080TI 顯示卡，在所有套件支援的前提下使用以下版本工具

Python 3.9.7

YOLOv11n

其他詳見 requirements.txt

============================================

安裝方式概述：

1.建立正確目錄及資料夾 (請參照目錄圖001.jpg)

2.使用python -m venv venv001 建立的虛擬環境，讓套件只用在此venv001環境，不與其他環境衝突。

建立虛擬環境後，記得要啟用虛擬環境才能開始使用程式，在CMD下	venv001\Scripts\activate.bat 啟用虛擬環境。

3.把以下東西拷貝到目錄下 (請參照目錄圖001.jpg)

(1)requirements.txt

(2)packages <==打包好的套件包 下載位置https://drive.google.com/drive/folders/11FA6dMVvL3azhjeAWPuirO85jtni_akS?usp=drive_link

(3)六支.py程式  

(4)YOLOv11n <== 去官網的GITHUB抓  https://github.com/ultralytics/ultralytics

4.在啟動虛擬環境下，CMD執行安裝指令 pip install --no-index --find-links=packages -r requirements.txt

5.在啟動虛擬環境下，CMD執行安裝指令 pip install torch==2.1.0+cu118 torchvision==0.16.0+cu118 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118

============================================

程式說明：

  vedio11-detect.py (開啟本地影像進行偵測，使用YOLOv11n原始模型)

  vediobest-detect.py (開啟本地影像進行偵測，使用訓練過後模型)

  vediocut.py (開啟本地影像進行截圖，存檔於output_images資料夾，按S)

  webcan11-detect.py (開啟攝影鏡頭進行偵測，使用YOLOv11n原始模型)

  webcanbest-detect.py (開啟攝影鏡頭進行偵測，使用訓練過後模型)

  webcancut.py (開啟攝影鏡頭進行截圖，存檔於output_images資料夾，按S)

============================================

影像檔要放在vedio目錄下

venv001這資料夾是在CMD下，使用python -m venv venv001 建立的虛擬環境，讓套件只用在此venv001環境，不與其他環境衝突。

建立虛擬環境後，記得要啟用虛擬環境才能開始使用程式。

在CMD下	venv001\Scripts\activate.bat 啟用虛擬環境。

便可執行程式



