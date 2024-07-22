import tkinter as tk
from tkinter import ttk, font
from tkinter import END
from tkinter import messagebox
import googletrans
from googletrans import Translator
from httpcore import SyncHTTPProxy
    
ENABLE_PROXY = False

class WriteFrame:

    def __init__(self, low_frm_write_tab, root):
        self.root = root
        # low frame write tab - [LEFT] text list
        self.__init_write_tab_texts_tool(low_frm_write_tab)

        # low frame write tab - [RIGHT] style tool and buttons
        self.__init_write_tab_style_tool(low_frm_write_tab)

        # low frame write tab - [CENTER] translation tool
        self.__init_write_tab_translation_tool(low_frm_write_tab)

    # low frame write tab - [LEFT] texts tool
    def __init_write_tab_texts_tool(self, low_frm_write_tab):
        
        # Create a frame to hold both the button and the text list
        left_frame = ttk.Frame(low_frm_write_tab)
        left_frame.pack(side="left", fill="y")
        
        # Adding the 'Read Text' button
        from oot.control.low_write_control import clicked_read_text
        read_text_button = ttk.Button(left_frame, text='텍스트 읽어오기', command=clicked_read_text)
        read_text_button.pack(padx=2, pady=2, anchor='nw')
    
        # Packing the text list below the button
        from oot.gui.subframes.common import ScrollableList, ScrollableListType
        from oot.control.low_write_control import WriteTextListHandler
        write_tab_text_list = ScrollableList(left_frame, ScrollableListType.RADIO_BUTTON, WriteTextListHandler())
        write_tab_text_list.text.config(width=20)
        write_tab_text_list.pack(padx=2, pady=2, fill="both", expand=True)
        write_tab_text_list.reset()

        WriteFrame.write_tab_text_list = write_tab_text_list
        

    # low frame write tab - [RIGHT] style tool and buttons
    # font
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

        # 기본값 설정
        default_font_size = 5
        
        # 입력 검증 함수
        def validate_font_size(input_str):
            if input_str.isdigit():
                value = int(input_str)
                if 1 <= value <= 60:
                    return True
            messagebox.showwarning("경고", "1~60까지 숫자만 입력해주세요")
            combo_box2.set(default_font_size)  # 경고 후 기본값으로 되돌림

            return False

        
        # 입력 검증을 위한 Tkinter 변수와 함수 설정
        validate_cmd = self.root.register(validate_font_size)
        
        # Spinbox 추가 - 값의 범위를 1에서 60으로 설정, 입력 검증 추가
        combo_box2 = ttk.Spinbox(b, from_=1, to=60, validate='focusout', validatecommand=(validate_cmd, '%P'))
        combo_box2.set(default_font_size)  # 기본값 설정
        combo_box2.grid(column=0, row=3, columnspan=2, sticky=tk.W + tk.E)

        write_tab_right_label_font_color = ttk.Label(b, text='폰트 색상 :')
        write_tab_right_label_font_color.grid(column=0, row=4, columnspan=2, sticky=tk.W)

        from oot.control.low_write_control import choose_color
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



    # low frame write tab - [CENTER] translation tool
    def __init_write_tab_translation_tool(self, low_frm_write_tab):
        write_tab_trans_frm = ttk.LabelFrame(low_frm_write_tab, text="번역 도구")
        write_tab_trans_frm.pack(padx=2, pady=2, fill='both', side='top', expand=True)
        write_tab_trans_frm.columnconfigure(0, weight=1)

        write_tab_label_org = ttk.Label(write_tab_trans_frm, text='원본 텍스트 :')
        write_tab_label_org.grid(column=0, row=0, sticky=tk.W)
        write_tab_text_org = tk.Text(write_tab_trans_frm, height=3)
        write_tab_text_org.grid(column=0, row=1, sticky=tk.W+tk.E+tk.N+tk.S)

        write_tab_label_google = ttk.Label(write_tab_trans_frm, text='적용할 텍스트 :')
        write_tab_label_google.grid(column=0, row=2, sticky=tk.W)
        write_tab_text_google = tk.Text(write_tab_trans_frm, height=3)
        write_tab_text_google.grid(column=0, row=3, sticky=tk.W+tk.E+tk.N+tk.S)

        write_tab_label_final = ttk.Label(write_tab_trans_frm, text='추천 상업용 문구 :')
        write_tab_label_final.grid(column=0, row=4, sticky=tk.W)
        write_tab_text_final = tk.Text(write_tab_trans_frm, height=3)
        write_tab_text_final.grid(column=0, row=5, sticky=tk.W+tk.E+tk.N+tk.S)

        WriteFrame.write_tab_text_org = write_tab_text_org
        WriteFrame.write_tab_text_google = write_tab_text_google
        WriteFrame.write_tab_text_final = write_tab_text_final
    
    def write_tab_changed(self):
            print("[write_tab_changed] called()!!...")
            radiobuttons = WriteFrame.write_tab_text_list
            
            # 라디오 버튼 목록이 있고, 라디오 값이 None이 아닌 경우
            if radiobuttons is not None and radiobuttons.radio_value is not None:
                selected_idx = radiobuttons.radio_value.get()
                target_string = None  # Initialize target_string
                
                # 라디오 버튼 목록의 텍스트 리스트가 있고, 선택된 인덱스가 유효한 경우
                if radiobuttons.text_list and 0 <= selected_idx < len(radiobuttons.text_list):
                    target_string = WriteFrame.write_tab_text_org.get("1.0", 'end-1c')

                    # 선택된 인덱스가 0이고, target_string이 비어 있는 경우
                    if selected_idx == 0 and (target_string is None or len(target_string) == 0):
                        # 원본 텍스트 영역에 선택된 텍스트를 설정
                        print("[write_tab_changed] 선택된 텍스트>>>",radiobuttons.text_list)
                        WriteFrame.reset_translation_target_text_in_write_tab(radiobuttons.text_list[selected_idx])

            
    @classmethod
    def reset_write_tab_data(cls, texts=None):
        print ('[WriteFrame.resetWriteTabData] called...')

        # clear test list found in the image
        cls.write_tab_text_list.reset(texts)

        # get the current work file from DataManager
        from oot.data.data_manager import DataManager
        current_work_file = DataManager.get_work_file()

        # clear 'translation tool' area
        cls.write_tab_text_org.config(state='normal')
        cls.write_tab_text_org.delete('1.0', END)
        cls.write_tab_text_google.config(state='normal')
        cls.write_tab_text_google.delete('1.0', END)
        cls.write_tab_text_final.delete('1.0', END)

        # load first text and its translation if it exists
        texts = current_work_file.get_texts()
        if texts:
            first_text_data = texts[0]
            original_text = first_text_data.get_text()
            translated_text = first_text_data.get_tr_text()
            cls.write_tab_text_org.insert('end', original_text + '\n')
            if translated_text:
                cls.write_tab_text_google.insert('end', translated_text + '\n')
                cls.write_tab_text_final.insert('end', translated_text + '\n')

        cls.write_tab_text_org.config(state='disabled')
        cls.write_tab_text_google.config(state='disabled')
        
    @classmethod
    def reset_translation_target_text_in_write_tab(cls, text=None):
        # clear 'translation tool' area
        cls.write_tab_text_org.config(state='normal')
        cls.write_tab_text_org.delete('1.0', END)
        cls.write_tab_text_google.config(state='normal')
        cls.write_tab_text_google.delete('1.0', END)
        cls.write_tab_text_final.delete('1.0', END)

        # set text to original text area
        cls.write_tab_text_org.insert("end", text)
        cls.write_tab_text_org.config(state='disabled')

        # translate it
        if ENABLE_PROXY:
            proxies_def = {'https': SyncHTTPProxy((b'http', b'www-proxy.us.oracle.com', 80, b''))}
            translator = googletrans.Translator(proxies=proxies_def)
        else:
            translator = Translator()
        result = translator.translate(text, dest='ko')

        # get the current work file from DataManager
        from oot.data.data_manager import DataManager
        current_work_file = DataManager.get_work_file()

        # store the translations in the current work file's TextData objects
        texts = current_work_file.get_texts()
        for text_data in texts:
            if text_data.get_text() == text:
                text_data.set_tr_text_with_position(result.text, text_data.get_position_info())

        # set result text to 
        cls.write_tab_text_google.insert("end", result.text)
        cls.write_tab_text_google.config(state='disabled')
        cls.write_tab_text_final.insert("end", result.text)
        
        # TODO: clear 'style tool' area
    
    @classmethod    
    def reset_color_of_button_in_write_tab(color='#FFFF00'):
        WriteFrame.button_color.configure(bg=color)