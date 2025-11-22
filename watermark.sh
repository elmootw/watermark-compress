#!/bin/bash
# 浮水印 + 壓縮 + 重命名工具
# 使用方式: ./watermark.sh <input_directory> [output_directory]

# 獲取腳本所在目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/watermark-venv"
SCRIPT_PATH="$SCRIPT_DIR/watermark_compress.py"

# 檢查虛擬環境
if [ ! -d "$VENV_PATH" ]; then
    echo "虛擬環境不存在，正在創建..."
    python3 -m venv "$VENV_PATH"
    "$VENV_PATH/bin/pip" install Pillow
fi

# 執行 Python 腳本
"$VENV_PATH/bin/python3" "$SCRIPT_PATH" "$@"
