# Import necessary modules
import os
import threading
from tkinter import Tk, filedialog, Button, Label, Listbox, Scrollbar, Canvas, VERTICAL
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas

# Create a class for the Image to PDF Converter application
class ImageToPdfConverter:
    def __init__(self, root):
        # Initialize the class with the root window
        self.root = root
        self.root.title("Image to PDF Converter")

        # Initialize instance variables for image paths, output PDF path, and progress tracking
        self.images = []
        self.output_pdf_path = ""
        self.total_images = 0
        self.current_progress = 0

        # Create and configure GUI elements using Tkinter
        self.label = Label(root, text="Select Images:")
        self.label.grid(row=0, column=0, columnspan=2)

        # Listbox to display selected image filenames
        self.listbox = Listbox(root, selectmode="extended", height=10, width=50)
        self.listbox.grid(row=1, column=0, rowspan=6, padx=10, pady=5)

        # Scrollbar for the listbox
        self.scrollbar = Scrollbar(root, orient=VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, rowspan=6, sticky="ns")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Canvas to display thumbnail of the first selected image
        self.thumbnail_canvas = Canvas(root, height=100, width=150, bg="white")
        self.thumbnail_canvas.grid(row=1, column=2, rowspan=2, padx=10, pady=5)

        # Buttons for interacting with the application
        self.select_button = Button(root, text="Select Images", command=self.select_images)
        self.select_button.grid(row=3, column=2, pady=5)

        self.clear_button = Button(root, text="Clear List", command=self.clear_list)
        self.clear_button.grid(row=4, column=2, pady=5)

        self.convert_button = Button(root, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.grid(row=5, column=2, pady=5)

        # Label to display progress percentage during PDF creation
        self.progress_label = Label(root, text="")
        self.progress_label.grid(row=6, column=0, columnspan=2)

    # Method to allow the user to select images
    def select_images(self):
        selected_images = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],
        )
        if selected_images:
            self.images.extend(selected_images)
            self.update_listbox()
            self.update_thumbnail()

    # Method to clear the list of selected images
    def clear_list(self):
        self.images.clear()
        self.update_listbox()
        self.update_thumbnail()

    # Method to initiate the PDF conversion process
    def convert_to_pdf(self):
        if not self.images:
            self.label.config(text="No images selected.")
            return

        # Ask the user for the output PDF file path
        self.output_pdf_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )

        if not self.output_pdf_path:
            self.label.config(text="PDF conversion canceled.")
            return

        # Initialize progress variables and start a new thread for PDF creation
        self.total_images = len(self.images)
        self.current_progress = 0
        self.progress_label.config(text="")

        # Create a separate thread for PDF creation to prevent GUI freezing
        progress_thread = threading.Thread(target=self.create_pdf_thread)
        progress_thread.start()

    # Method to create PDF in a separate thread
    def create_pdf_thread(self):
        # Initialize a PDF canvas
        pdf = canvas.Canvas(self.output_pdf_path)

        # Iterate through selected images, add them to the PDF, and update progress
        for i, image_path in enumerate(self.images):
            image = Image.open(image_path)
            width, height = image.size
            pdf.setPageSize((width, height))
            pdf.drawInlineImage(image_path, 0, 0, width, height)

            # Update progress and percentage
            self.current_progress = i + 1
            progress_percentage = (self.current_progress / self.total_images) * 100
            self.progress_label.config(text=f"Progress: {progress_percentage:.2f}%")

            # Update the GUI to reflect progress
            self.root.update()

            # Add a new page for each image except the last one
            if i < len(self.images) - 1:
                pdf.showPage()

        # Save the PDF and update progress label
        pdf.save()
        self.progress_label.config(text=f"PDF saved at {self.output_pdf_path}.")
        self.current_progress = 0

    # Method to update the listbox with selected image filenames
    def update_listbox(self):
        self.listbox.delete(0, "end")
        for image_path in self.images:
            self.listbox.insert("end", os.path.basename(image_path))

    # Method to update the thumbnail display based on the first selected image
    def update_thumbnail(self):
        if self.images:
            first_image = Image.open(self.images[0])
            thumbnail = first_image.resize((150, 100), Image.ANTIALIAS)
            thumbnail = ImageTk.PhotoImage(thumbnail)
            self.thumbnail_canvas.create_image(75, 50, anchor="center", image=thumbnail)
            self.thumbnail_canvas.thumbnail = thumbnail
        else:
            # Clear the canvas if no images are selected
            self.thumbnail_canvas.delete("all")

# Main block: Create Tkinter root window and run the application
if __name__ == "__main__":
    root = Tk()
    app = ImageToPdfConverter(root)
    root.mainloop()