"""
import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
from PIL import Image, ImageTk
from threading import Thread

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("500x400")

        self.style = ttk.Style()
        self.style.configure("TButton", padding=(10, 5), font=('Arial', 10))

        self.pdf_files = []
        self.pdf_icon = self.load_pdf_icon()
        self.merging_progress = tk.StringVar()
        self.merging_progress.set("")

        self.setup_gui()

    def load_pdf_icon(self):
        icon_path = "path/to/pdf_icon.png"  # Replace with the actual path to your PDF icon
        if os.path.exists(icon_path):
            pdf_icon = Image.open(icon_path).resize((20, 20), Image.ANTIALIAS)
            return ImageTk.PhotoImage(pdf_icon)
        else:
            return None

    def setup_gui(self):
        self.setup_buttons()
        self.setup_listbox()
        self.setup_result_label()

    def setup_buttons(self):
        merge_button = ttk.Button(self.root, text="Merge PDFs", command=self.on_merge_button_click)
        merge_button.pack(pady=10, padx=20, side=tk.TOP)

        add_button = ttk.Button(self.root, text="Add PDFs", command=self.on_add_button_click)
        add_button.pack(pady=5, padx=20, side=tk.TOP)

        clear_button = ttk.Button(self.root, text="Clear List", command=self.on_clear_button_click)
        clear_button.pack(pady=5, padx=20, side=tk.TOP)

    def setup_listbox(self):
        self.listbox = tk.Listbox(self.root, selectbackground="#a6a6a6", selectmode=tk.SINGLE)
        self.listbox.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=5)

    def setup_result_label(self):
        self.result_label = ttk.Label(self.root, text="", font=("Arial", 10, "italic"))
        self.result_label.pack(pady=5)

        self.progress_label = ttk.Label(self.root, textvariable=self.merging_progress, font=("Arial", 10, "italic"))
        self.progress_label.pack(pady=5)

    def on_merge_button_click(self):
        output_pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )

        if self.pdf_files and output_pdf_path:
            self.result_label.config(text="Merging in progress...")
            Thread(target=self.merge_pdfs, args=(output_pdf_path, self.pdf_files)).start()
        else:
            self.result_label.config(text="Merging canceled.")

    def merge_pdfs(self, output_path, input_paths):
        pdf_merger = PyPDF2.PdfMerger()

        total_files = len(input_paths)
        for count, path in enumerate(input_paths, start=1):
            pdf_merger.append(path)
            progress_percentage = int((count / total_files) * 100)
            self.merging_progress.set(f'Merging: {progress_percentage}% ({count}/{total_files})')
            self.root.update_idletasks()  # Update the GUI

        with open(output_path, 'wb') as output_file:
            pdf_merger.write(output_file)

        self.merging_progress.set("")
        self.result_label.config(text=f'Merged PDF saved at:\n{output_path}')

    def on_add_button_click(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files", filetypes=[("PDF files", "*.pdf")]
        )

        if files:
            self.pdf_files.extend(files)
            self.update_listbox()

    def on_clear_button_click(self):
        self.pdf_files.clear()
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, file_path in enumerate(self.pdf_files, start=1):
            file_name = os.path.basename(file_path)
            self.listbox.insert(tk.END, f"{i}. {file_name}", self.pdf_icon)

def main():
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
"""
# Import necessary libraries
import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
from PIL import Image, ImageTk
from threading import Thread

