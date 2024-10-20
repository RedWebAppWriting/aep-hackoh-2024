import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from vadersentiment import *


def upload_file():
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            messagebox.showinfo("Success", f"File uploaded successfully! \nDataFrame shape: {df.shape}")
            vadersentiment.cleanertext(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the file: {e}")

root = tk.Tk()
root.title("CSV Uploader")

# Create a button for uploading CSV files
upload_button = tk.Button(root, text="Upload CSV File", command=upload_file)
upload_button.pack(pady=20)




# Run the application
root.mainloop()
