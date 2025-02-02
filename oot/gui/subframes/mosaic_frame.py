from tkinter import ttk
import numpy as np
from oot.gui.common import ScrollableList, ScrollableListType

class MosaicFrame:
    root = None
    mosaic_tab_face_list = None

    def __init__(self, mosaic):
        self.__init_mosaic_area_detection(mosaic)
        self.__init_mosaic_model_apply(mosaic)
        
        from oot.control.low_mosaic_control import MosaicPostDrawHandler
        from oot.gui.middle_frame import MiddleFrame
        MiddleFrame.src_canvas_worker.set_post_draw_listener(MosaicPostDrawHandler())
        MiddleFrame.out_canvas_worker.set_post_draw_listener(MosaicPostDrawHandler())

    # ----------------------------------------------------------------
    # mosaic area detection
    # ---------------------------------------------------------------- 
    def __init_mosaic_area_detection(self, mosaic_frm):
        a = ttk.LabelFrame(mosaic_frm, text='모자이크 영역 검출')
        a.pack(fill='both', side='left', expand=True)
        
        from oot.control.low_mosaic_control import search_faces
        image_select = ttk.Button(a, text='얼굴 검출', command=search_faces)
        image_select.grid(column=0, row=0, columnspan=1, sticky='W')
        
        from oot.control.low_mosaic_control import MosaicTextListHandler
        mosaic_tab_list = ScrollableList(a, ScrollableListType.CHECK_BUTTON, MosaicTextListHandler())
        mosaic_tab_list.text.config(width=100)
        mosaic_tab_list.grid(column=0, row=1, columnspan=2, sticky='EW')
        mosaic_tab_list.reset()

        MosaicFrame.mosaic_tab_face_list = mosaic_tab_list

    # ----------------------------------------------------------------
    # mosaic model apply
    # ---------------------------------------------------------------- 
    def __init_mosaic_model_apply(self, mosaic_frm):
        
        b = ttk.LabelFrame(mosaic_frm, text='모자이크 적용')
        b.pack(fill='both', side='top')
        b.columnconfigure(0, weight=1)
        b.rowconfigure(0, weight=1)
        c = ttk.Frame(mosaic_frm)
        c.pack(side='bottom')
        
        mosaic_model = ttk.Label(b, text='모자이크 픽셀 선택')
        mosaic_model.grid(column=0, row=1, columnspan=2, sticky='W')

        combo_box = ttk.Combobox(b)
        combo_box.grid(column=0, row=1, columnspan=4, sticky='EW')
        
        px_list = tuple(round(x, 1) for x in np.arange(0.1, 0.4, 0.1))
        combo_box['values'] = px_list
        combo_box.current(0)
        MosaicFrame.combobox = combo_box
        
        from oot.control.low_mosaic_control import clicked_mosaic_faces
        model_apply = ttk.Button(c, text='적용', command=clicked_mosaic_faces)
        model_apply.pack(side='left')
        from oot.control.low_remove_control import clicked_revoke_image
        model_cancel = ttk.Button(c, text='원상태 복원', command=clicked_revoke_image)
        model_cancel.pack(side='left')

    @classmethod
    def get_face_list(cls):
        return cls.mosaic_tab_face_list

    @classmethod
    def reset_mosaic_tab_data(cls):
        # data 를 읽어 온다
        from oot.data.data_manager import DataManager
        faces = DataManager.get_work_file().get_faces_as_string()

        # 읽어온 data 로 변경(None 이면 list 모두 clear)
        cls.mosaic_tab_face_list.reset(faces)