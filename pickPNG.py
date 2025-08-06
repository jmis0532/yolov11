import os
import shutil
import re
from tqdm import tqdm  # 請先安裝： pip install tqdm

# 設定來源與目標資料夾
source_folder = r"C:\Users\User\Desktop\Pick_PNG_source"
target_folder = r"C:\Users\User\Desktop\Pick_PNG_destination"

# 確保目標資料夾存在
os.makedirs(target_folder, exist_ok=True)

# 掃描來源資料夾
all_png_files = []
files_to_copy = []

for filename in os.listdir(source_folder):
    if filename.lower().endswith(".png"):
        all_png_files.append(filename)
        numbers = re.findall(r'\d+', filename)
        if numbers:
            number = int(numbers[-1])  # 取最後一個數字
            if number % 5 == 0:
                files_to_copy.append(filename)

# 顯示統計資訊
print("偵測完成：")
print(f"來源資料夾中共偵測到 {len(all_png_files)} 張 PNG 圖片")
print(f"其中符合 5 的倍數條件的圖片有 {len(files_to_copy)} 張\n")

# 詢問是否開始複製
proceed = input("是否要開始複製？(y/n): ").strip().lower()
if proceed != 'y':
    print("已取消複製。")
    exit()

# 複製並顯示進度條
print("\n開始複製中...")
copied_count = 0

for filename in tqdm(files_to_copy, desc="複製進度", unit="張"):
    src_path = os.path.join(source_folder, filename)
    dst_path = os.path.join(target_folder, filename)
    try:
        shutil.copy2(src_path, dst_path)
        copied_count += 1
    except Exception as e:
        print(f"錯誤：無法複製 {filename}：{e}")

# 結果顯示
print("\n複製完成。")
print(f"共複製 {copied_count} 張圖片到 {target_folder}")
