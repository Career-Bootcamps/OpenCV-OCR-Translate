from abc import *
from oot.data.data_manager import DataManager
from oot.gui.subframes.common import ScrollableListListener

class MosaicListHandler(ScrollableListListener):
    def selected_radio_list(self, text):
        pass

    def selected_check_list(self, text):
        print ('[MosaicListHandler] selected_check_list() called!!...')
        text_info = text.split('|', 1)

        # get selected item's info (id, text, status)
        from oot.gui.subframes.mosaic_frame import MosaicFrame
        selected_item_id = int(text_info[0])
        selected_item_text = text_info[1]
        selected_item_status = MosaicFrame.get_status_of_check_list(selected_item_id)
        print ('[MosaicListHandler] selected_check_list() : id = ', selected_item_id)
        print ('[MosaicListHandler] selected_check_list() : text = ', selected_item_text)
        print ('[MosaicListHandler] selected_check_list() : status = ', selected_item_status.get())
