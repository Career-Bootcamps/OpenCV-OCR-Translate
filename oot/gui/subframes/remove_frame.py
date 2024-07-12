from tkinter import ttk


#------------------------------------------------------------------------------
# Low frame - remove tab : low frame remove tab controls
#------------------------------------------------------------------------------

class RemoveFrame:
    remove_tab_text_list = None

    def __init__(self, root):
        print("low_from_remove +++++++++++++++++++++++++++++++++++++")
        self.frame_btn = ttk.Frame(root)
        self.frame_btn.pack(padx=2, pady=2, fill='x')
        
        btn_search_text = ttk.Button(self.frame_btn, text='텍스트 찾기')
        btn_remove_text = ttk.Button(self.frame_btn, text='텍스트 지우기')
        btn_revoke_image = ttk.Button(self.frame_btn, text='원상태 복원')

        btn_search_text.pack(side='left')
        btn_remove_text.pack(side='left')
        btn_revoke_image.pack(side='left')

        remove_tab_down_frm = ttk.Frame(root)
        remove_tab_down_frm.pack(padx=2, pady=2, fill='both', expand=True)

        from oot.gui.low_frame import ScrollableList, ScrollableListType
        remove_tab_text_list = ScrollableList(remove_tab_down_frm, ScrollableListType.CHECK_BUTTON)

        remove_tab_text_list.pack(side="top", fill="x", expand=True)
        remove_tab_text_list.reset()
        self.remove_tab_text_list = remove_tab_text_list

    @classmethod
    def get_frame(cls):
        return cls.remove_tab_text_list