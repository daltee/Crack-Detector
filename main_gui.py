import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import numpy as np

# -----------------------------------------------------------------------------
# CORE LOGIC INTEGRATION
# -----------------------------------------------------------------------------
# These modules handle the mathematical and image processing pipelines.
from preprocessing import preprocess_image
from fft_logic import apply_fft_filter

# -----------------------------------------------------------------------------
# GUI APPLICATION CLASS
# -----------------------------------------------------------------------------
class CrackDetectorApp(ctk.CTk):
    """
    A professional-grade desktop application for crack detection using 2D FFT.
    Integrates real-time camera feed, image processing, and modern UI elements.
    """
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Crack Detector Pro - Infrastructure Analysis")
        self.geometry("1200x800")
        
        # Initial Theme & Appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        self.current_theme_color = "#2FA572" # Green default

        # State Management
        self.image_array = None
        self.camera_active = False
        self.cap = None

        self._build_ui()

    def _build_ui(self):
        """Builds the modern, sidebar-based layout."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CRACK DETECTOR",
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Input Controls
        self.btn_upload = ctk.CTkButton(self.sidebar_frame, text="📁 Upload Image",
                                        command=self.upload_image, height=40)
        self.btn_upload.grid(row=1, column=0, padx=20, pady=10)

        self.btn_camera = ctk.CTkButton(self.sidebar_frame, text="📷 Start Camera Feed",
                                        command=self.toggle_camera, height=40)
        self.btn_camera.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_capture = ctk.CTkButton(self.sidebar_frame, text="⚡ Capture & Process",
                                         command=self.capture_frame, state="disabled", height=40)
        self.btn_capture.grid(row=3, column=0, padx=20, pady=10)

        # Visual Settings
        self.appearance_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                 command=self.change_appearance_mode)
        self.appearance_menu.grid(row=10, column=0, padx=20, pady=(5, 10))

        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Accent Color Theme:", anchor="w")
        self.theme_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.theme_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Green", "Cyan"],
                                            command=self.change_theme)
        self.theme_menu.grid(row=12, column=0, padx=20, pady=(5, 30))

        # --- Main Display ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure((0, 1), weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        self.lbl_orig_title = ctk.CTkLabel(self.main_content, text="Original Image Source",
                                           font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_orig_title.grid(row=0, column=0, pady=(0, 10))
        
        self.lbl_proc_title = ctk.CTkLabel(self.main_content, text="Detected FFT Analysis",
                                           font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_proc_title.grid(row=0, column=1, pady=(0, 10))

        self.lbl_orig_img = ctk.CTkLabel(self.main_content, text="Waiting for input...",
                                         fg_color=("gray85", "gray15"), corner_radius=12)
        self.lbl_orig_img.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.lbl_proc_img = ctk.CTkLabel(self.main_content, text="Analysis ready",
                                         fg_color=("gray85", "gray15"), corner_radius=12)
        self.lbl_proc_img.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # -------------------------------------------------------------------------
    # THEME & APPEARANCE MANAGEMENT
    # -------------------------------------------------------------------------
    def change_appearance_mode(self, mode: str):
        ctk.set_appearance_mode(mode)

    def change_theme(self, color: str):
        """Switches the UI accent colors dynamically."""
        theme_map = {"Green": "green", "Cyan": "blue"}
        color_hex = "#2FA572" if color == "Green" else "#1F6AA5"
        
        ctk.set_default_color_theme(theme_map[color])
        self.current_theme_color = color_hex

        # Update interactive components
        for btn in [self.btn_upload, self.btn_camera, self.btn_capture]:
            btn.configure(fg_color=color_hex)
        self.appearance_menu.configure(fg_color=color_hex)
        self.theme_menu.configure(fg_color=color_hex)

    # -------------------------------------------------------------------------
    # INPUT HANDLING (UPLOAD & CAMERA)
    # -------------------------------------------------------------------------
    def upload_image(self):
        if self.camera_active: self.toggle_camera()

        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg *.bmp")])
        if path:
            self.image_array = cv2.imread(path)
            self._display_on_label(self.image_array, self.lbl_orig_img)
            self._execute_processing()

    def toggle_camera(self):
        """Threaded camera handling for non-blocking UI."""
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
                self.image_array = frame
                self._display_on_label(frame, self.lbl_orig_img)
            self.after(30, self._stream_loop)

    def capture_frame(self):
        if self.image_array is not None:
            self.toggle_camera()
            self._execute_processing()

    # -------------------------------------------------------------------------
    # PROCESSING PIPELINE
    # -------------------------------------------------------------------------
    def _execute_processing(self):
        """Offloads heavy math to a background thread."""
        self.lbl_proc_img.configure(text="Processing FFT...", image="")
        threading.Thread(target=self._process_worker, daemon=True).start()

    def _process_worker(self):
        try:
            # Step 1: Pre-process (cleaning/thresholding)
            refined = preprocess_image(self.image_array)
            # Step 2: FFT Core Logic
            result = apply_fft_filter(refined)
            
            self.after(0, lambda: self._display_on_label(result, self.lbl_proc_img))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Processing Error", str(e)))

    def _display_on_label(self, cv_img, label):
        """Helper to render OpenCV arrays in CustomTkinter labels."""
        if cv_img is None: return
        
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB) if len(cv_img.shape) == 3 else cv_img
        img = Image.fromarray(rgb)
        
        # Adaptive scaling
        w, h = label.winfo_width(), label.winfo_height()
        if w < 10: w, h = 500, 500 # Default if not yet rendered
        img.thumbnail((w, h), Image.Resampling.LANCZOS)
        
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        label.configure(image=ctk_img, text="")
        label.image = ctk_img

if __name__ == "__main__":
    app = CrackDetectorApp()
    app.mainloop()
