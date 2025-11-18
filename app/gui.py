# app/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from watermark import apply_watermark


class WatermarkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Watermarker")
        self.root.geometry("400x200")

        self._build_ui()

    def _build_ui(self):
        # Title label
        title_label = tk.Label(
            self.root,
            text="Photo Watermarker",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Upload button
        upload_btn = tk.Button(
            self.root,
            text="Upload Photo & Add Watermark",
            command=self.on_upload_clicked
        )
        upload_btn.pack(pady=20)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="No image processed yet.",
            fg="gray"
        )
        self.status_label.pack(pady=10)

    def on_upload_clicked(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            return  # user cancelled

        try:
            output_path = apply_watermark(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply watermark:\n{e}")
            return

        self.status_label.config(text=f"Saved watermarked image:\n{output_path}")
        messagebox.showinfo("Success", f"Watermarked image saved to:\n{output_path}")

    def run(self):
        self.root.mainloop()