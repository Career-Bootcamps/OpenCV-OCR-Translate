
import glob
from tkinter import filedialog
from tkinter import messagebox as mb

import sys
sys.path.append('.')
from oot.data.data_manager import DataManager
from oot.gui.top_frame import TopFrame

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
    dir_path = filedialog.askdirectory(parent=TopFrame.root, title='작업할 폴더를 선택하세요', initialdir=DataManager.folder_data.folder)
    print("##> dir_path : ", dir_path)
    if __check_work_folder(dir_path):
            # 폴더 변경
            DataManager.reset_work_folder(dir_path)
            
            # UI 업데이트
            TopFrame.change_work_file(DataManager.folder_data.get_work_file().name)

            