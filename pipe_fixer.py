import pdfplumber
import pandas as pd
import os

def fix_the_pipe(pdf_path):
    print(f"--- Fixing the leak in: {pdf_path} ---")
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found. Drop a PDF in this folder!")
        return

    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_data = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    all_data.extend(table)
            
            if not all_data:
                print("No table found. This PDF might be a scanned image.")
                return

            # Cleaning up the data
            df = pd.DataFrame(all_data[1:], columns=all_data[0])
            df = df.dropna(how='all') # Drop empty rows

            output_file = "Invoice_Converted.xlsx"
            df.to_excel(output_file, index=False)
            print(f"Success! Created {output_file}.")
            print("That's one manual task killed. Next stop: Payday.")

    except Exception as e:
        print(f"Something broke: {e}")

if __name__ == "__main__":
    # 1. Grab a PDF (Eskom, Takealot, whatever)
    # 2. Rename it to 'test.pdf' and put it in this folder
    # 3. Run this script: python pipe_fixer.py
    fix_the_pipe("test.pdf")