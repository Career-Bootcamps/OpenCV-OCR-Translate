from enum import Enum, auto
import tkinter as tk
from tkinter import END, IntVar, ttk

class ScrollableListType(Enum):
    CHECK_BUTTON = auto()
    RADIO_BUTTON = auto()

class ScrollableList(tk.Frame):
    # note : the following 2 variables should be reset when image changes
    #        - list_values
    #        - text
    def __init__(self, root, list_type, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.list_type = list_type
        self.vsb = ttk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(self, width=40, height=20, 
                            yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.text.yview)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.list_values = []
        
    def __get_indexed_text(self, idx, text):
        return str(idx) + '|' + text
    
    def reset(self, text_list=None):
        self.text.delete('1.0', END)
        self.list_values = []
        self.text_list = text_list
        print ('[LowFrame.ScrollableList] reset() called!!...')
        print ('[LowFrame.ScrollableList] reset() : text_list=', text_list)
        
        self.radio_value = None
        if text_list is not None:
            idx = 0
            self.radio_value = IntVar()
            self.list_values = [None] * len(text_list)
            for i in range(len(text_list)):
                self.list_values[i] = tk.BooleanVar()
            
            for t in text_list:
                if self.list_type == ScrollableListType.CHECK_BUTTON:
                    # Reference : checkbutton example getting value in callback
                    # - https://arstechnica.com/civis/viewtopic.php?t=69728
                    from oot.control.low_write_control import selectedCheckListInRemoveTab
                    cb = tk.Checkbutton(self, text=t, command=lambda i=self.__get_indexed_text(idx,t): selectedCheckListInRemoveTab(i), var=self.list_values[idx])
                elif self.list_type == ScrollableListType.RADIO_BUTTON:
                    from oot.control.low_write_control import selectedRadioListInRemoveTab
                    cb = tk.Radiobutton(self, text=t, command=lambda i=self.__get_indexed_text(idx,t): selectedRadioListInRemoveTab(i), variable=self.radio_value, value=idx)
                else:
                    cb = tk.Checkbutton(self, text=t)
                self.text.window_create("end", window=cb)
                self.text.insert("end", "\n") # to force one checkbox per line
                idx = idx + 1