import requests
import json
import time

REPO_OWNER = "YeHang-GitHub"
REPO_NAME = "Texture-Reference-Photo"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Images"

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

def fetch_directory_recursive(path="Images"):
    """ 递归获取 GitHub 仓库中的所有文件和目录 """
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        result = []
        for item in data:
            if item["type"] == "dir":  # 目录
                sub_items = fetch_directory_recursive(item["path"])  # 递归获取子目录内容
                result.append({
                    "name": item["name"],
                    "path": item["path"],
                    "type": "folder",
                    "children": sub_items
                })
            elif item["type"] == "file" and item["name"].lower().endswith((".jpg", ".png", ".jpeg", ".avif", ".webp")):
                result.append({
                    "name": item["name"],
                    "path": item["path"],
                    "type": "file",
                    "raw_url": f"https://cdn.jsdelivr.net/gh/{REPO_OWNER}/{REPO_NAME}@main/{item['path']}"
                })
            time.sleep(1)  # 避免 GitHub API 访问过快
        return result
    else:
        print(f"❌ 获取目录失败: {response.status_code}, {response.text}")
        return []

def save_directory_cache():
    """ 生成并保存完整的目录结构（包含图片文件） """
    print("📂 正在获取 GitHub 仓库目录...")
    directory_structure = fetch_directory_recursive()
    
    with open("directory_cache.json", "w", encoding="utf-8") as f:
        json.dump(directory_structure, f, indent=4, ensure_ascii=False)
    
    print("✅ 目录缓存已保存到 directory_cache.json")

save_directory_cache()