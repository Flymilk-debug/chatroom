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

# 你只需要把之前的代码替换成下面这段，最后一行已经改好，并增加了云平台适配。
if __name__ == "__main__":
    print("="*50)
    print("📺 B 站视频下载工具（带官方标签爬取功能）")
    print("="*50)
    target_video = input("👉 请输入 B 站视频链接（需包含 BV 号）: ")
    try:
        bv_id = extract_bvid_from_url(target_video)
        print(f"🔍 提取到 BV 号: {bv_id}")
        download_bilibili_video(bv_id)
        # 云平台环境兼容：避免自动退出导致日志丢失
        input("\n✅ 任务已结束，按回车退出...")
    except Exception as e:
        print(f"❌ 错误: {e}")
        input("\n按回车退出...")
from flask import Flask, render_template_string, request, session, redirect, url_for
from uuid import uuid4
import os

# ====================== 安全配置 ======================
app = Flask(__name__)
# 每次启动随机密钥，重启后所有旧会话自动失效
app.secret_key = os.urandom(32)

# ====================== 全局内存存储（重启即消失） ======================
active_rooms = {}    # 临时房间
user_tags = {}       # 用户标签
user_to_room = {}    # 用户所在房间

# ====================== 标签相似度计算 ======================
def similarity(uid_a, uid_b):
    if uid_a not in user_tags or uid_b not in user_tags:
        return 0.0
    set_a = set(user_tags[uid_a])
    set_b = set(user_tags[uid_b])
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return inter / union if union != 0 else 0.0

def find_similar(uid, threshold=0.2):
    for user in user_tags:
        if user == uid:
            continue
        sim = similarity(uid, user)
        if sim >= threshold:
            return user
    return None

# ====================== 临时房间创建/销毁 ======================
def create_room(uid1, uid2):
    room_id = str(uuid4())
    active_rooms[room_id] = {
        "users": [uid1, uid2],
        "messages": []
    }
    user_to_room[uid1] = room_id
    user_to_room[uid2] = room_id

def destroy_room(room_id):
    if room_id not in active_rooms:
        return
    uids = active_rooms[room_id]["users"]
    for uid in uids:
        if uid in user_to_room:
            del user_to_room[uid]
    del active_rooms[room_id]

# ====================== 网页界面 ======================
PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>临时兴趣聊天室 · 用完即焚</title>
    <style>
        body{max-width:700px;margin:20px auto;font-family:Arial;padding:10px;}
        .chat-box{border:1px solid #ddd;height:400px;overflow-y:auto;padding:10px;margin:10px 0;}
        .msg{margin:6px 0;padding:8px;border-radius:6px;max-width:70%;}
        .me{background:#e3f2fd;margin-left:auto;text-align:right;}
        .other{background:#f5f5f5;margin-right:auto;}
        input,button{padding:8px;margin:4px 0;width:100%;box-sizing:border-box;}
        button{background:#4285f4;color:white;border:none;border-radius:4px;cursor:pointer;}
        .danger{background:#ff5252;}
    </style>
</head>
<body>
    <h2>🔐 临时兴趣交流平台（退出即销毁）</h2>

    {% if not session.uid %}
        <form method=post action=/login>
            <input name=uid placeholder="输入你的临时昵称/ID" required>
            <input name=tags placeholder="输入兴趣标签，用逗号分隔：手游,动漫,编程">
            <button type=submit>进入</button>
        </form>
    {% else %}
        <p>你：{{ session.uid }} | <a href= >退出登录（销毁数据）</a ></p >

        {% if session.uid in user_to_room %}
            <div class=chat-box>
                {% for m in active_rooms[user_to_room[session.uid]].messages %}
                <div class="msg {{ 'me' if m.from == session.uid else 'other' }}">
                    {{ m.content }}
                </div>
                {% endfor %}
            </div>
            <form method=post action=/send>
                <input name=content placeholder="可发联系方式，退出即消失" required>
                <button type=submit>发送</button>
            </form>
            <form method=post action=/leave>
                <button type=submit class=danger>结束聊天并销毁房间</button>
            </form>
        {% else %}
            <form method=post action=/match>
                <button type=submit>匹配兴趣相似的人</button>
            </form>
        {% endif %}
    {% endif %}
</body>
</html>
"""

# ====================== 路由 ======================
@app.route('/')
def index():
    return render_template_string(PAGE,
        session=session,
        active_rooms=active_rooms,
        user_to_room=user_to_room)

@app.route('/login', methods=['POST'])
def login():
    uid = request.form['uid'].strip()
    tags = [t.strip() for t in request.form['tags'].split(',') if t.strip()]
    session['uid'] = uid
    user_tags[uid] = tags
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def match():
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('index'))
    other = find_similar(uid)
    if other:
        create_room(uid, other)
    return redirect(url_for('index'))

@app.route('/send', methods=['POST'])
def send():
    uid = session.get('uid')
    if uid not in user_to_room:
        return redirect(url_for('index'))
    room = user_to_room[uid]
    content = request.form['content'].strip()
    if content:
        active_rooms[room]['messages'].append({
            "from": uid,
            "content": content
        })
    return redirect(url_for('index'))

@app.route('/leave', methods=['POST'])
def leave():
    uid = session.get('uid')
    if uid in user_to_room:
        destroy_room(user_to_room[uid])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    uid = session.get('uid')
    if uid in user_to_room:
        destroy_room(user_to_room[uid])
    session.clear()
    return redirect(url_for('index'))

# ====================== 启动（云平台专用） ======================
if __name__ == '__main__':
    # Replit 会自动读取环境变量，不需要手动改 host
    app.run(host='0.0.0.0', port=5000, debug=False)