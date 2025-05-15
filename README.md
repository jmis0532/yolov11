由於我使用的是NVIDIA Geforce RTX 3080TI 顯示卡，在所有套件支援的前提下使用以下版本工具

Python 3.9.7

YOLOv11n

其他詳見 requirements.txt

安裝方式概述：

1.建立正確目錄及資料夾 (請參照目錄圖001)

2.把以下東西拷貝到目錄下 (請參照目錄圖001)

requirements.txt

packages <==打包好的套件包

六支.py程式  

YOLOv11n <== 去官網的GITHUB抓  https://github.com/ultralytics/ultralytics

3.執行安裝 pip install --no-index --find-links=packages -r requirements.txt

4.執行安裝 pip install torch==2.1.0+cu118 torchvision==0.16.0+cu118 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118



