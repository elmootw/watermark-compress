# 📸 Watermark Compress Tool

批量為照片添加浮水印、壓縮並重新命名的工具。

## ✨ 功能

✅ **浮水印**
- 文字: ELMO.H Photography
- 字體: Times New Roman 粗體
- 顏色: #D4AF37 (金色) 透明度 100%
- 位置: 中間下方
- 大小: 動態根據圖像尺寸計算

✅ **壓縮**
- 長邊限制: 3000px（等比例縮放）
- 質量: 85%
- 優化: 啟用 JPEG 優化

✅ **重新命名**
- 格式: `photo-1.jpg`, `photo-2.jpg`, ...
- 自然數字排序（photo-1, photo-2, photo-10 正確順序）

✅ **方向自動修正**
- 自動偵測並應用 EXIF 旋轉信息
- 保持相機/手機拍攝的原始方向（直/橫）

## 📋 系統要求

- Python 3.7+
- macOS/Linux/Windows
- 自動創建虛擬環境

## 🚀 快速開始

### 基本使用（自動安裝依賴）

```bash
./watermark.sh /path/to/photos
```

### 常見用法

```bash
# 按修改日期排序（新的照片排在前面）
./watermark.sh /path/to/photos --sort date

# 指定輸出目錄
./watermark.sh /path/to/photos --output /path/to/output

# 指定自訂字體
./watermark.sh /path/to/photos --font /path/to/font.ttf

# 組合使用
./watermark.sh /path/to/photos --sort date --output /path/to/output --font /path/to/font.ttf
```

### 排序選項

- `--sort name` 或省略：按文件名自然數字排序（默認）
- `--sort date`：按修改日期排序，最新的照片編號為 photo-1

## 📁 輸出

處理後的圖像會保存在：
- 默認: `input_dir/` (原目錄下)
- 自訂: 指定的輸出目錄

## 🔧 配置

如需修改設定，編輯 `watermark_compress.py`：

- **字體大小**: 修改 `get_watermark_font_size()` 方法
- **浮水印文字**: 修改 `__init__` 中的 `watermark_text`
- **浮水印顏色**: 修改 `watermark_color` (RGBA 格式)
- **壓縮質量**: 修改 `compress_image()` 中的 `quality` 參數
- **長邊尺寸**: 修改 `compress_image()` 中的 `max_long_side` 參數

## 📦 開發環境設置

如果手動安裝依賴：

```bash
python3 -m venv watermark-venv
source watermark-venv/bin/activate  # macOS/Linux
# 或
watermark-venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## 💡 使用場景

- 攝影作品集網站
- 批量圖像處理
- 保護版權（添加浮水印）

## 📄 授權

MIT License

---

Made with ❤️ for ELMO.H Photography
