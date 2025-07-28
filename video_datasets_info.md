# 视频数据集信息

## 推荐的公开数据集

### 1. KITTI数据集
- 网址: http://www.cvlibs.net/datasets/kitti/
- 内容: 自动驾驶场景，包含车辆、行人
- 格式: 图像序列和视频
- 许可: 学术使用免费

### 2. MOT Challenge数据集
- 网址: https://motchallenge.net/
- 内容: 多目标追踪基准数据集
- 格式: 视频序列
- 许可: 学术使用

### 3. UA-DETRAC数据集
- 网址: http://detrac-db.rit.albany.edu/
- 内容: 交通监控视频
- 格式: MP4视频文件
- 许可: 学术研究

### 4. VisDrone数据集
- 网址: http://aiskyeye.com/
- 内容: 无人机视角的交通场景
- 格式: 视频和图像
- 许可: 学术使用

## 在线视频源

### 1. Pixabay (免费商用)
- 网址: https://pixabay.com/videos/
- 搜索关键词: traffic, street, pedestrian, car
- 许可: Pixabay License (免费商用)

### 2. Pexels (免费商用)
- 网址: https://www.pexels.com/videos/
- 搜索关键词: traffic, city, street, car
- 许可: Pexels License (免费商用)

### 3. Unsplash (免费商用)
- 网址: https://unsplash.com/
- 主要是图片，但也有一些视频
- 许可: Unsplash License

## 使用建议

1. **测试用途**: 使用Pixabay或Pexels的免费视频
2. **学术研究**: 使用KITTI、MOT等学术数据集
3. **商业用途**: 确保获得适当的许可

## 下载方法

1. 手动下载: 访问上述网站手动下载
2. 使用脚本: 运行download_youtube_videos.py（需要yt-dlp）
3. 数据集API: 某些数据集提供API下载

## 文件命名建议

- video1.mp4, video2.mp4 (默认)
- traffic_scene1.mp4, pedestrian_scene1.mp4 (描述性)
- dataset_name_001.mp4 (数据集命名)
