from PIL import Image
import os
# Ensure pillow-avif-plugin is installed: pip install pillow-avif-plugin
try:
    import pillow_avif
except ImportError:
    print("pillow-avif-plugin is not installed. AVIF files might not be processed correctly. Please run: pip install pillow-avif-plugin")
from multiprocessing import Pool, cpu_count

# 提高 Pillow 允许的最大像素
Image.MAX_IMAGE_PIXELS = None

# 输入/输出目录
INPUT_DIR = "Images"
OUTPUT_DIR = "Thumbnails"
THUMBNAIL_SIZE = (1024, 1024)  # 设定缩略图大小

# 确保输出目录存在
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_image(file_info):
    """ 生成单个缩略图 """
    input_path, output_path = file_info
    
    try:
        with Image.open(input_path) as img:
            img.thumbnail(THUMBNAIL_SIZE)  # 生成缩略图（保持原比例）
            img.save(output_path)  # 保存缩略图
            print(f"✅ 生成缩略图: {output_path}")
    except Exception as e:
        print(f"❌ 处理失败: {input_path}，错误: {e}")

def get_image_files():
    """ 获取所有图片文件，并保持目录结构 """
    file_list = []
    
    for root, _, files in os.walk(INPUT_DIR):
        relative_path = os.path.relpath(root, INPUT_DIR)  # 计算相对路径
        target_path = os.path.join(OUTPUT_DIR, relative_path)  # 对应的 Thumbnails 目录
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)  # 确保目标目录存在
        
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif')):  # 处理常见格式
                input_path = os.path.join(root, file)
                output_path = os.path.join(target_path, file)  # 保持原文件名
                file_list.append((input_path, output_path))

    return file_list

def generate_thumbnails():
    """ 使用多进程加速缩略图生成 """
    image_files = get_image_files()

    if not image_files:
        print("⚠️ 没有找到图片文件！")
        return

    num_workers = min(cpu_count(), len(image_files))  # 使用 CPU 最大核心数
    print(f"🚀 开始生成 {len(image_files)} 张缩略图，使用 {num_workers} 个进程")

    with Pool(num_workers) as pool:
        pool.map(process_image, image_files)

    print("🎉 缩略图生成完成！")

if __name__ == "__main__":
    generate_thumbnails()