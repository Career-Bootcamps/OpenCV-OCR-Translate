import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sys
sys.path.append('.')
from oot.gui.low_frame import LowFrame

class CanvasWorker:
    def __init__(self, img_file, canvas):
        self.img_file = img_file
        self.canvas = canvas
        self.image = Image.open(img_file)
        self.photoimage = None
    
    def draw_image(self):
        self.photoimage = ImageTk.PhotoImage(file=self.img_file)
        
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        # sometimes at the very first draw, the canvas size was (1,1) and it makes error
        if canvas_w <= 1 or canvas_h <= 1:
            return

        self.scale_ratio = 1.0
        if canvas_w >= self.photoimage.width() and canvas_h >= self.photoimage.height():
            self.canvas.create_image(0,0, image=self.photoimage, anchor="nw")
        else:
            w1, h1 = self.image.size
            w, h = CanvasWorker.get_adapted_image_size(w1, h1, canvas_w, canvas_h)
            image_resized = self.image.resize((w, h), Image.ANTIALIAS)
            self.photoimage = ImageTk.PhotoImage(image_resized)
            self.canvas.create_image(0,0, image=self.photoimage, anchor="nw")
            self.scale_ratio = w/w1
            
    def change_image_file(self, img_file):
        self.img_file = img_file
        self.image = Image.open(img_file)

    def set_image(self, image):
        if image is not None:
            self.image = image
    
    def get_image(self):
        return self.image
    
    @classmethod
    def get_adapted_image_size(cls, img_w, img_h, canvas_w, canvas_h):
        w_ratio = img_h/img_w
        h_ratio = img_w/img_h
        if canvas_w*w_ratio <= canvas_h:
            return int(canvas_w), int(canvas_w*w_ratio)
        else:
            return int(canvas_h*h_ratio), int(canvas_h)


#------------------------------------------------------------------------------
# Middle frame : middle side canvases
#------------------------------------------------------------------------------
class MiddleFrame:
    def __init__(self, root):
        # middle canvases frame
        mid_frm = tk.Frame(root)
        MiddleFrame.mid_frm = mid_frm
        mid_frm.pack(padx=2, pady=2, fill='both', expand=True)

        left_canvas = tk.Canvas(mid_frm, bg='lightgray')
        left_canvas.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        right_canvas = tk.Canvas(mid_frm, bg='lightgray')
        right_canvas.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)

        from oot.data.data_manager import DataManager
        src_file = DataManager.folder_data.work_file.name
        out_file = DataManager.get_output_file()

        # Reference :
        # - https://www.youtube.com/watch?v=xiGQD2J47nA
        # - https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/image_bg_resize.py
        # - https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/
        def resizer(e):
            MiddleFrame.redraw_canvas_images()
 
        left_canvas.bind('<Configure>', resizer)
        # Added by Q&A from stackoverflow
        # https://stackoverflow.com/questions/72713209/how-to-keep-two-textboxes-the-same-size-when-resizing-window-with-python-tkinter
        mid_frm.columnconfigure((0,1), weight=1)
        mid_frm.rowconfigure(0, weight=1)

        MiddleFrame.src_canvas_worker = CanvasWorker(src_file, left_canvas)
        MiddleFrame.out_canvas_worker = CanvasWorker(out_file, right_canvas)


    @classmethod
    def redraw_canvas_images(cls):
        print ('[MiddleFrame.resizeCanvasImages] called...')
        cls.src_canvas_worker.draw_image()
        cls.out_canvas_worker.draw_image()

    @classmethod
    def get_adapted_image_size(cls, img_w, img_h, canvas_w, canvas_h):
        pass

    @classmethod
    def reset_canvas_images(cls, work_file):
        print ('[MiddleFrame] resetCanvasImages() called...')
        src_file = work_file.name
        from oot.data.data_manager import DataManager
        out_file = DataManager.get_output_file()

        cls.src_canvas_worker.change_image_file(src_file)
        cls.out_canvas_worker.change_image_file(out_file)

        cls.src_canvas_worker.draw_image()
        cls.out_canvas_worker.draw_image()
    

    @classmethod
    def remove_selected_texts(cls):
        pass
    