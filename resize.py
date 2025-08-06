import os
from PIL import Image
from tqdm import tqdm

input_folder = r'C:\Users\User\Desktop\resize_input'
output_folder = r'C:\Users\User\Desktop\resize_output'
target_size = (640, 640)
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def get_image_files(folder):
    return [f for f in os.listdir(folder) if is_image_file(f)]

def resize_and_pad_with_transparency(img, size):
    # 等比縮放
    img.thumbnail(size, Image.Resampling.LANCZOS)
    # 建立透明背景新圖 (RGBA, 透明)
    new_img = Image.new("RGBA", size, (0, 0, 0, 0))
    # 計算中心貼圖位置
    left = (size[0] - img.width) // 2
    top = (size[1] - img.height) // 2
    # 貼上縮放後圖片
    new_img.paste(img, (left, top))
    return new_img

def main():
    if not os.path.exists(input_folder):
        print(f"資料夾不存在: {input_folder}")
        return

    image_files = get_image_files(input_folder)
    total = len(image_files)

    if total == 0:
        print("沒有找到圖片檔案。")
        return

    print(f"偵測到 {total} 張圖片，將會被調整為 {target_size[0]}x{target_size[1]} 像素。")
    confirm = input("是否開始處理？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消操作。")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("開始處理圖片...\n")

    for img_name in tqdm(image_files, desc="處理進度", unit="張"):
        input_path = os.path.join(input_folder, img_name)
        output_path = os.path.join(output_folder, img_name)

        try:
            with Image.open(input_path) as img:
                img = img.convert("RGBA")  # 確保有 alpha 通道，才能處理透明
                new_img = resize_and_pad_with_transparency(img, target_size)
                new_img.save(output_path)  # 直接存 PNG 以保留透明
        except Exception as e:
            print(f"圖片處理失敗: {img_name}，錯誤: {e}")

    print("\n所有圖片已完成處理，輸出至:", output_folder)

if __name__ == "__main__":
    main()
