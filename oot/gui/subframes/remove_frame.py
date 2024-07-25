from tkinter import ttk

from oot.gui.subframes.common import ScrollableList, ScrollableListType
from oot.control.low_remove_control import RemoveTextListHandler


#------------------------------------------------------------------------------
# Low frame - remove tab : low frame remove tab controls
#------------------------------------------------------------------------------

class RemoveFrame:
    remove_tab_text_list = None

    def __init__(self, root):
        print("low_from_remove +++++++++++++++++++++++++++++++++++++")
        self.frame_btn = ttk.Frame(root)
        self.frame_btn.pack(padx=2, pady=2, fill='x')
        
        from oot.control.low_remove_control import clicked_search_text, clicked_remove_text
        btn_search_text = ttk.Button(self.frame_btn, text='텍스트 찾기', command=clicked_search_text)
        btn_remove_text = ttk.Button(self.frame_btn, text='텍스트 지우기', command=clicked_remove_text)
        btn_revoke_image = ttk.Button(self.frame_btn, text='원상태 복원')

        btn_search_text.pack(side='left')
        btn_remove_text.pack(side='left')
        btn_revoke_image.pack(side='left')

        remove_tab_down_frm = ttk.Frame(root)
        RemoveFrame.__set_remove_tab_text_list(remove_tab_down_frm)

        from oot.gui.middle_frame import MiddleFrame
        from oot.control.low_write_control import WritePostDrawListner
        MiddleFrame.src_canvas_worker.set_post_draw_listener(WritePostDrawListner())

    @classmethod
    def __set_remove_tab_text_list(cls, remove_tab_down_frm):
        remove_tab_down_frm.pack(padx=2, pady=2, fill='both', expand=True)
        cls.remove_tab_text_list = ScrollableList(remove_tab_down_frm, ScrollableListType.CHECK_BUTTON, RemoveTextListHandler())
        cls.remove_tab_text_list.pack(side="top", fill="x", expand=True)
    
    @classmethod
    def get_frame(cls):
        return cls.remove_tab_text_list

    @classmethod
    def get_status_of_check_list(cls, idx):
        print ('[RemoveFrame] get_status_of_check_list() called...')
        return cls.remove_tab_text_list.list_values[idx]
    
    @classmethod
    def reset_remove_tab_data(cls, texts=None):
        print ('[LowFrame] resetRemoveTabData() called...')
        print ('[LowFrame] resetRemoveTabData() : texts=', texts)
        cls.remove_tab_text_list.reset(texts)