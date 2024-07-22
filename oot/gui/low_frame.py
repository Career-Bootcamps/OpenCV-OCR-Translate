#from msilib.schema import Control
from tkinter import ttk

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
        self.remove_frame = RemoveFrame(remove_tab)
        
        # init write tab
        self.write_frame = WriteFrame(write_tab, root)
        
        # init mosaic tab
        MosaicFrame(mosaic_tab)

        # init edit tab
        EditFrame(edit_tab)

    
    def __tab_changed(self, event):
        tab_idx = LowFrame.notebook.index(LowFrame.notebook.select())
        print(f'tab_idx={tab_idx}')
        
        if tab_idx == 1:
            self.write_frame.write_tab_changed()
            
