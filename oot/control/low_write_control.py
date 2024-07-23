from tkinter import colorchooser
import sys
sys.path.append('.')
from oot.data.data_manager import DataManager
from oot.gui.middle_frame import MiddleFrame
from oot.gui.subframes.common import ScrollableListListener
from oot.gui.subframes.write_frame import WriteFrame



class WriteTextListHandler(ScrollableListListener):
    def selected_check_list(self, text):
        pass
        
    def selected_radio_list(self, text):
        print ('[WriteTextListHandler] selectedRadioListInRemoveTab() called!!...')
        text_info = text.split('|', 1)

        # get selected item's info (id, text, status)
        from oot.gui.subframes.write_frame import WriteFrame
        selected_item_id = int(text_info[0])
        selected_item_text = text_info[1]
        print ('[WriteTextListHandler] selected_radio_list() : id = ', selected_item_id)
        print ('[WriteTextListHandler] selected_radio_list() : text = ', selected_item_text)
        
        # write text to original text area of write tab in low frame
        WriteFrame.reset_translation_target_text_in_write_tab(selected_item_text)

        MiddleFrame.reset_canvas_images(DataManager.get_work_file())

def choose_color():
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title ="Choose color") 
    
    WriteFrame.reset_color_of_button_in_write_tab(color=color_code[1])

    
def clicked_read_text():
        print('[low_write_control] clicked_search_text() called!!...')
        from oot.data.data_manager import DataManager
        texts = DataManager.get_texts_from_image()

        if texts is None:
            return

        WriteFrame.reset_write_tab_data(texts)

        # 첫 번째 라디오 버튼을 선택하고 상자 그리기
        WriteFrame.write_tab_text_list.radio_value.set(0)
        WriteFrame.reset_translation_target_text_in_write_tab(texts[0])

        # 이미지에 상자 그리기
        from oot.gui.middle_frame import MiddleFrame
        MiddleFrame.redraw_canvas_images()
