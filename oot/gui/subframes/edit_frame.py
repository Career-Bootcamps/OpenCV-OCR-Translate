import tkinter as tk
from tkinter import ttk

class EditFrame:
    def __init__(self, edit_tab):
        edit_tab.pack_propagate(False)
        edit_tab.columnconfigure(0, weight=1)
        edit_tab.columnconfigure(1, weight=0)
        edit_tab.columnconfigure(2, weight=1)
        edit_tab.rowconfigure(0, weight=1)
        edit_tab.rowconfigure(1, weight=0)

        self.current_brightness = tk.DoubleVar()
        self.current_brightness.set(0)

        brightness_label = ttk.Label(edit_tab, text='Brightness:')
        brightness_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='ew')
        brightness_slider = ttk.Scale(
            edit_tab,
            from_=-50,
            to=50,
            orient='horizontal',
            command=self.brightness_changed,
            variable=self.current_brightness,
            length=150
        )
        brightness_slider.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='ew')

        brightness_value_label = ttk.Label(edit_tab, text='Current Value:')
        brightness_value_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky='s')
        self.brightness_value_label = ttk.Label(edit_tab, text=self.get_current_value(self.current_brightness))
        self.brightness_value_label.grid(row=3, column=0, padx=10, pady=(5, 10), sticky='s')

        separator = ttk.Separator(edit_tab, orient='vertical')
        separator.grid(row=0, column=1, rowspan=4, sticky='ns', padx=10)

        self.current_contrast = tk.DoubleVar()
        self.current_contrast.set(0)

        contrast_label = ttk.Label(edit_tab, text='Contrast:')
        contrast_label.grid(row=0, column=2, padx=10, pady=(10, 5), sticky='ew')
        contrast_slider = ttk.Scale(
            edit_tab,
            from_=-50,
            to=50,
            orient='horizontal',
            command=self.contrast_changed,
            variable=self.current_contrast,
            length=150
        )
        contrast_slider.grid(row=1, column=2, padx=10, pady=(5, 10), sticky='ew')

        contrast_value_label = ttk.Label(edit_tab, text='Current Value:')
        contrast_value_label.grid(row=2, column=2, padx=10, pady=(10, 5), sticky='s')
        self.contrast_value_label = ttk.Label(edit_tab, text=self.get_current_value(self.current_contrast))
        self.contrast_value_label.grid(row=3, column=2, padx=10, pady=(5, 10), sticky='s')

    def get_current_value(self, variable):
        return f"{variable.get():.2f}"

    def brightness_changed(self, event):
        self.brightness_value_label.config(text=self.get_current_value(self.current_brightness))

    def contrast_changed(self, event):
        self.contrast_value_label.config(text=self.get_current_value(self.current_contrast))
