import os
import tkinter as tk
from tkinter import ttk, font
from tkinter import END
from tkinter import messagebox
import googletrans
from googletrans import Translator
from httpcore import SyncHTTPProxy
from PIL import Image, ImageDraw, ImageFont

    
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
        
        from oot.control.low_write_control import WritePostDrawHandler
        from oot.gui.middle_frame import MiddleFrame
        MiddleFrame.src_canvas_worker.set_post_draw_listener(WritePostDrawHandler())
        MiddleFrame.out_canvas_worker.set_post_draw_listener(WritePostDrawHandler())

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
        from oot.gui.common import ScrollableList, ScrollableListType
        from oot.control.low_write_control import WriteTextListHandler
        # WriteFrame 인스턴스가 이미 생성되어 있다고 가정
        write_frame_instance = self
        write_tab_text_list = ScrollableList(left_frame, ScrollableListType.RADIO_BUTTON, WriteTextListHandler(write_frame_instance))
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

        self.combo_box = ttk.Combobox(b)
        self.combo_box.grid(column=0, row=1, columnspan=4, sticky=tk.W + tk.E)

        write_tab_right_label_font_size = ttk.Label(b, text='폰트 사이즈 :')
        write_tab_right_label_font_size.grid(column=0, row=2, columnspan=2, sticky=tk.W)

        # 기본값 설정
        default_font_size = 10
        
        # 입력 검증 함수
        def validate_font_size(input_str):
            if input_str.isdigit():
                value = int(input_str)
                if 1 <= value <= 90:
                    return True
            messagebox.showwarning("경고", "1~90까지 숫자만 입력해주세요")
            self.combo_box2.set(default_font_size)  # 경고 후 기본값으로 되돌림

            return False

        
        # 입력 검증을 위한 Tkinter 변수와 함수 설정
        validate_cmd = self.root.register(validate_font_size)
        
        # Spinbox 추가 - 값의 범위를 1에서 90으로 설정, 입력 검증 추가
        self.combo_box2 = ttk.Spinbox(b, from_=1, to=90, validate='focusout', validatecommand=(validate_cmd, '%P'))
        self.combo_box2.set(default_font_size)  # 기본값 설정
        self.combo_box2.grid(column=0, row=3, columnspan=2, sticky=tk.W + tk.E)

        write_tab_right_label_font_color = ttk.Label(b, text='폰트 색상 :')
        write_tab_right_label_font_color.grid(column=0, row=4, columnspan=2, sticky=tk.W)

        from oot.control.low_write_control import choose_color
        button_color = tk.Button(b, text='...', bg='#FFFF00', command=choose_color)
        button_color.grid(column=0, row=5, columnspan=1, sticky=tk.W + tk.E)
        WriteFrame.button_color = button_color

        write_tab_right_btn_apply = ttk.Button(c, text='적용', command=self.apply_text_to_image)
        write_tab_right_btn_apply.pack(side='left')
        write_tab_right_btn_cancel = ttk.Button(c, text='복귀')
        write_tab_right_btn_cancel.pack(side='left')

        # init font list
        #font_list = font.families()
        # 폴더 내의 모든 폰트 가져오기
        fonts_folder = "./fonts"
        all_fonts = []

        if os.path.isdir(fonts_folder):
            all_fonts = [os.path.join(fonts_folder, f) for f in os.listdir(fonts_folder) if f.endswith('.ttf')]

        # 폰트 파일 이름에서 확장자를 제거하고 리스트에 추가
        font_list = [os.path.basename(font).split('.')[0] for font in all_fonts]
        self.combo_box['values'] = font_list
        try:
            default_font_index = font_list.index('tvN 즐거운이야기 Medium')
        except ValueError as e:
            default_font_index = 0
        self.combo_box.current(default_font_index)



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

        write_tab_label_final = ttk.Label(write_tab_trans_frm, text='적용할 텍스트 :')
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
            
    @classmethod    
    def reset_color_of_button_in_write_tab(cls, color='#FFFF00'):
        WriteFrame.button_color.configure(bg=color)

    def get_complementary_color(self, color):
        """
        주어진 RGB 색상의 보색을 계산합니다.
        """
        r, g, b = color
        return (255 - r, 255 - g, 255 - b)
    
    def hex_to_rgb(self, hex_color):
        """Converts a hex color string to an RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def apply_text_to_image(self):
        from oot.data.data_manager import DataManager
        work_file = DataManager.get_work_file()
        selected_idx = self.write_tab_text_list.radio_value.get()
        
        try:
            start_pos, end_pos = work_file.get_rectangle_position_by_texts_index(selected_idx)
            
            apply_text = self.write_tab_text_final.get('1.0', 'end-1c')
            estimated_font_size = int(self.combo_box2.get())  # Get the selected font size
            font_style = self.combo_box.get()
            font_path = os.path.join("./fonts", f"{font_style}.ttf")
            
            try:
                font = ImageFont.truetype(font_path, estimated_font_size)
            except IOError:
                font = ImageFont.load_default()
                print(f"Could not load font '{font_style}', using default font.")


            out_file_path = DataManager.get_output_file()
            image = Image.open(out_file_path)
            draw = ImageDraw.Draw(image)
            
            # 배경색의 보색을 폰트 색상으로 설정
            background_color_hex = self.button_color.cget('bg')
            # Convert the hex color to RGB tuple
            background_color = self.hex_to_rgb(background_color_hex)

            draw.text(start_pos, apply_text, font=font, fill=background_color)
            print(f"텍스트 '{apply_text}'가 이미지에 추가되었습니다.")

            from oot.gui.middle_frame import MiddleFrame
            MiddleFrame.out_canvas_worker.set_image(image)
            MiddleFrame.redraw_canvas_images()
            
        except IndexError:
            print(f"IndexError: Text index {selected_idx} out of range.")