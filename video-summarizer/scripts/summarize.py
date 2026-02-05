#!/usr/bin/env python3
"""
Complete workflow: Download video, transcribe, and prepare for summary
"""

import sys
import json
import argparse
import subprocess
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Download and transcribe video')
    parser.add_argument('video_url', help='Video URL (YouTube or Bilibili)')
    parser.add_argument('--whisper-model', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--keep-files', action='store_true',
                       help='Keep downloaded video/audio files (default: delete)')
    parser.add_argument('--output-dir', default='/tmp/chat-skills-output/video-summarizer',
                       help='Base output directory')
    return parser.parse_args()

def run_script(script_name, args):
    """Run a script and return parsed JSON output"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    
    cmd = ['python3', script_path] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"{script_name} failed: {result.stderr}")
    
    return json.loads(result.stdout)

def main():
    args = parse_args()
    
    download_dir = os.path.join(args.output_dir, 'downloads')
    transcript_dir = os.path.join(args.output_dir, 'transcripts')
    
    try:
        # Step 1: Download video
        print("📥 Downloading video...", file=sys.stderr)
        download_result = run_script('download_video.py', [
            args.video_url,
            '--output-dir', download_dir
        ])
        
        if not download_result['success']:
            raise Exception(f"Download failed: {download_result.get('error', 'Unknown error')}")
        
        print(f"✅ Downloaded: {download_result['title']}", file=sys.stderr)
        audio_path = download_result['audio_path']
        
        # Step 2: Transcribe audio
        print(f"🎤 Transcribing audio (model: {args.whisper_model})...", file=sys.stderr)
        transcribe_result = run_script('transcribe_audio.py', [
            audio_path,
            '--model', args.whisper_model,
            '--output-dir', transcript_dir
        ])
        
        if not transcribe_result['success']:
            raise Exception(f"Transcription failed: {transcribe_result.get('error', 'Unknown error')}")
        
        print(f"✅ Transcribed: {transcribe_result['language']}", file=sys.stderr)
        
        # Step 3: Cleanup if requested
        if not args.keep_files:
            os.remove(audio_path)
            print("🗑️  Cleaned up audio file", file=sys.stderr)
        
        # Combine results
        result = {
            'success': True,
            'video_info': download_result,
            'transcription': transcribe_result
        }
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
