import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, Text
from argostranslate import package, translate

class PDFSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline PDF Zoek- en Vertaaltool")

        # Label
        self.label = tk.Label(root, text="Selecteer een map met PDF-bestanden om te doorzoeken")
        self.label.pack(pady=10)

        # Select Folder Button
        self.select_button = tk.Button(root, text="Selecteer Map", padx=10, pady=5, fg="white", bg="#263D42", command=self.select_folder)
        self.select_button.pack()

        # Search Term Entry
        self.search_label = tk.Label(root, text="Voer een zoekterm in:")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)

        # Search Button
        self.search_button = tk.Button(root, text="Zoeken en Vertalen", padx=10, pady=5, fg="white", bg="#263D42", command=self.search)
        self.search_button.pack(pady=10)

        # Result Box
        self.result_box = Text(root, height=15, width=80)
        self.result_box.pack(pady=10)

        self.folder_path = ""

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.label.config(text=f"Geselecteerde map: {self.folder_path}")

    def search(self):
        search_term = self.search_entry.get()
        if self.folder_path and search_term:
            self.result_box.delete(1.0, tk.END)
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.endswith(".pdf"):
                        file_path = os.path.join(root, file)
                        self.search_in_pdf(file_path, search_term)
        else:
            self.result_box.insert(tk.END, "Selecteer een map en voer een zoekterm in.\n")

    def search_in_pdf(self, file_path, search_term):
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if search_term.lower() in text.lower():
                    translated_text = self.translate_text(text)
                    self.result_box.insert(tk.END, f"Gevonden in {file_path}, pagina {page_num + 1}:\n{translated_text}\n\n")
            doc.close()
        except Exception as e:
            self.result_box.insert(tk.END, f"Fout bij het lezen van {file_path}: {e}\n")

    def translate_text(self, text):
        try:
            installed_languages = translate.get_installed_languages()
            if len(installed_languages) < 2:
                # Download Dutch and English packages if not installed
                package.install_from_path(package.download_package("en", "nl"))
            from_lang = installed_languages[0]
            to_lang = installed_languages[1]
            translation = from_lang.get_translation(to_lang)
            return translation.translate(text)
        except Exception as e:
            return f"Fout bij vertalen: {e}"

# Start the application
root = tk.Tk()
app = PDFSearchApp(root)
root.mainloop()
