#!/usr/bin/env python3
"""
Download videos from YouTube and Bilibili
Supports: YouTube links, Bilibili BV/av numbers, short links
"""

import sys
import json
import subprocess
import argparse
import os
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Download video from YouTube or Bilibili')
    parser.add_argument('video_url', help='Video URL (YouTube or Bilibili)')
    parser.add_argument('--output-dir', default='/tmp/chat-skills-output/video-summarizer/downloads',
                       help='Output directory for downloaded files')
    parser.add_argument('--quality', default='best', help='Video quality (default: best)')
    return parser.parse_args()

def detect_platform(url):
    """Detect if URL is from YouTube or Bilibili"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'bilibili.com' in url or 'b23.tv' in url or url.startswith('BV') or url.startswith('av'):
        return 'bilibili'
    else:
        return 'unknown'

def download_video(video_url, output_dir, quality='best'):
    """Download video using yt-dlp"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    platform = detect_platform(video_url)
    
    # Normalize URL
    if platform == 'bilibili':
        if video_url.startswith('BV') or video_url.startswith('av'):
            video_url = f'https://www.bilibili.com/video/{video_url}'
    
    # Prepare yt-dlp command
    output_template = os.path.join(output_dir, '%(id)s.%(ext)s')
    
    cmd = [
        'yt-dlp',
        '--format', 'bestaudio/best',
        '--extract-audio',
        '--audio-format', 'm4a',
        '--output', output_template,
        '--print', 'after_move:filepath',
        '--print', 'id',
        '--print', 'title',
        '--print', 'duration',
        video_url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        
        # Parse output
        if len(lines) >= 4:
            video_id = lines[0]
            title = lines[1]
            duration = lines[2]
            audio_path = lines[3]
        else:
            raise Exception(f"Unexpected yt-dlp output: {result.stdout}")
        
        return {
            'success': True,
            'platform': platform,
            'video_id': video_id,
            'title': title,
            'audio_path': audio_path,
            'duration': int(float(duration)) if duration else 0,
            'url': video_url
        }
    
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': f'yt-dlp failed: {e.stderr}',
            'url': video_url
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': video_url
        }

def main():
    args = parse_args()
    result = download_video(args.video_url, args.output_dir, args.quality)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if not result['success']:
        sys.exit(1)

if __name__ == '__main__':
    main()
