import glob
import os
import shutil
from typing import cast
from PIL import ImageTk, Image

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

    def set_texts(self, texts):
        self.texts = []
        for index, t in enumerate(texts):
            self.texts.append(TextData(t))

    def set_tr_text(self, index, tr_text):
        self.texts[index].text_ko = tr_text
    
    def get_text(self, index):
        return self.texts[index]

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
        target_path = os.path.abspath(target_folder)
        cls.folder_data = FolderData(target_path)
        cls.__init_output_folder(target_path)

    @classmethod
    def __init_output_folder(cls,target_folder):
        print ('[DataManager] __init_output_folder() called...')
        print ('[DataManager] __init_output_folder() : target_folder = ', target_folder)

        output_folder = os.path.join(target_folder, '__OUTPUT_FILES__')
        print ('[DataManager] __init_output_folder() : output_folder = ', output_folder)

        # create output folder if not exist
        if os.path.isdir(output_folder) == False:
            os.makedirs(output_folder)
            print ('[DataManager] __init_output_folder() : output_folder newly created!')
        
        if target_folder == None or len(target_folder) == 0:
            print ('[DataManager] __init_output_folder() : no source files!')
            return
        
        # copy files to output folder if source image file doesn't exist in output folder
        target_images = [file_data.name for file_data in cls.folder_data.files]
        
        for src_file in target_images:
            src_file_basename = os.path.basename(src_file)
            # 파일 이름과 확장자 분리
            src_file_name, src_file_ext = os.path.splitext(src_file_basename)
            # 이미지 저장 시 jpg는 PIL에서 지원하지 않는 이미지 포맷이므로 jpeg로 저장
            if src_file_ext.lower() == '.jpg':
                out_file = (target_folder + os.sep + '__OUTPUT_FILES__' + os.sep + src_file_name + '.jpeg')
            else:
                out_file = (target_folder + os.sep + '__OUTPUT_FILES__' + os.sep + src_file_basename)
            if not os.path.isfile(out_file):
                shutil.copy(src_file, out_file)
                if src_file_ext.lower() == '.jpg':
                    os.rename(out_file, (target_folder + os.sep + '__OUTPUT_FILES__' + os.sep + src_file_name + '.jpeg'))
                
    @classmethod
    def save_output_file(cls, src_file, out_image):
        print ('[DataManager] save_output_file() called...')

        # out_image는 PIL의 Image 객체
        if out_image is None:
            print ('[DataManager] save_output_file() : image is None, it can not be saved!')
       
        # out_file은 path
        out_file = cls.get_output_file()
        print ('[DataManager] save_output_file() : src_file=', src_file)
        print ('[DataManager] save_output_file() : out_file=', out_file)

        if out_file is not None:
            # 확장자에 따라서 저장을 달리함
            cls.__save_according_ext(out_file, out_image)
            print('[DataManager] save_output_file(): Image saved successfully!')
            return True
        return False
    
    @classmethod
    def __save_according_ext(cls, out_file, out_image):
        # 경로와 파일 이름 분리
        out_file_folder, out_file_full_name = os.path.split(out_file)
        # 파일 이름과 확장자 분리
        out_file_name, out_file_ext = os.path.splitext(out_file_full_name)
        # PIL 객체는 RGBA라서 RGB인 jpeg, gif를 저장하면 에러가 발생하므로 convert
        if out_file_ext != 'png':
            out_image = out_image.convert('RGB')
            
        out_image.save((out_file_folder + os.sep +out_file_name + out_file_ext), format = out_file_ext[1:].upper())

    @classmethod
    def get_output_file(cls):
        print ('[DataManager] get_output_file() called...')

        out_file_dir = cls.folder_data.folder
        out_file_basename = os.path.basename(cls.folder_data.work_file.name)
        out_file = os.path.join(out_file_dir, '__OUTPUT_FILES__', out_file_basename)
        out_file_name, out_file_ext = os.path.splitext(out_file_basename)

        if out_file_ext.lower() == '.jpg':
            out_file = (out_file_dir + os.sep + '__OUTPUT_FILES__' + os.sep + out_file_name + '.jpeg')
        
        return out_file
    
    @classmethod
    def get_prev_imagefile(cls, img_file):
        print('[DataManager] getPrevImageFile() called!!...')
        for i in range(len(cls.folder_data.files)):
            print('[DataManager] getPrevImageFile() i=', i, cls.folder_data.files[i].name)
            if cls.folder_data.files[i].name == img_file.name:
                if i != 0:
                    print('[DataManager] getPrevImageFile() - image found : ', cls.folder_data.files[i-1].name)
                    cls.folder_data.work_file = cls.folder_data.files[i-1] 
                    return cls.folder_data.files[i-1]
                else:
                    break
        print('[DataManager] getPrevImageFile() - image not found!!')
        return None

    @classmethod
    def get_next_imagefile(cls, img_file):
        print ('[DataManager] getNextImageFile() called!!...')
        for i in range(len(cls.folder_data.files)):
            print ('[DataManager] getNextImageFile() i=', i, ', curr_file=', img_file, ', compare=', cls.folder_data.files[i].name)
            if cls.folder_data.files[i].name == img_file.name:
                if (i+1) < len(cls.folder_data.files):
                    print ('[DataManager] getNextImageFile() - image found : ', cls.folder_data.files[i+1].name)
                    return cls.folder_data.files[i+1]
                else:
                    break
        print ('[DataManager] getNextImageFile() - image not found!!')
        return None
