import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np

class EditFrame:
    def __init__(self, edit_tab):
        edit_tab.pack_propagate(False)
        edit_tab.columnconfigure(0, weight=1)

        edit_tab.columnconfigure(1, weight=1)
        edit_tab.columnconfigure(2, weight=1)
        edit_tab.rowconfigure(0, weight=1)
        edit_tab.rowconfigure(1, weight=0)
        edit_tab.rowconfigure(2, weight=0)
        edit_tab.rowconfigure(3, weight=0)
        edit_tab.rowconfigure(4, weight=0)

        edit_tab.columnconfigure(1, weight=0)
        edit_tab.rowconfigure(0, weight=1)
        edit_tab.rowconfigure(1, weight=0)
        edit_tab.rowconfigure(2, weight=0)


        self.current_brightness = tk.DoubleVar()
        self.current_brightness.set(0)
        self.current_contrast = tk.DoubleVar()
        self.current_contrast.set(0)

        self.load_image_button = ttk.Button(edit_tab, text="Load Image", command=self.load_image)
        self.load_image_button.grid(row=0, column=1, padx=10, pady=(10, 5), sticky='n')

        self.load_image_button = ttk.Button(edit_tab, text="Load Image", command=self.load_image)
        self.load_image_button.grid(row=0, column=1, padx=10, pady=(10, 5), sticky='n')

        brightness_label = ttk.Label(edit_tab, text='Brightness:')
        brightness_label.grid(row=1, column=1, padx=10, pady=(10, 5), sticky='ew')

        contrast_label = ttk.Label(edit_tab, text='Contrast:')
        contrast_label.grid(row=1, column=2, padx=10, pady=(10, 5), sticky='ew')

        brightness_slider = ttk.Scale(
            edit_tab,
            from_=-50,
            to=50,
            orient='horizontal',
            command=self.update_image,
            variable=self.current_brightness,
            length=300
        )
        brightness_slider.grid(row=2, column=1, padx=10, pady=(5, 10), sticky='ew')

        contrast_slider = ttk.Scale(
            edit_tab,
            from_=-50,
            to=50,
            orient='horizontal',
            command=self.update_image,
            variable=self.current_contrast,
            length=150
        )
        contrast_slider.grid(row=2, column=2, padx=10, pady=(5, 10), sticky='ew')

        brightness_value_label = ttk.Label(edit_tab, text='Current Value:')
        brightness_value_label.grid(row=3, column=1, padx=10, pady=(10, 5), sticky='s')
        self.brightness_value_label = ttk.Label(edit_tab, text=self.get_current_value(self.current_brightness))
        self.brightness_value_label.grid(row=4, column=1, padx=10, pady=(5, 10), sticky='s')

        contrast_value_label = ttk.Label(edit_tab, text='Current Value:')
        contrast_value_label.grid(row=3, column=2, padx=10, pady=(10, 5), sticky='s')
        self.contrast_value_label = ttk.Label(edit_tab, text=self.get_current_value(self.current_contrast))
        self.contrast_value_label.grid(row=4, column=2, padx=10, pady=(5, 10), sticky='s')

        self.canvas = tk.Canvas(edit_tab, width=300, height=300)
        self.canvas.grid(row=0, column=0, rowspan=5, padx=10, pady=(10, 5), sticky='nsew')

        self.scrollbar = ttk.Scrollbar(edit_tab, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=3, rowspan=5, sticky='ns')

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.image_label = ttk.Label(self.canvas)
        self.image_label.grid(row=0, column=0)



        brightness_value_label = ttk.Label(edit_tab, text='Current Value:')
        brightness_value_label.grid(row=3, column=1, padx=10, pady=(10, 5), sticky='s')
        self.brightness_value_label = ttk.Label(edit_tab, text=self.get_current_value(self.current_brightness))
        self.brightness_value_label.grid(row=4, column=1, padx=10, pady=(5, 10), sticky='s')

        self.canvas = tk.Canvas(edit_tab, width=300, height=300)
        self.canvas.grid(row=0, column=0, rowspan=4, padx=10, pady=(10, 5), sticky='nsew')

        self.scrollbar = ttk.Scrollbar(edit_tab, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=2, rowspan=4, sticky='ns')

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.image_label = ttk.Label(self.canvas)
        self.image_label.grid(row=0, column=0)

        self.original_image = None
        self.processed_image = None
        self.image_display_size = (500, 600)  # Display size of the image

    def get_current_value(self, variable):
        return f"{variable.get():.2f}"

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.update_image(None)

    def update_image(self, event):
        if self.original_image is None:
            return

        brightness = self.current_brightness.get()
        contrast = self.current_contrast.get()

        self.processed_image = self.adjust_brightness_contrast(self.original_image, brightness, contrast)
        self.processed_image = self.adjust_brightness(self.original_image, brightness)

        im = Image.fromarray(self.processed_image)
        im = im.resize(self.image_display_size, Image.ANTIALIAS)  # Resize the image for display
        imgtk = ImageTk.PhotoImage(image=im)
        self.image_label.imgtk = imgtk
        self.image_label.config(image=imgtk)

        self.canvas.create_window((0, 0), window=self.image_label, anchor='nw')
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.brightness_value_label.config(text=self.get_current_value(self.current_brightness))
        self.contrast_value_label.config(text=self.get_current_value(self.current_contrast))

    def adjust_brightness_contrast(self, img, brightness=0, contrast=0):
        brightness = (brightness / 50.0) * 255
        buf = cv2.addWeighted(img, contrast, img, 0, brightness - 128 * (contrast - 1))
        return np.clip(buf, 0, 255).astype(np.uint8)
    def adjust_brightness(self, img, brightness=0):
        brightness = (brightness / 50.0) * 255
        buf = cv2.addWeighted(img, 1, img, 0, brightness)

        return np.clip(buf, 0, 255).astype(np.uint8)