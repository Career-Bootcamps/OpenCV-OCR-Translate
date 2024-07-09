import tkinter as tk
from tkinter import ttk
import sys
sys.path.append('.')
from oot.data.data_manager import DataManager



#------------------------------------------------------------------------------
# Top frame : top side buttons layout and command handlers
#------------------------------------------------------------------------------
class TopFrame:
    root = None
    label_curr_file_name = None

    def __init__(self, root):
        top_frm = tk.Frame(root)
        top_frm.pack(padx=2, pady=2, fill='both', side='top')

        # top buttons : '이전 이미지', '다음 이미지', '폴더 변경'
        from oot.control.top_control import clicked_change_folder
        btn_change_folder = ttk.Button(top_frm, text='폴더 변경', command=clicked_change_folder)
        

        label_curr_file_title = ttk.Label(top_frm, text='작업 파일:')
        TopFrame.label_curr_file_name = ttk.Label(top_frm, text=DataManager.folder_data.work_file.name)

        btn_change_folder.pack(side='left')
        label_curr_file_title.pack(side='left')
        TopFrame.label_curr_file_name.pack(side='left')
        
    @classmethod    
    def change_work_file(cls, work_file=None):
        print("work_file_name>> :",work_file)
        
        if cls.label_curr_file_name:
            cls.label_curr_file_name.config(text=work_file)
    