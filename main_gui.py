import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import numpy as np

# -----------------------------------------------------------------------------
# Import Core Logic 
# -----------------------------------------------------------------------------
from preprocessing import preprocess_image
from fft_logic import apply_fft_filter

# -----------------------------------------------------------------------------
# GUI Application Class
# -----------------------------------------------------------------------------
class CrackDetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Crack Detector - 2D FFT Analysis")
        self.geometry("1100x700")
        
        # Default styling
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        self.current_theme = "green"

        # State variables
        self.image_array = None
        self.camera_active = False
        self.cap = None

        self._build_ui()

    def _build_ui(self):
        # Configure Grid Layout (1 row, 2 columns: Sidebar & Main Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= Sidebar =================
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Crack Detector", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input Buttons
        self.btn_upload = ctk.CTkButton(self.sidebar_frame, text="Upload Image", command=self.upload_image)
        self.btn_upload.grid(row=1, column=0, padx=20, pady=10)

        self.btn_camera = ctk.CTkButton(self.sidebar_frame, text="Start Camera Feed", command=self.toggle_camera)
        self.btn_camera.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_capture = ctk.CTkButton(self.sidebar_frame, text="Capture & Process", command=self.capture_frame, state="disabled")
        self.btn_capture.grid(row=3, column=0, padx=20, pady=10)

        # Appearance & Theme Toggles
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_menu.set("Dark")

        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Accent Color:", anchor="w")
        self.theme_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.theme_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Green", "Cyan"], command=self.change_theme)
        self.theme_menu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # ================= Main Canvas =================
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Titles
        self.lbl_orig_title = ctk.CTkLabel(self.main_frame, text="Original Image", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_orig_title.grid(row=0, column=0, pady=(10, 0))
        
        self.lbl_proc_title = ctk.CTkLabel(self.main_frame, text="FFT Detection Result", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_proc_title.grid(row=0, column=1, pady=(10, 0))

        # Image Displays
        self.lbl_orig_img = ctk.CTkLabel(self.main_frame, text="No Image Uploaded", fg_color="gray15", corner_radius=10)
        self.lbl_orig_img.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.lbl_proc_img = ctk.CTkLabel(self.main_frame, text="Awaiting Processing...", fg_color="gray15", corner_radius=10)
        self.lbl_proc_img.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # -------------------------------------------------------------------------
    # UI Toggles
    # -------------------------------------------------------------------------
    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_theme(self, new_theme: str):
        # We simulate cyan using the default "blue" theme in CustomTkinter
        theme_map = {"Green": "green", "Cyan": "blue"}
        ctk.set_default_color_theme(theme_map[new_theme])
        
        # Requires widget redraw to apply base theme changes safely.
        color = "#2FA572" if new_theme == "Green" else "#1F6AA5"
        self.btn_upload.configure(fg_color=color)
        self.btn_camera.configure(fg_color=color)
        self.btn_capture.configure(fg_color=color)
        self.appearance_mode_menu.configure(fg_color=color)
        self.theme_menu.configure(fg_color=color)

    # -------------------------------------------------------------------------
    # Input Processing
    # -------------------------------------------------------------------------
    def upload_image(self):
        if self.camera_active:
            self.toggle_camera() # Turn off camera if active

        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.image_array = cv2.imread(file_path)
            self.display_image(self.image_array, self.lbl_orig_img)
            self.process_and_display()

    # -------------------------------------------------------------------------
    # Camera Integration (Optimized via Threading & Hardware Acceleration)
    # -------------------------------------------------------------------------
    def toggle_camera(self):
        if not self.camera_active:
            # Threaded camera start prevents UI freezing
            threading.Thread(target=self._start_camera_stream, daemon=True).start()
        else:
            self.camera_active = False
            self.btn_camera.configure(text="Start Camera Feed")
            self.btn_capture.configure(state="disabled")
            if self.cap:
                self.cap.release()

    def _start_camera_stream(self):
        self.cap = cv2.VideoCapture(0) # Standard webcam
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return

        self.camera_active = True
        self.btn_camera.configure(text="Stop Camera Feed")
        self.btn_capture.configure(state="normal")
        
        self._update_camera_frame()

    def _update_camera_frame(self):
        if self.camera_active and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.image_array = frame
                self.display_image(frame, self.lbl_orig_img)
            
            self.after(33, self._update_camera_frame)

    def capture_frame(self):
        if self.image_array is not None:
            self.toggle_camera() # Stop live feed
            self.process_and_display()

    # -------------------------------------------------------------------------
    # Core Image Processing Execution
    # -------------------------------------------------------------------------
    def process_and_display(self):
        self.lbl_proc_img.configure(text="Processing...", image="")
        threading.Thread(target=self._run_detection_logic, daemon=True).start()

    def _run_detection_logic(self):
        try:
            # 1. Image Cleaning/Thresholding
            preprocessed = preprocess_image(self.image_array)
            # 2. 2D FFT & High-pass filtering
            result = apply_fft_filter(preprocessed)
            
            # 3. Update GUI
            self.after(0, lambda: self.display_image(result, self.lbl_proc_img))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Processing Error", f"An error occurred:\n{str(e)}"))

    # -------------------------------------------------------------------------
    # Utility: Convert OpenCV Image to Tkinter Image
    # -------------------------------------------------------------------------
    def display_image(self, cv_img, target_label):
        if cv_img is None:
            return
            
        if len(cv_img.shape) == 3:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        
        pil_img = Image.fromarray(cv_img)
        
        max_size = (400, 400)
        pil_img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
        
        target_label.configure(image=ctk_img, text="")
        target_label.image = ctk_img

if __name__ == "__main__":
    app = CrackDetectorApp()
    app.mainloop()
