import platform 
import customtkinter as ctk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import ImageDraw
import os
import sys

RELATIVE_POPPLER_PATH = os.path.join("poppler", "poppler-24.08.0", "Library", "bin")
ICON_PATH = os.path.join("assets", "icon.ico")

class Pdf2ImgApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        if sys.platform.startswith("windows"):
            self.iconbitmap(self._resource_path(ICON_PATH))
        
        # Set the window icon (this will also show up on the taskbar)
        self.title("PDF to Image Converter")
        self.geometry("600x600")
        self.configure(bg="#1e1e1e")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.output_folder = None
        self.only_first_page = ctk.BooleanVar(value=True)
        self.hide_additives = ctk.BooleanVar(value=True) 
        self.crop_values = {
            "left": ctk.StringVar(value="180"),
            "top": ctk.StringVar(value="200"),
            "right": ctk.StringVar(value="2200"),
            "bottom": ctk.StringVar(value="2500"),
        }

        self._build_ui()

    def _build_ui(self):
        self.frame = ctk.CTkFrame(master=self, fg_color="#1e1e1e")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.frame, text="Select PDF files to convert", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=10)

        self.select_files_button = ctk.CTkButton(self.frame, text="Select PDF Files", command=self._select_pdfs)
        self.select_files_button.pack(pady=12)

        # Checkbox: Only convert first page
        self.first_page_checkbox = ctk.CTkCheckBox(
            self.frame, text="Only convert first page", variable=self.only_first_page)
        self.first_page_checkbox.pack(pady=6)

        # Checkbox: Hide additives
        self.hide_additives_checkbox = ctk.CTkCheckBox(
            self.frame, text="Hide additives", variable=self.hide_additives)
        self.hide_additives_checkbox.pack(pady=6)

        # Crop input
        crop_label = ctk.CTkLabel(self.frame, text="Crop (px): Left, Top, Right, Bottom")
        crop_label.pack(pady=(6, 4))

        crop_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        crop_frame.pack(pady=12)

        for key in ["left", "top", "right", "bottom"]:
            entry = ctk.CTkEntry(crop_frame, width=80, textvariable=self.crop_values[key])
            entry.pack(side="left", padx=5)

        self.output_button = ctk.CTkButton(self.frame, text="Choose Output Folder", command=self._choose_output_folder)
        self.output_button.pack(pady=3)

        self.folder_label = ctk.CTkLabel(self.frame, text="Output: [Same as PDF]", text_color="#a0ffa0", font=ctk.CTkFont(size=12))
        self.folder_label.pack(pady=6)

        self.log_box = ctk.CTkTextbox(self.frame, height=220, fg_color="#111111", text_color="#d0ffd6")
        self.log_box.pack(fill="both", expand=True)
        self.log_box.insert("end", "Logs:\n")

    def _choose_output_folder(self):
        selected = filedialog.askdirectory()
        if selected:
            self.output_folder = selected
            self.folder_label.configure(text=f"Output: {selected}")
        else:
            self.folder_label.configure(text="Output: [Same as PDF]")

    def _select_pdfs(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.log_box.insert("end", "Convterting PDFs Wait Please...\n")

        for path in file_paths:
            self.log_box.insert("end", f"→ Converting: {path}\n")
            self._convert_pdf_to_image(path)

    def _resource_path(self, relative_path):
        """ Get absolute path to resource, works for PyInstaller """
        try:
            base_path = sys._MEIPASS  # PyInstaller temporary folder
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def _convert_pdf_to_image(self, pdf_path, dpi=300):
        try:
            convert_first = self.only_first_page.get()
            crop_box = self._get_crop_box()
            hide_add = self.hide_additives.get()

            kwargs = {"dpi": dpi}

            self.log_box.insert("end", f"Platform: {platform.system()}\n")
            if platform.system() == "Windows":
                kwargs["poppler_path"] = self._resource_path(RELATIVE_POPPLER_PATH)
                self.log_box.insert("end", f"Poppler Path: {self._resource_path(RELATIVE_POPPLER_PATH)}\n")

            pages = convert_from_path(pdf_path, **kwargs)

            if convert_first:
                pages = [pages[0]]

            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            target_dir = self.output_folder if self.output_folder else os.path.dirname(pdf_path)

            for i, page in enumerate(pages):
                if crop_box:
                    page = page.crop(crop_box)
                
                if hide_add:
                    draw = ImageDraw.Draw(page)
                    additive_box = (20, 500, 2000, 620)
                    draw.rectangle(additive_box, fill="white")
                    self.log_box.insert("end", f"🔒 Additive area hidden at {additive_box}\n")

                out_path = os.path.join(target_dir, f"{base_name}_page{i+1}.png")
                page.save(out_path, 'PNG')
                self.log_box.insert("end", f"✓ Saved: {out_path}\n")
        except Exception as e:
            self.log_box.insert("end", f"✗ Error with {pdf_path}: {e}\n")

    def _get_crop_box(self):
        try:
            l = int(self.crop_values["left"].get())
            t = int(self.crop_values["top"].get())
            r = int(self.crop_values["right"].get())
            b = int(self.crop_values["bottom"].get())

            if l == t == r == b == 0:
                return None
            return (l, t, r, b)
        except ValueError:
            self.log_box.insert("end", "⚠️ Invalid crop values. Skipping crop.\n")
            return None


if __name__ == "__main__":
    app = Pdf2ImgApp()
    app.mainloop()
