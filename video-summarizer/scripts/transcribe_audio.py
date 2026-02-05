#!/usr/bin/env python3
"""
Transcribe audio using OpenAI Whisper
Generates both SRT subtitles and plain text transcript
"""

import sys
import json
import argparse
import os
import whisper
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Transcribe audio using Whisper')
    parser.add_argument('audio_path', help='Path to audio file')
    parser.add_argument('--model', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--language', default=None, help='Audio language (auto-detect if not specified)')
    parser.add_argument('--output-dir', default=None, help='Output directory (default: same as audio file)')
    return parser.parse_args()

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(segments):
    """Generate SRT subtitle format"""
    srt_lines = []
    for i, segment in enumerate(segments, 1):
        start = format_timestamp(segment['start'])
        end = format_timestamp(segment['end'])
        text = segment['text'].strip()
        
        srt_lines.append(f"{i}")
        srt_lines.append(f"{start} --> {end}")
        srt_lines.append(text)
        srt_lines.append("")  # Empty line between subtitles
    
    return "\n".join(srt_lines)

def transcribe_audio(audio_path, model_name='base', language=None, output_dir=None):
    """Transcribe audio file using Whisper"""
    
    if not os.path.exists(audio_path):
        return {
            'success': False,
            'error': f'Audio file not found: {audio_path}'
        }
    
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(audio_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Load Whisper model
    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to load Whisper model: {str(e)}'
        }
    
    # Transcribe
    try:
        result = model.transcribe(audio_path, language=language)
    except Exception as e:
        return {
            'success': False,
            'error': f'Transcription failed: {str(e)}'
        }
    
    # Generate output files
    base_name = Path(audio_path).stem
    srt_path = os.path.join(output_dir, f"{base_name}.srt")
    txt_path = os.path.join(output_dir, f"{base_name}.txt")
    
    # Save SRT subtitles
    srt_content = generate_srt(result['segments'])
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    # Save plain text transcript
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    
    return {
        'success': True,
        'transcript': result['text'],
        'srt_path': srt_path,
        'txt_path': txt_path,
        'language': result['language'],
        'duration': result.get('duration', 0)
    }

def main():
    args = parse_args()
    result = transcribe_audio(args.audio_path, args.model, args.language, args.output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if not result['success']:
        sys.exit(1)

if __name__ == '__main__':
    main()
