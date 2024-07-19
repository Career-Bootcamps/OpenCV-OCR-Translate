
import glob
from tkinter import filedialog
from tkinter import messagebox as mb

import sys

sys.path.append('.')
from oot.data.data_manager import DataManager
from oot.gui.top_frame import TopFrame
from oot.gui.middle_frame import MiddleFrame
from oot.gui.subframes.remove_frame import RemoveFrame
from oot.gui.subframes.write_frame import WriteFrame

def __check_work_folder(work_dir):
    # check if image exists
    ext = ['png', 'jpg', 'gif']
    target_files = []
    [target_files.extend(glob.glob(work_dir + '/' + '*.' + e)) for e in ext]
    if len(target_files) == 0:
        mb.showerror("에러", "해당 폴더에는 이미지 파일이 없습니다")
        return False
    else:
        return True
    
def clicked_change_folder():
    print ('[TopFrameControl] clickedChangeFolder() called!!...')
    dir_path = filedialog.askdirectory(parent=TopFrame.root, title='작업할 폴더를 선택하세요', initialdir=DataManager.folder_data.get_folder_path())
    print("##> dir_path : ", dir_path)
    if __check_work_folder(dir_path):
            # 폴더 변경
            DataManager.reset_work_folder(dir_path)
            
            # 이전 문자 인식결과 초기화
            RemoveFrame.reset_remove_tab_data()
            WriteFrame.reset_write_tab_data()
            
            # UI 업데이트
            TopFrame.change_work_file(DataManager.get_work_file())

            # middle 이미지 업데이트
            MiddleFrame.reset_canvas_images(DataManager.get_work_file())

def clicked_prev_image():
    print('[TopFrameControl] clickedPrevImage() called!!...')
    work_file = DataManager.get_work_file()
    print(work_file)
    if work_file is None:
        mb.showerror("에러", "현재 작업중인 이미지 파일이 없습니다")
        return
    print('현재 작업중인 이미지: ', work_file.get_file_name())
    prev_img = DataManager.get_prev_file()

    if prev_img is None:
        mb.showerror("에러", "이전 이미지 파일이 없습니다")
        return
    print('[TopFrameControl] clickedPrevImage() : prev image = ', prev_img.get_file_name())
    DataManager.changed_work_image(prev_img)   
    
def clicked_next_image():
    print('[TopFrameControl] clickedNextImage() called!!...')
    work_file = DataManager.get_work_file()
    print(work_file)
    if work_file is None:
        mb.showerror("에러", "현재 작업중인 이미지 파일이 없습니다")
        return
    print('현재 작업중인 이미지: ', work_file.get_file_name())
    next_img = DataManager.get_next_file()

    if next_img is None:
        mb.showerror("에러", "다음 이미지 파일이 없습니다")
        return
    print('[TopFrameControl] clickedNextImage() : next image = ', next_img.get_file_name())
    DataManager.changed_work_image(next_img)   

def clicked_save_output():
    print('[TopFrameControl] clicked_save_output() called!!...')
    result = DataManager.save_output_file(DataManager.get_work_file().get_file_name(), MiddleFrame.out_canvas_worker.get_image())
    if result == True:
        MiddleFrame.reset_canvas_images(DataManager.get_work_file())
        mb.showinfo("성공", "저장에 성공했습니다")
    else:
        mb.showerror("에러", "저장에 실패했습니다")