from abc import *
from oot.data.data_manager import DataManager
from oot.gui.common import ScrollableListListener, CanvasWorkerPostDrawListner
from oot.gui.subframes.remove_frame import RemoveFrame

class RemovePostDrawHandler(CanvasWorkerPostDrawListner):
    def do_post_draw(self, canvas, scale_ratio):
        # draw lines for selected text in check list of remove tab in LowFrame
            idx = 0
            list_values = RemoveFrame.remove_tab_text_list.list_values
            if list_values == None or len(list_values) == 0:
                return
            for item in RemoveFrame.remove_tab_text_list.list_values:
                if item.get() == True:
                    image_index = DataManager.get_image_index()
                    work_file = DataManager.folder_data.get_file_by_index(image_index) # FileData
                    start_pos, end_pos = work_file.get_rectangle_position_by_texts_index(idx)
                    canvas.create_rectangle(
                        int(scale_ratio*start_pos[0]),  # start x 
                        int(scale_ratio*start_pos[1]),  # start y
                        int(scale_ratio*end_pos[0]),    # end x
                        int(scale_ratio*end_pos[1]),    # end y
                        #outline='green'
                        outline='#00ff00'
                    )
                idx = idx + 1

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
        scrollable_frame = RemoveFrame.get_remove_tab_text_list()
        scrollable_frame.reset(texts)

def clicked_remove_text(): 
    from oot.gui.middle_frame import MiddleFrame
    print('[low_remove_control] clicked_search_text() called!!...')
    MiddleFrame.remove_selected_texts()

def clicked_revoke_image(): 
    from oot.gui.middle_frame import MiddleFrame
    print('[low_remove_control] clicked_revoke_image() called!!...')
    temp_file = DataManager.get_work_file().get_file_name()
    MiddleFrame.temp_out_canvas_image(temp_file)