# Define a class for the PDF Merger application
class PDFMergerApp:
    def __init__(self, root):
        """
        Constructor method for initializing the PDFMergerApp class.

        Parameters:
        - root: Tkinter root window
        """
        # Initialize the Tkinter root window
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("500x400")

        # Configure the style for Tkinter elements
        self.style = ttk.Style()
        self.style.configure("TButton", padding=(10, 5), font=('Arial', 10))

        # Initialize attributes for PDF files, PDF icon, and merging progress
        self.pdf_files = []
        self.pdf_icon = self.load_pdf_icon()
        self.merging_progress = tk.StringVar()
        self.merging_progress.set("")

        # Set up the graphical user interface
        self.setup_gui()

    def load_pdf_icon(self):
        """
        Load and resize the PDF icon.

        Returns:
        - ImageTk.PhotoImage: PhotoImage object containing the resized PDF icon
        """
        icon_path = "path/to/pdf_icon.png"  # Replace with the actual path to your PDF icon
        if os.path.exists(icon_path):
            pdf_icon = Image.open(icon_path).resize((20, 20), Image.ANTIALIAS)
            return ImageTk.PhotoImage(pdf_icon)
        else:
            return None

    def setup_gui(self):
        """Set up the graphical user interface by configuring buttons, listbox, and result labels."""
        self.setup_buttons()
        self.setup_listbox()
        self.setup_result_label()

    def setup_buttons(self):
        """Set up buttons for merging PDFs, adding PDFs, and clearing the list."""
        merge_button = ttk.Button(self.root, text="Merge PDFs", command=self.on_merge_button_click)
        merge_button.pack(pady=10, padx=20, side=tk.TOP)

        add_button = ttk.Button(self.root, text="Add PDFs", command=self.on_add_button_click)
        add_button.pack(pady=5, padx=20, side=tk.TOP)

        clear_button = ttk.Button(self.root, text="Clear List", command=self.on_clear_button_click)
        clear_button.pack(pady=5, padx=20, side=tk.TOP)

    def setup_listbox(self):
        """Set up the listbox for displaying the added PDF files."""
        self.listbox = tk.Listbox(self.root, selectbackground="#a6a6a6", selectmode=tk.SINGLE)
        self.listbox.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=5)

    def setup_result_label(self):
        """Set up result labels for displaying merging progress and the path of the merged PDF."""
        self.result_label = ttk.Label(self.root, text="", font=("Arial", 10, "italic"))
        self.result_label.pack(pady=5)

        self.progress_label = ttk.Label(self.root, textvariable=self.merging_progress, font=("Arial", 10, "italic"))
        self.progress_label.pack(pady=5)

    def on_merge_button_click(self):
        """Event handler for the 'Merge PDFs' button click."""
        # Open a file dialog to get the output path for the merged PDF
        output_pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )

        # Check if there are PDF files to merge and an output path is provided
        if self.pdf_files and output_pdf_path:
            self.result_label.config(text="Merging in progress...")
            # Start a thread to merge PDFs asynchronously
            Thread(target=self.merge_pdfs, args=(output_pdf_path, self.pdf_files)).start()
        else:
            self.result_label.config(text="Merging canceled.")

    def merge_pdfs(self, output_path, input_paths):
        """
        Merge multiple PDFs into a single PDF.

        Parameters:
        - output_path: str, path for the merged PDF file
        - input_paths: list, paths of input PDF files to be merged
        """
        pdf_merger = PyPDF2.PdfMerger()

        total_files = len(input_paths)
        # Iterate through input PDF paths and append to the PDF merger
        for count, path in enumerate(input_paths, start=1):
            pdf_merger.append(path)
            progress_percentage = int((count / total_files) * 100)
            self.merging_progress.set(f'Merging: {progress_percentage}% ({count}/{total_files})')
            self.root.update_idletasks()  # Update the GUI

        # Write the merged PDF to the output path
        with open(output_path, 'wb') as output_file:
            pdf_merger.write(output_file)

        # Reset merging progress and update result label
        self.merging_progress.set("")
        self.result_label.config(text=f'Merged PDF saved at:\n{output_path}')

    def on_add_button_click(self):
        """Event handler for the 'Add PDFs' button click."""
        # Open a file dialog to select multiple PDF files
        files = filedialog.askopenfilenames(
            title="Select PDF files", filetypes=[("PDF files", "*.pdf")]
        )

        # If files are selected, extend the list of PDF files and update the listbox
        if files:
            self.pdf_files.extend(files)
            self.update_listbox()

    def on_clear_button_click(self):
        """Event handler for the 'Clear List' button click."""
        # Clear the list of PDF files and update the listbox
        self.pdf_files.clear()
        self.update_listbox()

    def update_listbox(self):
        """Update the listbox with the current list of PDF files."""
        self.listbox.delete(0, tk.END)
        for i, file_path in enumerate(self.pdf_files, start=1):
            file_name = os.path.basename(file_path)
            self.listbox.insert(tk.END, f"{i}. {file_name}", self.pdf_icon)

# Main function to create and run the Tkinter application
def main():
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()

# Entry point to execute the main function when the script is run
if __name__ == "__main__":
    main()
