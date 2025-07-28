#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频目标追踪系统
基于supervision库对视频中的行人、小轿车和摩托车进行轨迹追踪
"""

import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
import argparse
import os
import sys
from pathlib import Path
from tqdm import tqdm
import time

class VideoTracker:
    def __init__(self, model_path="yolov8n.pt"):
        """
        初始化视频追踪器
        
        Args:
            model_path: YOLO模型路径
        """
        print("🚀 初始化视频追踪系统...")
        
        # 加载YOLO模型
        try:
            self.model = YOLO(model_path)
            print(f"✅ 成功加载模型: {model_path}")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            sys.exit(1)
        
        # 初始化追踪器
        self.tracker = sv.ByteTrack()
        
        # 目标类别映射 (COCO数据集)
        self.target_classes = {
            0: "person",      # 行人
            2: "car",        # 小轿车
            3: "motorcycle", # 摩托车
            5: "bus",        # 公交车
            7: "truck"       # 卡车
        }
        
        # 颜色映射
        self.colors = {
            "person": (0, 255, 0),      # 绿色
            "car": (255, 0, 0),        # 蓝色
            "motorcycle": (0, 0, 255), # 红色
            "bus": (255, 255, 0),      # 青色
            "truck": (255, 0, 255)     # 紫色
        }
        
        print("✅ 追踪器初始化完成")
    
    def process_video(self, video_path, output_path=None):
        """
        处理单个视频文件
        
        Args:
            video_path: 输入视频路径
            output_path: 输出视频路径
        """
        if not os.path.exists(video_path):
            print(f"❌ 视频文件不存在: {video_path}")
            return False
        
        print(f"\n📹 开始处理视频: {video_path}")
        
        # 打开视频
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ 无法打开视频文件: {video_path}")
            return False
        
        # 获取视频信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📊 视频信息: {width}x{height}, {fps}FPS, 总帧数: {total_frames}")
        
        # 设置输出视频
        if output_path is None:
            output_path = video_path.replace('.mp4', '_tracked.mp4')
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 初始化统计信息
        detection_stats = {class_name: 0 for class_name in self.target_classes.values()}
        track_history = {}
        
        # 进度条
        pbar = tqdm(total=total_frames, desc="处理进度", unit="帧")
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # YOLO检测
            results = self.model(frame, verbose=False)
            
            # 转换为supervision格式
            detections = sv.Detections.from_ultralytics(results[0])
            
            # 过滤目标类别
            mask = np.isin(detections.class_id, list(self.target_classes.keys()))
            detections = detections[mask]
            
            # 更新追踪器
            detections = self.tracker.update_with_detections(detections)
            
            # 绘制检测结果和轨迹
            annotated_frame = self.draw_annotations(frame, detections, track_history)
            
            # 更新统计信息
            for class_id in detections.class_id:
                if class_id in self.target_classes:
                    detection_stats[self.target_classes[class_id]] += 1
            
            # 写入输出视频
            out.write(annotated_frame)
            
            # 更新进度条
            elapsed_time = time.time() - start_time
            fps_current = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            pbar.set_postfix({
                '当前FPS': f'{fps_current:.1f}',
                '检测数': len(detections),
                '行人': detection_stats.get('person', 0),
                '车辆': detection_stats.get('car', 0) + detection_stats.get('bus', 0) + detection_stats.get('truck', 0),
                '摩托车': detection_stats.get('motorcycle', 0)
            })
            pbar.update(1)
        
        # 清理资源
        cap.release()
        out.release()
        pbar.close()
        
        print(f"\n✅ 视频处理完成: {output_path}")
        print(f"📈 检测统计:")
        for class_name, count in detection_stats.items():
            if count > 0:
                print(f"  - {class_name}: {count} 次检测")
        
        return True
    
    def draw_annotations(self, frame, detections, track_history):
        """
        在帧上绘制检测框和轨迹
        
        Args:
            frame: 输入帧
            detections: 检测结果
            track_history: 轨迹历史
        
        Returns:
            annotated_frame: 标注后的帧
        """
        annotated_frame = frame.copy()
        
        if len(detections) == 0:
            return annotated_frame
        
        # 绘制检测框
        for i, (bbox, class_id, confidence, track_id) in enumerate(
            zip(detections.xyxy, detections.class_id, detections.confidence, detections.tracker_id)
        ):
            if class_id not in self.target_classes:
                continue
            
            class_name = self.target_classes[class_id]
            color = self.colors.get(class_name, (255, 255, 255))
            
            # 绘制边界框
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # 绘制标签
            label = f"{class_name} #{track_id} ({confidence:.2f})"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), color, -1)
            cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # 更新轨迹历史
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            if track_id not in track_history:
                track_history[track_id] = []
            track_history[track_id].append(center)
            
            # 限制轨迹长度
            if len(track_history[track_id]) > 30:
                track_history[track_id] = track_history[track_id][-30:]
            
            # 绘制轨迹
            if len(track_history[track_id]) > 1:
                points = np.array(track_history[track_id], dtype=np.int32)
                cv2.polylines(annotated_frame, [points], False, color, 2)
        
        return annotated_frame

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="视频目标追踪系统")
    parser.add_argument("--videos", nargs="+", default=["video1.mp4", "video2.mp4"],
                       help="输入视频文件列表")
    parser.add_argument("--model", default="yolov8n.pt", help="YOLO模型路径")
    parser.add_argument("--output-dir", default="output", help="输出目录")
    
    args = parser.parse_args()
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print("🎯 视频目标追踪系统启动")
    print("=" * 50)
    
    # 初始化追踪器
    tracker = VideoTracker(args.model)
    
    # 处理每个视频
    for video_path in args.videos:
        if os.path.exists(video_path):
            output_path = output_dir / f"{Path(video_path).stem}_tracked.mp4"
            success = tracker.process_video(video_path, str(output_path))
            if not success:
                print(f"❌ 处理失败: {video_path}")
        else:
            print(f"⚠️  视频文件不存在: {video_path}")
    
    print("\n🎉 所有视频处理完成！")
    print(f"📁 输出目录: {output_dir.absolute()}")

if __name__ == "__main__":
    main()