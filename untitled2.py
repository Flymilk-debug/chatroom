import os
import re
import requests

def download_bilibili_video(bv_id, output_dir="./video/"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📂 已创建下载目录: {output_dir}")
    
    video_url = f'https://www.bilibili.com/video/{bv_id}'
    cmd = f'you-get -o {output_dir} {video_url}'
    print(f"▶️  正在执行下载命令: {cmd}")
    print("⏳ 开始下载... 请等待完成")
    
    try:
        result = os.system(cmd)
        if result == 0:
            print("✅ 视频下载完成！")
            abs_path = os.path.abspath(output_dir)
            print(f"📁 文件保存在: {abs_path}")
            
            print("\n🔍 开始爬取视频官方标签...")
            tags = get_bilibili_tags(bv_id)
            if tags:
                print(f"🏷️  成功获取B站官方标签: {tags}")
            else:
                print("⚠️  未获取到标签（可能是网络问题或视频无公开标签）")
        else:
            print("❌ 下载失败，可能是网络问题或 BV 号错误。")
    except Exception as e:
        print(f"⚠️  发生异常: {e}")

def extract_bvid_from_url(url):
    pattern = r'BV[0-9A-Za-z]{10,}'
    match = re.search(pattern, url)
    if match:
        return match.group()
    else:
        raise ValueError("❌ 无法从链接中提取 BV 号，请检查链接格式")

def get_bilibili_tags(bv_id):
    """
    ✅ 修复版：调用B站标签专用接口获取标签
    """
    # 1. 先通过 view 接口获取 aid（视频aid，标签接口需要aid参数）
    view_api = f'https://api.bilibili.com/x/web-interface/view?bvid={bv_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # 第一步：获取视频aid
        view_resp = requests.get(view_api, headers=headers, timeout=10)
        view_resp.raise_for_status()
        view_data = view_resp.json()
        
        if view_data.get('code') != 0:
            print(f"❌ 获取视频信息失败：{view_data.get('message')}")
            return None
        aid = view_data['data']['aid']
        
        # 第二步：调用标签专用接口
        tag_api = f'https://api.bilibili.com/x/tag/archive/tags?aid={aid}'
        tag_resp = requests.get(tag_api, headers=headers, timeout=10)
        tag_resp.raise_for_status()
        tag_data = tag_resp.json()
        
        if tag_data.get('code') == 0:
            tags = [tag['tag_name'] for tag in tag_data['data']]
            return tags
        else:
            print(f"❌ 标签爬取失败：{tag_data.get('message', '未知错误')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  标签爬取异常：{e}")
        return None
    except KeyError as e:
        print(f"⚠️  数据解析错误：缺少字段 {e}")
        return None

if __name__ == "__main__":
    print("="*50)
    print("📺 B 站视频下载工具（带官方标签爬取功能）")
    print("="*50)
    target_video = input("👉 请输入 B 站视频链接（需包含 BV 号）: ")
    try:
        bv_id = extract_bvid_from_url(target_video)
        print(f"🔍 提取到 BV 号: {bv_id}")
        download_bilibili_video(bv_id)
    except Exception as e:
        print(f"❌ 错误: {e}")
        