import os
import re
import subprocess
import jieba
import jieba.analyse
import whisper

# ====================== 你原有的 B 站视频下载代码（完全未改动）======================
def download_bilibili_video(bv_id, output_dir="./video/"):
    """
    使用 you-get 下载 B 站视频
    :param bv_id: 视频 BV 号
    :param output_dir: 下载保存目录（默认 ./video/）
    :return: 下载后视频的完整路径
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ 已创建下载目录：{output_dir}")

    cmd = f'you-get -o {output_dir} https://www.bilibili.com/video/{bv_id}/'
    print(f"▶️ 正在执行下载命令：{cmd}")
    print("⏳ 开始下载... 请等待完成")

    try:
        result = os.system(cmd)
        if result == 0:
            print("✅ 视频下载完成！")
            abs_path = os.path.abspath(output_dir)
            print(f"📂 文件保存在：{abs_path}")
            # 找到下载的视频文件（假设目录下只有一个视频文件）
            for file in os.listdir(output_dir):
                if file.endswith(('.mp4', '.flv', '.mkv')):
                    return os.path.join(output_dir, file)
        else:
            print("❌ 下载失败，可能是网络问题或 BV 号错误。")
            return None
    except Exception as e:
        print(f"⚠️ 发生异常：{e}")
        return None

def extract_bvid_from_url(url):
    """
    从任意格式 B 站链接中提取 BV 号
    支持：完整播放链接、带参数链接、短链 b23.tv
    :param url: B 站视频链接
    :return: BV 号
    """
    pattern = r"BV([0-9A-Za-z]{10,})"
    match = re.search(pattern, url)
    if match:
        return match.group()
    else:
        raise ValueError("❌ 无法从链接中提取 BV 号，请检查链接格式")

# ====================== 优化后：视频标签分析模块（标签更丰富）======================
def extract_audio_from_video(video_path, output_audio="temp_audio.wav"):
    """从视频中提取音频（wav格式，适合ASR）"""
    cmd = f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar 16000 -ac 1 {output_audio} -y"
    subprocess.run(cmd, shell=True, check=True)
    return output_audio

def audio_to_text(audio_path, model_size="base"):
    """使用 Whisper 进行语音转文字"""
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

def extract_keywords(text, top_k=15):
    """提取文本关键词（TextRank，增加数量）"""
    keywords = jieba.analyse.textrank(text, topK=top_k, withWeight=False, allowPOS=('n', 'vn', 'v', 'a'))
    return keywords

# 扩充后的客户主标签库（模糊匹配用）
CUSTOM_TAGS = {
    "科技": ["AI", "Python", "编程", "代码", "算法", "程序员", "开发", "技术", "软件", "互联网", "前端", "后端"],
    "美食": ["做饭", "炒菜", "火锅", "烧烤", "美食", "探店", "料理", "烹饪", "小吃", "餐饮", "甜品", "饮品"],
    "美妆": ["化妆", "护肤", "口红", "粉底", "美妆", "教程", "彩妆", "香水", "美容", "美甲", "美发"],
    "知识": ["学习", "考试", "考研", "四六级", "知识", "科普", "教育", "课程", "读书", "干货", "公考"],
    "生活": ["日常", "vlog", "生活", "旅行", "探店", "家居", "好物", "分享", "生活方式", "通勤", "健身"],
    "娱乐": ["游戏", "综艺", "影视", "明星", "娱乐", "搞笑", "追剧", "动漫", "二次元", "直播", "电竞"]
}

# 细分标签库（多维度标签）
SUB_TAGS = {
    "编程语言": ["Python", "Java", "C++", "JavaScript", "Go", "PHP"],
    "美食类型": ["中餐", "西餐", "日料", "韩料", "甜品", "饮品", "夜宵"],
    "美妆品类": ["底妆", "眼妆", "唇妆", "护肤", "美发", "香水"],
    "知识领域": ["考研", "四六级", "公考", "职业技能", "兴趣科普", "语言学习"],
    "生活场景": ["居家", "通勤", "旅行", "探店", "健身", "购物"],
    "娱乐类型": ["游戏", "综艺", "影视", "动漫", "直播", "搞笑"]
}

def map_keywords_to_tags(keywords):
    """模糊匹配主标签"""
    tags = []
    for tag, keywords_list in CUSTOM_TAGS.items():
        for kw in keywords:
            if any(kw in target_kw or target_kw in kw for target_kw in keywords_list):
                tags.append(tag)
                break
    return list(set(tags))

def extract_sub_tags(keywords):
    """提取细分标签"""
    sub_tags = []
    for tag, keywords_list in SUB_TAGS.items():
        for kw in keywords:
            if any(kw in target_kw or target_kw in kw for target_kw in keywords_list):
                sub_tags.append(tag)
                break
    return list(set(sub_tags))

def get_full_tags(keywords):
    """生成多维度完整标签：主标签 + 细分标签 + 高频关键词"""
    main_tags = map_keywords_to_tags(keywords)
    sub_tags = extract_sub_tags(keywords)
    keyword_tags = keywords[:4]  # 取前4个高频关键词作为标签
    return main_tags + sub_tags + keyword_tags

def video_to_tags(video_path):
    """完整 pipeline：视频 → 音频 → 文本 → 关键词 → 多维度标签"""
    if not video_path:
        return [], []
    # 1. 提取音频
    audio_path = extract_audio_from_video(video_path)
    # 2. 音频转文字
    text = audio_to_text(audio_path)
    print(f"📝 识别文本预览：{text[:150]}...")  # 打印前150字预览
    # 3. 提取关键词（数量增加到15个）
    keywords = extract_keywords(text, top_k=15)
    # 4. 生成完整标签
    full_tags = get_full_tags(keywords)
    # 清理临时音频文件
    os.remove(audio_path)
    return full_tags, keywords

# ====================== 主程序入口（保留你原有的交互逻辑）======================
if __name__ == "__main__":
    print("🎬 B 站视频下载 & 标签分析工具")
    print("="*60)
    target_video = input("🔗 请输入 B 站视频链接（需包含 BV 号）：")
    try:
        bv_id = extract_bvid_from_url(target_video)
        print(f"✅ 提取到 BV 号：{bv_id}")
        # 1. 下载视频
        video_path = download_bilibili_video(bv_id)
        if video_path:
            print("\n🏷️  开始分析视频标签...")
            # 2. 生成丰富标签
            full_tags, keywords = video_to_tags(video_path)
            print("\n" + "="*60)
            print(f"🎯 最终标签（{len(full_tags)} 个）：{full_tags}")
            print(f"🔍 核心关键词：{keywords}")
            print("="*60)
    except Exception as e:
        print(f"❌ 错误：{e}")