#!/usr/bin/env python3
"""
Image watermarking, compression, and batch renaming tool
功能: 添加浮水印 -> 壓縮 -> 重新命名
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
import math

class ImageProcessor:
    def __init__(self, input_dir, output_dir=None, watermark_text="ELMO.H Photography"):
        """
        初始化圖像處理器
        
        Args:
            input_dir: 輸入資料夾路徑
            output_dir: 輸出資料夾路徑（默認為 input_dir/output）
            watermark_text: 浮水印文字
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir / "output"
        self.watermark_text = watermark_text
        
        # 浮水印顏色（#D4AF37 金色，透明度 100%）
        self.watermark_color = (212, 175, 55, int(255 * 1.0))  # RGBA with 100% opacity
        
        # 確保輸出資料夾存在
        self.output_dir.mkdir(exist_ok=True)
        
    def get_watermark_font_size(self, image_width, image_height):
        """
        根據圖像尺寸動態計算浮水印字體大小
        字體大小約為短邊的 3%
        """
        short_side = min(image_width, image_height)
        font_size = int(short_side * 0.03)
        return max(font_size, 20)  # 最小 20px
        
    def add_watermark(self, image, font_path=None):
        """
        添加浮水印到圖像
        
        Args:
            image: PIL Image 對象
            font_path: 字體路徑（defaults to system font）
        """
        # 轉換為 RGBA 以支持透明度
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        width, height = image.size
        font_size = self.get_watermark_font_size(width, height)
        
        # 嘗試加載 Times New Roman 粗體
        try:
            if font_path is None:
                # 嘗試常見的字體路徑
                possible_paths = [
                    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",  # macOS (correct path)
                    "/System/Library/Fonts/Times New Roman.ttf",  # macOS fallback
                    "/Windows/Fonts/timesbd.ttf",  # Windows
                    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",  # Linux
                ]
                font = None
                for path in possible_paths:
                    if os.path.exists(path):
                        font = ImageFont.truetype(path, font_size)
                        print(f"✓ 字體已加載 (大小: {font_size}pt): {path}", file=sys.stderr)
                        break
                if font is None:
                    # 如果沒找到，使用默認字體
                    print(f"⚠ 使用默認字體", file=sys.stderr)
                    font = ImageFont.load_default()
            else:
                font = ImageFont.truetype(font_path, font_size)
                print(f"✓ 字體已加載 (大小: {font_size}pt): {font_path}", file=sys.stderr)
        except Exception as e:
            print(f"✗ 警告: 無法加載字體，使用默認字體。錯誤: {e}", file=sys.stderr)
            font = ImageFont.load_default()
        
        # 創建透明層用於繪製浮水印
        watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        # 計算文字位置（中間下方）
        # 獲取文字邊界
        bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 中間下方位置（距離底部約 5% 的高度）
        x = (width - text_width) // 2
        y = int(height * 0.95) - text_height
        
        # 繪製浮水印（字母間距寬 10%）
        draw.text((x, y), self.watermark_text, font=font, fill=self.watermark_color, spacing=int(text_width * 0.1 / len(self.watermark_text)))
        
        # 合併浮水印層和原始圖像
        image = Image.alpha_composite(image, watermark_layer)
        
        return image
    
    def compress_image(self, image, max_long_side=3000, quality=85):
        """
        壓縮圖像
        
        Args:
            image: PIL Image 對象
            max_long_side: 長邊最大像素值
            quality: JPEG 質量 (1-100)
        """
        width, height = image.size
        long_side = max(width, height)
        
        if long_side > max_long_side:
            scale = max_long_side / long_side
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image, quality
    
    def process_images(self, font_path=None):
        """
        處理資料夾中的所有圖像
        """
        # 支持的圖像格式
        image_extensions = {'.jpg', '.jpeg', '.png'}
        
        # 獲取所有圖像文件並排序
        image_files = sorted([
            f for f in self.input_dir.iterdir()
            if f.suffix.lower() in image_extensions and f.is_file()
        ])
        
        if not image_files:
            print(f"在 {self.input_dir} 中未找到任何圖像文件")
            return
        
        print(f"找到 {len(image_files)} 個圖像文件")
        print(f"輸出文件夾: {self.output_dir}\n")
        
        for index, file_path in enumerate(image_files, 1):
            try:
                print(f"[{index}/{len(image_files)}] 處理中: {file_path.name}", end=" ... ")
                
                # 打開圖像
                image = Image.open(file_path)
                
                # 先壓縮圖像
                image, quality = self.compress_image(image)
                
                # 後添加浮水印
                image = self.add_watermark(image, font_path)
                
                # 生成新文件名（序列號 + 原始副檔名）
                new_filename = f"photo-{index}.jpg"  # 使用 photo-N 格式
                output_path = self.output_dir / new_filename
                
                # 保存圖像（轉換為 RGB 用於 JPEG）
                if image.mode == 'RGBA':
                    # 創建白色背景
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[3])
                    image = background
                
                image.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                # 獲取文件大小
                file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                print(f"✓ ({file_size:.2f} MB)")
                
            except Exception as e:
                print(f"✗ 錯誤: {e}")
        
        print(f"\n✅ 完成！所有圖像已保存到 {self.output_dir}")


def main():
    """主程序入口"""
    if len(sys.argv) < 2:
        print("使用方式:")
        print(f"  {sys.argv[0]} <input_directory> [output_directory] [font_path]")
        print("\n範例:")
        print(f"  {sys.argv[0]} ./photos")
        print(f"  {sys.argv[0]} ./photos ./output")
        print(f"  {sys.argv[0]} ./photos ./output \"/System/Library/Fonts/Times New Roman.ttf\"")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    font_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 驗證輸入目錄
    if not os.path.isdir(input_dir):
        print(f"錯誤: 輸入目錄不存在 - {input_dir}")
        sys.exit(1)
    
    # 創建處理器並開始處理
    processor = ImageProcessor(input_dir, output_dir)
    processor.process_images(font_path)


if __name__ == "__main__":
    main()
