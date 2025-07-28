#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础测试脚本 - 检查环境和基本功能
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python版本符合要求")
        return True
    else:
        print("❌ Python版本过低，需要3.8+")
        return False

def check_packages():
    """检查必要的包"""
    required_packages = [
        'cv2',
        'numpy', 
        'tqdm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    # 检查可选包
    optional_packages = {
        'supervision': 'supervision',
        'ultralytics': 'ultralytics',
        'torch': 'torch'
    }
    
    for package_name, import_name in optional_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name} 已安装")
        except ImportError:
            print(f"⚠️  {package_name} 未安装（可选）")
    
    return len(missing_packages) == 0

def check_video_files():
    """检查视频文件"""
    video_files = ['video1.mp4', 'video2.mp4']
    found_files = []
    
    for video_file in video_files:
        if os.path.exists(video_file):
            size = os.path.getsize(video_file) / (1024*1024)  # MB
            print(f"✅ 发现视频文件: {video_file} ({size:.1f}MB)")
            found_files.append(video_file)
        else:
            print(f"⚠️  视频文件不存在: {video_file}")
    
    return found_files

def create_sample_videos():
    """创建示例视频文件说明"""
    print("\n📝 创建示例视频文件说明...")
    
    sample_info = """
# 示例视频文件说明

## 视频文件要求
- 格式: MP4 (推荐)
- 分辨率: 任意 (建议不超过1920x1080)
- 时长: 建议不超过5分钟
- 内容: 包含行人、车辆、摩托车等目标

## 测试视频建议
1. 交通路口监控视频
2. 街道行人视频
3. 停车场监控视频

## 文件命名
- video1.mp4
- video2.mp4

或者使用命令行参数指定:
python video_tracker.py --videos your_video1.mp4 your_video2.mp4
"""
    
    with open('video_files_info.txt', 'w', encoding='utf-8') as f:
        f.write(sample_info)
    
    print("✅ 已创建 video_files_info.txt 说明文件")

def main():
    """主函数"""
    print("🔍 视频追踪系统环境检查")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    print("\n📦 检查依赖包...")
    packages_ok = check_packages()
    
    print("\n📹 检查视频文件...")
    video_files = check_video_files()
    
    print("\n📁 项目文件结构:")
    files = [
        'video_tracker.py',
        'run_tracker.py', 
        'requirements.txt',
        'README.md'
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    # 创建输出目录
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    print(f"✅ 输出目录: {output_dir.absolute()}")
    
    # 创建示例说明
    create_sample_videos()
    
    print("\n📋 环境检查总结:")
    if packages_ok:
        print("✅ 基础依赖包完整")
    else:
        print("❌ 缺少基础依赖包，请运行: pip install opencv-python numpy tqdm")
    
    if video_files:
        print(f"✅ 发现 {len(video_files)} 个视频文件")
        print("\n🚀 可以运行追踪系统:")
        print("   python run_tracker.py")
        print("   或")
        print("   python video_tracker.py")
    else:
        print("⚠️  未发现视频文件")
        print("\n📝 请参考 video_files_info.txt 准备视频文件")
    
    print("\n💡 提示:")
    print("   - 首次运行会自动下载YOLO模型")
    print("   - 建议使用GPU加速（需要CUDA）")
    print("   - 处理大视频文件需要足够内存")

if __name__ == "__main__":
    main()