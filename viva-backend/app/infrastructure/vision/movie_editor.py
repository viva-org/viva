import os
from moviepy.editor import VideoFileClip

def compress_video_low_res(video_path, output_path, target_size, max_resolution=(480, 360)):
    # 读取视频
    clip = VideoFileClip(video_path)

    # 计算目标分辨率，保持原视频的宽高比
    aspect_ratio = clip.size[0] / clip.size[1]
    target_height = max_resolution[1]
    target_width = int(target_height * aspect_ratio)

    # 限制最大宽度，保持宽高比不变
    if target_width > max_resolution[0]:
        target_width = max_resolution[0]
        target_height = int(target_width / aspect_ratio)

    # 获取原视频文件大小（字节）
    original_size_bytes = os.path.getsize(video_path)

    # 计算压缩比率
    ratio = (target_size * 1024 * 1024) / original_size_bytes

    # 计算目标比特率
    target_bitrate = ratio * clip.reader.fps * target_width * target_height / clip.duration

    # 导出压缩视频
    clip.resize(newsize=(target_width, target_height)).write_videofile(output_path, bitrate=f"{int(target_bitrate)}k")



# 使用示例
video_path = "/Users/liuyishou/Library/Mobile Documents/com~apple~CloudDocs/B-口语之路/2024/240331.mp4"
output_path = "/Users/liuyishou/Library/Mobile Documents/com~apple~CloudDocs/B-口语之路/2024/240331_compressed.mp4"
target_size = 10.0  # 只有这个参数才可以实现 100 多 mb 的压缩成 100 以下的 ！！！

compress_video_low_res(video_path, output_path, target_size)
