import os
import json
import subprocess

def get_last_commit_with_large_images():
    """获取最后一次包含大于5MB图片的提交中的所有图片文件列表"""
    try:
        # 获取所有提交的哈希值
        commits = subprocess.check_output(
            ['git', 'log', '--pretty=format:%H', '--', 'Images/'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        ).decode('utf-8').strip().split('\n')
        
        for commit in commits:
            # 获取该提交中修改的文件列表
            changed_files = subprocess.check_output(
                ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit],
                cwd=os.path.dirname(os.path.abspath(__file__))
            ).decode('utf-8').strip().split('\n')
            
            # 筛选出 Images/ 目录下的 jpg/jpeg 文件
            image_files = [f for f in changed_files if f.startswith('Images/') and f.lower().endswith(('.jpg', '.jpeg'))]
            
            # 检查是否有大于5MB的图片
            has_large_image = False
            for img_file in image_files:
                img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_file)
                if os.path.exists(img_path):
                    file_size = os.path.getsize(img_path)
                    if file_size > 5 * 1024 * 1024:  # 5MB
                        has_large_image = True
                        break
            
            # 如果找到了包含大图的提交，返回该提交中的所有图片
            if has_large_image:
                print(f"Found last commit with large images: {commit[:8]}")
                print(f"Images in this commit: {len(image_files)}")
                return set(image_files)
        
        print("No commits with large images found")
        return set()
    
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return set()
    except Exception as e:
        print(f"Error getting git history: {e}")
        return set()

def generate_image_data(images_dir, thumbnails_dir, output_file):
    image_data = []
    
    # 获取最后一批上传的图片列表
    last_batch_images = get_last_commit_with_large_images()
    print(f"Total files in last batch: {len(last_batch_images)}")

    # 允许的图片格式
    valid_ext = ('.jpg', '.jpeg')  # 只支持 jpg/jpeg

    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(valid_ext):

                # 原图相对路径
                relative_path = os.path.relpath(os.path.join(root, file), images_dir)
                full_path = os.path.join(root, file)

                # 缩略图路径（与原图目录结构相同，但目录换成 Thumbnails）
                thumbnail_path = os.path.join(thumbnails_dir, relative_path)

                # 如果缩略图存在才写入 JSON（避免缺文件）
                if os.path.exists(thumbnail_path):
                    file_size = os.path.getsize(full_path)
                    # 获取文件修改时间（Unix时间戳）
                    modified_time = os.path.getmtime(full_path)
                    
                    # 检查是否属于最后一批上传
                    git_path = os.path.join('Images', relative_path).replace("\\", "/")
                    is_new = git_path in last_batch_images
                    
                    image_data.append({
                        'name': file,
                        'fullsize_path': git_path,
                        'thumbnail_path': thumbnail_path.replace("\\", "/"),
                        'size': file_size,
                        'modified_time': int(modified_time),
                        'is_new': is_new  # 添加是否为新图片的标记
                    })

    # 统计新图片数量
    new_count = sum(1 for item in image_data if item['is_new'])
    print(f"Total images: {len(image_data)}, New images: {new_count}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(image_data, f, indent=4, ensure_ascii=False) 

if __name__ == "__main__":
    images_dir = 'Images'
    thumbnails_dir = 'Thumbnails'
    output_file = 'directory_cache.json'
    generate_image_data(images_dir, thumbnails_dir, output_file)
    print(f"Image data has been written to {output_file}")
