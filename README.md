2025/07/13

add makeAVI.py 將資料夾下所有PNG壓為AVI，可選擇壓縮格式&FPS

==========================

2025/06/22

新增兩支自動標註程式

桌面設立資料夾，執行程式後，輸出存檔至outputs資料夾

以YOLOv11x自動標註

add autolable_f1.py  自動標註程式，留標註框外背景原圖

add autolable_f2.py  自動標註程式，標註框外背景遮蔽

==========================

2025/06/07

移植Jetson orin NX成功，將幾個步驟寫成.py，以便以後使用

位置在For_ubuntu資料夾內(在板子上使用)

1.detect.py 偵測(正式時使用，用影片偵測)

2.webcan.py 偵測(正式時使用，用攝像頭偵測)

3.onnxtoengine.py onnx轉engine

4.pttoonnx.py pytorch(.pt)轉onnx

5.videotest.py 只是測試攝像頭

移植Jetson orin NX成功

影片位置: https://www.youtube.com/watch?v=2jZ4SvMqsbk

==========================

2025/06/03

2028/06/03 by Summer

修改攻擊順序:

增加權重w1,w2

w1為距離底部距離，距離越小數字越大(10~1)

w2為WK出現與否，數字固定為3


![DEMO](https://github.com/jmis0532/yolov11/blob/main/W123.png)

==========================

2025/05/31

新增vedio11-detect.py功能
顯示攻擊順序#紅色數字

![DEMO](https://github.com/jmis0532/yolov11/blob/main/attack_sequence.png)

==========================

2025/05/25

![DEMO](https://github.com/jmis0532/yolov11/blob/main/PPT.png)

==========================

2025/05/22 

(一)新增vedio11-detect.py功能(影像偵測工具)

船艦中心藍十字

畫面中心紅十字 

1.新增空白鍵暫停功能

2.按Q回到第一幀

3.按A回到上一幀

4.按D回到下一幀

![DEMO](https://github.com/jmis0532/yolov11/blob/main/demo01.png)
![DEMO](https://github.com/jmis0532/yolov11/blob/main/demo02.png)
![DEMO](https://github.com/jmis0532/yolov11/blob/main/demo03.png)

(二)新增vediocut.py功能(影像截圖工具)

影像截圖工具vediocut.py 

1.新增空白建暫停功能

2.按Q回到第一幀

3.按A回到上一幀

4.按D回到下一幀

5.按S存至output_images\png

==========================

2025/05/22

啟用虛擬環境指令(venv002)

CMD	 venv\Scripts\activate.bat

PowerShell	 .\venv002\Scripts\Activate.ps1

Git Bash/Bash 	source venv002/Scripts/activate


==========================

船艦標註分類代號

空母AC

驅逐艦DDG

護衛艦FF

海警船CCG

AC-16 遼寧號

AC-17 山東號

AC-18 福建號

==========================

<h2>2025/05/01</h2>

<h2>(這裡是故事開始...)</h2>

由於我使用的是NVIDIA Geforce RTX 3080TI 顯示卡，在所有套件支援的前提下使用以下版本工具

(主要是pytorch和cuda必須available)

Python 3.9.7

YOLOv11n

其他詳見 requirements.txt

==========================

安裝方式概述：

1.建立正確目錄及資料夾 (目錄長這樣...)
![目錄長這樣](https://github.com/jmis0532/yolov11/blob/main/%E7%9B%AE%E9%8C%84%E5%9C%96001.jpg)




2.使用python -m venv venv002 建立的虛擬環境，讓套件只用在此venv002環境，不與其他環境衝突。

建立虛擬環境後，記得要啟用虛擬環境才能開始使用程式，在CMD下	venv001\Scripts\activate.bat 啟用虛擬環境。

3.把以下東西複製到目錄下

(1)requirements.txt

(2)packages <==打包好的套件包 下載位置https://drive.google.com/drive/folders/11FA6dMVvL3azhjeAWPuirO85jtni_akS?usp=drive_link

(3)六支.py程式  

(4)YOLOv11n <== 去官網的GITHUB抓  https://github.com/ultralytics/ultralytics

4.在啟動虛擬環境下，CMD執行安裝指令 pip install --no-index --find-links=packages -r requirements.txt

5.在啟動虛擬環境下，CMD執行安裝指令 pip install torch==2.1.0+cu118 torchvision==0.16.0+cu118 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118

==========================

程式說明：

  vedio11-detect.py (開啟本地影像進行偵測，使用YOLOv11n原始模型，記得修正路徑)

  vediobest-detect.py (開啟本地影像進行偵測，使用訓練過後模型，記得修正路徑)

  vediocut.py (開啟本地影像進行截圖，存檔於output_images資料夾，按S，記得修正路徑)

  webcan11-detect.py (開啟攝影鏡頭進行偵測，使用YOLOv11n原始模型，記得修正路徑)

  webcanbest-detect.py (開啟攝影鏡頭進行偵測，使用訓練過後模型，記得修正路徑)

  webcancut.py (開啟攝影鏡頭進行截圖，存檔於output_images資料夾，按S，記得修正路徑)

==========================

注意：

1. 影像檔要放在vedio目錄下。

2. venv001這資料夾是在CMD下，使用python -m venv venv001 建立的虛擬環境，讓套件只用在此venv001環境，不與其他環境衝突。

3. 建立虛擬環境後，記得要啟用虛擬環境才能開始使用程式。

4. 在CMD下	venv001\Scripts\activate.bat 啟用虛擬環境。

5. 完成以上便可執行程式

==========================

訓練過程需要用到 roboflow.com 網站工具 ，因此還必須在目錄下複製 roboflow.com 增值過的整個打包圖片資料夾。

內有test，train，valid 三個資料夾，各有images(圖片)及label(標註資料) 

及data.yaml路徑須修改如下(自行修正路徑)

train: H:\github\yolo11\yolo11_test\train\images

val: H:\github\yolo11\yolo11_test\valid\images

test: H:\github\yolo11\yolo11_test\test\images


nc: 1
names: ['RC']

roboflow:

  workspace: summer-jyu2t

  project: yolo10_test-61exz

  version: 1

  license: CC BY 4.0

  url: 

==========================

CMD下訓練指令(虛擬環境啟動中)

yolo detect train data=yolo10_test/data.yaml model=yolo11n.pt epochs=30 batch=8 imgsz=640 device=0


data(自行修正路徑)


model=yolo11n.pt(訓練模型)


epochs=30(訓練週期)


batch=8(訓練批次)


imgsz=640(圖像大小)


device=0 (顯卡單張為0，顯卡兩張為1....)























