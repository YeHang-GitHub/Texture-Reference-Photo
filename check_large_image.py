from PIL import Image
import os

def check_large_images(directory, limit=89478485):  # 默认 Pillow 限制
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, file)
                with Image.open(img_path) as img:
                    pixels = img.size[0] * img.size[1]
                    if pixels > limit:
                        print(f"⚠️ 图片过大: {img_path}，像素数: {pixels}")

check_large_images("Images")