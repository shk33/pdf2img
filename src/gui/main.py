import customtkinter as ctk
from tkinter import filedialog
from pdf2image import convert_from_path
import os

class Pdf2ImgApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("PDF to Image Converter")
        self.geometry("600x460")
        self.configure(bg="#1e1e1e")
        self.output_folder = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self._build_ui()

    def _build_ui(self):
        self.frame = ctk.CTkFrame(master=self, fg_color="#1e1e1e")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.frame, text="Select PDF files to convert", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=10)

        self.output_button = ctk.CTkButton(self.frame, text="Choose Output Folder", command=self._choose_output_folder, fg_color="#2a8c6f", hover_color="#206a58")
        self.output_button.pack()

        self.folder_label = ctk.CTkLabel(self.frame, text="Output: [Same as PDF Path]", text_color="#a0ffa0", font=ctk.CTkFont(size=12))
        self.folder_label.pack(pady=4)

        self.select_files_button = ctk.CTkButton(self.frame, text="Select PDF Files", command=self._select_pdfs)
        self.select_files_button.pack(pady=10)

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
        for path in file_paths:
            self.log_box.insert("end", f"→ Converting: {path}\n")
            self._convert_pdf_to_image(path)

    def _convert_pdf_to_image(self, pdf_path, dpi=300):
        try:
            pages = convert_from_path(pdf_path, dpi=dpi)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            target_dir = self.output_folder if self.output_folder else os.path.dirname(pdf_path)

            for i, page in enumerate(pages):
                out_path = os.path.join(target_dir, f"{base_name}_page{i+1}.png")
                page.save(out_path, 'PNG')
                self.log_box.insert("end", f"✓ Saved: {out_path}\n")
        except Exception as e:
            self.log_box.insert("end", f"✗ Error with {pdf_path}: {e}\n")


if __name__ == "__main__":
    app = Pdf2ImgApp()
    app.mainloop()
