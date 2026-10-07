import os
import pygame
from tkinter import Tk, Listbox, Button, filedialog, END, SINGLE, Label, Frame, Scale, HORIZONTAL, LEFT, BOTH, X

class CyberMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ CYBER AUDIO ENGINE v2.0")
        self.root.geometry("520x620")
        self.root.configure(bg="#0b0e14") # สีพื้นหลังเข้ม Cyber Dark
        self.root.resizable(False, False)

        # เริ่มต้นระบบเสียง Pygame
        pygame.mixer.init()

        self.playlist = []
        self.current_index = 0
        self.is_paused = False

        # โทนสีหลัก (Cyber Palette)
        BG_COLOR = "#0b0e14"
        CARD_BG = "#161b22"
        ACCENT_CYAN = "#00f3ff"
        ACCENT_PINK = "#ff0055"
        TEXT_COLOR = "#e6edf3"
        SUBTEXT_COLOR = "#8b949e"

        # --- ส่วนหัวข้อโปรแกรม ---
        header_frame = Frame(root, bg=BG_COLOR)
        header_frame.pack(fill=X, padx=20, pady=(20, 10))

        title_label = Label(
            header_frame,
            text="⚡ CYBER AUDIO PLAYER ⚡",
            font=("Helvetica", 16, "bold"),
            fg=ACCENT_CYAN,
            bg=BG_COLOR
        )
        title_label.pack()

        self.status_label = Label(
            header_frame,
            text="SYSTEM READY // NO TRACK LOADED",
            font=("Courier", 10, "bold"),
            fg=SUBTEXT_COLOR,
            bg=BG_COLOR
        )
        self.status_label.pack(pady=5)

        # --- ปุ่มเพิ่มเพลง ---
        add_btn = Button(
            root,
            text="➕ IMPORT AUDIO FILES",
            font=("Helvetica", 10, "bold"),
            bg=ACCENT_CYAN,
            fg="#000000",
            activebackground="#00c4d1",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.add_songs
        )
        add_btn.pack(pady=10)

        # --- กล่องแสดงรายการเพลง ---
        list_frame = Frame(root, bg=CARD_BG, highlightbackground=ACCENT_CYAN, highlightthickness=1)
        list_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.listbox = Listbox(
            list_frame,
            bg=CARD_BG,
            fg=TEXT_COLOR,
            selectbackground=ACCENT_PINK,
            selectforeground="#ffffff",
            font=("Consolas", 10),
            bd=0,
            highlightthickness=0,
            selectmode=SINGLE
        )
        self.listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- แถบปรับระดับเสียง (Volume Slider) ---
        vol_frame = Frame(root, bg=BG_COLOR)
        vol_frame.pack(fill=X, padx=30, pady=5)

        vol_label = Label(
            vol_frame,
            text="🔊 VOL",
            font=("Helvetica", 10, "bold"),
            fg=ACCENT_CYAN,
            bg=BG_COLOR
        )
        vol_label.pack(side=LEFT, padx=(0, 10))

        self.vol_slider = Scale(
            vol_frame,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            command=self.set_volume,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            troughcolor=CARD_BG,
            activebackground=ACCENT_CYAN,
            highlightthickness=0,
            bd=0,
            length=380
        )
        self.vol_slider.set(70)  # ค่าเริ่มต้นระดับเสียง 70%
        pygame.mixer.music.set_volume(0.7)
        self.vol_slider.pack(side=LEFT, fill=X, expand=True)

        # --- แผงปุ่มควบคุม (Controls) ---
        ctrl_frame = Frame(root, bg=BG_COLOR)
        ctrl_frame.pack(pady=20)

        btn_opts = {
            "font": ("Helvetica", 12, "bold"),
            "bg": CARD_BG,
            "fg": ACCENT_CYAN,
            "activebackground": ACCENT_CYAN,
            "activeforeground": "#000000",
            "bd": 0,
            "width": 5,
            "height": 1,
            "cursor": "hand2"
        }

        # ปุ่มถอยหลัง, เล่น, พัก, หยุด, ข้าม
        self.prev_btn = Button(ctrl_frame, text="⏮", command=self.prev_song, **btn_opts)
        self.prev_btn.grid(row=0, column=0, padx=5)

        self.play_btn = Button(ctrl_frame, text="▶", command=self.play_song, **btn_opts)
        self.play_btn.grid(row=0, column=1, padx=5)

        self.pause_btn = Button(ctrl_frame, text="⏸", command=self.pause_song, **btn_opts)
        self.pause_btn.grid(row=0, column=2, padx=5)

        self.stop_btn = Button(ctrl_frame, text="⏹", command=self.stop_song, **btn_opts)
        self.stop_btn.grid(row=0, column=3, padx=5)

        self.next_btn = Button(ctrl_frame, text="⏭", command=self.next_song, **btn_opts)
        self.next_btn.grid(row=0, column=4, padx=5)

    def add_songs(self):
        songs = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        for song in songs:
            if song not in self.playlist:
                self.playlist.append(song)
                song_name = os.path.basename(song)
                self.listbox.insert(END, f" Track: {song_name}")

    def play_song(self):
        selected = self.listbox.curselection()
        if selected:
            self.current_index = selected[0]
            song_path = self.playlist[self.current_index]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_paused = False
            
            song_name = os.path.basename(song_path)
            self.status_label.config(text=f"▶ PLAYING: {song_name[:28]}", fg="#00ff66")

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            if not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.status_label.config(text="⏸ PAUSED", fg="#ffaa00")
            else:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.status_label.config(text="▶ PLAYING", fg="#00ff66")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.status_label.config(text="⏹ STOPPED", fg="#ff0055")

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.update_selection_and_play()

    def prev_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.update_selection_and_play()

    def update_selection_and_play(self):
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(self.current_index)
        self.listbox.activate(self.current_index)
        self.play_song()

    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = Tk()
    app = CyberMusicPlayer(root)
    root.mainloop()