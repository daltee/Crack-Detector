import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import numpy as np

# -----------------------------------------------------------------------------
# CORE LOGIC INTEGRATION
# -----------------------------------------------------------------------------
from preprocessing import preprocess_image
from fft_logic import apply_fft_filter

class CrackDetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Crack Detector Pro - Infrastructure Analysis")
        self.geometry("1200x900")
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        self.current_theme_color = "#2FA572"

        self.image_array = None
        self.current_frame = None
        self.camera_active = False
        self.cap = None

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CRACK DETECTOR",
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_upload = ctk.CTkButton(self.sidebar_frame, text="📁 Upload Image",
                                        command=self.upload_image, height=40)
        self.btn_upload.grid(row=1, column=0, padx=20, pady=10)

        self.btn_camera = ctk.CTkButton(self.sidebar_frame, text="📷 Start Camera Feed",
                                        command=self.toggle_camera, height=40)
        self.btn_camera.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_capture = ctk.CTkButton(self.sidebar_frame, text="⚡ Capture & Process",
                                         command=self.capture_frame, state="disabled", height=40)
        self.btn_capture.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light"],
                                                 command=self.change_appearance_mode)
        self.appearance_menu.grid(row=10, column=0, padx=20, pady=(5, 10))

        self.accent_label = ctk.CTkLabel(self.sidebar_frame, text="Accent Color:", anchor="w")
        self.accent_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.accent_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Green", "Cyan"],
                                               command=self.change_accent_color)
        self.accent_menu.grid(row=12, column=0, padx=20, pady=(5, 30))

        # --- Main Display (4 Panel Grid) ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure((0, 1), weight=1)
        self.main_content.grid_rowconfigure((1, 3), weight=1)

        # Labels for 5 panels
        self.titles = ["Live Camera", "Original Gray", "Frequency Spectrum", "High-Pass Filter", "Detected Features"]
        self.display_labels = []

        for i, title in enumerate(self.titles):
            # 2 columns, dynamic rows
            r, c = (i // 2) * 2, i % 2
            lbl_title = ctk.CTkLabel(self.main_content, text=title, font=ctk.CTkFont(size=14, weight="bold"))
            lbl_title.grid(row=r, column=c, pady=(10, 5))

            lbl_img = ctk.CTkLabel(self.main_content, text="Ready", fg_color=("gray85", "gray15"), corner_radius=12)
            lbl_img.grid(row=r+1, column=c, padx=10, pady=5, sticky="nsew")
            self.display_labels.append(lbl_img)

    def change_appearance_mode(self, mode: str):
        ctk.set_appearance_mode(mode)

    def change_accent_color(self, color: str):
        theme = "green" if color == "Green" else "blue" # blue looks like cyan in CTK
        ctk.set_default_color_theme(theme)
        # Note: CTK doesn't support hot-swapping themes perfectly without restart,
        # but we can try to update some manual colors.
        self.current_theme_color = "#2FA572" if color == "Green" else "#3B8ED0"
        self.logo_label.configure(text_color=self.current_theme_color)

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg *.bmp")])
        if path:
            self.image_array = cv2.imread(path)
            self._display_on_label(self.image_array, self.display_labels[1]) # Original Gray is index 1
            self._execute_processing()

    def toggle_camera(self):
        if not self.camera_active:
            threading.Thread(target=self._start_stream, daemon=True).start()
        else:
            self.camera_active = False
            self.btn_camera.configure(text="📷 Start Camera Feed")
            self.btn_capture.configure(state="disabled")
            if self.cap: self.cap.release()

    def _start_stream(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.after(0, lambda: messagebox.showerror("Hardware Error", "No camera detected."))
            return
        self.camera_active = True
        self.after(0, lambda: self.btn_camera.configure(text="⏹ Stop Camera"))
        self.after(0, lambda: self.btn_capture.configure(state="normal"))
        self._stream_loop()

    def _stream_loop(self):
        if self.camera_active and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Update only the Camera panel (index 0)
                self._display_on_label(frame, self.display_labels[0])
                self.current_frame = frame
            self.after(30, self._stream_loop)

    def capture_frame(self):
        if hasattr(self, 'current_frame'):
            self.image_array = self.current_frame.copy()
            self._display_on_label(self.image_array, self.display_labels[1])
            self._execute_processing()

    def _execute_processing(self):
        for lbl in self.display_labels[2:]:
            lbl.configure(text="Processing...", image="")
        threading.Thread(target=self._process_worker, daemon=True).start()

    def _process_worker(self):
        try:
            refined = preprocess_image(self.image_array)
            components = apply_fft_filter(refined)
            
            # components are [OriginalGray, Spectrum, Filter, Result]
            # We map them to display_labels index 1, 2, 3, 4
            for i, img in enumerate(components):
                if img is not None:
                    self.after(0, lambda x=img, l=self.display_labels[i+1]: self._display_on_label(x, l))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Processing Error", str(e)))

    def _display_on_label(self, cv_img, label):
        if cv_img is None: return
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB) if len(cv_img.shape) == 3 else cv_img
        img = Image.fromarray(rgb)
        
        w = label.winfo_width() if label.winfo_width() > 10 else 400
        h = label.winfo_height() if label.winfo_height() > 10 else 300
        img.thumbnail((w, h), Image.Resampling.LANCZOS)
        
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        label.configure(image=ctk_img, text="")
        label.image = ctk_img

if __name__ == "__main__":
    app = CrackDetectorApp()
    app.mainloop()
