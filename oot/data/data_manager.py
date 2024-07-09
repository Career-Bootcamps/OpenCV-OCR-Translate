import glob
import os
from typing import cast
import shutil

# FolderData > FileData > TextData

class FolderData:
    
    def __init__(self, path):
        self.folder = path
        self.files = []
        self.work_file = None
        self.__init_work_folder()

    def __init_work_folder(self):
        FILE_EXT = ['png', 'jpg', 'gif']
        target_files = []
        [target_files.extend(glob.glob(self.folder + '/' + '*.' + e)) for e in FILE_EXT]

        for tf in target_files:
            self.files.append(FileData(tf))

        if len(self.files) == 0:
            return

        self.work_file = self.files[0]

    def get_work_file(self):
        return self.work_file

class FileData:
    def __init__(self, file):
        self.name = file
        self.texts = []
        self.is_ocr_detected = False
        self.position_info=[]

    def set_texts(self, texts):
        self.texts = []
        for index, t in enumerate(texts):
            self.texts.append(TextData(t))

    def set_tr_text(self, index, tr_text):
        self.texts[index].text_ko = tr_text
    
    def get_text(self, index):
        return self.texts[index]
    
    def set_position_info(self, character, position):
        self.position_info.append((character, position))

    def get_char_positions(self, text_index):
        return self.char_positions[text_index]
    
class TextData:
    def __init__(self, text):
        self.text = text
        self.tr_text = None

    def set_tr_text(self, tr_text):
        self.tr_text = tr_text

class DataManager:
    folder_data = None
    def init():
        DataManager.curr_path = os.getcwd()
        default_image_path = DataManager.curr_path + os.sep + "image"
        print(DataManager.curr_path)
        print(default_image_path)
        DataManager.folder_data = FolderData(default_image_path)

        DataManager.reset_work_folder()
        
    @classmethod
    def reset_work_folder(cls, target_folder='./image'):
        print ('[DataManager.reset] reset, target=', target_folder)
        cls.target_folder = os.path.abspath(target_folder)

        cls.__init_output_folder()

    @classmethod
    def __init_output_folder(cls):
        print ('[DataManager] initOutputFiles() called...')
        target_folder = cls.folder_data.folder
        print ('[DataManager] initOutputFiles() : target_folder = ', target_folder)

        output_folder = os.path.join(target_folder + os.sep + '__OUTPUT_FILES__')
        print ('[DataManager] initOutputFiles() : output_folder = ', output_folder)

        # create output folder if not exist
        if os.path.isdir(output_folder) == False:
            os.makedirs(output_folder)
            print ('[DataManager] initOutputFiles() : output_folder newly created!')
        
        if target_folder == None or len(target_folder) == 0:
            print ('[DataManager] initOutputFiles() : no source files!')
            return
        
        # copy files to output folder if source image file doesn't exist in output folder
        target_images = [file_data.name for file_data in cls.folder_data.files]
        for src_file in target_images:
            src_file_name = os.path.basename(src_file)
            out_file = os.path.join(cls.target_folder, '__OUTPUT_FILES__', src_file_name)
            if not os.path.isfile(out_file):
                shutil.copy(src_file, out_file)
