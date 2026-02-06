import customtkinter as ctk
from tkinter import filedialog, messagebox
import pdfplumber
import pandas as pd
import os
import threading

class PipeFixerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("The Digital Plumber | Admin Killer v1.0")
        self.geometry("600x400")

        # --- UI Elements ---
        self.label = ctk.CTkLabel(self, text="Cape Town Batch PDF Converter", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.select_btn = ctk.CTkButton(self, text="Select Folder of PDFs", command=self.select_folder)
        self.select_btn.pack(pady=10)

        self.status_box = ctk.CTkTextbox(self, width=500, height=150)
        self.status_box.pack(pady=10)

        self.convert_btn = ctk.CTkButton(self, text="RUN BATCH FIX", fg_color="green", hover_color="darkgreen", 
                                          command=self.start_conversion, state="disabled")
        self.convert_btn.pack(pady=20)

        self.folder_path = ""

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.status_box.insert("end", f"Selected Folder: {self.folder_path}\n")
            self.convert_btn.configure(state="normal")

    def start_conversion(self):
        # We run this in a thread so the UI doesn't freeze
        threading.Thread(target=self.process_pdfs, daemon=True).start()

    def process_pdfs(self):
        self.convert_btn.configure(state="disabled")
        pdf_files = [f for f in os.listdir(self.folder_path) if f.endswith('.pdf')]
        
        if not pdf_files:
            self.status_box.insert("end", "Error: No PDFs found in this folder.\n")
            return

        all_frames = []
        for file in pdf_files:
            path = os.path.join(self.folder_path, file)
            self.status_box.insert("end", f"Extracting: {file}...\n")
            
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        all_frames.append(df)

        if all_frames:
            master_df = pd.concat(all_frames, ignore_index=True)
            output_path = os.path.join(self.folder_path, "MASTER_CONSOLIDATED.xlsx")
            master_df.to_excel(output_path, index=False)
            self.status_box.insert("end", f"\nSUCCESS! Created {output_path}\n")
            messagebox.showinfo("Payday!", f"Batch complete. {len(pdf_files)} files merged.")
        
        self.convert_btn.configure(state="normal")

if __name__ == "__main__":
    app = PipeFixerApp()
    app.mainloop()