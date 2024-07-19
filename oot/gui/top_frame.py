import os
import tkinter as tk
from tkinter import ttk



#------------------------------------------------------------------------------
# Top frame : top side buttons layout and command handlers
#------------------------------------------------------------------------------
class TopFrame:
    root = None
    label_curr_file_name = None

    def __init__(self, root):
        top_frm = tk.Frame(root)
        top_frm.pack(padx=2, pady=2, fill='both', side='top')

        # top buttons : '이전 이미지', '다음 이미지', '폴더 변경', '결과 저장'
        from oot.control.top_control import clicked_prev_image, clicked_next_image
        btn_prev_image = ttk.Button(top_frm, text='이전 이미지', command=clicked_prev_image)
        btn_next_image = ttk.Button(top_frm, text='다음 이미지', command=clicked_next_image)
        
        from oot.control.top_control import clicked_change_folder
        btn_change_folder = ttk.Button(top_frm, text='폴더 변경', command=clicked_change_folder)

        from oot.control.top_control import clicked_save_output
        btn_save_image = ttk.Button(top_frm, text='결과 저장', command=clicked_save_output)        

        label_curr_file_title = ttk.Label(top_frm, text='작업 파일:')
        
        from oot.data.data_manager import DataManager
        TopFrame.label_curr_file_name = ttk.Label(top_frm, text=DataManager.get_work_file().get_file_name())

        btn_prev_image.pack(side='left')
        btn_next_image.pack(side='left')
        btn_change_folder.pack(side='left')
        btn_save_image.pack(side='right')
        label_curr_file_title.pack(side='left')
        TopFrame.label_curr_file_name.pack(side='left')
        
    @classmethod    
    def change_work_file(cls, work_file=None):
        print("work_file_name>> :", work_file.get_file_name())
        
        if cls.label_curr_file_name:
            cls.label_curr_file_name.config(text=work_file.get_file_name())

    @classmethod
    def reset_work_file(cls):
        from oot.data.data_manager import DataManager
        new_work_file = DataManager.get_work_file()
        cls.change_work_file(new_work_file)
        print(f"{cls.__name__}: 작업 파일이 재설정되었습니다.")