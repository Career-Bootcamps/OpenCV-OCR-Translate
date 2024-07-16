import tkinter as tk
from tkinter import ttk, font
from tkinter import END
from tkinter import colorchooser



def choose_color():
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title ="Choose color") 
    
    from oot.gui.low_frame import LowFrame
    LowFrame.reset_color_of_button_in_write_tab(color=color_code[1])
    
class WriteFrame:

    def __init__(self, low_frm_write_tab):
        # low frame write tab - [LEFT] text list
        self.__init_write_tab_texts_tool(low_frm_write_tab)

        # low frame write tab - [RIGHT] style tool and buttons
        self.__init_write_tab_style_tool(low_frm_write_tab)

        # low frame write tab - [CENTER] translation tool
        self.__init_write_tab_translation_tool(low_frm_write_tab)

    # low frame write tab - [LEFT] texts tool
    def __init_write_tab_texts_tool(self, low_frm_write_tab):
        
        from oot.gui.subframes.common import ScrollableList, ScrollableListType
        write_tab_text_list = ScrollableList(low_frm_write_tab, ScrollableListType.RADIO_BUTTON)
        write_tab_text_list.text.config(width=20)
        write_tab_text_list.pack(padx=2, pady=2, side="left", fill="y")
        write_tab_text_list.reset()

        WriteFrame.write_tab_text_list = write_tab_text_list

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
        combo_box.grid(column=0, row=1, columnspan=4, sticky=tk.W + tk.E)

        write_tab_right_label_font_size = ttk.Label(b, text='폰트 사이즈 :')
        write_tab_right_label_font_size.grid(column=0, row=2, columnspan=2, sticky=tk.W)

        combo_box2 = ttk.Combobox(b)
        combo_box2.grid(column=0, row=3, columnspan=2, sticky=tk.W + tk.E)

        write_tab_right_label_font_color = ttk.Label(b, text='폰트 색상 :')
        write_tab_right_label_font_color.grid(column=0, row=4, columnspan=2, sticky=tk.W)
        
        
        button_color = tk.Button(b, text='...', bg='yellow', command=choose_color)
        button_color.grid(column=0, row=5, columnspan=1, sticky=tk.W + tk.E)
        WriteFrame.button_color = button_color

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

        from oot.gui.low_frame import LowFrame
        WriteFrame.write_tab_text_org = write_tab_text_org
        WriteFrame.write_tab_text_google = write_tab_text_google
        WriteFrame.write_tab_text_final = write_tab_text_final
    
    def write_tab_changed(self):
            from oot.gui.low_frame import LowFrame

            radiobuttons = WriteFrame.write_tab_text_list
            if radiobuttons is not None and radiobuttons.radio_value is not None:
                selected_idx = radiobuttons.radio_value.get()
                target_string = WriteFrame.write_tab_text_org.get("1.0",'end-1c')
                if selected_idx == 0 and target_string is None or len(target_string) == 0:
                    # write text to original text area of write tab in low frame
                    LowFrame.reset_translation_target_text_in_write_tab(radiobuttons.text_list[selected_idx])