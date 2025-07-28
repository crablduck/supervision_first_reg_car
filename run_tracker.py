#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频追踪系统运行脚本
自动检查环境并运行视频追踪
"""

import os
import sys
import subprocess
from pathlib import Path

def check_conda_env():
    """
    检查conda环境supervisionTest是否存在
    """
    try:
        result = subprocess.run(['conda', 'env', 'list'], 
                              capture_output=True, text=True, check=True)
        if 'supervisionTest' in result.stdout:
            print("✅ 发现conda环境: supervisionTest")
            return True
        else:
            print("⚠️  未发现conda环境: supervisionTest")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  conda命令不可用")
        return False

def create_conda_env():
    """
    创建conda环境supervisionTest
    """
    print("🔧 创建conda环境: supervisionTest")
    try:
        subprocess.run(['conda', 'create', '-n', 'supervisionTest', 'python=3.9', '-y'], 
                      check=True)
        print("✅ conda环境创建成功")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ conda环境创建失败")
        return False

def install_dependencies():
    """
    安装项目依赖
    """
    print("📦 安装项目依赖...")
    try:
        # 尝试使用pip安装
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False

def check_video_files():
    """
    检查视频文件是否存在
    """
    video_files = ['video1.mp4', 'video2.mp4']
    existing_files = []
    
    for video_file in video_files:
        if os.path.exists(video_file):
            existing_files.append(video_file)
            print(f"✅ 发现视频文件: {video_file}")
        else:
            print(f"⚠️  视频文件不存在: {video_file}")
    
    if not existing_files:
        print("\n📝 请将视频文件放置在当前目录下:")
        print("  - video1.mp4")
        print("  - video2.mp4")
        print("\n或者使用以下命令指定视频文件:")
        print("  python video_tracker.py --videos your_video1.mp4 your_video2.mp4")
        return False
    
    return existing_files

def run_tracker(video_files):
    """
    运行视频追踪器
    """
    print("\n🚀 启动视频追踪系统...")
    try:
        cmd = [sys.executable, 'video_tracker.py', '--videos'] + video_files
        subprocess.run(cmd, check=True)
        print("\n🎉 视频追踪完成！")
        return True
    except subprocess.CalledProcessError:
        print("❌ 视频追踪失败")
        return False

def main():
    """
    主函数
    """
    print("🎯 视频目标追踪系统")
    print("=" * 50)
    
    # 检查conda环境
    if not check_conda_env():
        print("\n尝试创建conda环境...")
        if not create_conda_env():
            print("继续使用当前Python环境...")
    
    # 安装依赖
    if not install_dependencies():
        print("请手动安装依赖: pip install -r requirements.txt")
        return
    
    # 检查视频文件
    video_files = check_video_files()
    if not video_files:
        return
    
    # 运行追踪器
    run_tracker(video_files)
    
    print("\n📁 输出文件位置: ./output/")
    print("🎬 处理后的视频文件以 '_tracked.mp4' 结尾")

if __name__ == "__main__":
    main()