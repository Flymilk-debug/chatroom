import os
import subprocess
import requests

def download_video(url, save_path="C:\\Users\\xingc\\.spyder-py3\\video"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # 构造 you-get 命令
    cmd = [
        "you-get",
        "--format=dash-flv480-AVC",
        "--output-dir", save_path,
        url
    ]
    
    try:
        print("开始下载视频...")
        # 执行命令并捕获输出
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"✅ 视频下载完成！文件保存于：{save_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 视频下载失败：{e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 未知错误：{e}")
        return False

# 标签爬取部分同上