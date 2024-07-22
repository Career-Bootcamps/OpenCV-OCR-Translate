import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
sys.path.append('.')
from oot.data.data_manager import DataManager
from oot.gui.top_frame import TopFrame
from oot.gui.middle_frame import MiddleFrame
from oot.gui.low_frame import LowFrame

# 메인 애플리케이션 클래스
class GuiManager:
    @staticmethod
    def init():
        # root window
        root = tk.Tk()
        root.geometry('1200x600+20+20')
        root.title('Image Text Master')

        # Top frame : top side buttons layout and command handlers
        GuiManager.top_frm = TopFrame(root)

        # Middle frame : middle side canvases
        GuiManager.mid_frm = MiddleFrame(root)

        # Low frame : low side tabbed pane (tools)
        GuiManager.low_frm = LowFrame(root)

        root.mainloop()
    
    @classmethod
    def changed_work_image(cls, work_file):
        
        print('[ControlManager.changedWorkImage] work_img=', work_file.get_file_name())
        DataManager.set_work_file(work_file) # 현재 작업 파일을 업데이트

        # clear all data in 'remove tab' of 'RemoveFrame'
        from oot.gui.subframes.remove_frame import RemoveFrame
        RemoveFrame.reset_remove_tab_data()
        
        # set texts to remove tab in 'WriteFrame'
        if work_file.is_ocr_executed():
            texts = work_file.get_texts_as_string()
        else:
            texts=None
        # clear all data in 'write tab' of 'WriteFrame'
        from oot.gui.subframes.write_frame import WriteFrame
        WriteFrame.reset_write_tab_data(texts)
        
        from oot.gui.middle_frame import MiddleFrame
        # Change images in canvases of 'MiddleFrame' with the 1st image of new dir
        MiddleFrame.reset_canvas_images(work_file)
        
        from oot.gui.top_frame import TopFrame
        # Set new dir to 'TopFrame' at the label displaying work dir
        TopFrame.change_work_file(work_file)