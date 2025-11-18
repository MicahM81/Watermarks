# app/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from watermark import apply_watermark


class WatermarkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Watermarker")
        # self.root.geometry("400x200")

        self._build_ui()

    def _build_ui(self):
        title_label = tk.Label(
            self.root,
            text="Photo Watermarker",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        upload_btn = tk.Button(
            self.root,
            text="Upload Photo",
            command=self.on_upload_clicked
        )
        upload_btn.pack(pady=5)

        # Watermark text label + entry
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=5)

        tk.Label(text_frame, text="Watermark Text:").pack(side="left", padx=5)

        self.watermark_text_var = tk.StringVar()
        self.watermark_text_var.set("Sample Watermark")  # default text

        text_entry = tk.Entry(text_frame, textvariable=self.watermark_text_var, width=30)
        text_entry.pack(side="left", padx=5)

        apply_btn = tk.Button(
            self.root,
            text="Apply Watermark",
            command=self.on_apply_watermark,
            state="disabled"  # disabled until an image is loaded
        )
        apply_btn.pack(pady=5)
        self.apply_btn = apply_btn

        save_btn = tk.Button(
            self.root,
            text="Save Watermarked Image",
            command=self.on_save_clicked,
            state="disabled"
        )
        save_btn.pack(pady=5)
        self.save_btn = save_btn

        self.status_label = tk.Label(self.root, text="", fg="gray")
        self.status_label.pack(pady=10)

        # Preview area
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

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

        self.original_path = file_path
        self.status_label.config(text="Image loaded. Ready to apply watermark.")

        # Display preview of original image
        self.show_image_preview(file_path)

        # Enable next step
        self.apply_btn.config(state="normal")

        # Auto-resize window to fit new preview
        self.root.update_idletasks()
        self.root.geometry("")

    def on_apply_watermark(self):
        from watermark import apply_watermark_preview

        wm_text = self.watermark_text_var.get()

        try:
            preview_image = apply_watermark_preview(self.original_path, wm_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.watermarked_image = preview_image
        self.status_label.config(text="Preview updated with watermark.")

        self.show_image_preview(preview_image)

        self.root.update_idletasks()
        self.root.geometry("")

        self.save_btn.config(state="normal")

    def on_save_clicked(self):
        if not hasattr(self, "watermarked_image"):
            messagebox.showwarning("No Image", "You must apply the watermark first.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")]
        )

        if not save_path:
            return

        self.watermarked_image.save(save_path)
        self.status_label.config(text=f"Saved: {save_path}")
        messagebox.showinfo("Saved", f"Watermarked image saved to:\n{save_path}")

    def show_image_preview(self, image_source):
        from PIL import Image, ImageTk

        if isinstance(image_source, str):
            image = Image.open(image_source)
        else:
            image = image_source

        # Resize image for UI
        max_width = 350
        if image.width > max_width:
            ratio = max_width / image.width
            new_size = (max_width, int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        self.display_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.display_image)

    def run(self):
        self.root.mainloop()