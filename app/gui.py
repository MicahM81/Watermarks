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
        #Image Preview
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

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
            return

        try:
            output_path = apply_watermark(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply watermark:\n{e}")
            return

        self.status_label.config(text=f"Watermarked image saved:\n{output_path}")

        # --- NEW CODE: Display output image in GUI ---
        from PIL import Image, ImageTk
        image = Image.open(output_path)

        # Resize to fit the window width
        max_width = 350
        if image.width > max_width:
            ratio = max_width / image.width
            new_size = (max_width, int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        tk_image = ImageTk.PhotoImage(image)

        # Save reference or Tkinter will garbage-collect it
        self.display_image = tk_image
        self.image_label.config(image=tk_image)

        messagebox.showinfo("Success", f"Watermarked image saved to:\n{output_path}")

    def run(self):
        self.root.mainloop()