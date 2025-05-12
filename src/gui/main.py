import platform 
import customtkinter as ctk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import ImageDraw, Image, ImageFont
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
        self.hide_interest_rate = ctk.BooleanVar(value=True)
        self.add_watermark = ctk.BooleanVar(value=False)
        self.watermark_text = ctk.StringVar(value="Jhoana Gonzalez")
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
            self.frame, text="Esconder Aditivas", variable=self.hide_additives)
        self.hide_additives_checkbox.pack(pady=6)

        # Checkbox: Hide interest rate
        self.hide_interest_rate_checkbox = ctk.CTkCheckBox(
            self.frame, text="Esconder Tasa de Interes", variable=self.hide_interest_rate)
        self.hide_interest_rate_checkbox.pack(pady=6)

        # Checkbox: Watermark
        self.watermark_checkbox = ctk.CTkCheckBox(
            self.frame, text="Colocar Marca de Agua", variable=self.add_watermark)
        self.watermark_checkbox.pack(pady=6)

        # Entry for watermark text
        self.watermark_entry = ctk.CTkEntry(
            self.frame, textvariable=self.watermark_text, placeholder_text="Watermark Text")
        self.watermark_entry.pack(pady=(0, 10))

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
            hide_interest_rate = self.hide_interest_rate.get()

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

                if hide_interest_rate:
                    draw = ImageDraw.Draw(page)
                    interest_rate_box = (400, 1500, 1100, 1640)
                    draw.rectangle(interest_rate_box, fill="white")
                    self.log_box.insert("end", f"🔒 Interest rate area hidden at {interest_rate_box}\n")

                if self.add_watermark.get():
                    text = self.watermark_text.get()
                    font_size = int(page.width / 10)

                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        try:
                            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
                        except:
                            self.log_box.insert("end", "⚠️ Warning: No scalable font found. Watermark size may be small.\n")
                            font = ImageFont.load_default()

                    # Ensure both base and overlay are in RGBA and same size
                    page = page.convert("RGBA")
                    watermark = Image.new("RGBA", page.size, (255, 255, 255, 0))
                    draw = ImageDraw.Draw(watermark)

                    # Position text diagonally
                    text_x = page.width / 4
                    text_y = page.height / 2

                    draw.text((text_x, text_y), text, font=font, fill=(255, 0, 0, 125))

                    # Rotate watermark then paste it centered
                    rotated = watermark.rotate(45, expand=True)

                    # Make a blank transparent layer the same size as original page
                    composite_layer = Image.new("RGBA", page.size, (255, 255, 255, 0))
                    offset_x = (page.width - rotated.width) // 2
                    offset_y = (page.height - rotated.height) // 2
                    composite_layer.paste(rotated, (offset_x, offset_y), rotated)

                    # Composite onto page
                    page = Image.alpha_composite(page, composite_layer).convert("RGB")

                    self.log_box.insert("end", f"💧 Watermark applied: \"{text}\"\n")

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
