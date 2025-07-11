import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# 使用 ffmpeg 命令，而不是硬编码路径
FFMPEG_PATH = "ffmpeg"

def setup_logging(log_file):
    """设置日志记录"""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def convert_video(input_file, output_file, temp_output):
    """转换单个视频文件到 H264"""
    if os.path.isfile(output_file):
        logging.info(f"Skipped {input_file}: Output file {output_file} already exists.")
        return
    cmd = [
        FFMPEG_PATH,
        "-i", input_file,
        "-c:v", "libx264",
        "-c:a", "copy",
        "-y",
        temp_output
    ]
    logging.info(f"Converting {input_file} to H264...")
    try:
        subprocess.run(cmd, check=True)
        os.replace(temp_output, output_file)
        # print(f"Replaced original file with H264 version: {os.path.basename(input_file)}")
        logging.info(f"Conversion completed: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Conversion failed for {input_file}: {e}")
        logging.error(f"Conversion failed: {input_file}, error: {e}")

def convert_videos_to_h264(input_base_dir, output_base_dir):
    """收集所有需要转换的视频文件"""
    # 确保输出基目录存在
    os.makedirs(output_base_dir, exist_ok=True)
    
    log_file = os.path.join(output_base_dir, "convert_log.txt")
    setup_logging(log_file)

    tasks = []
    for chunk_dir in os.listdir(input_base_dir):
        chunk_path = os.path.join(input_base_dir, chunk_dir)
        if os.path.isdir(chunk_path):
            output_chunk_dir = os.path.join(output_base_dir, chunk_dir)
            os.makedirs(output_chunk_dir, exist_ok=True)
            
            # 遍历 chunk 目录下的所有子目录
            for camera_dir in os.listdir(chunk_path):
                camera_path = os.path.join(chunk_path, camera_dir)
                if os.path.isdir(camera_path) and camera_dir.startswith("observation.images."):
                    output_camera_dir = os.path.join(output_chunk_dir, camera_dir)
                    os.makedirs(output_camera_dir, exist_ok=True)
                    
                    for episode_file in os.listdir(camera_path):
                        if episode_file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                            input_file = os.path.join(camera_path, episode_file)
                            output_file = os.path.join(output_camera_dir, episode_file)
                            temp_output = output_file + ".tmp.mp4"
                            tasks.append((input_file, output_file, temp_output))
    return tasks

def main():
    input_base_dir = "/Users/macbook/Workspace/project/pjlab/test/S2data/a2d/task_2/videos"
    output_base_dir = "/Users/macbook/Workspace/project/pjlab/test/S2data/a2d/task_2/videos_h264"

    # 收集转换任务
    tasks = convert_videos_to_h264(input_base_dir, output_base_dir)

    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(convert_video, input_file, output_file, temp_output) 
                   for input_file, output_file, temp_output in tasks]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"Generated an exception: {exc}")
                logging.error(f"Exception occurred: {exc}")

    print(f" 输出路径：{output_base_dir}")
    logging.info(f"All videos processed. Output path: {output_base_dir}")
 
if __name__ == "__main__":
    main()