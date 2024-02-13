import os
import threading
import shutil
from tkinter import Tk, filedialog, Button, Label, Listbox, Scrollbar, VERTICAL, messagebox
from PIL import Image
import fitz  # PyMuPDF

class PdfToImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Image Converter")

        self.pdf_path = ""
        self.image_paths = []
        self.total_pages = 0
        self.current_progress = 0

        self.label = Label(root, text="Select PDF:")
        self.label.grid(row=0, column=0, columnspan=2)

        self.listbox = Listbox(root, selectmode="extended", height=10, width=50)
        self.listbox.grid(row=1, column=0, rowspan=6, padx=10, pady=5)

        self.scrollbar = Scrollbar(root, orient=VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, rowspan=6, sticky="ns")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.select_button = Button(root, text="Select PDF", command=self.select_pdf)
        self.select_button.grid(row=3, column=2, pady=5)

        self.clear_button = Button(root, text="Clear List", command=self.clear_list)
        self.clear_button.grid(row=4, column=2, pady=5)

        self.zip_button = Button(root, text="Create Zip File", command=self.create_zip_file)
        self.zip_button.grid(row=5, column=2, pady=5)

        self.progress_label = Label(root, text="")
        self.progress_label.grid(row=6, column=0, columnspan=2)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if self.pdf_path:
            self.load_pdf_info()
            self.update_listbox()

    def clear_list(self):
        self.pdf_path = ""
        self.image_paths = []
        self.total_pages = 0
        self.current_progress = 0
        self.listbox.delete(0, "end")
        self.progress_label.config(text="")

    def create_zip_file(self):
        if not self.image_paths:
            messagebox.showerror("Error", "No images to zip. Please select a PDF file first.")
            return

        if not self.pdf_path:
            messagebox.showerror("Error", "No PDF selected.")
            return

        # Create a temporary folder for the images
        temp_folder = os.path.join(os.path.dirname(self.pdf_path), "temp_images")
        os.makedirs(temp_folder, exist_ok=True)

        # Save images to the temporary folder
        for i, image_path in enumerate(self.image_paths):
            page_number = i + 1
            output_filename = os.path.join(temp_folder, f"page_{page_number}.png")

            image = Image.open(image_path)
            image.save(output_filename)

        zip_filename = filedialog.asksaveasfilename(
            title="Save Zip As",
            defaultextension=".zip",
            filetypes=[("Zip files", "*.zip")],
        )

        if not zip_filename:
            messagebox.showinfo("Info", "Zip creation canceled.")
            return

        shutil.make_archive(os.path.splitext(zip_filename)[0], 'zip', temp_folder)

        # Delete temporary folder after creating the zip file
        shutil.rmtree(temp_folder)

        # Delete temporary images after creating the zip file
        self.delete_temp_images()

        self.progress_label.config(text=f"Zip file created at {zip_filename}.")

    def delete_temp_images(self):
        for image_path in self.image_paths:
            os.remove(image_path)

    def load_pdf_info(self):
        self.image_paths = []
        pdf_document = fitz.open(self.pdf_path)

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image = page.get_pixmap()
            image_path = f"temp_page_{page_number + 1}.png"
            image.save(image_path)
            self.image_paths.append(image_path)

        pdf_document.close()

    def update_listbox(self):
        self.listbox.delete(0, "end")
        for image_path in self.image_paths:
            self.listbox.insert("end", os.path.basename(image_path))

if __name__ == "__main__":
    root = Tk()
    app = PdfToImageConverter(root)
    root.mainloop()
