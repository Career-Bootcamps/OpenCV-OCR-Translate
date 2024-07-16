import glob
import os
import shutil
from PIL import ImageTk, Image
import sys
sys.path.append('.')
from oot.gui.middle_frame import MiddleFrame
from oot.gui.top_frame import TopFrame

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
        self.position_info=[]
        
    def set_tr_text_with_position(self, tr_text, position):
        self.tr_text = tr_text
        self.position_info.append(position)
        
    
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
    def get_work_file(cls):
        return DataManager.folder_data.get_work_file() 
    
    @classmethod
    def set_work_file(cls, target_file):
        DataManager.folder_data.work_file = target_file
        
    @classmethod
    def reset_work_folder(cls, target_folder='./image'):
        print ('[DataManager.reset] reset, target=', target_folder)
        target_path = os.path.abspath(target_folder)
        cls.folder_data = FolderData(target_path)
        cls.__init_output_folder(target_path)

    @classmethod
    def __init_output_folder(cls,target_folder):
        print ('[DataManager] initOutputFiles() called...')
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
            out_file = os.path.join(target_folder, '__OUTPUT_FILES__', src_file_name)
            if not os.path.isfile(out_file):
                shutil.copy(src_file, out_file)
                
    
    @classmethod
    def get_output_file(cls):
        print ('[DataManager] get_output_file() called...')

        out_file_dir = cls.folder_data.folder
        out_file_name = os.path.basename(cls.folder_data.work_file.name)
        out_file = os.path.join(out_file_dir, '__OUTPUT_FILES__', out_file_name)
        
        return out_file
    
    @classmethod
    def save_output_file(cls, src_file, out_image):  #src_file 인자필요없음(로그확인용) - 추후에 삭제예정
        print ('[DataManager] save_output_file() called...')

        # out_image는 PIL의 Image 객체
        if out_image is None:
            print ('[DataManager] save_output_file() : image is None, it can not be saved!')

        # out_file은 path
        out_file = cls.get_output_file()
        print ('[DataManager] save_output_file() : src_file=', src_file)
        print ('[DataManager] save_output_file() : out_file=', out_file)

        if out_file is not None:
            if out_file.lower().endswith(("png")) == False:
                out_image.convert("RGB").save(out_file)
            else:
                out_image.save(out_file)
            print('[DataManager] save_output_file(): Image saved successfully!')
            return True
        return False

    @classmethod
    def get_prev_imagefile(cls):
        img_file=DataManager.get_work_file()
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


    @classmethod
    def changed_work_image(cls, work_file):
        
        print('[ControlManager.changedWorkImage] work_img=', work_file.name)
        DataManager.set_work_file(work_file) # 현재 작업 파일을 업데이트

        # Change images in canvases of 'MiddleFrame' with the 1st image of new dir
        MiddleFrame.reset_canvas_images(work_file)
        
        # Set new dir to 'TopFrame' at the label displaying work dir
        TopFrame.change_work_file(work_file)