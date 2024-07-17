#from msilib.schema import Control
from tkinter import ttk

import googletrans
from googletrans import Translator
from httpcore import SyncHTTPProxy

from PIL import ImageTk, Image
from tkinter import END, scrolledtext

from oot.gui.subframes.remove_frame import RemoveFrame
from oot.gui.subframes.write_frame import WriteFrame
from oot.gui.subframes.mosaic_frame import MosaicFrame
from oot.gui.subframes.edit_frame import EditFrame



#------------------------------------------------------------------------------
# Low frame : low side tabbed pane (tools)
#------------------------------------------------------------------------------
class LowFrame:

    def __init__(self, root):
        # create a notebook
        low_frm = ttk.Notebook(root)
        LowFrame.notebook = low_frm
        low_frm.bind("<<NotebookTabChanged>>", self.__tab_changed)
        
        low_frm.pack(pady=10, fill='both')
        low_frm.config(height=220)

        # create frames
        remove_tab = ttk.Frame(low_frm, height=50)
        write_tab = ttk.Frame(low_frm, height=50)
        edit_tab = ttk.Frame(low_frm, height=50)
        mosaic_tab = ttk.Frame(low_frm, height=50)

        remove_tab.pack(fill='both', expand=True)
        write_tab.pack(fill='both', expand=True)
        edit_tab.pack(fill='both', expand=True)
        mosaic_tab.pack(fill='both', expand=True)


        # add frames to notebook
        low_frm.add(remove_tab, text='지우기')
        low_frm.add(write_tab, text='쓰기')
        low_frm.add(edit_tab, text='이미지편집')
        low_frm.add(mosaic_tab, text='모자이크')
        
        # init remove tab
        remove_tab_content = RemoveFrame(remove_tab)
        
        # init write tab
        self.write_frame = WriteFrame(write_tab, root)
        
        # init mosaic tab
        MosaicFrame(mosaic_tab)

        # init edit tab
        EditFrame(edit_tab)

    @classmethod
    def get_status_of_check_list_in_remove_tab(cls, idx):
        pass

    @classmethod
    def reset_remove_tab_data(cls, texts=None):
        pass

    @classmethod
    def reset_write_tab_data(cls, texts=None):
        pass

    @classmethod
    def reset_translation_target_text_in_write_tab(cls, text=None):
        pass

    @classmethod
    def reset_color_of_button_in_write_tab(cls, color='#FFFF00'):
        pass
    
    def __tab_changed(self, event):
        tab_idx = LowFrame.notebook.index(LowFrame.notebook.select())
        print(f'tab_idx={tab_idx}')
        
        if tab_idx == 1:
          self.write_frame.write_tab_changed()
            
