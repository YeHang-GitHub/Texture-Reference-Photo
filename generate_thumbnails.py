from PIL import Image
import os

from multiprocessing import Pool, cpu_count

Image.MAX_IMAGE_PIXELS = None

INPUT_DIR = "Images"
OUTPUT_DIR = "Thumbnails"
THUMBNAIL_SIZE = (1024, 1024)

# 输出缩略图格式为 JPG
OUTPUT_EXT = ".jpg"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_image(file_info):
    input_path, output_path = file_info
    
    # 目标缩略图强制 .jpg
    output_path = os.path.splitext(output_path)[0] + OUTPUT_EXT

    try:
        with Image.open(input_path) as img:
            img.thumbnail(THUMBNAIL_SIZE)

            # 保存成 JPG（quality 可调节）
            img.save(output_path, format="JPEG", quality=60)

        print(f"✅ 生成缩略图: {output_path}")

    except Exception as e:
        print(f"❌ 处理失败: {input_path}，错误: {e}")

def get_image_files():
    valid_ext = ('.jpg', '.jpeg')  # 只支持 jpg/jpeg
    file_list = []
    
    for root, _, files in os.walk(INPUT_DIR):
        relative = os.path.relpath(root, INPUT_DIR)
        target_dir = os.path.join(OUTPUT_DIR, relative)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for file in files:
            if file.lower().endswith(valid_ext):
                input_path = os.path.join(root, file)

                # 输出路径同名但后缀改成 .jpg
                output_raw = os.path.join(target_dir, file)

                file_list.append((input_path, output_raw))

    return file_list

def clean_orphaned_thumbnails():
    removed = 0

    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            thumb = os.path.join(root, file)

            # 原图路径（换目录，保持路径结构）
            relative = os.path.relpath(thumb, OUTPUT_DIR)
            original_ext_removed = os.path.splitext(relative)[0]
            possible_matches = [
                original_ext_removed + ext
                for ext in ('.jpg', '.jpeg')  # 只支持 jpg/jpeg
            ]

            original_exists = any(
                os.path.exists(os.path.join(INPUT_DIR, pm))
                for pm in possible_matches
            )

            if not original_exists:
                os.remove(thumb)
                print(f"🗑️ 删除孤立缩略图: {thumb}")
                removed += 1

    if removed > 0:
        print(f"♻️ 已清理 {removed} 个孤立缩略图")

    # 清理空文件夹
    for root, dirs, files in os.walk(OUTPUT_DIR, topdown=False):
        for d in dirs:
            folder = os.path.join(root, d)
            if not os.listdir(folder):
                os.rmdir(folder)
                print(f"🗑️ 删除空文件夹: {folder}")

def generate_thumbnails():
    image_files = get_image_files()

    if not image_files:
        print("⚠️ 未找到图片文件")
        return

    num = min(cpu_count(), len(image_files))
    print(f"🚀 开始生成 {len(image_files)} 张缩略图，使用 {num} 进程")

    with Pool(num) as pool:
        pool.map(process_image, image_files)

    print("🎉 缩略图生成完成")

    clean_orphaned_thumbnails()

if __name__ == "__main__":
    generate_thumbnails()