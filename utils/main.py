import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import yt_dlp


def get_app_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))

    utils_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(utils_dir)


def get_resource_dir() -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

class YoutubeApp:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(theme="superhero")

        self.root.title("YouTube Downloader - Pro")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        self.is_downloading = False
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(pady=(10, 20), fill=X)
        
        ttk.Label(header_frame, text="Ytd Pro", font=("Orbitron", 26, "bold"), bootstyle="primary").pack()
        ttk.Label(header_frame, text="MP3 & MP4 • Auto-Folder • Anti-Doublons", font=("Segoe UI", 10), bootstyle="primary").pack()

        input_frame = ttk.Labelframe(main_frame, text="Lien", padding=15, bootstyle="primary")
        input_frame.pack(fill=X, pady=10)

        self.url_var = tk.StringVar()
        self.entry_url = ttk.Entry(input_frame, textvariable=self.url_var, font=("Consolas", 10))
        self.entry_url.pack(fill=X, expand=True)

        config_frame = ttk.Labelframe(main_frame, text="Format", padding=15, bootstyle="info")
        config_frame.pack(fill=X, pady=10)

        self.format_var = tk.StringVar(value="mp4")
        ttk.Radiobutton(config_frame, text="Vidéo MP4", variable=self.format_var, value="mp4", bootstyle="primary-toolbutton").pack(side=LEFT, padx=10, expand=True, fill=X)
        ttk.Radiobutton(config_frame, text="Audio MP3", variable=self.format_var, value="mp3", bootstyle="primary-toolbutton").pack(side=LEFT, padx=10, expand=True, fill=X)

        action_frame = ttk.Frame(main_frame, padding=20)
        action_frame.pack(fill=BOTH, expand=True)

        self.btn_download = ttk.Button(action_frame, text="⚡ LANCER ⚡", command=self.start_thread, bootstyle="warning", width=30, cursor="hand2")
        self.btn_download.pack(pady=(5, 15))

        self.progress = ttk.Progressbar(action_frame, bootstyle="info-striped", length=400, mode="determinate")
        self.progress.pack(fill=X, pady=5)

        self.lbl_counter = ttk.Label(action_frame, text="", font=("Segoe UI", 9, "bold"), bootstyle="warning", wraplength=600, justify="center")
        self.lbl_counter.pack(pady=2)

        self.lbl_status = ttk.Label(action_frame, text="Prêt", font=("Segoe UI", 9), bootstyle="secondary")
        self.lbl_status.pack()

        ttk.Label(self.root, text="Powered by yt-dlp & ffmpeg", font=("Segoe UI", 8), bootstyle="secondary").place(relx=0.98, rely=0.98, anchor=SE)

    def start_thread(self):
        url = self.url_var.get()
        if not url:
            messagebox.showerror("Erreur", "URL manquante.")
            return

        if self.is_downloading: return

        self.is_downloading = True
        self.btn_download.configure(state="disabled", text="EN COURS...")
        self.entry_url.configure(state="disabled")
        self.progress['value'] = 0
        self.lbl_status.configure(text="Analyse...")
        self.lbl_counter.configure(text="")
        
        threading.Thread(target=self.download_logic, args=(url, self.format_var.get()), daemon=True).start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = (downloaded / total) * 100
                    self.root.after(0, lambda: self.update_progress(percent))

                filename = os.path.basename(d.get('filename', ''))
                
                index = d.get('playlist_index')
                count = d.get('playlist_count')
                
                if index and count:
                    msg = f"[{index}/{count}] {filename}"
                else:
                    msg = filename
                
                self.root.after(0, lambda: self.lbl_counter.configure(text=msg))
                
            except:
                pass

        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.lbl_status.configure(text="Conversion en cours..."))
            self.root.after(0, lambda: self.progress.configure(value=100))

    def update_progress(self, percent):
        self.progress['value'] = percent
        self.lbl_status.configure(text=f"Téléchargement : {percent:.1f}%")

    def download_logic(self, url, fmt):
        try:
            base_dir = get_app_base_dir()
            resource_dir = get_resource_dir()

            target_folder = os.path.join(base_dir, "playlist_&_videos")
            os.makedirs(target_folder, exist_ok=True)

            ydl_opts = {
                'outtmpl': os.path.join(
                    target_folder,
                    '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'
                ),
                'download_archive': os.path.join(base_dir, 'archive.txt'),
                'retries': 10,
                'ignoreerrors': True,
                'ffmpeg_location': resource_dir,
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
            }

            if fmt == 'mp3':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4'
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.after(0, lambda: self.finish(True, f"Terminé !\nDossier : {target_folder}"))

        except Exception as e:
            self.root.after(0, lambda: self.finish(False, str(e)))

    def finish(self, success, message):
        self.is_downloading = False
        self.btn_download.configure(state="normal", text="⚡ LANCER")
        self.entry_url.configure(state="normal")
        self.lbl_status.configure(text="Prêt")
        self.lbl_counter.configure(text="")
        self.progress['value'] = 0
        
        if success:
            messagebox.showinfo("Succès", message)
        else:
            messagebox.showerror("Erreur", message)

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = YoutubeApp(root)
    root.mainloop()

#python -m PyInstaller --noconsole --onefile --name "YTD-Pro" main.py