import os
import json

def generate_image_data(images_dir, thumbnails_dir, output_file):
    image_data = []

    # 允许的图片格式
    valid_ext = ('.jpg', '.jpeg')  # 只支持 jpg/jpeg

    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(valid_ext):

                # 原图相对路径
                relative_path = os.path.relpath(os.path.join(root, file), images_dir)

                # 缩略图路径（与原图目录结构相同，但目录换成 Thumbnails）
                thumbnail_path = os.path.join(thumbnails_dir, relative_path)

                # 如果缩略图存在才写入 JSON（避免缺文件）
                if os.path.exists(thumbnail_path):
                    image_data.append({
                        'name': file,
                        'fullsize_path': os.path.join('Images', relative_path).replace("\\", "/"),
                        'thumbnail_path': thumbnail_path.replace("\\", "/")
                    })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(image_data, f, indent=4, ensure_ascii=False) 

if __name__ == "__main__":
    images_dir = 'Images'
    thumbnails_dir = 'Thumbnails'
    output_file = 'directory_cache.json'
    generate_image_data(images_dir, thumbnails_dir, output_file)
    print(f"Image data has been written to {output_file}")