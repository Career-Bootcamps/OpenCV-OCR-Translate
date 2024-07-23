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

        from  oot.data.data_manager import DataManager
        from  oot.gui.subframes.remove_frame import RemoveFrame
        tab_idx = LowFrame.notebook.index(LowFrame.notebook.select())
        if tab_idx == 0:
            # draw lines for selected text in check list of remove tab in LowFrame
            idx = 0
            list_values = RemoveFrame.remove_tab_text_list.list_values
            if list_values == None or len(list_values) == 0:
                return
            for item in RemoveFrame.remove_tab_text_list.list_values:
                if item.get() == True:
                    image_index = DataManager.get_image_index()
                    work_file = DataManager.folder_data.get_file_by_index(image_index) # FileData
                    start_pos, end_pos = work_file.get_rectangle_position_by_texts_index(idx)
                    self.canvas.create_rectangle(
                        int(self.scale_ratio*start_pos[0]),  # start x 
                        int(self.scale_ratio*start_pos[1]),  # start y
                        int(self.scale_ratio*end_pos[0]),    # end x
                        int(self.scale_ratio*end_pos[1]),    # end y
                        #outline='green'
                        outline='#00ff00'
                    )
                idx = idx + 1
        from  oot.gui.subframes.write_frame import WriteFrame
        if tab_idx == 1:
            # draw lines for selected text in check list of write tab in LowFrame
            if WriteFrame.write_tab_text_list is not None and WriteFrame.write_tab_text_list.radio_value is not None:
                idx = WriteFrame.write_tab_text_list.radio_value.get()
                image_index = DataManager.get_image_index()
                work_file = DataManager.folder_data.get_file_by_index(image_index) # FileData
                try:
                    start_pos, end_pos = work_file.get_rectangle_position_by_texts_index(idx)
                    self.canvas.create_rectangle(
                        int(self.scale_ratio*start_pos[0]),  # start x 
                        int(self.scale_ratio*start_pos[1]),  # start y
                        int(self.scale_ratio*end_pos[0]),    # end x
                        int(self.scale_ratio*end_pos[1]),    # end y
                        outline='#FF00FF'
                    )
                except IndexError:
                    print(f"IndexError: Text index {idx} out of range.")
            
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
        src_file = DataManager.get_work_file().get_file_name()
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
        src_file = work_file.get_file_name()
        from oot.data.data_manager import DataManager
        out_file = DataManager.get_output_file()

        cls.src_canvas_worker.change_image_file(src_file)
        cls.out_canvas_worker.change_image_file(out_file)

        cls.src_canvas_worker.draw_image()
        cls.out_canvas_worker.draw_image()
    

    @classmethod
    def remove_selected_texts(cls):
        from oot.data.data_manager import DataManager
        print ('[MiddleFrame] remove_selected_texts() called...')
        image_index = DataManager.get_image_index()
        work_file = DataManager.folder_data.get_file_by_index(image_index) # FileData
        texts = work_file.get_texts_as_string()       # 해당 워크 파일에 해당하는 TextData의 text
        if texts == None:
            print ('[MiddleFrame] remove_selected_texts() : no texts were selected!')
            return None
        
        # Reference : Image conversion from cv2 to PhotoImage (PIL)
        # - https://m.blog.naver.com/heennavi1004/222028305376
        import cv2
        out_file = DataManager.get_output_file()
        positions = work_file.get_positions_as_string()
        img_cv2 = cls.__inpaint_for_selected_texts(out_file, positions)
        if img_cv2 is None:
            print ('[MiddleFrame] remove_selected_texts() : no need to redraw image!')
            return
        
        img_conv = Image.fromarray(img_cv2)

        # reset (redraw) output canvas with image which selected texts were removed in
        cls.out_canvas_worker.set_image(img_conv)
        cls.redraw_canvas_images()
    
    @classmethod
    def __inpaint_for_selected_texts(cls, img_path, texts_position):
        import math
        import numpy as np
        import cv2
        import easyocr
        from oot.gui.subframes.remove_frame import RemoveFrame
        # texts # Example: [[24, 48], [345, 48], [345, 109], [24, 109]]
        print ('[MiddleFrame] __inpaint_for_selected_texts() called...')
        
        # generate (word, box) tuples 
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
        mask = np.zeros(img.shape[:2], dtype="uint8")

        img_return = None
        idx = 0
        for t in texts_position:
            list_status = RemoveFrame.remove_tab_text_list.list_values
            if list_status[idx].get() == True:
                x0, y0 = t[0]
                x1, y1 = t[1] 
                x2, y2 = t[2]
                x3, y3 = t[3] 

                x_mid0, y_mid0 = cls.__midpoint(x1, y1, x2, y2)
                x_mid1, y_mi1 = cls.__midpoint(x0, y0, x3, y3)
                thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
                
                cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255, thickness)
                img_return = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
            idx = idx+1
        return img_return
    
    @classmethod
    def __midpoint(cls, x1, y1, x2, y2):
        x_mid = int((x1 + x2)/2)
        y_mid = int((y1 + y2)/2)
        return (x_mid, y_mid)