---
name: video-summarizer
description: 下载 YouTube 和 B站视频，使用 Whisper 进行语音识别，生成结构化的视频内容摘要。支持触发词：总结视频、下载视频、分析视频内容、这个视频讲了什么。适用平台：YouTube、Bilibili。支持 YouTube 标准链接、短链接，B站 BV号、av号、短链接。使用场景：当用户要求总结、分析、下载 YouTube 或 B站视频时使用此 skill。
---

# 视频智能总结 Skill

自动下载 YouTube 和 B站视频，使用 Whisper 进行语音识别，生成结构化的内容摘要。

## 功能特性

- **双平台支持**：支持 YouTube 和 B站视频下载
- **自动解析**：支持 YouTube 链接、B站 BV号/av号/短链接
- **语音识别**：使用 OpenAI Whisper 模型进行高精度语音转文字
- **智能总结**：基于语音识别文本生成结构化摘要
- **多语言支持**：自动检测视频语言（中文、英文等）
- **字幕导出**：生成 SRT 字幕文件和纯文本转录

## 使用方式

用户可以通过以下方式触发此 skill：

```
帮我总结这个 YouTube 视频：https://www.youtube.com/watch?v=xxxxx
总结这个 B站视频：https://www.bilibili.com/video/BV1xx411c7XD
分析这个视频讲了什么：https://youtu.be/xxxxx
下载并总结 BV1xx411c7XD
这个视频主要内容是什么：https://b23.tv/xxxxx
```

## 工作流程

### 1. 视频下载

使用 `yt-dlp` 下载视频音频流：

> ⚠️ Skill **video-summarizer** is not installed.

**参数：**
- `video_url`（必需）：视频链接（YouTube 或 B站）
- `--output-dir`：输出目录（默认：`/tmp/chat-skills-output/video-summarizer/downloads`）
- `--quality`：视频质量（默认：`best`）

**返回：**
```json
{
  "success": true,
  "platform": "youtube",
  "video_id": "xxxxx",
  "title": "视频标题",
  "audio_path": "/tmp/chat-skills-output/video-summarizer/downloads/xxxxx.m4a",
  "duration": 600,
  "url": "原始链接"
}
```

### 2. 语音识别

使用 Whisper 进行语音识别：

> ⚠️ Skill **video-summarizer** is not installed.

**参数：**
- `audio_path`（必需）：音频文件路径（步骤 1 返回的路径）
- `--model`：Whisper 模型（默认：`base`，可选：`tiny/base/small/medium/large`）
- `--language`：指定语言（默认自动检测）
- `--output-dir`：输出目录（默认：与音频文件同目录）

**返回：**
```json
{
  "success": true,
  "transcript": "完整的识别文本...",
  "srt_path": "/path/to/subtitles.srt",
  "txt_path": "/path/to/transcript.txt",
  "language": "zh",
  "duration": 600
}
```

### 3. 完整流程（推荐）

使用一键脚本完成下载+识别：

> ⚠️ Skill **video-summarizer** is not installed.

**参数：**
- `video_url`（必需）：视频链接
- `--whisper-model`：Whisper 模型（默认：`base`）
- `--keep-files`：保留下载的音频文件（默认删除）
- `--output-dir`：基础输出目录（默认：`/tmp/chat-skills-output/video-summarizer`）

**返回：**
```json
{
  "success": true,
  "video_info": {
    "platform": "youtube",
    "title": "视频标题",
    "duration": 600,
    "url": "原始链接"
  },
  "transcription": {
    "transcript": "完整文本...",
    "srt_path": "/path/to/subtitles.srt",
    "txt_path": "/path/to/transcript.txt",
    "language": "zh"
  }
}
```

### 4. 生成内容总结

获得识别文本后，生成结构化摘要：

```markdown
# 视频总结

## 视频信息
- **平台**: YouTube / Bilibili
- **标题**: [视频标题]
- **时长**: X分钟
- **语言**: 中文/英文
- **链接**: [原始链接]

## 核心观点

1. **观点一**：简要描述
2. **观点二**：简要描述
3. **观点三**：简要描述

## 详细内容

### 开头部分（0:00 - X:XX）
- 要点 1
- 要点 2

### 中间部分（X:XX - Y:YY）
- 要点 1
- 要点 2

### 结尾部分（Y:YY - 结束）
- 要点 1
- 要点 2

## 关键信息

- **重要数据**：列举视频中提到的重要数字、统计数据
- **专业术语**：解释视频中的专业名词
- **推荐资源**：视频中提到的工具、网站、书籍等

## 一句话总结

[用一句话概括视频的核心内容]
```

## Whisper 模型对比

| 模型 | 大小 | 速度 | 精度 | 推荐场景 |
|------|------|------|------|----------|
| tiny | ~39MB | 最快 | 较低 | 快速预览 |
| base | ~74MB | 快 | 中等 | 日常使用（推荐） |
| small | ~244MB | 中等 | 较高 | 要求较高精度 |
| medium | ~769MB | 较慢 | 高 | 专业用途 |
| large | ~2.9GB | 慢 | 最高 | 最高精度要求 |

## 环境要求

### 系统依赖

**FFmpeg**（必需，用于音频处理）：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# Windows
winget install Gyan.FFmpeg
```

**yt-dlp**（必需，用于下载视频）：

```bash
# 使用 pip 安装
pip install yt-dlp

# 或使用 brew (macOS)
brew install yt-dlp
```

### Python 依赖

```bash
pip install openai-whisper yt-dlp
```

## 注意事项

1. **首次使用 Whisper**：第一次运行时会自动下载模型文件（约 140MB - 3GB）
2. **视频时长**：建议处理 30 分钟以内的视频，超长视频识别时间会很长
3. **识别精度**：
   - `tiny/base`：速度快，适合快速预览
   - `small/medium`：平衡精度和速度
   - `large`：最高精度，但速度较慢
4. **磁盘空间**：确保有足够空间存储临时下载文件
5. **网络要求**：YouTube 可能需要代理访问

## 平台支持

### YouTube
- 标准链接：`https://www.youtube.com/watch?v=xxxxx`
- 短链接：`https://youtu.be/xxxxx`
- 自动选择最佳音频质量

### Bilibili
- 标准链接：`https://www.bilibili.com/video/BV1xx411c7XD`
- 短链接：`https://b23.tv/xxxxx`
- BV号：`BV1xx411c7XD`
- av号：`av12345678`

## 常见问题

**Q: 下载 YouTube 视频失败怎么办？**

A: 
1. 检查网络连接，可能需要配置代理
2. 确保 yt-dlp 是最新版本：`pip install -U yt-dlp`
3. 检查视频是否有地区限制

**Q: 识别结果不准确？**

A: 尝试使用更大的 Whisper 模型（如 `medium` 或 `large`）。

**Q: 处理时间太长？**

A: 使用更小的模型（如 `tiny` 或 `base`），或处理较短的视频。

**Q: B站视频下载失败？**

A: 检查视频是否需要登录观看，yt-dlp 支持通过 cookies 下载需要登录的视频。
