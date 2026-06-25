import subprocess
import os
import json

def get_video_info(input_file):
    """Uses ffprobe to get the duration and file size of the video."""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', input_file
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        info = json.loads(result.stdout)
        
        duration = float(info['format']['duration'])
        size_bytes = int(info['format']['size'])
        return duration, size_bytes
    except Exception as e:
        print(f"Error reading video info: {e}")
        return None, None

def compress_video_to_half(input_file, output_file):
    """Compresses a video to exactly half its current file size."""
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    print(f"Analyzing '{input_file}'...")
    duration, original_size = get_video_info(input_file)
    
    if not duration or not original_size:
        print("Could not retrieve video information. Make sure FFmpeg is installed.")
        return

    # Calculate bitrates
    # Formula: Bitrate (bits per second) = (Size in bytes * 8) / Duration in seconds
    original_bitrate = (original_size * 8) / duration
    target_total_bitrate = original_bitrate / 2
    
    # We'll allocate a standard 128k (128000 bps) for audio, and the rest for video
    audio_bitrate = 128000
    target_video_bitrate = target_total_bitrate - audio_bitrate

    # If the target is too low, set a hard minimum to prevent the video from breaking
    if target_video_bitrate < 100000:
        target_video_bitrate = 100000
        print("Warning: Target video bitrate is extremely low. Quality will drop significantly.")

    print(f"Original Size: {original_size / (1024 * 1024):.2f} MB")
    print(f"Target Size: {(original_size / 2) / (1024 * 1024):.2f} MB")
    print(f"Target Video Bitrate: {int(target_video_bitrate)} bps")

    # Construct the FFmpeg command
    # -y overwrites output file if it exists
    # -c:v libx264 uses the standard H.264 encoder
    # -b:v sets the video bitrate
    # -c:a aac uses the standard AAC audio encoder
    # -b:a sets the audio bitrate
    cmd = [
        'ffmpeg', '-y', 
        '-i', input_file,
        '-c:v', 'libx264',
        '-b:v', str(int(target_video_bitrate)),
        '-c:a', 'aac',
        '-b:a', '128k',
        output_file
    ]

    print(f"Starting compression... This might take a few minutes depending on the video length.")
    
    # Run the compression
    try:
        subprocess.run(cmd, check=True)
        print(f"\nSuccess! Compressed video saved to '{output_file}'")
    except subprocess.CalledProcessError as e:
        print(f"\nError during compression. FFmpeg failed.")

# --- Usage Example ---
if __name__ == "__main__":
    # Replace these with your actual file names
    input_video = "teaser.mp4"
    output_video = "teaser_compressed.mp4"
    
    compress_video_to_half(input_video, output_video)