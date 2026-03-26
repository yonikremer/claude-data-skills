---
name: ffmpeg
description: Processes and transforms audio, video, and image files using the FFmpeg CLI. Use for media conversion, compression, stream extraction, and complex filtering.
---
# FFmpeg

FFmpeg is the leading multimedia framework, able to decode, encode, transcode, mux, demux, stream, filter and play almost anything that humans and machines have created.

## Core Concepts

- **Muxing**: Combining multiple streams (video, audio, subtitles) into one container (MP4, MKV).
- **Transcoding**: Changing the encoding of a stream (e.g., H.264 to H.265).
- **Codecs**: The software/hardware used to compress/decompress (e.g., `libx264`, `aac`).

## Common Operations

### 1. Basic Conversion
```bash
# Convert video from one format to another
ffmpeg -i input.avi output.mp4

# Convert audio
ffmpeg -i input.wav output.mp3
```

### 2. Compression & Resizing
```bash
# Compress video using CRF (Constant Rate Factor, 0-51, 23 is default, lower is better quality)
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4

# Resize video to 720p while maintaining aspect ratio
ffmpeg -i input.mp4 -vf "scale=-1:720" output_720p.mp4
```

### 3. Stream Extraction & Manipulation
```bash
# Extract audio from video (without re-encoding)
ffmpeg -i input.mp4 -vn -acodec copy output.m4a

# Remove audio from video
ffmpeg -i input.mp4 -an output_silent.mp4

# Trim a clip (from 00:01:00 for 30 seconds)
ffmpeg -i input.mp4 -ss 00:01:00 -t 30 -c copy output_clip.mp4
```

### 4. Advanced Filtering
```bash
# Create a GIF from a video
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" output.gif

# Stack two videos side-by-side
ffmpeg -i left.mp4 -i right.mp4 -filter_complex hstack output_stacked.mp4

# Extract all frames as images
ffmpeg -i input.mp4 "frames/out-%03d.png"
```

## Professional Best Practices

- **Use `-c copy`**: Whenever possible, use `copy` for codecs to avoid quality loss and save CPU (muxing only).
- **Check Resources**: FFmpeg can consume 100% CPU. Run `get-available-resources` first.
- **Verification**: Always run `ffprobe input.mp4` to inspect stream metadata before processing.
- **Hardware Acceleration**: On supported systems, use `h264_nvenc` (NVIDIA) or `h264_videotoolbox` (Apple) for 10x faster encoding.

## Troubleshooting

- **Out of Sync**: If audio/video are out of sync, try `-async 1` or `-async 1 -vsync 1`.
- **Unknown Encoder**: Ensure the required library is installed (e.g., `libx264` for H.264).
- **Invalid Argument**: FFmpeg arguments are order-sensitive. Generally: `ffmpeg [global] [input_opts] -i input [output_opts] output`.
