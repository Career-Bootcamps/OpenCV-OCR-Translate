from tkinter import messagebox as mb

from oot.data.data_manager import DataManager


def clicked_search_text(): 
    print('[low_remove_control] clicked_search_text() called!!...')

    # check error case
    if DataManager.folder_data.get_work_file() == None:
        mb.showerror("에러", "선택된 이미지가 없습니다.")
        return
    
    # check if text search has been done already
    if DataManager.folder_data.work_file.is_ocr_detected:
        mb.showwarning("경고", "이미 text를 읽었습니다.")
        return

    # can not read texts in image
    texts = DataManager.read_text_image(DataManager.folder_data.work_file.name)
    if texts == None or len(texts) == 0:
        mb.showwarning("경고", "text를 찾을 수 없습니다.")
        return
    
    else:
        mb.showinfo("결과", texts)