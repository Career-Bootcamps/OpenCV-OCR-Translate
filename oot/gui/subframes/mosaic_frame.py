import tkinter as tk
from tkinter import ttk, messagebox as mb
import cv2
from PIL import Image, ImageTk
from oot.data.data_manager import DataManager
from oot.gui.subframes.common import ScrollableList, ScrollableListType
from oot.control.low_mosaic_control import MosaicListHandler

class MosaicFrame:
    root = None
    def __init__(self, mosaic):
        self.faces = []
        self.face_vars = []
        self.image = None
        self.canvas = None
        self.__init_mosaic_area_detection(mosaic)
        self.__init_mosaic_model_apply(mosaic)
        
    # ---------------------------------------------------------
    # 모자이크 영역 검출
    # ---------------------------------------------------------
        
    def __init_mosaic_area_detection(self, mosaic_frm):
        a = ttk.LabelFrame(mosaic_frm, text='얼굴 영역 검출')
        a.grid(row=0, column=0, sticky='NS')
        
        image_select = ttk.Button(a, text='보호 이미지 선택', command=self.get_mosaic_image)
        image_select.grid(column=0, row=0, columnspan=1, sticky='W')
        
        mosaic_tab_list = ScrollableList(a, ScrollableListType.CHECK_BUTTON, MosaicListHandler())
        mosaic_tab_list.text.config(width=100)
        mosaic_tab_list.grid(row=1, column=0, sticky='NS')
        mosaic_tab_list.reset()

        MosaicFrame.mosaic_tab_list = mosaic_tab_list
    
    # ---------------------------------------------------------
    # 모자이크 적용
    # ---------------------------------------------------------
         
    def __init_mosaic_model_apply(self, mosaic_frm):
        b = ttk.LabelFrame(mosaic_frm, text='모자이크 적용')
        b.grid(row=1, column=0, sticky='NE')
        b.columnconfigure(0, weight=1)
        b.rowconfigure(0, weight=1)
        c = ttk.Frame(mosaic_frm)
        c.grid(row=2, column=0, sticky='NE')
        
        mosaic_model = ttk.Label(b, text='모자이크 모델 선택')
        mosaic_model.grid(column=0, row=1, columnspan=2, sticky='W')

        combo_box = ttk.Combobox(b)
        combo_box.grid(column=0, row=1, columnspan=4, sticky='EW')
        
        font_size_list = tuple(range(5, 30))
        combo_box['values'] = font_size_list
        combo_box.current(5)
        
        model_apply = ttk.Button(c, text='적용')
        model_apply.grid(row=0, column=0, sticky='w')
        model_cancel = ttk.Button(c, text='취소')

    # ---------------------------------------------------------
    # 얼굴 영역 검출
    # ---------------------------------------------------------    

    def get_mosaic_image(self):
        work_file = DataManager.get_work_file()
        if work_file:
            file_path = work_file.get_file_name()
            self.image = cv2.imread(file_path)
            if self.image is not None:
                self.detect_faces()
            else:
                mb.showwarning("경고", "이미지를 불러올 수 없습니다.")
        else:
            mb.showwarning("경고", "작업할 이미지가 없습니다.")

    def detect_faces(self):
        self.faces = []
        self.face_vars = []
        self.mosaic_tab_list.reset()

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(detected_faces) == 0:
            mb.showwarning("경고", "보호이미지 부분을 찾을 수 없습니다.")
            return
        
        # 사각형 그리기
        for i, (x, y, w, h) in enumerate(detected_faces):
            cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            var = tk.IntVar(value=1)
            self.face_vars.append(var)
            self.faces.append((x, y, w, h))
            checkbox = tk.Checkbutton(self.mosaic_tab_list.text, variable=var, text=f"얼굴 {i+1}")
            self.mosaic_tab_list.text.window_create(tk.END, window=checkbox)
            self.mosaic_tab_list.text.insert(tk.END, "\n")
        
        self.update_right_canvas()

    def update_right_canvas(self):
        from oot.gui.middle_frame import MiddleFrame
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        MiddleFrame.out_canvas_worker.set_image(image_pil)
        MiddleFrame.out_canvas_worker.draw_image()

