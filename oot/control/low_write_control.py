from tkinter import colorchooser
from PIL import Image
import sys
sys.path.append('.')
from oot.data.data_manager import DataManager
from oot.gui.middle_frame import MiddleFrame
from oot.gui.common import ScrollableListListener, CanvasWorkerPostDrawListner
from oot.gui.subframes.write_frame import WriteFrame

class WritePostDrawHandler(CanvasWorkerPostDrawListner):
    def do_post_draw(self, canvas, scale_ratio, rectangle_ids):
        from oot.gui.low_frame import LowFrame
        # draw lines for selected text in check list of write tab in LowFrame
        tab_idx = LowFrame.notebook.index(LowFrame.notebook.select())
        if tab_idx == 1:
            if WriteFrame.write_tab_text_list is not None and WriteFrame.write_tab_text_list.radio_value is not None:
                idx = WriteFrame.write_tab_text_list.radio_value.get()
                image_index = DataManager.get_image_index()
                work_file = DataManager.folder_data.get_file_by_index(image_index) # FileData
                try:
                    start_pos, end_pos = work_file.get_rectangle_position_by_texts_index(idx)
                    # 새로운 사각형 그리기
                    rectangle_id = canvas.create_rectangle(
                        int(scale_ratio*start_pos[0]),  # start x 
                        int(scale_ratio*start_pos[1]),  # start y
                        int(scale_ratio*end_pos[0]),    # end x
                        int(scale_ratio*end_pos[1]),    # end y
                        outline='#FF00FF'
                    )
                    # 사각형 ID를 CanvasWorker 인스턴스에 저장
                    rectangle_ids.append(rectangle_id)
                except IndexError:
                    print(f"IndexError: Text index {idx} out of range.")


class WriteTextListHandler(ScrollableListListener):
    def __init__(self, write_frame_instance):
        self.write_frame_instance = write_frame_instance
        
    def selected_check_list(self, text):
        pass
        
    def selected_radio_list(self, text):
        print ('[WriteTextListHandler] selectedRadioListInRemoveTab() called!!...')
        text_info = text.split('|', 1)

        # get selected item's info (id, text, status)
        selected_item_id = int(text_info[0])
        selected_item_text = text_info[1]
        print ('[WriteTextListHandler] selected_radio_list() : id = ', selected_item_id)
        print ('[WriteTextListHandler] selected_radio_list() : text = ', selected_item_text)
        
        # write text to original text area of write tab in low frame
        self.write_frame_instance.reset_translation_target_text_in_write_tab(selected_item_text)

        # Preview the font size and color based on the text's position
        try:
            from oot.data.data_manager import DataManager
            work_file = DataManager.get_work_file()
            start_pos, end_pos = work_file.get_rectangle_position_by_texts_index(selected_item_id)
            box_height = end_pos[1] - start_pos[1]
            
            # Use the instance of WriteFrame to access combo_box2
            estimated_font_size=box_height
            self.write_frame_instance.combo_box2.set(estimated_font_size)  # Set estimated font size
            
            # Get the image and background color
            out_file_path = DataManager.get_output_file()
            image = Image.open(out_file_path)
            
            # Get pixel color at the center of the box
            mid_x = (start_pos[0] + end_pos[0]) // 2
            mid_y = (start_pos[1] + end_pos[1]) // 2
            background_color = image.getpixel((mid_x, mid_y))
            
            # Calculate complementary font color
            font_color_rgb = self.write_frame_instance.get_complementary_color(background_color)
            font_color_hex = f"#{font_color_rgb[0]:02x}{font_color_rgb[1]:02x}{font_color_rgb[2]:02x}"
            
            # Set the preview color in the UI
            self.write_frame_instance.button_color.configure(bg=font_color_hex)

        except Exception as e:
            print(f"Error in previewing font size and color: {e}")
        
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

        # 첫 번째 라디오 버튼을 선택
        WriteFrame.write_tab_text_list.radio_value.set(0)
        WriteFrame.reset_translation_target_text_in_write_tab(texts[0])
        
        # 첫 번째 텍스트로 selected_radio_list 호출
        WriteFrame.write_tab_text_list.listener.selected_radio_list(f"0|{texts[0]}")


        # 이미지에 상자 그리기
        from oot.gui.middle_frame import MiddleFrame
        MiddleFrame.redraw_canvas_images()
