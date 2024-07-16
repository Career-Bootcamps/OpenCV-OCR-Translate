#from msilib.schema import Control
from tkinter import ttk

import googletrans
from googletrans import Translator
from httpcore import SyncHTTPProxy

from PIL import ImageTk, Image
from tkinter import END, scrolledtext
import cv2

from oot.gui.subframes.edit_frame import EditFrame

# import sys
# sys.path.append('.')

from oot.gui.subframes.remove_frame import RemoveFrame
from oot.gui.subframes.write_frame import WriteFrame
from oot.gui.subframes.mosaic_frame import MosaicFrame



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
        self.write_frame = WriteFrame(write_tab)
        
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
            # write text to original text area of write tab in low frame
            radiobuttons = LowFrame.write_tab_text_list
            if radiobuttons is not None and radiobuttons.radio_value is not None:
                selected_idx = radiobuttons.radio_value.get()
                target_string = LowFrame.write_tab_text_org.get("1.0",'end-1c')
                if selected_idx == 0 and target_string is None or len(target_string) == 0:
                    # write text to original text area of write tab in low frame
                    LowFrame.reset_translation_target_text_in_write_tab(radiobuttons.text_list[selected_idx])

        
        
    #------------------------------------------------------------------------------
    # Low frame - write tab : low frame write tab controls
    #------------------------------------------------------------------------------
    def __init_write_tab(self, low_frm_write_tab):
        # low frame write tab - [LEFT] text list
        self.__init_write_tab_texts_tool(low_frm_write_tab)

        # low frame write tab - [RIGHT] style tool and buttons
        self.__init_write_tab_style_tool(low_frm_write_tab)
        
        # low frame write tab - [CENTER] translation tool
        self.__init_write_tab_translation_tool(low_frm_write_tab)

    # low frame write tab - [LEFT] texts tool
    def __init_write_tab_texts_tool(self, low_frm_write_tab):
        write_tab_text_list = scrollable_list(low_frm_write_tab, scrollable_list_type.RADIO_BUTTON)
        write_tab_text_list.text.config(width=20)
        write_tab_text_list.pack(padx=2, pady=2, side="left", fill="y")
        write_tab_text_list.reset()

        LowFrame.write_tab_text_list = write_tab_text_list

    # low frame write tab - [RIGHT] style tool and buttons
    def __init_write_tab_style_tool(self, low_frm_write_tab):
        a = ttk.Frame(low_frm_write_tab)
        a.pack(side='right', fill='both')

        b = ttk.LabelFrame(a, text='스타일 도구')
        b.pack(fill='both', side='top')
        b.columnconfigure(0, weight=1)
        b.rowconfigure(0, weight=1)
        c = ttk.Frame(a)
        c.pack(side='bottom')

        write_tab_right_label_font_style = ttk.Label(b, text='폰트 스타일 :')
        write_tab_right_label_font_style.grid(column=0, row=0, columnspan=2, sticky=tk.W)

        combo_box = ttk.Combobox(b)
        combo_box.grid(column=0, row=1, columnspan=4, sticky=tk.W+tk.E)

        write_tab_right_label_font_size = ttk.Label(b, text='폰트 사이즈 :')
        write_tab_right_label_font_size.grid(column=0, row=2, columnspan=2, sticky=tk.W)

        combo_box2 = ttk.Combobox(b)
        combo_box2.grid(column=0, row=3, columnspan=2, sticky=tk.W+tk.E)

        write_tab_right_label_font_color = ttk.Label(b, text='폰트 색상 :')
        write_tab_right_label_font_color.grid(column=0, row=4, columnspan=2, sticky=tk.W)

        button_color = tk.Button(b, text='...', bg='yellow', command = choose_color)
        button_color.grid(column=0, row=5, columnspan=1, sticky=tk.W+tk.E)
        LowFrame.button_color = button_color

        write_tab_right_btn_apply = ttk.Button(c, text='적용')
        write_tab_right_btn_apply.pack(side='left')
        write_tab_right_btn_cancel = ttk.Button(c, text='취소')
        write_tab_right_btn_cancel.pack(side='left')

        # init font list
        font_list = font.families()
        combo_box['values'] = font_list
        try:
            default_font_index = font_list.index('맑은 고딕')
        except ValueError as e:
            default_font_index = 0
        combo_box.current(default_font_index)

        # init font size list
        font_size_list = tuple(range(5, 30))
        combo_box2['values'] = font_size_list
        combo_box2.current(5)


    # low frame write tab - [CENTER] translation tool
    def __init_write_tab_translation_tool(self, low_frm_write_tab):
        write_tab_trans_frm = ttk.LabelFrame(low_frm_write_tab, text="번역 도구")
        write_tab_trans_frm.pack(padx=2, pady=2, fill='both', side='top', expand=True)
        write_tab_trans_frm.columnconfigure(0, weight=1)

        write_tab_label_org = ttk.Label(write_tab_trans_frm, text='원본 텍스트 :')
        write_tab_label_org.grid(column=0, row=0, sticky=tk.W)
        write_tab_text_org = tk.Text(write_tab_trans_frm, height=3)
        write_tab_text_org.grid(column=0, row=1, sticky=tk.W+tk.E+tk.N+tk.S)

        write_tab_label_google = ttk.Label(write_tab_trans_frm, text='구글 번역 결과 :')
        write_tab_label_google.grid(column=0, row=2, sticky=tk.W)
        write_tab_text_google = tk.Text(write_tab_trans_frm, height=3)
        write_tab_text_google.grid(column=0, row=3, sticky=tk.W+tk.E+tk.N+tk.S)

        write_tab_label_final = ttk.Label(write_tab_trans_frm, text='추천 상업용 문구 :')
        write_tab_label_final.grid(column=0, row=4, sticky=tk.W)
        write_tab_text_final = tk.Text(write_tab_trans_frm, height=3)
        write_tab_text_final.grid(column=0, row=5, sticky=tk.W+tk.E+tk.N+tk.S)

        LowFrame.write_tab_text_org = write_tab_text_org
        LowFrame.write_tab_text_google = write_tab_text_google
        LowFrame.write_tab_text_final = write_tab_text_final

class scrollable_list_type(Enum):
    CHECK_BUTTON = auto()
    RADIO_BUTTON = auto()

class scrollable_list(tk.Frame):
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
          self.write_frame.write_tab_changed()
            
