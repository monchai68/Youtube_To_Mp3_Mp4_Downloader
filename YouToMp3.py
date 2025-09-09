#!/usr/bin/env python3
"""
YouTube Downloader - MP3 & MP4
A simple GUI application to download MP3 audio or MP4 video from YouTube videos, playlists, or channels
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp
import os
import sys
import threading
from urllib.parse import urlparse

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader - MP3 & MP4")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.download_path = tk.StringVar()
        self.download_path.set(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.is_downloading = False
        self.output_format = tk.StringVar(value="mp3")  # Default to MP3
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Downloader - MP3 & MP4", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input section
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50, font=('Arial', 10))
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Download path section
        ttk.Label(main_frame, text="Download Path:").grid(row=2, column=0, sticky=tk.W, pady=5)
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.download_path, 
                                   font=('Arial', 10))
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(path_frame, text="Browse", 
                  command=self.browse_download_path).grid(row=0, column=1)
        
        # Output format selection
        ttk.Label(main_frame, text="Output Format:").grid(row=3, column=0, sticky=tk.W, pady=5)
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Radiobutton(format_frame, text="MP3 (Audio Only)", 
                       variable=self.output_format, value="mp3", 
                       command=self.on_format_change).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(format_frame, text="MP4 (Video)", 
                       variable=self.output_format, value="mp4",
                       command=self.on_format_change).pack(side=tk.LEFT)
        
        # Quality selection
        ttk.Label(main_frame, text="Quality:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="best")
        self.quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                         values=["best", "320", "192", "128", "96"], 
                                         state="readonly", width=20)
        self.quality_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Download options
        options_frame = ttk.LabelFrame(main_frame, text="Download Options", padding="5")
        options_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.playlist_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Download entire playlist/channel", 
                       variable=self.playlist_var).grid(row=0, column=0, sticky=tk.W)
        
        self.metadata_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Add metadata (artist, title, etc.)", 
                       variable=self.metadata_var).grid(row=1, column=0, sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        self.download_btn = ttk.Button(button_frame, text="Download MP3", 
                                     command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", 
                                 command=self.stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=7, column=0, columnspan=2, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Log output
        ttk.Label(main_frame, text="Download Log:").grid(row=9, column=0, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, 
                                                 font=('Consolas', 9))
        self.log_text.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(10, weight=1)
        
    def browse_download_path(self):
        """Browse for download directory"""
        directory = filedialog.askdirectory(initialdir=self.download_path.get())
        if directory:
            self.download_path.set(directory)
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def on_format_change(self):
        """Handle format change between MP3 and MP4"""
        format_type = self.output_format.get()
        
        if format_type == "mp3":
            # Update button text and quality options for audio
            self.download_btn.config(text="Download MP3")
            self.quality_combo.config(values=["best", "320", "192", "128", "96"])
            self.log_message("Format changed to MP3 (Audio Only)")
        else:  # mp4
            # Update button text and quality options for video
            self.download_btn.config(text="Download MP4")
            self.quality_combo.config(values=["best", "1080p", "720p", "480p", "360p"])
            self.log_message("Format changed to MP4 (Video)")
        
        # Reset quality to "best" when format changes
        self.quality_var.set("best")
    
    def validate_url(self, url):
        """Validate YouTube URL"""
        youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com', 'www.youtube.com']
        try:
            parsed = urlparse(url)
            return any(domain in parsed.netloc.lower() for domain in youtube_domains)
        except:
            return False
    
    def get_ydl_opts(self):
        """Get yt-dlp options based on user selection"""
        format_type = self.output_format.get()
        file_extension = format_type
        
        output_path = os.path.join(self.download_path.get(), f'%(title)s.{file_extension}')
        
        opts = {
            'outtmpl': output_path,
            'ignoreerrors': True,
        }
        
        quality = self.quality_var.get()
        
        if format_type == "mp3":
            # MP3 (Audio only) configuration
            opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
                'extractaudio': True,
                'audioformat': 'mp3',
            })
            
            # Set audio quality for MP3
            if quality != "best" and quality.isdigit():
                opts['postprocessors'][0]['preferredquality'] = quality
                
        else:  # MP4 (Video)
            # MP4 (Video) configuration
            if quality == "best":
                opts['format'] = 'best[ext=mp4]/best'
            elif quality == "1080p":
                opts['format'] = 'best[height<=1080][ext=mp4]/best[height<=1080]'
            elif quality == "720p":
                opts['format'] = 'best[height<=720][ext=mp4]/best[height<=720]'
            elif quality == "480p":
                opts['format'] = 'best[height<=480][ext=mp4]/best[height<=480]'
            elif quality == "360p":
                opts['format'] = 'best[height<=360][ext=mp4]/best[height<=360]'
            else:
                opts['format'] = 'best[ext=mp4]/best'
            
            # Ensure MP4 output with video postprocessor if needed
            opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        
        # Add metadata if requested
        if self.metadata_var.get():
            opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            })
        
        # Playlist handling
        if not self.playlist_var.get():
            opts['noplaylist'] = True
        
        return opts
    
    def download_progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(f"Downloading: {percent:.1f}%")
            else:
                self.progress_var.set(f"Downloading: {d.get('downloaded_bytes', 0)} bytes")
        elif d['status'] == 'finished':
            self.progress_var.set("Processing audio...")
            self.log_message(f"Downloaded: {os.path.basename(d['filename'])}")
    
    def download_worker(self, url):
        """Worker thread for downloading"""
        try:
            # Validate URL
            if not self.validate_url(url):
                self.log_message("ERROR: Invalid YouTube URL")
                return
            
            # Create download directory if it doesn't exist
            os.makedirs(self.download_path.get(), exist_ok=True)
            
            format_type = self.output_format.get().upper()
            self.log_message(f"Starting {format_type} download from: {url}")
            
            # Configure yt-dlp
            opts = self.get_ydl_opts()
            opts['progress_hooks'] = [self.download_progress_hook]
            
            # Download
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Get video info first
                try:
                    info = ydl.extract_info(url, download=False)
                    if 'entries' in info:
                        # Playlist/Channel
                        count = len(info['entries'])
                        self.log_message(f"Found {count} videos to download")
                    else:
                        # Single video
                        self.log_message(f"Title: {info.get('title', 'Unknown')}")
                        self.log_message(f"Duration: {info.get('duration', 'Unknown')} seconds")
                except Exception as e:
                    self.log_message(f"Warning: Could not extract info - {str(e)}")
                
                # Start download
                ydl.download([url])
                
            format_type = self.output_format.get().upper()
            self.log_message(f"{format_type} download completed successfully!")
            
        except Exception as e:
            self.log_message(f"ERROR: {str(e)}")
        finally:
            # Reset UI
            self.root.after(0, self.download_finished)
    
    def start_download(self):
        """Start the download process"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not os.path.exists(self.download_path.get()):
            messagebox.showerror("Error", "Download path does not exist")
            return
        
        # Update UI
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.progress_var.set("Initializing download...")
        
        # Start download in separate thread
        self.download_thread = threading.Thread(target=self.download_worker, args=(url,))
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def stop_download(self):
        """Stop the download process"""
        if self.is_downloading:
            self.log_message("Stopping download...")
            # Note: yt-dlp doesn't have a clean way to stop mid-download
            # This is a limitation of the library
            self.download_finished()
    
    def download_finished(self):
        """Called when download is finished"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.progress_var.set("Ready")

def main():
    """Main function to run the application"""
    # Check if ffmpeg is available
    ffmpeg_available = False
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        ffmpeg_available = True
        print("✓ FFmpeg is available and ready for audio conversion")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try to refresh environment variables on Windows
        import os
        if os.name == 'nt':
            try:
                # Refresh PATH from registry
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                    machine_path = winreg.QueryValueEx(key, "PATH")[0]
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                    try:
                        user_path = winreg.QueryValueEx(key, "PATH")[0]
                    except FileNotFoundError:
                        user_path = ""
                
                os.environ['PATH'] = machine_path + ";" + user_path
                
                # Try FFmpeg again
                result = subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                ffmpeg_available = True
                print("✓ FFmpeg found after PATH refresh")
            except:
                pass
        
        if not ffmpeg_available:
            response = messagebox.askyesno(
                "FFmpeg Not Found", 
                "FFmpeg is required for audio conversion but was not found on your system.\n\n"
                "You can download it from https://ffmpeg.org/download.html\n"
                "or install it via package manager.\n\n"
                "Continue anyway? (Downloads may fail without FFmpeg)"
            )
            if not response:
                return
    
    # Create and run the application
    root = tk.Tk()
    app = YouTubeDownloader(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
