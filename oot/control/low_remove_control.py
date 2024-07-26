from abc import *
from oot.data.data_manager import DataManager
from oot.gui.subframes.common import ScrollableListListener


class RemoveTextListHandler(ScrollableListListener):
    def selected_radio_list(self, text):
        pass

    def selected_check_list(self, text):
        print ('[RemoveTextListHandler] selected_check_list() called!!...')
        text_info = text.split('|', 1)

        # get selected item's info (id, text, status)
        from oot.gui.subframes.remove_frame import RemoveFrame
        selected_item_id = int(text_info[0])
        selected_item_text = text_info[1]
        selected_item_status = RemoveFrame.get_status_of_check_list(selected_item_id)
        print ('[RemoveTextListHandler] selected_check_list() : id = ', selected_item_id)
        print ('[RemoveTextListHandler] selected_check_list() : text = ', selected_item_text)
        print ('[RemoveTextListHandler] selected_check_list() : status = ', selected_item_status.get())

        from oot.gui.middle_frame import MiddleFrame
        # 체크하는 경우(status =  True) 양쪽 이미지에 사각형 그리기
        MiddleFrame.redraw_canvas_images()

def clicked_search_text(): 
    print('[low_remove_control] clicked_search_text() called!!...')
    texts = DataManager.get_texts_from_image()
    print(f'[low_remove_control] clicked_search_text() result : {texts}')
    
    if texts != None:
        from oot.gui.subframes.remove_frame import RemoveFrame
        scrollable_frame = RemoveFrame.get_frame()
        scrollable_frame.reset(texts)

def clicked_remove_text(): 
    from oot.gui.middle_frame import MiddleFrame
    print('[low_remove_control] clicked_search_text() called!!...')
    MiddleFrame.remove_selected_texts()

def clicked_revoke_image(): 
    from oot.gui.middle_frame import MiddleFrame
    print('[low_remove_control] clicked_revoke_image() called!!...')
    temp_file = DataManager.get_work_file().get_file_name()
    MiddleFrame.temp_out_canvas_images(temp_file)