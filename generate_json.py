import os
import json

def generate_image_data(images_dir, thumbnails_dir, output_file):
    image_data = []

    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                relative_path = os.path.relpath(os.path.join(root, file), images_dir)
                thumbnail_path = os.path.join(thumbnails_dir, relative_path)
                if os.path.exists(thumbnail_path):
                    image_data.append({
                        'name': file,
                        'fullsize_path': os.path.join('Images', relative_path),
                        'thumbnail_path': thumbnail_path
                    })

    with open(output_file, 'w') as f:
        json.dump(image_data, f, indent=4)

if __name__ == "__main__":
    images_dir = 'Images'
    thumbnails_dir = 'Thumbnails'
    output_file = 'directory_cache.json'
    generate_image_data(images_dir, thumbnails_dir, output_file)
    print(f"Image data has been written to {output_file}")