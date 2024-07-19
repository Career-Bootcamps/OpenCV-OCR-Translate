from oot.gui.subframes.remove_frame import RemoveFrame
from oot.data.data_manager import DataManager

def clicked_search_text(): 
    print('[low_remove_control] clicked_search_text() called!!...')
    texts = DataManager.get_texts_from_image()
    print(f'[low_remove_control] clicked_search_text() result : {texts}')
    
    if texts != None:
        scrollable_frame = RemoveFrame.get_frame()
        scrollable_frame.reset(texts)

def selected_radio_list_in_remove_tab(text):
    print ('[RemoveFrameControl] selected_radio_list_in_remove_tab() called!!...')
    text_info = text.split('|', 1)

    # get selected item's info (id, text, status)
    selected_item_id = int(text_info[0])
    selected_item_text = text_info[1]
    print ('[RemoveFrameControl] selected_radio_list_in_remove_tab() : id = ', selected_item_id)
    print ('[RemoveFrameControl] selected_radio_list_in_remove_tab() : text = ', selected_item_text)

    # write text to original text area of write tab in low frame
    from oot.gui.low_frame import LowFrame
    LowFrame.reset_translation_target_text_in_write_tab(selected_item_text)

    from oot.gui.middle_frame import MiddleFrame
    from oot.data.data_manager import DataManager
    MiddleFrame.reset_canvas_images(DataManager.folder_data.get_work_file())

def selected_check_list_in_remove_tab(text):
    from oot.gui.subframes.remove_frame import RemoveFrame
    print ('[RemoveFrameControl] selected_check_list_in_remove_tab() called!!...')
    text_info = text.split('|', 1)

    # get selected item's info (id, text, status)
    selected_item_id = int(text_info[0])
    selected_item_text = text_info[1]
    selected_item_status = RemoveFrame.get_status_of_check_list(selected_item_id)
    print ('[RemoveFrameControl] selected_check_list_in_remove_tab() : id = ', selected_item_id)
    print ('[RemoveFrameControl] selected_check_list_in_remove_tab() : text = ', selected_item_text)
    print ('[RemoveFrameControl] selected_check_list_in_remove_tab() : status = ', selected_item_status.get())
    from oot.gui.middle_frame import MiddleFrame
    from oot.data.data_manager import DataManager
    MiddleFrame.reset_canvas_images(DataManager.folder_data.get_work_file())

