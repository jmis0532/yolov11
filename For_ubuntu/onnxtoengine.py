#使用時記得後面要加參數
#範例: python3 trtexec --onnx=best.onnx --saveEngine=best.engine --fp16
#精度--fp16 可以耶，本板照支援 bu Summer

import os
import subprocess
import argparse
import shutil
import sys

def find_trtexec():
    """在系統中尋找 trtexec，並確保可以執行"""
    trtexec_path = shutil.which("trtexec")
    if trtexec_path:
        return trtexec_path

    # 常見 Jetson 安裝路徑
    default_paths = [
        "/usr/src/tensorrt/bin/trtexec",
        "/usr/local/bin/trtexec"
    ]

    for path in default_paths:
        if os.path.exists(path):
            return path

    print("❌ 找不到 trtexec，請確認已安裝 TensorRT 並設定 PATH。")
    sys.exit(1)

def convert_onnx_to_engine(onnx_path, engine_path, fp16=True):
    trtexec = find_trtexec()

    cmd = [
        trtexec,
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}"
    ]

    if fp16:
        cmd.append("--fp16")

    print(f"🚀 正在執行：{' '.join(cmd)}")

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("❌ 轉換失敗：")
        print(result.stderr)
    else:
        print("✅ 轉換成功！輸出檔案：", engine_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="將 ONNX 模型轉換為 TensorRT Engine")
    parser.add_argument("--onnx", default="input.onnx", help="ONNX 模型路徑 (預設: input.onnx)")
    parser.add_argument("--engine", default="output.engine", help="輸出 engine 檔案名稱 (預設: output.engine)")
    parser.add_argument("--no-fp16", action="store_true", help="停用 FP16 模式")

    args = parser.parse_args()

    convert_onnx_to_engine(args.onnx, args.engine, not args.no_fp16)

