# YouTube Downloader - MP3 & MP4

A simple GUI application to download MP3 audio or MP4 video from YouTube videos, playlists, or channels.

## Features

- **Easy-to-use GUI**: Simple interface built with Tkinter
- **Multiple formats**: Choose between MP3 (audio only) or MP4 (video)
- **Multiple download options**: Single videos, playlists, or entire channels
- **Quality selection**: 
  - **MP3**: Choose audio quality (best, 320kbps, 192kbps, 128kbps, 96kbps)
  - **MP4**: Choose video quality (best, 1080p, 720p, 480p, 360p)
- **Metadata support**: Automatically adds title, artist, and other metadata to files
- **Progress tracking**: Real-time download progress and logging
- **Customizable download path**: Choose where to save your files

## Requirements

- Python 3.7 or higher
- FFmpeg (required for audio conversion)

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (required for audio conversion):
   
   **Windows:**
   - Download from https://ffmpeg.org/download.html
   - Extract and add to your system PATH
   - Or use chocolatey: `choco install ffmpeg`
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

## Usage

1. **Run the application**:
   ```bash
   python YouToMp3.py
   ```

2. **Enter a YouTube URL**:
   - Single video: `https://www.youtube.com/watch?v=VIDEO_ID`
   - Playlist: `https://www.youtube.com/playlist?list=PLAYLIST_ID`
   - Channel: `https://www.youtube.com/channel/CHANNEL_ID` or `https://www.youtube.com/@USERNAME`

3. **Configure options**:
   - Choose output format (MP3 or MP4)
   - Choose download path
   - Select quality (audio quality for MP3, video quality for MP4)
   - Enable/disable playlist download
   - Enable/disable metadata addition

4. **Click "Download MP3" or "Download MP4"** (button text changes based on format) and wait for completion

## Supported URLs

- Individual YouTube videos
- YouTube playlists
- YouTube channels
- YouTube shorts
- youtu.be shortened URLs

## Notes

- **Legal Notice**: Only download content you have permission to download. Respect copyright laws and YouTube's Terms of Service.
- **Performance**: Download speed depends on your internet connection and YouTube's servers.
- **File Names**: Files are saved with the video title as the filename.
- **Error Handling**: The app will continue downloading other videos in a playlist even if one fails.

## Troubleshooting

**"FFmpeg Not Found" Error:**
- Make sure FFmpeg is installed and available in your system PATH
- Try restarting your terminal/command prompt after installing FFmpeg

**Download Fails:**
- Check your internet connection
- Verify the YouTube URL is correct and accessible
- Some videos may be region-restricted or have download limitations

**Slow Downloads:**
- This is usually due to YouTube's rate limiting
- Try downloading during off-peak hours
- Consider reducing the quality setting

## License

This project is for educational purposes only. Please respect YouTube's Terms of Service and copyright laws when using this tool.
